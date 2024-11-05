import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException

@pytest.mark.e_test(1)
def test_teacher_login(drivers, login_data):
    driver_normal, driver_incognito = drivers
    WEBSITE_URL, TEACHER_ID, PASSWORD = login_data['teacher']

    # 교사 로그인 (시크릿 모드)
    driver_incognito.get(WEBSITE_URL)
    print("교사 로그인: 웹사이트에 접속했습니다.")

    try:
        WebDriverWait(driver_incognito, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".login--item:nth-child(2) > .login--item-button"))
        ).click()
        driver_incognito.find_element(By.ID, "mbrId").send_keys(TEACHER_ID)
        driver_incognito.find_element(By.ID, "loginPw").send_keys(PASSWORD)
        driver_incognito.find_element(By.CSS_SELECTOR, ".margin-t-29").click()
        print("교사 로그인 정보 입력 및 로그인 버튼 클릭")
    except Exception as e:
        print(f"Fail: 교사 로그인 실패 - {str(e)}")
        driver_incognito.save_screenshot("teacher_login_failure.png")
        assert False, "교사 로그인 실패"

    # 로그인 후 페이지 확인
    try:
        WebDriverWait(driver_incognito, 10).until(
            lambda driver: driver.current_url == "https://tb-edu.ontactedu.co.kr/today"
        )
        print("교사가 https://tb-edu.ontactedu.co.kr/today 페이지에 접근했습니다.")
    except TimeoutException:
        print("Fail: 교사 로그인 실패 또는 페이지 접근 불가")
        driver_incognito.save_screenshot("teacher_login_failure.png")
        assert False, "교사 로그인 실패"

@pytest.mark.e_test(2)
def test_student_login(drivers, login_data):
    driver_normal, driver_incognito = drivers
    WEBSITE_URL, SCHOOL_NAME, STUDENT_NUM, PASSWORD = login_data['student']

    # 학생 로그인 (일반 모드)
    driver_normal.get(WEBSITE_URL)
    print("학생 로그인: 웹사이트에 접속했습니다.")

    try:
        student_login_button = WebDriverWait(driver_normal, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#login > div > div.main-login > div.main-login--button > button:nth-child(1) > div.login--item-button"))
        )
        student_login_button.click()
        print("학생 로그인 버튼을 클릭했습니다.")
    except TimeoutException:
        print("Fail: 학생 로그인 버튼을 찾을 수 없습니다.")
        driver_normal.save_screenshot("student_login_failed.png")
        assert False, "학생 로그인 버튼을 찾을 수 없습니다."

    # 로그인 후 페이지 확인
    try:
        WebDriverWait(driver_normal, 20).until(
            EC.any_of(
                EC.title_contains("학생 대시보드"),
                EC.presence_of_element_located((By.CSS_SELECTOR, ".user-info")),
                EC.url_contains("/today")
            )
        )
        print("학생이 대시보드 페이지에 접근했습니다.")
    except TimeoutException:
        print("Fail: 학생 로그인 실패 또는 대시보드 접근 불가")
        driver_normal.save_screenshot("student_login_failure.png")
        assert False, "학생 로그인 실패"




