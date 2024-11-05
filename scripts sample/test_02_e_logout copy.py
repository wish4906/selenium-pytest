import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException

def find_and_click_element(driver, selector, timeout=20):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(selector)
        )
        element.click()
        return True
    except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
        print(f"Element not clickable: {e}")
        return False

@pytest.mark.e_test(3)
def test_teacher_logout(drivers):
    driver_normal, driver_incognito = drivers

    # 로그아웃 버튼 클릭
    if find_and_click_element(driver_incognito, (By.CSS_SELECTOR, "#gnb > div.header--wrapper > div.header--utill > div.header--utill__user > button")):
        print("교사 로그아웃: 버튼 클릭 성공.")
    else:
        print("Fail: 교사 로그아웃 버튼 클릭 실패.")
        driver_incognito.save_screenshot("teacher_logout_failure.png")
        return

    # 로그아웃 확인 버튼 클릭
    if find_and_click_element(driver_incognito, (By.CSS_SELECTOR, "#gnb > div:nth-child(3) > div > div > div.layer__container.confirm.active > div.page__button > button.button-main.is--large.violet")):
        print("로그아웃 확인 버튼 클릭 성공.")
    else:
        print("Fail: 로그아웃 확인 버튼 클릭 실패.")
        driver_incognito.save_screenshot("teacher_logout_failure.png")
        return

@pytest.mark.e_test(4)
def test_student_logout(drivers):
    driver_normal, driver_incognito = drivers  # 두 드라이버를 받음
    # 로그아웃 버튼 클릭
    if find_and_click_element(driver_normal, (By.CSS_SELECTOR, "#gnb > div.header--wrapper > div.header--utill > div.header--utill__user > button")):
        print("학생 로그아웃: 버튼 클릭 성공.")
    else:
        print("학생 로그아웃: 버튼 클릭 실패.")
        return

    # 로그아웃 확인 버튼 클릭
    if find_and_click_element(driver_normal, (By.CSS_SELECTOR, "#gnb > div:nth-child(3) > div > div > div.layer__container.confirm.active > div.page__button > button.button-main.is--large.violet")):
        print("로그아웃 확인 버튼 클릭 성공.")
    else:
        print("로그아웃 확인 버튼 클릭 실패.")
        return



