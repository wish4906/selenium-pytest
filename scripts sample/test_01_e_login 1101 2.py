import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException

@pytest.mark.e_test
@pytest.mark.order(1)
def test_teacher_login(driver_incognito, login_data):
    WEBSITE_URL, TEACHER_ID, PASSWORD = login_data
    driver_incognito.get(WEBSITE_URL)
    print("교사 로그인: 웹사이트에 접속했습니다.")

    try:
        WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".login--item:nth-child(2) > .login--item-button"))
        )
        WebDriverWait(driver_incognito, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".login--item:nth-child(2) > .login--item-button"))
        ).click()
        driver_incognito.find_element(By.ID, "mbrId").send_keys(TEACHER_ID)
        driver_incognito.find_element(By.ID, "loginPw").send_keys(PASSWORD)
        driver_incognito.find_element(By.CSS_SELECTOR, ".margin-t-29").click()
        print("교사 로그인 정보 입력 및 로그인 버튼 클릭")
    except TimeoutException:
        print("Fail: 교사 로그인 실패")
        driver_incognito.save_screenshot("teacher_login_failure.png")
        assert False, "교사 로그인 실패"

    try:
        WebDriverWait(driver_incognito, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#notiPopupOk"))
        ).click()
        print("팝업 확인 버튼 클릭")
    except TimeoutException:
        print("Fail: 팝업 확인 버튼 클릭 실패")
        driver_incognito.save_screenshot("popup_click_failure.png")
        assert False, "팝업 확인 버튼 클릭 실패"

    try:
        otp_input = WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#login_form > div > div > div > div.otp-box > input"))
        )
        otp_input.send_keys("999999")
        driver_incognito.find_element(By.CSS_SELECTOR, "#login_form > div > div > div > div.otp-box > div > button.button-main.violet").click()
        print("인증번호 입력 및 확인 버튼 클릭")
    except TimeoutException:
        print("Fail: 인증번호 입력 또는 확인 버튼 클릭 실패")
        driver_incognito.save_screenshot("otp_failure.png")
        assert False, "인증번호 입력 또는 확인 버튼 클릭 실패"

    try:
        WebDriverWait(driver_incognito, 10).until(
            lambda driver: driver.current_url == "https://tb-edu.ontactedu.co.kr/today"
        )
        print("교사가 대시보드 페이지에 접근했습니다.")
    except TimeoutException:
        print("Fail: 교사 대시보드 접근 실패")
        driver_incognito.save_screenshot("teacher_dashboard_failure.png")
        assert False, "교사 대시보드 접근 실패"

@pytest.mark.e_test
@pytest.mark.order(2)
def test_student_login(driver_normal, login_data):
    """학생 로그인 테스트"""
    try:
        # 학생 로그인 데이터 가져오기
        student_data = login_data['student']
        WEBSITE_URL, STUDENT_ID, STUDENT_NUM, PASSWORD = student_data
        
        # URL 접속
        driver_normal.get(WEBSITE_URL)
        print("학생 로그인: 웹사이트에 접속했습니다.")
        
        # 로그인 버튼 클릭 전에 페이지 로드 대기
        WebDriverWait(driver_normal, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#login"))
        )
        
        # 로그인 버튼 클릭
        student_login_button = WebDriverWait(driver_normal, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#login > div > div.main-login > div.main-login--button > button:nth-child(1) > div.login--item-button"))
        )
        student_login_button.click()
        
        # 로그인 폼 입력
        WebDriverWait(driver_normal, 10).until(
            EC.visibility_of_element_located((By.ID, "mbrId"))
        )
        driver_normal.find_element(By.ID, "mbrId").send_keys(STUDENT_ID)
        driver_normal.find_element(By.ID, "loginPw").send_keys(PASSWORD)
        driver_normal.find_element(By.CSS_SELECTOR, ".margin-t-29").click()
        print("학생 로그인 정보 입력 및 로그인 버튼 클릭")
    except (TimeoutException, ElementNotInteractableException) as e:
        print(f"Fail: 학생 로그인 실패 - {str(e)}")
        driver_normal.save_screenshot("student_login_failure.png")
        assert False, "학생 로그인 실패"

    try:
        WebDriverWait(driver_normal, 20).until(
            EC.any_of(
                EC.title_contains("학생 대시보드"),
                EC.presence_of_element_located((By.CSS_SELECTOR, ".user-info")),
                EC.url_contains("/today"),
                EC.url_contains("/main")  # live 환경용 URL 패턴 추가
            )
        )
        print("학생이 대시보드 페이지에 접근했습니다.")
    except TimeoutException:
        print("Fail: 학생 대시보드 접근 실패")
        driver_normal.save_screenshot("student_dashboard_failure.png")
        assert False, "학생 대시보드 접근 실패"

