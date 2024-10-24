import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

@pytest.mark.h_test
def test_high_teacher_login(setup_drivers, login_data):
    driver_normal, _ = setup_drivers
    WEBSITE_URL, TEACHER_ID, PASSWORD, _, _ = login_data

    driver_normal.get(WEBSITE_URL)
    driver_normal.find_element(By.CSS_SELECTOR, ".login--item:nth-child(2) > .login--item-button").click()
    driver_normal.find_element(By.ID, "mbrId").send_keys(TEACHER_ID)
    driver_normal.find_element(By.ID, "loginPw").send_keys(PASSWORD)
    driver_normal.find_element(By.CSS_SELECTOR, ".margin-t-29").click()

    try:
        WebDriverWait(driver_normal, 10).until(
            lambda driver: driver.current_url == "https://tb-edu.ontactedu.co.kr/today"
        )
        print("Pass: 정상 로그인 후 페이지에 아무 이상이 없음")
    except TimeoutException:
        print("Fail 조건1: 해당 페이지에 접근을 못함")
        assert False, "고등학교 교사 로그인 실패: 올바른 페이지로 리다이렉트되지 않음"

@pytest.mark.h_test
def test_high_student_login(setup_drivers, login_data):
    _, driver_incognito = setup_drivers
    WEBSITE_URL, _, PASSWORD, SCHOOL_NAME, STUDENT_NUM = login_data

    driver_incognito.get(WEBSITE_URL)
    driver_incognito.find_element(By.CSS_SELECTOR, ".login--item:nth-child(1) > .login--item-button").click()
    driver_incognito.find_element(By.ID, "schoolFind").send_keys(SCHOOL_NAME)
    driver_incognito.find_element(By.ID, "schFindBtn").click()
    driver_incognito.find_element(By.ID, "000270").click()
    driver_incognito.find_element(By.ID, "schSelectBtn").click()
    driver_incognito.find_element(By.ID, "selectedStdnNum").send_keys(STUDENT_NUM)
    driver_incognito.find_element(By.ID, "stdn_loginPw").send_keys(PASSWORD)
    driver_incognito.find_element(By.CSS_SELECTOR, ".login--button").click()

    try:
        WebDriverWait(driver_incognito, 10).until(
            lambda driver: "학생 대시보드" in driver.title
        )
        print("Pass: 학생 정상 로그인 후 대시보드에 접근")
    except TimeoutException:
        print("Fail: 학생 로그인 실패 또는 대시보드 접근 불가")
        assert False, "고등학교 학생 로그인 실패"
