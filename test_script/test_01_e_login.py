import pytest
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@pytest.mark.e_test

def click_element(driver, element):
    """JavaScript를 사용하여 요소 클릭"""
    driver.execute_script("arguments[0].click();", element)


def test_001_teacher_login(driver_incognito, login_data):
    """교사 로그인 테스트"""
    WEBSITE_URL, TEACHER_ID, PASSWORD = login_data
    driver_incognito.get(WEBSITE_URL)
    logging.info("교사 로그인: 웹사이트에 접속했습니다.")

# 1. 시스템 공지 팝업 닫기 버튼 클릭 전에 체크박스 체크
    try:
        # 시스템 공지 팝업 닫기 버튼 확인
        sys_notice_button = WebDriverWait(driver_incognito, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#sysNoticeTemp > div > div.layer__contents > div.page__button.padding-t-25.padding-b-20 > button"))
        )
        if sys_notice_button.is_displayed():  # 시스템 공지 팝업 닫기 버튼이 보이는지 확인

            # 체크박스 체크
            hide_all_day_checkbox = WebDriverWait(driver_incognito, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#hideAllDay"))
            )
            if not hide_all_day_checkbox.is_selected():  # 체크박스가 체크되어 있지 않으면 체크
                hide_all_day_checkbox.click()
                logging.info("오늘 하루 보지 않기 체크박스 체크")

            sys_notice_button.click()
            logging.info("시스템 공지 팝업 닫기 버튼 클릭")

        else:
            logging.info("시스템 공지 팝업이 보이지 않음, 클릭하지 않음.")
    except TimeoutException:
        logging.warning("시스템 공지 팝업 닫기 버튼이 없음, 클릭하지 않음.")

    # 2. 노티 팝업 확인 버튼 클릭
    try:
        popup_button = WebDriverWait(driver_incognito, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#notiPopupOk"))
        )
        if popup_button.is_displayed():  # 노티 팝업 확인 버튼이 보이는지 확인
            driver_incognito.execute_script("arguments[0].scrollIntoView(true);", popup_button)  # 버튼이 보이도록 스크롤
            popup_button.click()
            logging.info("노티 팝업 확인 버튼 클릭")
        else:
            logging.info("노티 팝업이 보이지 않음, 클릭하지 않음.")
    except TimeoutException:
        logging.warning("노티 팝업 확인 버튼이 없음, 클릭하지 않음.")


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
        logging.info("교사 로그인 정보 입력 및 로그인 버튼 클릭")
    except TimeoutException:
        logging.error("Fail: 교사 로그인 실패")
        driver_incognito.save_screenshot("teacher_login_failure.png")
        assert False, "교사 로그인 실패"

    # 2. 인증번호 발송 확인 팝업의 확인 버튼 클릭
    try:
        confirm_button = WebDriverWait(driver_incognito, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#notiPopupOk"))  # 인증번호 발송 확인 버튼
        )
        if confirm_button.is_displayed():  # 인증번호 발송 확인 버튼이 보이는지 확인
            driver_incognito.execute_script("arguments[0].scrollIntoView(true);", confirm_button)  # 버튼이 보이도록 스크롤
            confirm_button.click()  # JavaScript로 버튼 클릭
            logging.info("인증번호 발송 확인 버튼 클릭")
        else:
            logging.info("인증번호 발송 확인 버튼이 보이지 않음, 클릭하지 않음.")
    except TimeoutException:
        logging.warning("인증번호 발송 확인 버튼이 없음, 클릭하지 않음.")

    # 3. 인증번호 입력 처리
    try:
        otp_input = WebDriverWait(driver_incognito, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#login_form > div > div > div > div.otp-box > input"))
        )
        if otp_input.is_displayed():  # 인증번호 입력 필드가 보이는지 확인
            otp_input.send_keys("999999")
            driver_incognito.find_element(By.CSS_SELECTOR, "#login_form > div > div > div > div.otp-box > div > button.button-main.violet").click()
            logging.info("인증번호 입력 및 확인 버튼 클릭")
        else:
            logging.info("인증번호 입력 필드가 보이지 않음, 입력하지 않음.")
    except TimeoutException:
        logging.warning("인증번호 입력 필드가 없음, 입력하지 않음.")

    # 4. 중복 로그인 팝업 처리
    try:
        # 중복 로그인 팝업 확인
        multi_login_popup = WebDriverWait(driver_incognito, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#teacher-multi-login > div.layer__container"))
        )
        logging.info("중복 로그인 팝업이 나타났습니다.")

        # 다른 기기 로그아웃 라디오 버튼 선택
        force_logout_radio = driver_incognito.find_element(By.CSS_SELECTOR, "#force-logout")
        force_logout_radio.click()
        logging.info("다른 기기 로그아웃 라디오 버튼 선택")

        # 로그인 버튼 클릭
        login_button = driver_incognito.find_element(By.CSS_SELECTOR, "#teacher-multi-login > div.layer__container > div.page__button > button.button-main.violet.width-150")
        login_button.click()
        logging.info("로그인 버튼 클릭")

    except TimeoutException:
        logging.warning("중복 로그인 팝업이 나타나지 않았습니다. 대시보드 페이지 접근 확인합니다.")

    # 대시보드 페이지 접근 확인
    try:
        WebDriverWait(driver_incognito, 10).until(
            EC.url_contains("/today")  # /main 제거
        )
        logging.info("교사가 대시보드 페이지에 접근했습니다.")
    except TimeoutException:
        logging.error("Fail: 교사 대시보드 접근 실패")
        driver_incognito.save_screenshot("teacher_dashboard_failure.png")
        assert False, "교사 대시보드 접근 실패"

@pytest.mark.e_test

