import os
from dotenv import load_dotenv
from smolagents import CodeAgent, Tool, InferenceClientModel
from config import Config
import re

# 환경 변수 로드
load_dotenv()

def calculate(expression):
    """수학 표현식을 계산하는 도구"""
    try:
        # 안전한 수학 표현식만 허용
        allowed_chars = set('0123456789+-*/(). ')
        if not all(c in allowed_chars for c in expression):
            return "Error: 안전하지 않은 표현식입니다."
        
        result = eval(expression)
        return f"계산 결과: {result}"
    except Exception as e:
        return f"계산 오류: {str(e)}"

def extract_math_expression(text):
    """텍스트에서 수학 표현식을 추출하는 도구"""
    # 간단한 수학 표현식 패턴 매칭
    patterns = [
        r'\d+\s*[\+\-\*\/]\s*\d+',  # 기본 연산
        r'\(\s*\d+\s*[\+\-\*\/]\s*\d+\s*\)',  # 괄호가 있는 연산
        r'\d+\s*\*\s*\d+\s*\+\s*\d+',  # 복합 연산
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        if matches:
            return f"발견된 수학 표현식: {', '.join(matches)}"
    
    return "텍스트에서 수학 표현식을 찾을 수 없습니다."

# 도구들 정의
calculate_tool = Tool(
    name="calculate",
    description="수학 표현식을 계산합니다. 예: 2 + 3, 10 * 5, (3 + 4) * 2",
    func=calculate
)

extract_math_tool = Tool(
    name="extract_math",
    description="텍스트에서 수학 표현식을 추출합니다.",
    func=extract_math_expression
)

tools = [calculate_tool, extract_math_tool]

# 에이전트 생성
config = Config.get_model_config()
if config and config['provider'] == 'gemini':
    # Gemini는 직접 사용 (SmolAgents가 공식 지원하지 않을 수 있음)
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
    print("🤖 계산 도우미 에이전트가 시작되었습니다!")
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