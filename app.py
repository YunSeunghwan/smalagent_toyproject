import streamlit as st
import os
from dotenv import load_dotenv
from simple_agent import agent as calc_agent
from web_search_agent import agent as search_agent

# 환경 변수 로드
load_dotenv()

# 페이지 설정
st.set_page_config(
    page_title="SmolAgents 토이프로젝트",
    page_icon="🤖",
    layout="wide"
)

# 사이드바
st.sidebar.title("🤖 SmolAgents 데모")
st.sidebar.markdown("---")

# 에이전트 선택
agent_type = st.sidebar.selectbox(
    "에이전트 선택",
    ["계산 도우미", "정보 검색 도우미"]
)

# 메인 페이지
st.title("🤖 SmolAgents 토이프로젝트")
st.markdown("---")

# 에이전트 정보 표시
if agent_type == "계산 도우미":
    st.subheader("🧮 계산 도우미")
    st.markdown("""
    **기능:**
    - 수학 표현식 계산
    - 텍스트에서 수학 표현식 추출
    
    **사용 예시:**
    - "2 + 3 * 4를 계산해줘"
    - "이 텍스트에서 수학 표현식을 찾아줘: 5 + 10 그리고 3 * 7"
    """)
    agent = calc_agent
else:
    st.subheader("🔍 정보 검색 도우미")
    st.markdown("""
    **기능:**
    - 웹 검색
    - 날씨 정보 조회
    - 간단한 번역
    
    **사용 예시:**
    - "파이썬이란 무엇인가요?"
    - "서울 날씨 알려줘"
    - "hello를 한국어로 번역해줘"
    """)
    agent = search_agent

# 채팅 인터페이스
st.markdown("---")
st.subheader("💬 에이전트와 대화하기")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 메시지들 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
if prompt := st.chat_input("질문을 입력하세요..."):
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 에이전트 응답
    with st.chat_message("assistant"):
        with st.spinner("🤖 에이전트가 생각 중..."):
            try:
                response = agent.run(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_msg = f"❌ 오류가 발생했습니다: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# 사이드바에 추가 정보
st.sidebar.markdown("---")
st.sidebar.subheader("📋 사용법")
st.sidebar.markdown("""
1. 왼쪽에서 원하는 에이전트를 선택하세요
2. 하단의 채팅창에 질문을 입력하세요
3. 에이전트가 자동으로 적절한 도구를 사용하여 답변합니다
""")

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ 설정")
st.sidebar.markdown("""
**필요한 환경 변수:**
- `OPENAI_API_KEY`: OpenAI API 키

**선택적 환경 변수:**
- `OPENWEATHER_API_KEY`: 날씨 정보용 (정보 검색 에이전트)
""")

# 대화 기록 초기화 버튼
if st.sidebar.button("🗑️ 대화 기록 초기화"):
    st.session_state.messages = []
    st.rerun()

# 푸터
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>SmolAgents를 사용한 토이프로젝트 | 
    <a href='https://huggingface.co/docs/smolagents/index' target='_blank'>SmolAgents 문서</a></p>
</div>
""", unsafe_allow_html=True) 