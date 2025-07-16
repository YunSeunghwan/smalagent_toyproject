"""
Google Gemini API를 사용하는 간단한 에이전트
"""

import google.generativeai as genai
from config import Config

class GeminiAgent:
    """Gemini API를 사용하는 에이전트 클래스"""
    
    def __init__(self, tools=None):
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
당신은 도움이 되는 AI 어시스턴트입니다.

사용 가능한 도구들:
"""
            
            for tool in self.tools:
                system_prompt += f"- {tool.name}: {tool.description}\n"
            
            system_prompt += """
사용자의 질문에 답변할 때, 필요하면 적절한 도구를 사용하세요.
도구를 사용해야 할 때는 다음 형식으로 답변하세요:
TOOL_USE: tool_name
INPUT: 도구에 전달할 입력

그렇지 않으면 직접 답변하세요.
"""
            
            # Gemini 모델에 요청
            response = self.model.generate_content([
                system_prompt,
                f"사용자 질문: {prompt}"
            ])
            
            response_text = response.text
            
            # 도구 사용이 필요한지 확인
            if "TOOL_USE:" in response_text:
                lines = response_text.split('\n')
                tool_name = None
                tool_input = None
                
                for line in lines:
                    if line.startswith("TOOL_USE:"):
                        tool_name = line.replace("TOOL_USE:", "").strip()
                    elif line.startswith("INPUT:"):
                        tool_input = line.replace("INPUT:", "").strip()
                
                if tool_name and tool_input:
                    # 도구 실행
                    for tool in self.tools:
                        if tool.name == tool_name:
                            tool_result = tool.func(tool_input)
                            return f"도구 '{tool_name}' 실행 결과:\n{tool_result}"
                    
                    return f"도구 '{tool_name}'을 찾을 수 없습니다."
            
            return response_text
            
        except Exception as e:
            return f"오류가 발생했습니다: {str(e)}"

def create_gemini_agent(tools):
    """Gemini 에이전트 생성 헬퍼 함수"""
    return GeminiAgent(tools=tools) 