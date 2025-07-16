import os
from dotenv import load_dotenv
from smolagents import Agent, Tool
from config import Config
from gemini_agent import create_gemini_agent
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
tools = [
    Tool(
        name="calculate",
        description="수학 표현식을 계산합니다. 예: 2 + 3, 10 * 5, (3 + 4) * 2",
        func=calculate
    ),
    Tool(
        name="extract_math",
        description="텍스트에서 수학 표현식을 추출합니다.",
        func=extract_math_expression
    )
]

# 에이전트 생성
config = Config.get_model_config()
if config and config['provider'] == 'gemini':
    agent = create_gemini_agent(
        name="계산 도우미",
        description="수학 문제를 해결하는 도움이 되는 AI 에이전트입니다.",
        tools=tools
    )
else:
    agent = Agent(
        name="계산 도우미",
        description="수학 문제를 해결하는 도움이 되는 AI 에이전트입니다.",
        tools=tools,
        model=config['model'] if config else "gpt-3.5-turbo"
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