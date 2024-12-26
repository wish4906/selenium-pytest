import pytest
import os
import importlib
import sys

ENV = os.getenv('TEST_ENV', 'dev')
config = importlib.import_module(f'config.{ENV}_config')

def get_test_type_from_file(filename):
    """테스트 파일 이름에서 테스트 타입을 결정합니다."""
    if 'test_e.py' in filename:
        print("초등 테스트 실행")
        return 'e_tests', config.SELENIUM_URLS['e_test']
    elif 'test_m.py' in filename:
        print("중등 테스트 실행")
        return 'm_tests', config.SELENIUM_URLS['m_test']
    elif 'test_h.py' in filename:
        print("고등 테스트 실행")
        return 'h_tests', config.SELENIUM_URLS['h_test']
    elif 'test_scripts.py' in filename:
        print("스크립트 테스트 실행")
        return 'test_script', config.SELENIUM_URLS['e_test']
    raise ValueError(f"알 수 없는 테스트 파일: {filename}")

def pytest_configure(config):
    """테스트 설정 초기화"""
    # 실행할 테스트 파일 확인
    if config.args:
        test_file = config.args[0]
        test_type, selenium_url = get_test_type_from_file(test_file)
        # 전역 설정으로 저장
        config.test_type = test_type
        config.selenium_url = selenium_url

@pytest.fixture(scope="session")
def test_type(request):
    """테스트 타입을 반환합니다."""
    return request.config.test_type

@pytest.fixture(scope="session")
def selenium_url(request):
    """테스트 타입에 맞는 Selenium Grid URL을 반환합니다."""
    return request.config.selenium_url

@pytest.fixture(scope="session")
def login_data(test_type):
    """테스트 타입에 맞는 로그인 데이터를 반환합니다."""
    test_map = {
        'e_tests': 'e_test',
        'm_tests': 'm_test',
        'h_tests': 'h_test',
        'test_script': 'e_test'
    }
    return config.LOGIN_DATA[test_map[test_type]]

def pytest_collection_modifyitems(session, config, items):
    """테스트 실행 전에 테스트 타입을 확인합니다."""
    if not items:
        return
    
    # 테스트 타입 출력
    print(f"실행할 테스트 타입: {config.test_type} ({len(items)} 테스트)")
