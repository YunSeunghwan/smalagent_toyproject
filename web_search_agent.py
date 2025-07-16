import os
import requests
from dotenv import load_dotenv
from smolagents import CodeAgent, InferenceClientModel
from smolagents.tools import tool
from config import Config
import json

# 환경 변수 로드
load_dotenv()

@tool
def search_web(query: str) -> str:
    """웹에서 정보를 검색하는 도구 (DuckDuckGo API 사용)
    
    Args:
        query: 검색할 질문이나 키워드
    
    Returns:
        검색 결과 문자열
    """
    try:
        # DuckDuckGo Instant Answer API 사용
        url = "https://api.duckduckgo.com/"
        params = {
            'q': query,
            'format': 'json',
            'no_html': '1',
            'skip_disambig': '1'
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data.get('Abstract'):
            return f"검색 결과: {data['Abstract']}"
        elif data.get('Answer'):
            return f"답변: {data['Answer']}"
        elif data.get('RelatedTopics'):
            topics = data['RelatedTopics'][:3]  # 처음 3개만
            results = []
            for topic in topics:
                if isinstance(topic, dict) and topic.get('Text'):
                    results.append(topic['Text'])
            if results:
                return f"관련 정보:\n" + "\n".join(f"- {result}" for result in results)
        
        return "검색 결과를 찾을 수 없습니다."
        
    except Exception as e:
        return f"검색 중 오류가 발생했습니다: {str(e)}"

@tool
def get_weather_info(city: str) -> str:
    """도시의 날씨 정보를 가져오는 도구 (OpenWeatherMap API 사용)
    
    Args:
        city: 날씨를 조회할 도시 이름
    
    Returns:
        날씨 정보 문자열
    """
    try:
        # OpenWeatherMap API 키가 있다면 사용, 없으면 기본 정보 제공
        api_key = os.getenv('OPENWEATHER_API_KEY')
        
        if api_key:
            url = f"http://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': city,
                'appid': api_key,
                'units': 'metric',
                'lang': 'kr'
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if response.status_code == 200:
                temp = data['main']['temp']
                humidity = data['main']['humidity']
                description = data['weather'][0]['description']
                return f"{city}의 날씨: {description}, 온도: {temp}°C, 습도: {humidity}%"
            else:
                return f"{city}의 날씨 정보를 가져올 수 없습니다."
        else:
            return f"{city}의 날씨 정보를 확인하려면 OpenWeatherMap API 키가 필요합니다."
            
    except Exception as e:
        return f"날씨 정보 조회 중 오류가 발생했습니다: {str(e)}"

@tool
def translate_text(text: str, target_lang: str = 'en') -> str:
    """텍스트를 번역하는 도구 (Google Translate API 대체)
    
    Args:
        text: 번역할 텍스트
        target_lang: 목표 언어 (기본값: 'en')
    
    Returns:
        번역 결과 문자열
    """
    try:
        # 간단한 번역 예시 (실제로는 Google Translate API나 다른 번역 서비스 사용)
        translations = {
            'hello': '안녕하세요',
            'goodbye': '안녕히 가세요',
            'thank you': '감사합니다',
            'how are you': '어떻게 지내세요',
            '안녕하세요': 'hello',
            '감사합니다': 'thank you'
        }
        
        text_lower = text.lower()
        if text_lower in translations:
            return f"번역 결과: {translations[text_lower]}"
        else:
            return f"'{text}'의 번역을 찾을 수 없습니다. (제한된 단어만 지원)"
            
    except Exception as e:
        return f"번역 중 오류가 발생했습니다: {str(e)}"

# 도구들 정의
tools = [search_web, get_weather_info, translate_text]

# 에이전트 생성
config = Config.get_model_config()
if config and config['provider'] == 'gemini':
    # Gemini는 직접 사용
    from gemini_agent import create_gemini_agent
    agent = create_gemini_agent(tools=tools)
else:
    # OpenAI 또는 기본 모델 사용
    model = InferenceClientModel(model_id=config['model'] if config else "meta-llama/Llama-2-7b-chat-hf")
    agent = CodeAgent(
        tools=tools,
        model=model
    )

def main():
    print("🔍 정보 검색 도우미 에이전트가 시작되었습니다!")
    print("사용 가능한 기능:")
    print("- 웹 검색: '파이썬이란?' 같은 질문")
    print("- 날씨 정보: '서울 날씨' 같은 요청")
    print("- 번역: 'hello' 같은 단어 번역")
    print("종료하려면 'quit' 또는 'exit'를 입력하세요.\n")
    
    while True:
        user_input = input("질문을 입력하세요: ")
        
        if user_input.lower() in ['quit', 'exit', '종료']:
            print("👋 안녕히 가세요!")
            break
        
        try:
            response = agent.run(user_input)
            print(f"🤖 에이전트: {response}")
        except Exception as e:
            print(f"❌ 오류가 발생했습니다: {str(e)}")
        
        print()

if __name__ == "__main__":
    main() 