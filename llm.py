from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, FewShotChatMessagePromptTemplate
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

store = {}

# 감정 분석 함수
def initialize_emotion_analyzer():
    try:
        # 로컬 디렉토리에서 모델과 토크나이저 로드
        tokenizer = AutoTokenizer.from_pretrained("D:\wow\fine_tuned_model\fine_tuned_model")  # 로컬 경로 지정
        model = AutoModelForSequenceClassification.from_pretrained("./fine_tuned_model")  # 로컬 경로 지정
        return pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    except Exception as e:
        print(f"Failed to load emotion analyzer: {e}")
        return None

# 파이프라인 초기화
emotion_analyzer = initialize_emotion_analyzer()

# 테스트: 감정 분석
if emotion_analyzer:
    sample_text = "오늘 하루가 정말 즐거웠어요!"
    result = emotion_analyzer(sample_text)
    print(f"Input: {sample_text}\nAnalysis Result: {result}")
else:
    print("Emotion analyzer is not initialized.")

def analyze_emotion(user_input: str) -> str:
    if not emotion_analyzer:
        return "Error loading emotion analyzer"
    result = emotion_analyzer(user_input)
    return result[0]['label']


def get_retriever():
    embedding = OpenAIEmbeddings(model='text-embedding-3-large')
    database = PineconeVectorStore.from_existing_index(index_name='foryou', embedding=embedding)
    return database.as_retriever(search_kwargs={'k': 4})


def get_llm(model='gpt-4o'):
    return ChatOpenAI(model=model, temperature=0.7)

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
    retriever = get_retriever()

    # 기존의 시스템 프롬프트 유지
    system_prompt = (
        "당신은 인문학 관점에서 정신건강을 관리해주는 분야에서 전문가입니다. "
        "사용자의 감정 상태와 관련된 질문에 답변을 제공해주세요. "
        "자신의 감정이 들어가지 않은 질의의 경우 해결책은 제시하지 않고 질문에 대한 답변만 해주세요."
        "정답을 말하기 보단 우선은 공감만 해주시고 감정이 계속되면 조언의 형식으로 답변 부탁드립니다."
        "순서를 매기는 답변은 지양해주세요."
        "더 필요한게 있는지는 물어보지 않아도 돼요."
        "아래에 제공된 문서를 활용하여 인문학적 통찰력을 포함한 답변을 해주시고, 이모지도 가끔씩 활용해주세요."
        "문장을 ~다 로 끝내는 것이 아닌 ~요 형태로 친근하게 답변해주세요."
        "사용자와의 소통이 계속된다면 가끔씩은 함께 보면 좋을 자료를 추천해드릴까요? 이런 식으로 추가 자료 필요를 물어봐주세요 하지만 치료와 관련된 책은 아니어야 합니다."
        "\n\n"
        "{context}"
    )

    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        lambda session_id: store.setdefault(session_id, ChatMessageHistory()),
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    ).pick('answer')

    return conversational_rag_chain

resources = {
    "슬픔": [
        "안톤 체홉의 단편 소설 '가을' - 슬픔과 우울감에 대한 통찰.",
        "니체의 '차라투스트라는 이렇게 말했다' - 인간 존재에 대한 고찰."
    ],
    "행복": [
        "미셸 드 몽테뉴의 수필 - 행복의 본질에 대한 탐구.",
        "긍정적 사고와 행복 추구에 대한 철학적 논의."
    ],
    "스트레스": [
        "명상과 호흡법을 통한 스트레스 해소.",
        "스트레스 관리 매뉴얼 및 실용적인 조언."
    ],
}

def recommend_resources(emotion: str):
    return resources.get(emotion, ["관련 자료가 없습니다."])

def get_ai_response(user_message: str, session_id: str = "default"):
    emotion = analyze_emotion(user_message)
    recommended_resources = recommend_resources(emotion)

    # dictionary_chain 활용
    dictionary_chain = get_dictionary_chain()
    refined_question = dictionary_chain.invoke({"question": user_message})

    rag_chain = get_rag_chain()
    response = rag_chain.invoke(
        {"input": refined_question, "chat_history": [], "emotion": emotion},
        config={"configurable": {"session_id": session_id}},
    )
    ai_response_text = ''.join([resp for resp in response])

    if emotion != "중립" and recommended_resources[0] != "관련 자료가 없습니다.":
        full_response = f"{ai_response_text}\n\n추천 자료: {', '.join(recommended_resources)}"
    else:
        full_response = ai_response_text

    return full_response
