import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException

@pytest.mark.h_test

def click_element(driver, element):
    """JavaScript를 사용하여 요소 클릭"""
    driver.execute_script("arguments[0].click();", element)

def test_01_teacher_login(driver_incognito, login_data):
    """교사 로그인 테스트"""
    WEBSITE_URL, TEACHER_ID, PASSWORD = login_data
    driver_incognito.get(WEBSITE_URL)
    print("교사 로그인: 웹사이트에 접속했습니다.")

    # 1. 시스템 공지 팝업 닫기 버튼 클릭 전에 체크박스 체크
    try:
        ispopup = WebDriverWait(driver_incognito, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,"#sysNoticeTemp > div > div.layer__contents > div.page__button.padding-t-25.padding-b-20 > button"))
        )
        if ispopup.is_displayed() :
            # 체크박스 체크
            hide_all_day_checkbox = WebDriverWait(driver_incognito, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#hideAllDay"))
            )
            if not hide_all_day_checkbox.is_selected():  # 체크박스가 체크되어 있지 않으면 체크
                hide_all_day_checkbox.click()
                print("오늘 하루 보지 않기 체크박스 체크")

            # 시스템 공지 팝업 닫기 버튼 확인
            if ispopup.is_displayed():  # 시스템 공지 팝업 닫기 버튼이 보이는지 확인
                ispopup.click()
                print("시스템 공지 팝업 닫기 버튼 클릭")
            else:
                print("시스템 공지 팝업 닫기 버튼 클릭 하지 않음.")

        else: #Git push test
            print("팝업 없음 1111111")

    except TimeoutException:
        print("시스템 공지 팝업 닫기 버튼이 없음, 클릭하지 않음.")

    # 2. 노티 팝업 확인 버튼 클릭
    try:
        popup_button = WebDriverWait(driver_incognito, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#notiPopupOk"))
        )
        if popup_button.is_displayed():  # 노티 팝업 확인 버튼이 보이는지 확인
            driver_incognito.execute_script("arguments[0].scrollIntoView(true);", popup_button)  # 버튼이 보이도록 스크롤
            popup_button.click()
            print("노티 팝업 확인 버튼 클릭")
        else:
            print("노티 팝업이 보이지 않음, 클릭하지 않음.")
    except TimeoutException:
        print("노티 팝업 확인 버튼이 없음, 클릭하지 않음.")


    # 3. 아이디 / 패스워드 입력
    try:
        login_button = WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".login--item:nth-child(2) > .login--item-button"))
        )
        click_element(driver_incognito, login_button)
        
        # 다른 클릭 동작들도 동일하게 처리
        driver_incognito.find_element(By.ID, "mbrId").send_keys(TEACHER_ID)
        driver_incognito.find_element(By.ID, "loginPw").send_keys(PASSWORD)
        login_submit = driver_incognito.find_element(By.CSS_SELECTOR, ".margin-t-29")
        click_element(driver_incognito, login_submit)
        print("교사 로그인 정보 입력 및 로그인 버튼 클릭")
    except TimeoutException:
        print("Fail: 교사 로그인 실패")
        driver_incognito.save_screenshot("teacher_login_failure.png")
        assert False, "교사 로그인 실패"

    try: # 인증번호 안내 팝업
        popup_button = driver_incognito.find_elements(By.CSS_SELECTOR, "#notiPopupOk")
        if popup_button and popup_button[0].is_displayed():
            WebDriverWait(driver_incognito, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#notiPopupOk"))
        ).click()
        print("인증번호 팝업 확인 버튼 클릭")
    except TimeoutException:
        print("Fail: 인증번호 팝업 확인 버튼 클릭 실패")
        driver_incognito.save_screenshot("popup_click_failure.png")
        # assert False, "팝업 확인 버튼 클릭 실패"
        pytest.fail("팝업 확인 버튼 클릭 실패111111111111111111111111", pytrace=True)

    try: # 인증번호 입력
        otp_inputs = driver_incognito.find_elements(By.CSS_SELECTOR,"#login_form > div > div > div > div.otp-box > input")
        if otp_inputs and otp_inputs[0].is_displayed():
            otp_inputs[0].send_keys("999999")
            driver_incognito.find_element(By.CSS_SELECTOR,"#login_form > div > div > div > div.otp-box > div > button.button-main.violet").click()
            print("인증번호 입력 및 확인 버튼 클릭")
        else:
            print("OTP 입력 창이 없어 넘어갑니다.")
    except TimeoutException:
        print("Fail: 인증번호 입력 또는 확인 버튼 클릭 실패")
        driver_incognito.save_screenshot("otp_failure.png")
        # assert False, "인증번호 입력 또는 확인 버튼 클릭 실패"
        pytest.fail("인증번호 팝업 확인 버튼 클릭 실패2222222222222222222222222222", pytrace=True)

    try:
        WebDriverWait(driver_incognito, 10).until(
            EC.any_of(
                EC.url_contains("/today")
            )
        )
        print("교사가 대시보드 페이지에 접근했습니다.")
    except TimeoutException:
        print("Fail: 교사 대시보드 접근 실패")
        driver_incognito.save_screenshot("teacher_dashboard_failure.png")
        assert False, "교사 대시보드 접근 실패"

