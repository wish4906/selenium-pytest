import pytest
import sys
import os
import importlib

# 환경 설정 로드
ENV = os.getenv('TEST_ENV', 'dev')  # 기본값은 dev
config = importlib.import_module(f'config.{ENV}_config')

@pytest.fixture(scope="session")
def selenium_url():
    """테스트 유형에 맞는 Selenium Grid URL을 반환합니다."""
    for arg in sys.argv:
        if 'test_e' in arg:
            return config.SELENIUM_URLS['e_test']
        elif 'test_m' in arg:
            return config.SELENIUM_URLS['m_test']
        elif 'test_h' in arg:
            return config.SELENIUM_URLS['h_test']
    return config.SELENIUM_URLS['e_test']

@pytest.fixture(scope="session")
def test_data():
    """테스트 데이터를 관리하는 피처"""
    for arg in sys.argv:
        if 'test_e' in arg:
            return config.LOGIN_DATA['e_test']
        elif 'test_m' in arg:
            return config.LOGIN_DATA['m_test']
        elif 'test_h' in arg:
            return config.LOGIN_DATA['h_test']
    return config.LOGIN_DATA['e_test']

@pytest.fixture(scope="session")
def base_url(test_data):
    """테스트 유형별 base URL을 제공하는 fixture"""
    def _get_base_url(test_func_name):
        if 'teacher' in test_func_name:
            return test_data['teacher'][0]
        else:
            return test_data['student'][0]
    return _get_base_url
