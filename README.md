# SmolAgents 토이프로젝트

이 프로젝트는 [SmolAgents](https://huggingface.co/docs/smolagents/index)를 사용한 간단한 AI 에이전트 데모입니다.

## 기능

- **간단한 계산 에이전트**: 수학 문제를 해결하는 에이전트
- **웹 검색 에이전트**: 인터넷에서 정보를 검색하는 에이전트
- **Streamlit 웹 인터페이스**: 사용자 친화적인 웹 UI
- **다중 모델 지원**: OpenAI GPT와 Google Gemini 모두 지원

## 설치

```bash
pip install -r requirements.txt
```

## 환경 변수 설정

`.env` 파일을 생성하고 API 키를 설정하세요:

### Gemini 사용 (권장)
```
DEFAULT_MODEL=gemini
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash
```

### OpenAI 사용
```
DEFAULT_MODEL=openai
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
```

### 선택적 설정
```
OPENWEATHER_API_KEY=your_openweather_api_key_here
```

## 실행

### 방법 1: 데모 스크립트 사용 (권장)
```bash
python run_demo.py
```

### 방법 2: 직접 실행
```bash
# Streamlit 웹 앱 실행
streamlit run app.py

# 또는 직접 Python 스크립트 실행
python simple_agent.py
python web_search_agent.py
```

## 프로젝트 구조

- `run_demo.py`: 메인 데모 실행 스크립트
- `config.py`: API 키와 모델 설정 관리
- `gemini_agent.py`: Google Gemini API 에이전트 클래스
- `check_config.py`: 설정 확인 및 테스트 스크립트
- `simple_agent.py`: 기본 계산 에이전트
- `web_search_agent.py`: 웹 검색 에이전트
- `app.py`: Streamlit 웹 인터페이스
- `requirements.txt`: 필요한 패키지들
- `env_example.txt`: 환경 변수 설정 예시 