@pytest.mark.h_test

def test_02_student_login(driver_normal, login_data):
    """학생 로그인 테스트"""
    WEBSITE_URL, STUDENT_ID, STUDENT_NUM, PASSWORD = login_data
    driver_normal.get(WEBSITE_URL)
    print("학생 로그인: 웹사이트에 접속했습니다.")
    
    try:
        # 로그인 버튼 클릭
        student_login_button = WebDriverWait(driver_normal, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#login > div > div.main-login > div.main-login--button > button:nth-child(1)"))
        )
        click_element(driver_normal, student_login_button)
        print("학생 로그인 버튼 클릭")
        
        # 학교 검색 버튼 클릭하여 팝업 열기
        search_button = WebDriverWait(driver_normal, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#login_form > div > div > div.input-box.input-box--text.is--search.bg--gray > button"))
        )
        click_element(driver_normal, search_button)
        print("학교 검색 팝업 열기")
        
        # 학교명 입력
        WebDriverWait(driver_normal, 10).until(
            EC.visibility_of_element_located((By.ID, "schoolFind"))
        )
        school_input = driver_normal.find_element(By.ID, "schoolFind")
        school_input.send_keys(STUDENT_ID)
        
        # 검색 버튼 클릭
        search_btn = driver_normal.find_element(By.ID, "schFindBtn")
        click_element(driver_normal, search_btn)
        print("학교 검색 버튼 클릭")
        
        # 검색 결과가 나올 때까지 대기 (라벨 텍스트로 확인)
        search_result = WebDriverWait(driver_normal, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//label[contains(text(), '{STUDENT_ID}')]"))
        )
        print("학교 검색 결과 확인")
        
        # 검색된 학교의 라디오 버튼 클릭
        radio_id = search_result.get_attribute("for")
        radio_button = driver_normal.find_element(By.ID, radio_id)
        click_element(driver_normal, radio_button)
        print("학교 라디오 버튼 선택")
        
        # 선택 버튼 클릭
        select_button = WebDriverWait(driver_normal, 10).until(
            EC.element_to_be_clickable((By.ID, "schSelectBtn"))
        )
        click_element(driver_normal, select_button)
        print("학교 선택 완료")
        
        # 팝업 확인 버튼 클릭 후 대기
        popup_confirm = WebDriverWait(driver_normal, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.wrap.is--dark > div.layer-area.modal-area.modal-default.is--school--setting > div.layer__container > div.page__button > button.button-main.violet"))
        )
        click_element(driver_normal, popup_confirm)
        print("학교 선택 팝업 확인")
        
        # 팝업이 사라질 때까지 대기
        WebDriverWait(driver_normal, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.layer-area.modal-area.modal-default.is--school--setting"))
        )
        
        # 학년 선택
        grade_dropdown = WebDriverWait(driver_normal, 10).until(
            EC.element_to_be_clickable((By.ID, "selectedStdnSchyr"))
        )
        click_element(driver_normal, grade_dropdown)
        first_grade = WebDriverWait(driver_normal, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".dropdown--item"))
        )
        click_element(driver_normal, first_grade)
        
        # 반 선택
        class_dropdown = WebDriverWait(driver_normal, 10).until(
            EC.element_to_be_clickable((By.ID, "selectedStdnBan"))
        )
        click_element(driver_normal, class_dropdown)
        first_class = WebDriverWait(driver_normal, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".open .dropdown--item"))
        )
        click_element(driver_normal, first_class)
        
        # 번호 선택
        number_dropdown = WebDriverWait(driver_normal, 10).until(
            EC.element_to_be_clickable((By.ID, "selectedStdnNum"))
        )
        click_element(driver_normal, number_dropdown)
        first_number = WebDriverWait(driver_normal, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".open .dropdown--item:nth-child(1)"))
        )
        click_element(driver_normal, first_number)
        
        # 비밀번호 입력
        driver_normal.find_element(By.ID, "stdn_loginPw").send_keys(PASSWORD)
        
        # 로그인 버튼 클릭
        login_button = driver_normal.find_element(By.CSS_SELECTOR, "#login_form > div > div > button")
        click_element(driver_normal, login_button)
        print("학생 로그인 정보 입력 및 로그인 버튼 클릭")
        
        # 중복 로그인 팝업 처리
        try:
            duplicate_login_confirm = WebDriverWait(driver_normal, 5).until(
                EC.element_to_be_clickable((By.ID, "confirmPoupOk"))
            )
            click_element(driver_normal, duplicate_login_confirm)
            print("중복 로그인 팝업 확인")
        except TimeoutException:
            print("중복 로그인 팝업이 없습니다.")
            pass
        
    except TimeoutException:
        print("Fail: 학생 로그인 실패")
        driver_normal.save_screenshot("student_login_failure.png")
        assert False, "학생 로그인 실패"

    try:
        WebDriverWait(driver_normal, 20).until(
            EC.any_of(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".user-info")),
                EC.url_contains("/today"),
            )
        )
        print("학생이 대시보드 페이지에 접근했습니다.")
    except TimeoutException:
        print("Fail: 학생 대시보드 접근 실패")
        driver_normal.save_screenshot("student_dashboard_failure.png")
        assert False, "학생 대시보드 접근 실패"

