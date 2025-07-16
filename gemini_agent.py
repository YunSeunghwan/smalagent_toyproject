"""
Google Gemini API를 사용하는 SmolAgents 에이전트
"""

import google.generativeai as genai
from smolagents import Agent, Tool
from config import Config

class GeminiAgent:
    """Gemini API를 사용하는 에이전트 클래스"""
    
    def __init__(self, name, description, tools=None):
        self.name = name
        self.description = description
        self.tools = tools or []
        
        # Gemini API 설정
        config = Config.get_model_config()
        if config and config['provider'] == 'gemini':
            genai.configure(api_key=config['api_key'])
            self.model = genai.GenerativeModel(config['model'])
        else:
            raise ValueError("Gemini API 키가 설정되지 않았습니다.")
    
    def run(self, prompt):
        """에이전트 실행"""
        try:
            # 도구 설명을 포함한 시스템 프롬프트 생성
            system_prompt = f"""
당신은 {self.name}입니다. {self.description}

사용 가능한 도구들:
"""
            
            for tool in self.tools:
                system_prompt += f"- {tool.name}: {tool.description}\n"
            
            system_prompt += """
사용자의 질문에 답변할 때, 필요하면 적절한 도구를 사용하세요.
도구를 사용할 때는 도구 이름과 필요한 매개변수를 명확히 표시하세요.
"""
            
            # Gemini 모델에 요청
            response = self.model.generate_content([
                system_prompt,
                prompt
            ])
            
            # 도구 사용이 필요한지 확인
            response_text = response.text
            
            # 도구 사용 처리
            for tool in self.tools:
                if tool.name in response_text.lower():
                    # 도구 실행 로직 (간단한 구현)
                    tool_result = self._execute_tool(tool, prompt)
                    response_text += f"\n\n도구 실행 결과: {tool_result}"
            
            return response_text
            
        except Exception as e:
            return f"오류가 발생했습니다: {str(e)}"
    
    def _execute_tool(self, tool, user_input):
        """도구 실행"""
        try:
            # 간단한 도구 실행 로직
            # 실제로는 더 정교한 파싱이 필요할 수 있습니다
            return tool.func(user_input)
        except Exception as e:
            return f"도구 실행 오류: {str(e)}"

def create_gemini_agent(name, description, tools):
    """Gemini 에이전트 생성 헬퍼 함수"""
    return GeminiAgent(name, description, tools) 