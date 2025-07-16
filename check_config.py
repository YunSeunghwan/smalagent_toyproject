#!/usr/bin/env python3
"""
설정 확인 및 테스트 스크립트
"""

from config import Config
import google.generativeai as genai

def test_gemini_connection():
    """Gemini API 연결 테스트"""
    try:
        config = Config.get_model_config()
        if not config or config['provider'] != 'gemini':
            print("❌ Gemini가 기본 모델로 설정되지 않았습니다.")
            return False
        
        # Gemini API 설정
        genai.configure(api_key=config['api_key'])
        model = genai.GenerativeModel(config['model'])
        
        # 간단한 테스트 요청
        response = model.generate_content("안녕하세요! 간단한 테스트입니다.")
        
        if response.text:
            print("✅ Gemini API 연결 성공!")
            print(f"테스트 응답: {response.text[:100]}...")
            return True
        else:
            print("❌ Gemini API 응답이 비어있습니다.")
            return False
            
    except Exception as e:
        print(f"❌ Gemini API 연결 실패: {str(e)}")
        return False

def test_openai_connection():
    """OpenAI API 연결 테스트"""
    try:
        import openai
        from openai import OpenAI
        
        config = Config.get_model_config()
        if not config or config['provider'] != 'openai':
            print("❌ OpenAI가 기본 모델로 설정되지 않았습니다.")
            return False
        
        client = OpenAI(api_key=config['api_key'])
        
        # 간단한 테스트 요청
        response = client.chat.completions.create(
            model=config['model'],
            messages=[{"role": "user", "content": "안녕하세요! 간단한 테스트입니다."}],
            max_tokens=50
        )
        
        if response.choices[0].message.content:
            print("✅ OpenAI API 연결 성공!")
            print(f"테스트 응답: {response.choices[0].message.content[:100]}...")
            return True
        else:
            print("❌ OpenAI API 응답이 비어있습니다.")
            return False
            
    except Exception as e:
        print(f"❌ OpenAI API 연결 실패: {str(e)}")
        return False

def main():
    """메인 함수"""
    print("🔍 설정 확인 및 테스트")
    print("=" * 50)
    
    # 현재 설정 출력
    Config.print_config()
    
    # 설정 유효성 검사
    errors = Config.validate_config()
    if errors:
        print("❌ 설정 오류:")
        for error in errors:
            print(f"  - {error}")
        print("\n📝 .env 파일을 확인하고 필요한 API 키를 설정하세요.")
        return
    
    print("✅ 설정 유효성 검사 통과!")
    print()
    
    # API 연결 테스트
    config = Config.get_model_config()
    if config['provider'] == 'gemini':
        print("🧪 Gemini API 연결 테스트 중...")
        test_gemini_connection()
    elif config['provider'] == 'openai':
        print("🧪 OpenAI API 연결 테스트 중...")
        test_openai_connection()
    
    print("\n" + "=" * 50)
    print("🎉 설정 확인 완료!")
    print("이제 run_demo.py를 실행하여 에이전트를 사용할 수 있습니다.")

if __name__ == "__main__":
    main() 