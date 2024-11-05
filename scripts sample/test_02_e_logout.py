import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def setup_method():
    driver = webdriver.Chrome()
    driver.set_window_size(810, 960)
    return driver

def teardown_method(driver):
    driver.quit()

@pytest.mark.e_test
def test_logout():
    driver = setup_method()
    try:
        driver.get("https://tb-edu.ontactedu.co.kr/today")

        # 로그아웃 버튼 클릭
        try:
            logout_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".header--utill__logout"))
            )
            logout_button.click()
            print("로그아웃 버튼을 클릭했습니다.")
        except TimeoutException:
            print("로그아웃 버튼을 찾을 수 없습니다.")
            driver.save_screenshot("logout_button_failed.png")
            raise Exception("로그아웃 버튼을 찾을 수 없습니다.")

        # 확인 팝업의 확인 버튼 클릭
        try:
            confirm_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".confirm .violet"))
            )
            confirm_button.click()
            print("확인 팝업의 확인 버튼을 클릭했습니다.")
        except TimeoutException:
            print("확인 팝업의 확인 버튼을 찾을 수 없습니다.")
            driver.save_screenshot("confirm_button_failed.png")
            raise Exception("확인 팝업의 확인 버튼을 찾을 수 없습니다.")

        # 최종 확인 팝업의 확인 버튼 클릭
        try:
            final_confirm_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".alert .button-main"))
            )
            final_confirm_button.click()
            print("최종 확인 팝업의 확인 버튼을 클릭했습니다.")
        except TimeoutException:
            print("최종 확인 팝업의 확인 버튼을 찾을 수 없습니다.")
            driver.save_screenshot("final_confirm_button_failed.png")
            raise Exception("최종 확인 팝업의 확인 버튼을 찾을 수 없습니다.")

        print("로그아웃이 완료되었습니다.")

    finally:
        teardown_method(driver)


