#!/usr/bin/env python3
"""
SmolAgents 토이프로젝트 데모 실행 스크립트
"""

import os
import sys
from dotenv import load_dotenv

def check_environment():
    """환경 설정 확인"""
    load_dotenv()
    
    print("🔍 환경 설정 확인 중...")
    
    # 설정 유효성 검사
    from config import Config
    errors = Config.validate_config()
    
    if errors:
        print("❌ 설정 오류:")
        for error in errors:
            print(f"  - {error}")
        print("\n📝 .env 파일을 생성하고 필요한 API 키를 설정하세요.")
        print("📋 env_example.txt 파일을 참고하세요.")
        return False
    
    # 현재 설정 출력
    Config.print_config()
    return True

def show_menu():
    """메뉴 표시"""
    print("\n" + "="*50)
    print("🤖 SmolAgents 토이프로젝트")
    print("="*50)
    print("1. 계산 도우미 에이전트 실행")
    print("2. 정보 검색 도우미 에이전트 실행")
    print("3. Streamlit 웹 앱 실행")
    print("4. 설정 확인 및 테스트")
    print("5. 종료")
    print("="*50)

def main():
    """메인 함수"""
    if not check_environment():
        sys.exit(1)
    
    while True:
        show_menu()
        choice = input("선택하세요 (1-5): ").strip()
        
        if choice == '1':
            print("\n🧮 계산 도우미 에이전트를 시작합니다...")
            try:
                from simple_agent import main as calc_main
                calc_main()
            except KeyboardInterrupt:
                print("\n👋 계산 도우미를 종료합니다.")
            except Exception as e:
                print(f"❌ 오류: {e}")
        
        elif choice == '2':
            print("\n🔍 정보 검색 도우미 에이전트를 시작합니다...")
            try:
                from web_search_agent import main as search_main
                search_main()
            except KeyboardInterrupt:
                print("\n👋 정보 검색 도우미를 종료합니다.")
            except Exception as e:
                print(f"❌ 오류: {e}")
        
        elif choice == '3':
            print("\n🌐 Streamlit 웹 앱을 시작합니다...")
            print("브라우저에서 http://localhost:8501 을 열어주세요.")
            print("종료하려면 Ctrl+C를 누르세요.")
            try:
                os.system("streamlit run app.py")
            except KeyboardInterrupt:
                print("\n👋 웹 앱을 종료합니다.")
            except Exception as e:
                print(f"❌ 오류: {e}")
        
        elif choice == '4':
            print("\n🔍 설정 확인 및 테스트를 시작합니다...")
            try:
                from check_config import main as check_main
                check_main()
            except Exception as e:
                print(f"❌ 오류: {e}")
        
        elif choice == '5':
            print("👋 안녕히 가세요!")
            break
        
        else:
            print("❌ 잘못된 선택입니다. 1-5 중에서 선택하세요.")

if __name__ == "__main__":
    main() 