def test_002_student_login(driver_normal, login_data):
    """학생 로그인 테스트"""
    WEBSITE_URL, STUDENT_ID, STUDENT_NUM, PASSWORD = login_data
    driver_normal.get(WEBSITE_URL)
    logging.info("학생 로그인: 웹사이트에 접속했습니다.")

# 1. 시스템 공지 팝업 닫기 버튼 클릭 전에 체크박스 체크
    try:
        # 시스템 공지 팝업 닫기 버튼 확인
        sys_notice_button = WebDriverWait(driver_normal, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#sysNoticeTemp > div > div.layer__contents > div.page__button.padding-t-25.padding-b-20 > button"))
        )
        if sys_notice_button.is_displayed():  # 시스템 공지 팝업 닫기 버튼이 보이는지 확인

            # 체크박스 체크
            hide_all_day_checkbox = WebDriverWait(driver_normal, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#hideAllDay"))
            )
            if not hide_all_day_checkbox.is_selected():  # 체크박스가 체크되어 있지 않으면 체크
                hide_all_day_checkbox.click()
                logging.info("오늘 하루 보지 않기 체크박스 체크")

            sys_notice_button.click()
            logging.info("시스템 공지 팝업 닫기 버튼 클릭")

        else:
            logging.info("시스템 공지 팝업이 보이지 않음, 클릭하지 않음.")
    except TimeoutException:
        logging.warning("시스템 공지 팝업 닫기 버튼이 없음, 클릭하지 않음.")

    # 2. 노티 팝업 확인 버튼 클릭
    try:
        popup_button = WebDriverWait(driver_normal, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#notiPopupOk"))
        )
        if popup_button.is_displayed():  # 노티 팝업 확인 버튼이 보이는지 확인
            driver_normal.execute_script("arguments[0].scrollIntoView(true);", popup_button)  # 버튼이 보이도록 스크롤
            popup_button.click()
            logging.info("노티 팝업 확인 버튼 클릭")
        else:
            logging.info("노티 팝업이 보이지 않음, 클릭하지 않음.")
    except TimeoutException:
        logging.warning("노티 팝업 확인 버튼이 없음, 클릭하지 않음.")
    
    try:
        # 로그인 버튼 클릭
        student_login_button = WebDriverWait(driver_normal, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#login > div > div.main-login > div.main-login--button > button:nth-child(1)"))
        )
        click_element(driver_normal, student_login_button)
        logging.info("학생 로그인 버튼 클릭")
        
        # 학교 검색 버튼 클릭하여 팝업 열기
        search_button = WebDriverWait(driver_normal, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#login_form > div > div > div.input-box.input-box--text.is--search.bg--gray > button"))
        )
        click_element(driver_normal, search_button)
        logging.info("학교 검색 팝업 열기")
        
        # 학교명 입력
        WebDriverWait(driver_normal, 10).until(
            EC.visibility_of_element_located((By.ID, "schoolFind"))
        )
        school_input = driver_normal.find_element(By.ID, "schoolFind")
        school_input.send_keys(STUDENT_ID)
        
        # 검색 버튼 클릭
        search_btn = driver_normal.find_element(By.ID, "schFindBtn")
        click_element(driver_normal, search_btn)
        logging.info("학교 검색 버튼 클릭")
        
        # 검색 결과가 나올 때까지 대기 (라벨 텍스트로 확인)
        search_result = WebDriverWait(driver_normal, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//label[contains(text(), '{STUDENT_ID}')]"))
        )
        logging.info("학교 검색 결과 확인")
        
        # 검색된 학교의 라디오 버튼 클릭
        radio_id = search_result.get_attribute("for")
        radio_button = driver_normal.find_element(By.ID, radio_id)
        click_element(driver_normal, radio_button)
        logging.info("학교 라디오 버튼 선택")
        
        # 선택 버튼 클릭
        select_button = WebDriverWait(driver_normal, 10).until(
            EC.element_to_be_clickable((By.ID, "schSelectBtn"))
        )
        click_element(driver_normal, select_button)
        logging.info("학교 선택 완료")
        
        # 팝업 확인 버튼 클릭 후 대기
        popup_confirm = WebDriverWait(driver_normal, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.wrap.is--dark > div.layer-area.modal-area.modal-default.is--school--setting > div.layer__container > div.page__button > button.button-main.violet"))
        )
        click_element(driver_normal, popup_confirm)
        logging.info("학교 선택 팝업 확인")
        
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
        logging.info("학생 로그인 정보 입력 및 로그인 버튼 클릭")
        
        # 중복 로그인 팝업 처리
        try:
            duplicate_login_confirm = WebDriverWait(driver_normal, 5).until(
                EC.element_to_be_clickable((By.ID, "confirmPoupOk"))
            )
            click_element(driver_normal, duplicate_login_confirm)
            logging.info("중복 로그인 팝업 확인")
        except TimeoutException:
            logging.info("중복 로그인 팝업이 없습니다.")
            pass
        
    except TimeoutException:
        logging.error("Fail: 학생 로그인 실패")
        driver_normal.save_screenshot("student_login_failure.png")
        assert False, "학생 로그인 실패"

    try:
        WebDriverWait(driver_normal, 20).until(
            EC.any_of(
                EC.title_contains("학생 대시보드"),
                EC.presence_of_element_located((By.CSS_SELECTOR, ".user-info")),
                EC.url_contains("/today")                
            )
        )
        logging.info("학생이 대시보드 페이지에 접근했습니다.")
    except TimeoutException:
        logging.error("Fail: 학생 대시보드 접근 실패")
        driver_normal.save_screenshot("student_dashboard_failure.png")
        assert False, "학생 대시보드 접근 실패"

