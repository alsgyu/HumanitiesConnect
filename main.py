import streamlit as st
from dotenv import load_dotenv
from llm import get_ai_response, analyze_emotion
from PIL import Image
import base64

st.set_page_config(page_title="정신 건강 인문학 앱")

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
        margin: 0px 0;
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
        position: fixed;
        display: inline-block;
        padding: 20px 45px 20px 15px;
        width: 260px; /* 포스트잇 너비 */
        margin: 5px 0;
        border: 1px solid #f8f861;
        border-left: 30px solid #f8f861;
        border-bottom-right-radius: 60px 10px;
        font-family: 'Nanum Pen Script';
        font-size: 13px;
        color: #555;
        word-break: break-all;
        background: #ffff88; /* Old browsers */
        background: -moz-linear-gradient(-45deg, #ffff88 81%, #ffff88 82%, #ffff88 82%, #ffffc6 100%); /* FF3.6+ */
        background: -webkit-gradient(linear, left top, right bottom, color-stop(81%, #ffff88), color-stop(82%, #ffff88), color-stop(82%, #ffff88), color-stop(100%, #ffffc6)); /* Chrome,Safari4+ */
        background: -webkit-linear-gradient(-45deg, #ffff88 81%, #ffff88 82%, #ffff88 82%, #ffffc6 100%); /* Chrome10+,Safari5.1+ */
        background: -o-linear-gradient(-45deg, #ffff88 81%, #ffff88 82%, #ffff88 82%, #ffffc6 100%); /* Opera 11.10+ */
        background: -ms-linear-gradient(-45deg, #ffff88 81%, #ffff88 82%, #ffff88 82%, #ffffc6 100%); /* IE10+ */
        background: linear-gradient(135deg, #ffff88 81%, #ffff88 82%, #ffff88 82%, #ffffc6 100%); /* W3C */
        filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#ffff88', endColorstr='#ffffc6', GradientType=1); /* IE6-9 fallback on horizontal gradient */
        transition: all 0.2s;
        -webkit-transition: all 0.2s;
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
        bottom: 330px; /* 아래에서 20px */
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
        background-color: #6AC793; /* 사용자 메시지 배경색 */
        border-radius: 10px; /* 모서리 둥글게 */
        padding: 10px; /* 패딩 추가 */
        color: white; /* 검정색 글씨 */
        max-width: 450px; /* 최대 너비 설정 */
    }
    .message.ai {
        background-color: #b4b4b4; /* AI 메시지 배경색 */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<h1>함께 오늘을 이야기해 보아요</h1>', unsafe_allow_html=True)
st.markdown('<h2>결코 감정에 정답을 찾지 않으셔도 돼요🌞.</h2>', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

st.markdown('<div class="post-it top-right">항상 파이팅!', unsafe_allow_html=True)
st.markdown('<div class="post-it bottom-right">너무 심각할 것 없어<br>잘 될거야<br>시간을 가져<br><br><피너츠></div>', unsafe_allow_html=True)
st.markdown('<div class="post-it bottom-left">등불을 잃지 않았으면 좋겠어</div>', unsafe_allow_html=True)

load_dotenv()

if 'message_list' not in st.session_state:
    st.session_state.message_list = []


user_profile_pic = "https://search.pstatic.net/sunny/?src=https%3A%2F%2Fcdn-icons-png.flaticon.com%2F512%2F5726%2F5726399.png&type=sc960_832"  # 사용자 프로필 사진
ai_profile_pic_path = "C:/Users/host0/foryou/for_you/images/ai_image.jpg"

def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

ai_image_base64 = image_to_base64(ai_profile_pic_path)
ai_image_html = f"data:image/jpeg;base64,{ai_image_base64}"


if "message_list" not in st.session_state:
    st.session_state.message_list = []

for message in st.session_state.message_list:
    if message["role"] == "user":
        st.markdown(f'<div class="message-container"><div class="message">'
                    f'<strong></strong> {message["content"]}<img src="{user_profile_pic}" style="width: 22px; height: 22px; border-radius: 50%; margin-left: 5px; margin-right: 0px; vertical-align: top;"/></div>', unsafe_allow_html=True)
    else: 
        st.markdown(f'<div class="message-container ai"><div class="message ai"><img src="{ai_image_html}" style="width: 25px; height: 25px; border-radius: 50%; margin-right: 0px; vertical-align: middle;"/>'
                    f'<strong>:</strong> {message["content"]}</div></div>', unsafe_allow_html=True)


# 사용자 입력
if user_input := st.chat_input(placeholder="오늘을 이야기해 주세요 어떠셨나요?"):
    st.session_state.message_list.append({"role": "user", "content": user_input})

    st.markdown(f'<div class="message-container"><div class="message">'
                f'<strong></strong> {user_input}  <img src=" {user_profile_pic}" style="width: 22px; height: 22px; border-radius: 50%; margin-left: 5px; margin-right: 0px; vertical-align: top;"/>', unsafe_allow_html=True)

    with st.spinner("답변을 작성하고 있어요..."):
        try:
            # 답변
            ai_response = get_ai_response(user_input)

            if ai_response:  
                st.session_state.message_list.append({"role": "ai", "content": ai_response})
                st.markdown(f'<div class="message-container ai"><div class="message ai"><img src="{ai_image_html}" style="width: 25px; height: 25px; border-radius: 50%; margin-right: 0px; vertical-align: middle;"/>'
                            f'<strong></strong> {ai_response}</div></div>', unsafe_allow_html=True)
            else:
                st.error("AI로부터 응답을 받지 못했습니다. 다시 시도해 주세요.")
        except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}")
