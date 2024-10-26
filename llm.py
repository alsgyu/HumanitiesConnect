from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, FewShotChatMessagePromptTemplate
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from config import answer_examples

store = {}

# 감정 분석 함수
def analyze_emotion(user_input: str) -> str:

    if "슬픔" in user_input or "우울" in user_input:
        return "슬픔"
    elif "행복" in user_input or "기쁨" in user_input:
        return "행복"
    else:
        return "중립"

# 추천 자료 함수
def recommend_material(emotion: str) -> str:
    if emotion == "슬픔":
        return "우울증에 관한 문헌, 긍정적인 생각을 도와주는 책들"
    elif emotion == "행복":
        return "행복한 삶을 위한 인문학적 접근에 대한 자료"
    else:
        return "기본적인 인문학 자료"

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def get_retriever():
    embedding = OpenAIEmbeddings(model='text-embedding-3-large')
    index_name = 'foryou'
    database = PineconeVectorStore.from_existing_index(index_name=index_name, embedding=embedding)
    retriever = database.as_retriever(search_kwargs={'k': 4})
    return retriever

def get_history_retriever():
    llm = get_llm()
    retriever = get_retriever()
    
    contextualize_q_system_prompt = (
    "Given the chat history and the latest user question, "
    "reformulate it into a standalone question that can be understood "
    "without referencing the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
    )

    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )
    return history_aware_retriever

def get_llm(model='gpt-4o'):
    llm = ChatOpenAI(model=model)
    return llm

def get_dictionary_chain():
    # 인문학적 키워드 예시
    dictionary = [
        "슬픔 -> 우울감",
        "행복 -> 긍정적인 감정",
        "스트레스 -> 정신적 긴장"
    ]
    
    llm = get_llm()
    
    prompt = ChatPromptTemplate.from_template(f"""
        사용자의 질문이나 감정일기 등을 보고, 최대한 우리의 인문학적 관점을 참고해서 사용자의 질문을 변경해주세요.
        만약 변경할 필요가 없다고 판단된다면, 사용자의 질문을 변경하지 않아도 됩니다.
        그런 경우에는 질문만 리턴해주세요.
        인문학적 키워드: {dictionary}
        
        질문: {{question}}
    """)

    dictionary_chain = prompt | llm | StrOutputParser()
    
    return dictionary_chain

def get_rag_chain():
    llm = get_llm()
    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{input}"),
            ("ai", "{answer}"),
        ]
    )
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=answer_examples,
    )
    system_prompt = (
        "당신은 인문학 관점에서 정신건강을 관리해주는 분야에서 전문가입니다. "
        "사용자의 감정 상태와 관련된 질문에 답변을 제공해주세요. "
        "자신의 감정이 들어가지 않은 질의의 경우 해결책은 제시하지 않고 질문에 대한 답변만 해주세요."
        "정답을 말하기 보단 우선은 공감만 해주시고 감정이 계속되면 조언의 형식으로 답변 부탁드립니다."
        "순서를 매기는 답변은 지양해주세요."
        "아래에 제공된 문서를 활용하여 인문학적 통찰력을 포함한 답변을 해주시고, 이모지도 가끔씩 활용해주세요"
        "문장을 ~다 로 끝내는 것이 아닌 ~요 형태로 친근하게 답변해주세요."
        "사용자와의 소통이 계속된다면 가끔씩은 함께 보면 좋을 자료를 추천해드릴까요? 이런 식으로 추가 자료 필요를 물어봐주세요 하지만 치료와 관련된 책은 아니어야 합니다."
        "\n\n"
        "{context}"
    )
    
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            few_shot_prompt,
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    history_aware_retriever = get_history_retriever()
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    
    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    ).pick('answer')
    
    return conversational_rag_chain

resources = {
    "우울감": [
        "안톤 체홉의 단편 소설 '가을' - 슬픔과 우울감에 대한 통찰.",
        "정신 건강 관리 가이드 - 우울증을 이해하고 관리하는 방법.",
        "프리드리히 니체의 저서 '차라투스트라는 이렇게 말했다' - 우울감과 인간 존재에 대한 고찰."
    ],
    "행복": [
        "미셸 드 몽테뉴의 수필 - 행복의 본질에 대한 탐구.",
        "자기계발서 '긍정의 힘' - 긍정적인 사고를 통한 행복 추구 방법.",
        "정신 건강 관련 웹사이트 - 행복 관리에 대한 다양한 자료."
    ],
    "스트레스": [
        "스트레스 관리 매뉴얼 - 효과적인 스트레스 해소 방법.",
        "전통적인 치유 방법 - 명상과 호흡법.",
        "온라인 커뮤니티 - 스트레스에 대한 경험 공유 및 조언."
    ]
}

def recommend_resources(emotion: str):
    return resources.get(emotion, ["관련 자료가 없습니다."])

def get_ai_response(user_message: str):
    dictionary_chain = get_dictionary_chain()
    rag_chain = get_rag_chain()
    tax_chain = {"input": dictionary_chain} | rag_chain
    
    
    ai_response = tax_chain.stream(
        {
            "question": user_message,
            # "recommended_material": recommended_material
        },
        config={
            "configurable": {"session_id": "abc123"}
        },
    )
    ai_response_text = ''.join([response for response in ai_response])
    print(f"AI Response: {ai_response}")

    return ai_response_text
