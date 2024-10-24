import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException, ElementNotInteractableException, JavascriptException
import json

@pytest.mark.h_test
def test_high_school_logins(drivers, login_data):
    driver_normal, driver_incognito = drivers
    WEBSITE_URL, TEACHER_ID, PASSWORD, SCHOOL_NAME, _ = login_data

    # 교사 로그인 (시크릿 모드)
    driver_incognito.get(WEBSITE_URL)
    print("교사 로그인: 웹사이트에 접속했습니다.")

    WebDriverWait(driver_incognito, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".login--item:nth-child(2) > .login--item-button"))).click()
    driver_incognito.find_element(By.ID, "mbrId").send_keys(TEACHER_ID)
    driver_incognito.find_element(By.ID, "loginPw").send_keys(PASSWORD)
    driver_incognito.find_element(By.CSS_SELECTOR, ".margin-t-29").click()

    try:
        WebDriverWait(driver_incognito, 10).until(
            lambda driver: driver.current_url == "https://tb-edu.ontactedu.co.kr/today"
        )
        print("교사가 https://tb-edu.ontactedu.co.kr/today 페이지에 접근했습니다.")
        
        # 네트워크 오류 확인
        logs = driver_incognito.execute_script("var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;")
        network_errors = [log for log in logs if 'status' in log and log['status'] >= 400]
        
        if network_errors:
            print("Fail: 네트워크 요청 중 오류가 발생했습니다.")
            for error in network_errors:
                print(f"URL: {error['name']}, Status: {error['status']}")
            assert False, "교사 로그인 - 네트워크 오류 발생"
        else:
            print("Pass: 교사가 정상적으로 로그인하고 페이지에 접근했습니다.")
    except TimeoutException:
        print("Fail: 교사 로그인 실패 또는 페이지 접근 불가")
        driver_incognito.save_screenshot("teacher_login_failure.png")
        assert False, "교사 로그인 실패"

    # 학생 로그인 (일반 모드)
    driver_normal.get(WEBSITE_URL)
    print("학생 로그인: 웹사이트에 접속했습니다.")

    WebDriverWait(driver_normal, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".login--item:nth-child(1) > .login--item-button"))).click()
    print("학생 로그인 버튼을 클릭했습니다.")

    WebDriverWait(driver_normal, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".flex--fixed"))).click()
    print("학교 검색 입력란을 클릭했습니다.")

    school_find = WebDriverWait(driver_normal, 10).until(EC.presence_of_element_located((By.ID, "schoolFind")))
    school_find.clear()
    school_find.send_keys(SCHOOL_NAME)
    print(f"학교 이름 '{SCHOOL_NAME}'을 입력했습니다.")

    WebDriverWait(driver_normal, 10).until(EC.element_to_be_clickable((By.ID, "schFindBtn"))).click()
    print("학교 검색 버튼을 클릭했습니다.")

    WebDriverWait(driver_normal, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[id^='0']"))).click()
    print("검색 결과에서 학교를 선택했습니다.")

    try:
        popup_button = WebDriverWait(driver_normal, 10).until(
            EC.element_to_be_clickable((By.ID, "schSelectBtn"))
        )
        popup_button.click()
        print("첫 번째 팝업의 학교 선택 버튼을 클릭했습니다.")
    except (TimeoutException, ElementClickInterceptedException):
        print("첫 번째 팝업의 학교 선택 버튼을 클릭할 수 없습다.")
        driver_normal.save_screenshot("first_popup_button_not_clicked.png")

    try:
        confirm_button = WebDriverWait(driver_normal, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button-main.violet[onclick*='toggleOpen'][onclick*='popLayerCloseAndSchSettingConfirm']"))
        )
        
        if not confirm_button.is_displayed():
            print("두 번째 팝업의 확인 버튼이 화면에 표시되지 않습니다.")
            driver_normal.save_screenshot("second_popup_button_not_visible.png")
        else:
            driver_normal.execute_script("arguments[0].click();", confirm_button)
            print("두 번째 팝업의 확인 버튼을 JavaScript로 클릭했습니다.")
        
    except (TimeoutException, ElementClickInterceptedException, NoSuchElementException) as e:
        print(f"두 번째 팝업의 확인 버튼을 클릭할 수 없습니다. 오류: {str(e)}")
        driver_normal.save_screenshot("second_popup_button_not_clicked.png")
        
        print("현재 페이지의 HTML:")
        print(driver_normal.page_source)
        
        print("현재 페이지의 모든 버튼:")
        buttons = driver_normal.find_elements(By.TAG_NAME, "button")
        for button in buttons:
            print(f"Class: {button.get_attribute('class')}, Text: {button.text}, Onclick: {button.get_attribute('onclick')}, Displayed: {button.is_displayed()}")
        
        assert False, "두 번째 팝업의 확인 버튼 클릭 실패"

    WebDriverWait(driver_normal, 10).until(EC.element_to_be_clickable((By.ID, "selectedStdnSchyr"))).click()
    WebDriverWait(driver_normal, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".dropdown--item"))).click()
    print("학년을 선택했습니다.")

    WebDriverWait(driver_normal, 10).until(EC.element_to_be_clickable((By.ID, "selectedStdnBan"))).click()
    WebDriverWait(driver_normal, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".open .dropdown--item"))).click()
    print("반을 선택했습니다.")

    WebDriverWait(driver_normal, 10).until(EC.element_to_be_clickable((By.ID, "selectedStdnNum"))).click()
    WebDriverWait(driver_normal, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".open .dropdown--item"))).click()
    print("번호를 선택했습니다.")

    password_field = WebDriverWait(driver_normal, 10).until(EC.presence_of_element_located((By.ID, "stdn_loginPw")))
    password_field.clear()
    password_field.send_keys(PASSWORD)
    print("비밀번호를 입력했습니다.")

    WebDriverWait(driver_normal, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".login--button"))).click()
    print("로그인 버튼을 클릭했습니다.")

    # 중복 로그인 팝업 처리
    try:
        duplicate_login_popup = WebDriverWait(driver_normal, 10).until(
            EC.element_to_be_clickable((By.ID, "confirmPoupOk"))
        )
        print("중복 로그인 팝업이 감지되었습니다.")
        duplicate_login_popup.click()
        print("중복 로그인 팝업의 확인 버튼을 클릭했습니다.")
    except TimeoutException:
        print("중복 로그인 팝업이 나타나지 않았습니다.")
    except ElementNotInteractableException:
        print("중복 로그인 팝업의 확인 버튼이 클릭 가능한 상태가 아닙니다.")
        driver_normal.save_screenshot("duplicate_login_popup_not_interactable.png")

    try:
        # 대시보드 페이지로의 이동을 확인
        WebDriverWait(driver_normal, 20).until(
            EC.any_of(
                EC.title_contains("학생 대시보드"),
                EC.presence_of_element_located((By.CSS_SELECTOR, ".user-info")),
                EC.url_contains("/today")
            )
        )
        print("학생이 대시보드 페이지에 접근했습니다.")
        
        # 현재 URL 출력
        current_url = driver_normal.current_url
        print(f"현재 페이지 URL: {current_url}")
        
        # 페이지 제목 출력
        page_title = driver_normal.title
        print(f"현재 페이지 제목: {page_title}")
        
        # 네트워크 오류 확인 (수정된 부분)
        try:
            logs = driver_normal.execute_script("""
                var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {};
                var network = performance.getEntries() || {};
                return JSON.stringify(network);
            """)
            network_logs = json.loads(logs)
            network_errors = [log for log in network_logs if 'status' in log and log['status'] >= 400]
            
            if network_errors:
                print("Fail: 네트워크 요청 중 오류가 발생했습니다.")
                for error in network_errors:
                    print(f"URL: {error['name']}, Status: {error['status']}")
                assert False, "학생 로그인 - 네트워크 오류 발생"
            else:
                print("Pass: 학생이 정상적으로 로그인하고 대시보드에 접근했습니다.")
        except JavascriptException as js_error:
            print(f"JavaScript 실행 중 오류 발생: {str(js_error)}")
            print("네트워크 로그를 가져오는 데 실패했지만, 로그인은 성공한 것으로 간주합니다.")
        except json.JSONDecodeError as json_error:
            print(f"JSON 파싱 중 오류 발생: {str(json_error)}")
            print("네트워크 로그를 파싱하는 데 실패했지만, 로그인은 성공한 것으로 간주합니다.")
    
    except TimeoutException:
        print("Fail: 학생 로그인 실패 또는 대시보드 접근 불가")
        driver_normal.save_screenshot("student_login_failure.png")
        
        # 현재 URL과 페이지 소스 출력
        print(f"현재 URL: {driver_normal.current_url}")
        print("현재 페이지 소스:")
        print(driver_normal.page_source)
        
        assert False, "학생 로그인 실패"

    driver_normal.save_screenshot("student_login_success.png")
