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
import pinecone
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import os

store = {}

def initialize_emotion_analyzer():
    try:
        # 업로드된 Hugging Face 모델에서 로드
        tokenizer = AutoTokenizer.from_pretrained("alsgyu/sentiment-analysis-fine-tuned-model")  # Hugging Face 레포지토리 경로
        model = AutoModelForSequenceClassification.from_pretrained("alsgyu/sentiment-analysis-fine-tuned-model") 
        return pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    except Exception as e:
        print(f"Failed to load emotion analyzer: {e}")
        return None

emotion_analyzer = initialize_emotion_analyzer()

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


# 환경 변수 로드
load_dotenv()

api_key = os.getenv("PINECONE_API_KEY")
environment = os.getenv("PINECONE_ENVIRONMENT")

pinecone_client = Pinecone(api_key=api_key)

if "foryou" not in pinecone_client.list_indexes().names():
    pinecone_client.create_index(
        name="foryou",
        dimension=3072,  
        metric="cosine",  
        spec=ServerlessSpec(
            cloud="aws", 
            region=environment  
        )
    )

# 전역 변수
embedding = None
retriever = None

def get_retriever():
    """Pinecone retriever를 초기화하고 반환합니다."""
    global embedding, retriever

    if not embedding:
        embedding = OpenAIEmbeddings(model="text-embedding-3-large")  # 모델 이름 확인 필요

    if not retriever:
        retriever = PineconeVectorStore.from_existing_index(
            index_name="foryou",  # Pinecone 인덱스 이름
            embedding=embedding
        ).as_retriever(search_kwargs={"k": 4})

    return retriever


def get_llm(model='gpt-4o'):
    return ChatOpenAI(model=model, temperature=0.7)

def get_dictionary_chain():
    
    dictionary = [
    "슬픔 -> 우울감, 상실, 고독",
    "행복 -> 긍정적인 감정, 만족, 기쁨",
    "스트레스 -> 정신적 긴장, 압박감, 불안",
    "두려움 -> 공포, 불확실성, 자기 방어",
    "분노 -> 좌절, 억울함, 정의감",
    "희망 -> 기대, 회복, 낙관",
    "사랑 -> 애정, 헌신, 유대감",
    "불안 -> 초조함, 의심, 긴장"
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

    system_prompt = (
        "당신은 인문학 관점에서 정신건강을 관리해주는 분야에서 전문가입니다."
        "당신은 사용자의 친구이기 때문에 인문학 견해보다 일상적인 대화가 우선입니다."
        "사용자의 감정 상태와 관련된 질문에 답변을 제공해주세요."
        "자신의 감정이 들어가지 않은 질의의 경우 해결책은 제시하지 않고 질문에 대한 답변만 해주세요."
        "해결책을 말하기 보단 공감을 우선시 해주시고 감정이 계속되면 조언의 형식으로 답변 부탁드립니다."
        "순서를 매기는 답변은 지양해주시고, 더 필요한게 있는지는 물어보지 않아도 돼요."
        "답변의 길이는 세 문장을 넘어가지 않도록 해주세요."
        "아래에 제공된 문서를 활용하여 인문학적 통찰력을 포함한 답변을 해주시고, 이모지도 가끔씩 활용해주세요."
        "문장을 ~다 로 끝내는 것이 아닌 ~요 형태로 친근하게 답변해주세요."
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
        "프란츠 카프카의 '변신' - 인간 존재에 대한 불안과 고독.",
        "에드바르드 뭉크의 '절규' - 불안과 고통의 시각적 표현.",
        "고흐의 '별이 빛나는 밤에' - 내면의 고독을 담은 작품."
    ],
    "행복": [
        "미셸 드 몽테뉴의 수필 - 행복의 본질에 대한 탐구.",
        "긍정적 사고와 행복 추구에 대한 철학적 논의.",
        "모네의 '수련' - 평온함과 행복의 상징.",
        "르누아르의 '물랭 드 라 갈레트의 무도회' - 일상의 기쁨을 표현한 그림."
    ],
    "스트레스": [
        "명상과 호흡법을 통한 스트레스 해소.",
        "스트레스 관리 매뉴얼 및 실용적인 조언.",
        "바흐의 'G선상의 아리아' - 마음을 진정시키는 음악.",
        "엔야의 'Only Time' - 평온함을 주는 뉴에이지 음악."
    ],
    "분노": [
        "플라톤의 '정의론' - 분노와 정의에 대한 고찰.",
        "마틴 루터 킹의 연설 - 분노를 평화적 저항으로 승화한 사례.",
        "톨스토이의 '전쟁과 평화' - 분노와 갈등 속에서 평화를 찾는 이야기.",
        "피카소의 '게르니카' - 전쟁의 분노와 고통을 표현한 작품."
    ],
    "불안": [
        "키르케고르의 '공포와 전율' - 불안과 신뢰에 대한 철학적 고찰.",
        "하이데거의 '존재와 시간' - 불안의 존재론적 의미.",
        "오노레 드 발자크의 '고리오 영감' - 불안한 인간 관계를 묘사.",
        "라흐마니노프의 '피아노 협주곡 2번' - 불안과 희망이 교차하는 음악."
    ],
    "희망": [
        "빅터 프랭클의 '죽음의 수용소에서' - 희망과 의미를 찾는 이야기.",
        "헬렌 켈러의 '사흘만 볼 수 있다면' - 삶의 가능성에 대한 희망.",
        "샤갈의 'I and the Village' - 희망과 꿈을 상징하는 그림.",
        "모차르트의 'Eine kleine Nachtmusik' - 밝고 경쾌한 희망의 선율."
    ],
    "사랑": [
        "알랭 드 보통의 '사랑의 기초' - 사랑의 다양한 형태를 탐구.",
        "제인 오스틴의 '오만과 편견' - 사랑과 인간 관계에 대한 통찰.",
        "로댕의 '키스' - 사랑의 강렬함을 표현한 조각 작품.",
        "비틀즈의 'All You Need Is Love' - 사랑의 보편적 메시지."
    ],
    "외로움": [
        "헤르만 헤세의 '데미안' - 고독과 자기 발견에 대한 이야기.",
        "알베르 카뮈의 '이방인' - 존재와 고독에 대한 철학적 이야기.",
        "베토벤의 '월광 소나타' - 고독 속에서 피어난 아름다움.",
        "에드워드 호퍼의 '밤의 올빼미' - 도시 속 고독을 담은 그림."
    ]
}

def recommend_resources(emotion: str):
    return resources.get(emotion, ["일상대화를 할게요"])

def get_ai_response(user_message: str, session_id: str = "default"):
    emotion = analyze_emotion(user_message) 
    recommended_resources = recommend_resources(emotion) # 추천자료 가져오기

    dictionary_chain = get_dictionary_chain()
    refined_question = dictionary_chain.invoke({"question": user_message})

    rag_chain = get_rag_chain()
    response = rag_chain.invoke(
        {"input": refined_question, "chat_history": [], "emotion": emotion},
        config={"configurable": {"session_id": session_id}},
    )
    ai_response_text = ''.join([resp for resp in response])

    if emotion != "중립" and recommended_resources[0] != "일상대화를 할게요":
        full_response = f"{ai_response_text}\n\n추천 자료: {', '.join(recommended_resources)}"
    else:
        full_response = ai_response_text

    return full_response
