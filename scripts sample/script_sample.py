import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException, ElementNotInteractableException, JavascriptException
import json
import time
from selenium.webdriver.common.action_chains import ActionChains

##기본 클래스
#네트워크 요청 로그를 확인하는 클래스로 Failed 조건2 확인 시 필수
def get_network_logs(driver):
    script = """
    var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {};
    var network = performance.getEntries() || {};
    return JSON.stringify(network);
    """
    try:
        logs = driver.execute_script(script)
        return json.loads(logs)
    except Exception as e:
        print(f"네트워크 로그를 가져오는 중 오류 발생: {str(e)}")
        return []

##기본 클래스    
#페이지 로드까지 기다리는 로드가 완료되지 않으면 버튼 정보를 불러올 수 없어 find_and_click_element 함수가 동작하지 않을 수 있음 밑 코드랑 세트
def wait_for_page_load(driver, timeout=30):
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
    )

##기본 클래스    
#테스트 코드에서 지속적으로 호출이 필요한 클래스 개념
def find_and_click_element(driver, selectors, timeout=20):
    for selector in selectors:
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable(selector)
            )
            element.click()
            return True
        except (TimeoutException, NoSuchElementException, ElementClickInterceptedException):
            continue
    return False

@pytest.mark.e_test
def test_Elementary_school_logins(drivers, login_data):
    driver_normal, driver_incognito = drivers
    WEBSITE_URL, TEACHER_ID, PASSWORD, SCHOOL_NAME, STUDENT_NUM = login_data

    # 교사 로그인 (시크릿 모드)
    driver_incognito.get(WEBSITE_URL)
    #print("교사 로그인: 웹사이트에 접속했습니다.")

    WebDriverWait(driver_incognito, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".login--item:nth-child(2) > .login--item-button"))).click()
    driver_incognito.find_element(By.ID, "mbrId").send_keys(TEACHER_ID)
    driver_incognito.find_element(By.ID, "loginPw").send_keys(PASSWORD)
    driver_incognito.find_element(By.CSS_SELECTOR, ".margin-t-29").click()

    # 인증번호 팝업 확인 및 처리
    try:
        # 인증번호 팝업이 나타날 때까지 대기
        WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located((By.ID, "notiPopupMsg"))
        )
       # print("인증번호 팝업이 나타났습니다. 확인 버튼을 클릭합니다.")
        
        # 스크롤하여 요소가 보이도록 함
        noti_popup_ok = driver_incognito.find_element(By.ID, "notiPopupOk")
        driver_incognito.execute_script("arguments[0].scrollIntoView();", noti_popup_ok)
        
        # 확인 버튼 클릭
        WebDriverWait(driver_incognito, 10).until(EC.element_to_be_clickable((By.ID, "notiPopupOk"))).click()

        # OTP 입력
        otp_input = WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".otp"))
        )
        otp_input.click()
        otp_input.send_keys("999999")  # 인증번호 입력
       # print("인증번호를 입력했습니다.")

        # 확인 및 로그인 버튼 클릭
        try:
            otp_button = WebDriverWait(driver_incognito, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".button-main.violet"))
            )
            driver_incognito.execute_script("arguments[0].scrollIntoView();", otp_button)  # 버튼이 보이도록 스크롤
            otp_button.click()  # 클릭
          #  print("확인 및 로그인 버튼을 클릭했습니다.")
        except TimeoutException:
           # print("확인 및 로그인 버튼을 찾을 수 없습니다.")
            driver_incognito.save_screenshot("otp_button_click_failed.png")
            raise Exception("확인 및 로그인 버튼을 찾을 수 없습니다.")

    except TimeoutException:
        print("인증번호 팝업이 나타나지 않았습니다. 로그인 진행 중...")
        driver_incognito.find_element(By.CSS_SELECTOR, ".login--button > .violet").click()  # 로그인 버튼 클릭

    # 로그인 후 페이지 확인
    try:
        WebDriverWait(driver_incognito, 10).until(
            lambda driver: driver.current_url == "https://tb-edu.ontactedu.co.kr/today"
        )
      #  print("교사가 https://tb-edu.ontactedu.co.kr/today 페이지에 접근했습니다.")
    except TimeoutException:
     #   print("Fail: 교사 로그인 실패 또는 페이지 접근 불가")
        driver_incognito.save_screenshot("teacher_login_failure.png")
        assert False, "교사 로그인 실패"

    # 학생 로그인 (일반 모드)
    driver_normal.get(WEBSITE_URL)
  #  print("학생 로그인: 웹사이트에 접속했습니다.")

    wait_for_page_load(driver_normal)

    # 학생 로그인 버튼 클릭
    student_login_selectors = [
        (By.XPATH, "//div[contains(@class, 'login--item-button') and text()='로그인 하기']"),
        (By.CSS_SELECTOR, "div.login--item-button"),
        (By.XPATH, "//*[text()='로그인 하기']"),
        (By.XPATH, "//div[contains(text(), '로그인 하기')]"),
    ]

    def click_student_login(driver):
        for selector in student_login_selectors:
            try:
                element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(selector))
                driver.execute_script("arguments[0].click();", element)
                print("학생 로그인 버튼을 클릭했습니다.")
                return True
            except (TimeoutException, NoSuchElementException, ElementClickInterceptedException):
                continue
        return False

    if click_student_login(driver_normal):
        wait_for_page_load(driver_normal)
    else:
        print("학생 로그인 버튼을 찾을 수 없습니다.")
        print("현재 페이지 소스:")
        print(driver_normal.page_source)
        driver_normal.save_screenshot("student_login_failed.png")
        raise Exception("학생 로그인 버튼을 찾을 수 없습니다.")

    # 디버깅을 위한 스크린샷 저장
    driver_normal.save_screenshot("after_student_login_click.png")

    # 현재 URL 출력
    print(f"현재 페이지 URL: {driver_normal.current_url}")

    # 잠시 대기
    time.sleep(2)

    # 학교 검색 팝업 버튼 클릭
    school_search_popup_selectors = [
        (By.CSS_SELECTOR, "button.ico-main-search-black"),
        (By.XPATH, "//button[contains(@class, 'ico-main-search-black')]"),
        (By.XPATH, "//button[text()='검색']"),
        (By.XPATH, "//button[contains(@class, 'flex--fixed') and contains(@class, 'margin-r-19')]"),
    ]

    def click_school_search_popup(driver):
        for selector in school_search_popup_selectors:
            try:
                element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(selector))
                driver.execute_script("arguments[0].click();", element)
                print("학교 검색 팝업 버튼을 클릭했습니다.")
                return True
            except (TimeoutException, NoSuchElementException, ElementClickInterceptedException):
                continue
        return False

    if click_school_search_popup(driver_normal):
        wait_for_page_load(driver_normal)
    else:
        print("학교 검색 팝업 버튼을 찾을 수 없습니다.")
        print("현재 페이지 소스:")
        print(driver_normal.page_source)
        driver_normal.save_screenshot("school_search_popup_failed.png")
        raise Exception("학교 검색 팝업 버튼을 찾을 수 없습니다.")

    # 팝업이 열릴 때까지 잠시 대기
    time.sleep(2)

    # 학교 검색 입력란 찾기 및 입력
    try:
        school_input = WebDriverWait(driver_normal, 10).until(
            EC.presence_of_element_located((By.ID, "schoolFind"))
        )
        school_input.clear()
        school_input.send_keys(SCHOOL_NAME)
        print(f"학교 이름 '{SCHOOL_NAME}'을 입력했습니다.")
    except TimeoutException:
        print("학교 검색 입력란을 찾을 수 없습니다.")
        driver_normal.save_screenshot("school_input_failed.png")
        raise Exception("학교 검색 입력란을 찾을 수 없습니다.")

    # 검색 버튼 클릭
    try:
        search_button = WebDriverWait(driver_normal, 10).until(
            EC.element_to_be_clickable((By.ID, "schFindBtn"))
        )
        search_button.click()
        print("학교 검색 버튼을 클릭했습니다.")
    except TimeoutException:
        print("학교 검색 버튼을 찾을 수 없습니다.")
        driver_normal.save_screenshot("school_search_button_failed.png")
        raise Exception("학교 검색 버튼을 찾을 수 없습니다.")

    wait_for_page_load(driver_normal)

    # 검색 결과에서 학교 선택
    try:
        # 검색 결과가 로드될 때까지 대기
        WebDriverWait(driver_normal, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "label.f-18-n.f-extrabold.f-black-80"))
        )
        
        # 모든 검색 결과 라벨 찾기
        school_labels = driver_normal.find_elements(By.CSS_SELECTOR, "label.f-18-n.f-extrabold.f-black-80")
        
        matching_school = None
        for label in school_labels:
            if SCHOOL_NAME.lower() in label.text.lower():
                matching_school = label
                break
        
        if matching_school:
            # 라벨의 'for' 속성 값으로 라디오 버튼 찾기
            radio_id = matching_school.get_attribute('for')
            radio_button = driver_normal.find_element(By.ID, radio_id)
            
            # 라디오 버튼 클릭
            driver_normal.execute_script("arguments[0].click();", radio_button)
            print(f"'{SCHOOL_NAME}' 학교를 선택했습니다.")
        else:
            print(f"'{SCHOOL_NAME}' 학교를 검색 결과에서 찾을 수 없습니다.")
            driver_normal.save_screenshot("school_not_found.png")
            raise Exception(f"'{SCHOOL_NAME}' 학교를 검색 결과에서 찾을 수 없습니다.")

    except TimeoutException:
        print("검색 결과가 로드되지 않았습니다.")
        driver_normal.save_screenshot("search_results_not_loaded.png")
        raise Exception("검색 결과가 로드되지 않았습니다.")

    wait_for_page_load(driver_normal)

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
        print("중복 로그인 팝의 확인 버튼이 클릭 가능한 상태가 아닙니다.")
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
            print("네트워크 로그를 파싱하는 데 실패했지만, 로그인은 성한 것으로 간주합니다.")
    
    except TimeoutException:
        print("Fail: 학생 로그인 실패 또는 대시보드 접근 불가")
        driver_normal.save_screenshot("student_login_failure.png")
        
        # 현재 URL과 페이지 소스 출력
        print(f"현재 URL: {driver_normal.current_url}")
        print("현재 페이지 소스:")
        print(driver_normal.page_source)
        
        assert False, "학생 로그인 실패"

    driver_normal.save_screenshot("student_login_success.png")

@classmethod
def teardown_class(cls):
    if hasattr(cls, 'driver_normal') and cls.driver_normal:
        cls.driver_normal.quit()
    if hasattr(cls, 'driver_incognito') and cls.driver_incognito:
        cls.driver_incognito.quit()


