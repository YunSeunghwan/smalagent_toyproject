"""
SmolAgents 토이프로젝트 설정 파일
API 키와 모델 설정을 관리합니다.
"""

import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

class Config:
    """설정 클래스"""
    
    # OpenAI 설정
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    
    # Google Gemini 설정
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
    
    # OpenWeatherMap 설정 (선택적)
    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
    
    # 기본 모델 설정
    DEFAULT_MODEL = os.getenv('DEFAULT_MODEL', 'gemini')  # 'openai' 또는 'gemini'
    
    @classmethod
    def get_model_config(cls):
        """현재 설정된 모델 정보 반환"""
        if cls.DEFAULT_MODEL == 'gemini' and cls.GEMINI_API_KEY:
            return {
                'provider': 'gemini',
                'model': cls.GEMINI_MODEL,
                'api_key': cls.GEMINI_API_KEY
            }
        elif cls.OPENAI_API_KEY:
            return {
                'provider': 'openai',
                'model': cls.OPENAI_MODEL,
                'api_key': cls.OPENAI_API_KEY
            }
        else:
            return None
    
    @classmethod
    def validate_config(cls):
        """설정 유효성 검사"""
        errors = []
        
        if cls.DEFAULT_MODEL == 'gemini':
            if not cls.GEMINI_API_KEY:
                errors.append("GEMINI_API_KEY가 설정되지 않았습니다.")
        elif cls.DEFAULT_MODEL == 'openai':
            if not cls.OPENAI_API_KEY:
                errors.append("OPENAI_API_KEY가 설정되지 않았습니다.")
        
        return errors
    
    @classmethod
    def print_config(cls):
        """현재 설정 출력"""
        print("🔧 현재 설정:")
        print(f"  기본 모델: {cls.DEFAULT_MODEL}")
        
        if cls.GEMINI_API_KEY:
            masked_key = cls._mask_api_key(cls.GEMINI_API_KEY)
            print(f"  Gemini API 키: {masked_key}")
            print(f"  Gemini 모델: {cls.GEMINI_MODEL}")
        else:
            print("  Gemini API 키: 설정되지 않음")
        
        if cls.OPENAI_API_KEY:
            masked_key = cls._mask_api_key(cls.OPENAI_API_KEY)
            print(f"  OpenAI API 키: {masked_key}")
            print(f"  OpenAI 모델: {cls.OPENAI_MODEL}")
        else:
            print("  OpenAI API 키: 설정되지 않음")
        
        if cls.OPENWEATHER_API_KEY:
            masked_key = cls._mask_api_key(cls.OPENWEATHER_API_KEY)
            print(f"  OpenWeather API 키: {masked_key}")
        else:
            print("  OpenWeather API 키: 설정되지 않음")
        
        print()
    
    @staticmethod
    def _mask_api_key(api_key):
        """API 키를 마스킹하여 보안 강화"""
        if len(api_key) <= 8:
            return '*' * len(api_key)
        return '*' * (len(api_key) - 8) + api_key[-8:] 