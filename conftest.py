import pytest
from selenium import webdriver

# 각 PC의 Selenium 서버 URL
SELENIUM_URLS = {
    'e_test': 'http://192.168.0.72:4444/wd/hub',
    'm_test': 'http://192.168.0.18:4444/wd/hub',
    'h_test': 'http://192.168.0.106:4444/wd/hub'
}

# 각 PC에서 열 URL 및 로그인 정보 설정
LOGIN_DATA = {
    'e_test': ("https://tb-edu.ontactedu.co.kr/office/goe", "seleniumeclass1", "2w2w2w2w2w", "seleniume", "student_num1"),
    'm_test': ("https://tb-edu.ontactedu.co.kr/office/goe", "seleniummclass1", "2w2w2w2w2w", "seleniumm", "student_num2"),
    'h_test': ("https://tb-edu.ontactedu.co.kr/office/goe", "seleniumhclass1", "2w2w2w2w2w", "seleniumh", "student_num3"),
}

def get_screen_size():
    import ctypes
    user32 = ctypes.windll.user32
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

def get_test_type(module_name):
    if 'test_e' in module_name:
        return 'e_test'
    elif 'test_m' in module_name:
        return 'm_test'
    elif 'test_h' in module_name:
        return 'h_test'
    else:
        raise ValueError(f"Unknown test type: {module_name}")

@pytest.fixture(scope="class")
def setup_drivers(request):
    screen_width, screen_height = get_screen_size()
    half_width = screen_width // 2

    options_normal = webdriver.ChromeOptions()
    options_incognito = webdriver.ChromeOptions()
    options_incognito.add_argument('--incognito')

    test_type = get_test_type(request.module.__name__)
    selenium_url = SELENIUM_URLS[test_type]

    driver_normal = webdriver.Remote(command_executor=selenium_url, options=options_normal)
    driver_incognito = webdriver.Remote(command_executor=selenium_url, options=options_incognito)

    driver_normal.set_window_size(half_width, screen_height)
    driver_normal.set_window_position(0, 0)
    driver_incognito.set_window_size(half_width, screen_height)
    driver_incognito.set_window_position(half_width, 0)

    request.cls.driver_normal = driver_normal
    request.cls.driver_incognito = driver_incognito

    yield (driver_normal, driver_incognito)

@pytest.fixture(scope="function")
def login_data(request):
    test_type = get_test_type(request.module.__name__)
    return LOGIN_DATA[test_type]