@pytest.mark.h_test

def test_03_teacher_logout(driver_incognito, base_url):
    """교사 로그아웃 테스트"""
    try:
        # 로그아웃 버튼 찾기
        logout_button = WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#gnb > div.header--wrapper > div.header--utill > div.header--utill__user > button"))
        )
        driver_incognito.execute_script("arguments[0].click();", logout_button)
        print("로그아웃 버튼 클릭")
        
        # 로그아웃 확인 팝업의 확인 버튼 클릭
        confirm_button = WebDriverWait(driver_incognito, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#gnb > div:nth-child(3) > div > div > div.layer__container.confirm.active > div.page__button > button.button-main.is--large.violet"))
        )
        driver_incognito.execute_script("arguments[0].click();", confirm_button)
        print("로그아웃 확인 팝업 확인")
        
        # 로그아웃 완료 팝업의 확인 버튼 클릭
        complete_button = WebDriverWait(driver_incognito, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#gnb > div:nth-child(3) > div > div > div.layer__container.alert.active > div.page__button > button"))
        )
        driver_incognito.execute_script("arguments[0].click();", complete_button)
        print("로그아웃 완료 팝업 확인")
        
        # 로그인 페이지로 이동 확인
        WebDriverWait(driver_incognito, 10).until(
            EC.url_contains(base_url)
        )
        print("로그아웃 성공: 로그인 페이지로 이동")
        
    except Exception as e:
        print(f"Fail: 로그아웃 실패 - {str(e)}")
        driver_incognito.save_screenshot("teacher_logout_failure.png")
        assert False, f"로그아웃 실패: {str(e)}"

@pytest.mark.h_test
def test_04_student_logout(driver_normal, base_url):
    """학생 로그아웃 테스트"""
    try:
        # 로그아웃 버튼 찾기
        logout_button = WebDriverWait(driver_normal, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#gnb > div.header--wrapper > div.header--utill > div.header--utill__user > button"))
        )
        driver_normal.execute_script("arguments[0].click();", logout_button)
        print("로그아웃 버튼 클릭")
        
        # 로그아웃 확인 팝업의 확인 버튼 클릭
        confirm_button = WebDriverWait(driver_normal, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#gnb > div:nth-child(3) > div > div > div.layer__container.confirm.active > div.page__button > button.button-main.is--large.violet"))
        )
        driver_normal.execute_script("arguments[0].click();", confirm_button)
        print("로그아웃 확인 팝업 확인")
        
        # 로그아웃 완료 팝업의 확인 버튼 클릭
        complete_button = WebDriverWait(driver_normal, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#gnb > div:nth-child(3) > div > div > div.layer__container.alert.active > div.page__button > button"))
        )
        driver_normal.execute_script("arguments[0].click();", complete_button)
        print("로그아웃 완료 팝업 확인")
        
        # 로그인 페이지로 이동 확인
        WebDriverWait(driver_normal, 10).until(
            EC.url_contains(base_url)
        )
        print("로그아웃 성공: 로그인 페이지로 이동")
        
    except Exception as e:
        print(f"Fail: 로그아웃 실패 - {str(e)}")
        driver_normal.save_screenshot("student_logout_failure.png")
        assert False, f"로그아웃 실패: {str(e)}"