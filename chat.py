import streamlit as st
from dotenv import load_dotenv
from llm import get_ai_response, analyze_emotion

st.set_page_config(page_title="정신 건강 인문학 앱")

# Nunito 폰트를 포함한 배경색 및 글씨 색상 변경
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;600&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Brush+Script&display=swap');

    .main {
        background-color: #F9FFFF;  /* 부드러운 파란색 배경 */
    }
    h1 {
        color: #000000;  /* 검정색 글씨 */
        font-size: 47px; /* 폰트 크기 조정 */
        font-family: 'Nunito', sans-serif; /* Nunito 폰트 사용 */
    }
    h2 {
        color: #000000;  /* 검정색 글씨 */
        font-size: 14px; /* 폰트 크기 조정 */
        font-family: 'Nunito', sans-serif; /* Nunito 폰트 사용 */
    }
    .divider {
        border-top: 2px solid #a3a3a3;
        margin: 10px 0;
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
    }
    .chat-area {
        background-color: rgba(255, 255, 255, 0.8); /* 채팅 영역 배경색 */
        border-radius: 10px; /* 모서리 둥글게 */
        padding: 20px; /* 패딩 추가 */
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* 그림자 효과 추가 */
        margin-bottom: 20px; /* 아래쪽 여백 추가 */
    }
    .post-it {
        position: fixed;  /* 고정 위치 */
        background-color: #FFD732; /* 포스트잇 노란색 */
        border: 1px solid #f8f861;
        border-radius: 10px; /* 모서리 둥글게 */
        padding: 20px; /* 패딩 추가 */
        width: 200px; /* 포스트잇 너비 */
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); /* 그림자 효과 추가 */
        font-family: 'Nanum Brush Script', cursive; /* Nanum Brush Script 폰트 사용 */
        color: #555; /* 글씨 색상 */
        font-size: 19px;  /* 폰트 크기를 18px로 설정 */
    }
    .post-it.top-right {
        top: 200px; /* 위에서 20px */
        right: 130px; /* 오른쪽에서 20px */
    }
    .post-it.bottom-right {
        bottom: 200px; /* 위에서 20px */
        right: 130px; /* 오른쪽에서 20px */
    }
    .post-it.bottom-left {
        bottom: 300px; /* 아래에서 20px */
        left: 130px; /* 왼쪽에서 20px */
    }
    .message-container {
        display: flex;
        justify-content: flex-end; /* 기본적으로 오른쪽 정렬 */
        margin: 5px 0;
    }
    .message-container.ai {
        justify-content: flex-start; /* AI 메시지는 왼쪽 정렬 */
    }
    .message {
        background-color: #1E82FF; /* 사용자 메시지 배경색 */
        border-radius: 10px; /* 모서리 둥글게 */
        padding: 10px; /* 패딩 추가 */
        color: white; /* 검정색 글씨 */
        max-width: 450px; /* 최대 너비 설정 */
    }
    .message.ai {
        background-color: #d2d2d2; /* AI 메시지 배경색 */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# HTML로 직접 타이틀과 캡션 설정
st.markdown('<h1>함께 오늘을 이야기해 보아요</h1>', unsafe_allow_html=True)
st.markdown('<h2>결코 감정에 정답을 찾지 않으셔도 돼요🌞.</h2>', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
# 포스트잇 내용 예시
st.markdown('<div class="post-it top-right">항상 파이팅!', unsafe_allow_html=True)
st.markdown('<div class="post-it bottom-right">가장 어두운 순간에 우리는 빛을 찾을 수 있다<br>Ronald Reagan</div>', unsafe_allow_html=True)
st.markdown('<div class="post-it bottom-left">등불을 잃지 않았으면 좋겠어</div>', unsafe_allow_html=True)

load_dotenv()

if 'message_list' not in st.session_state:
    st.session_state.message_list = []


user_profile_pic = "https://search.pstatic.net/sunny/?src=https%3A%2F%2Fcdn-icons-png.flaticon.com%2F512%2F5726%2F5726399.png&type=sc960_832"  # 사용자 프로필 사진
ai_profile_pic = "https://www.shutterstock.com/shutterstock/photos/2314900373/display_1500/stock-vector-anthropology-thick-line-filled-colors-for-personal-and-commercial-use-2314900373.jpg"  # AI 프로필 사진


for message in st.session_state.message_list:
    if message["role"] == "user":
        st.markdown(f'<div class="message-container"><div class="message"><img src="{user_profile_pic}" style="width: 22px; height: 22px; border-radius: 50%; margin-right: 10px; vertical-align: top;"/>'
                    f'<strong></strong> {message["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="message-container ai"><div class="message ai"><img src="{ai_profile_pic}" style="width: 22px; height: 22px; border-radius: 50%; margin-right: 10px; vertical-align: middle;"/>'
                    f'<strong>:</strong> {message["content"]}</div></div>', unsafe_allow_html=True)

# 사용자 입력 받기
if user_input := st.chat_input(placeholder="오늘을 이야기해 주세요 어떠셨나요?"):
    st.session_state.message_list.append({"role": "user", "content": user_input})

    st.markdown(f'<div class="message-container"><div class="message">'
                f'<strong></strong> {user_input} <img src="{user_profile_pic}" style="width: 22px; height: 22px; border-radius: 50%; left-right: 30px; margin-right: 0px; vertical-align: middle;"/>', unsafe_allow_html=True)

    with st.spinner("응답을 생성하는 중입니다..."):
        try:
            # AI 응답 생성
            ai_response = get_ai_response(user_input)

            # AI 응답을 표시합니다.
            if ai_response:  # AI 응답이 None이 아닐 경우에만
                st.session_state.message_list.append({"role": "ai", "content": ai_response})
                st.markdown(f'<div class="message-container ai"><div class="message ai"><img src="{ai_profile_pic}" style="width: 30px; height: 30px; border-radius: 50%; margin-right: 10px; vertical-align: middle;"/>'
                            f'<strong></strong> {ai_response}</div></div>', unsafe_allow_html=True)
            else:
                st.error("AI로부터 응답을 받지 못했습니다. 다시 시도해 주세요.")
        except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}")
