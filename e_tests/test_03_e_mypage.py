import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException


@pytest.mark.e_test
def test_007_teacher_mypage1(driver_incognito, base_url):
    """대시보드 - 메인 페이지 진입"""
    try:
        # 대시보드 프로필 아이콘 클릭
        profile_box_button = WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#renewalMainPage > div:nth-child(2) > div > div.intro_today_area.intro_area > div.intro-today.intro_character > div > div.intro_profile.intro-today__info.box-bg__white > div.today-info__profile > div > p"))
        )
        driver_incognito.execute_script("arguments[0].click();", profile_box_button)
        print("대시보드 프로필 이미지 클릭")

    except Exception as e:
        print(f"Fail: 대시보드 프로필 이미지 클릭 실패 - {str(e)}")
        driver_incognito.save_screenshot("teacher_mypage_failure.png")
        assert False, f"대시보드 프로필 이미지 클릭 실패: {str(e)}"

    # 대시보드 > 마이페이지 접근 확인
    try:
        WebDriverWait(driver_incognito, 10).until(
            EC.url_contains("/v2/mypage/modify")
        )
        print("교사가 대시보드 프로필로 마이페이지에 접근했습니다.")
    except TimeoutException:
        print("Fail: 교사 대시보드 프로필로 마이페이지 접근 실패")
        driver_incognito.save_screenshot("teacher_dashboard_failure.png")
        assert False, "교사 대시보드 프로필로 마이페이지 접근 실패"

    # 마이페이지에서 뒤로가기 또는 /today로 진입
    try:
        # 뒤로가기
        driver_incognito.back()
        print("뒤로가기 클릭")

        # 또는 /today로 진입
        # driver_incognito.get("/today")
        # print("/today 페이지로 진입했습니다.")
        
        # 대시보드 페이지 접근 확인
        WebDriverWait(driver_incognito, 10).until(
            EC.url_contains("/today")  # /main 제거
        )
        print("교사가 대시보드 페이지에 접근했습니다.")
    except TimeoutException:
        print("Fail: 대시보드 접근 실패")
        driver_incognito.save_screenshot("dashboard_failure.png")
        assert False, "대시보드 접근 실패"

@pytest.mark.e_test
def test_008_teacher_mypage2(driver_incognito, base_url):
    """사용자 드롭다운 메뉴로 마이페이지 진입 및 버튼 확인"""
    
    try:
        # 대시보드 프로필 아이콘 클릭
        header_profile_button = WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#gnb > div.header--wrapper > div.header--utill > div.header--utill__user > div > div > button > span"))
        )
        driver_incognito.execute_script("arguments[0].click();", header_profile_button)
        print("대시보드 프로필 이미지 클릭")

        # 드롭다운 팝업 확인
        WebDriverWait(driver_incognito, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "#gnb > div.header--wrapper > div.header--utill > div.header--utill__user > div > div > div"))
        )
        print("드롭다운 팝업이 노출되었습니다.")

        # 버튼 확인
        button_selectors = [
            "#gnb > div.header--wrapper > div.header--utill > div.header--utill__user > div > div > div > div > div > div.mypage--left__menubox > div:nth-child(1) > div > a:nth-child(1)",  # 정보 수정
            "#gnb > div.header--wrapper > div.header--utill > div.header--utill__user > div > div > div > div > div > div.mypage--left__menubox > div:nth-child(1) > div > a:nth-child(2)",  # 나의 이력
            "#gnb > div.header--wrapper > div.header--utill > div.header--utill__user > div > div > div > div > div > div.mypage--left__menubox > div:nth-child(2) > div > a:nth-child(1)",  # 1:1 문의
            "#gnb > div.header--wrapper > div.header--utill > div.header--utill__user > div > div > div > div > div > div.mypage--left__menubox > div:nth-child(2) > div > a:nth-child(2)",  # 이용약관
            "#gnb > div.header--wrapper > div.header--utill > div.header--utill__user > div > div > div > div > div > div.mypage--left__menubox > div:nth-child(2) > div > a:nth-child(3)",  # 개인정보 처리방침
            "#gnb > div.header--wrapper > div.header--utill > div.header--utill__user > div > div > div > div > div > div.mypage--left__menubox > div:nth-child(2) > div > a:nth-child(4)",  # 탈퇴
            "#gnb > div.header--wrapper > div.header--utill > div.header--utill__user > div > div > div > div > div > div.mypage--left__menubox > div:nth-child(3) > div > a:nth-child(1)",  # 공지사항
            "#gnb > div.header--wrapper > div.header--utill > div.header--utill__user > div > div > div > div > div > div.mypage--left__menubox > div:nth-child(3) > div > a:nth-child(2)",  # 자주 묻는 질문
            "#gnb > div.header--wrapper > div.header--utill > div.header--utill__user > div > div > div > div > div > div.mypage--left__menubox > div:nth-child(3) > div > a:nth-child(3)"   # 이용 안내
        ]

        for selector in button_selectors:
            button = WebDriverWait(driver_incognito, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            assert button.is_displayed(), f"버튼이 노출되지 않았습니다: {selector}"
            print(f"버튼이 정상적으로 노출되었습니다: {selector}")

        print("모든 버튼이 정상적으로 노출되었습니다. - Pass")

    except Exception as e:
        print(f"Fail: 버튼 노출 확인 실패 - {str(e)}")


@pytest.mark.e_test
def test_009_teacher_mypage3(driver_incognito, base_url):
    """나의 이력 버튼 클릭을 통한 마이페이지 진입 확인 및 정보 수정 페이지 접근 확인"""
    
    try:
        # 드롭다운 팝업이 열려 있는 상태에서 나의 이력 버튼 클릭
        mypage_record_button = WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#gnb > div.header--wrapper > div.header--utill > div.header--utill__user > div > div > div > div > div > div.mypage--left__menubox > div:nth-child(1) > div > a:nth-child(2)"))  # 나의 이력
        )
        driver_incognito.execute_script("arguments[0].click();", mypage_record_button)
        print("나의 이력 버튼 클릭")

        # 나의 이력 페이지 확인
        WebDriverWait(driver_incognito, 10).until(
            EC.url_contains("/v2/mypage/record")  # 나의 이력 페이지 URL 확인
        )
        print("나의 이력 페이지에 접근했습니다.")

        # 정보 수정 버튼 클릭
        info_modify_button = WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#record > div > div > div.mypage--left > div.mypage--left__menubox > div:nth-child(1) > div > a:nth-child(1)"))  # 정보 수정
        )
        driver_incognito.execute_script("arguments[0].click();", info_modify_button)
        print("정보 수정 버튼 클릭")

        # 정보 수정 페이지 확인
        WebDriverWait(driver_incognito, 10).until(
            EC.url_contains("/v2/mypage/modify")  # 정보 수정 페이지 URL 확인
        )
        print("정보 수정 페이지에 접근했습니다.")

    except Exception as e:
        print(f"Fail: 나의 이력 페이지 접근 또는 정보 수정 페이지 접근 실패 - {str(e)}")
        driver_incognito.save_screenshot("mypage_history_failure.png")
        assert False, f"나의 이력 페이지 또는 정보 수정 페이지 접근 실패: {str(e)}"
        
@pytest.mark.e_test
def test_010_teacher_modify(driver_incognito, base_url):
    """회원정보 (비밀번호/이메일) 수정"""

    try:
        # 비밀번호 입력 필드 찾기 및 값 입력
        password_input = WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#modify > div > div > div.mypage--right.mypage-member > form > table > tbody > tr:nth-child(3) > td > div > input[type=password]"))
        )
        password_input.clear()  # 기존 값 지우기
        password_input.send_keys('2w2w2w2w2w')
        print("비밀번호 입력 완료")

        # 인증하기 버튼 클릭
        verify_button = WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#modify > div > div > div.mypage--right.mypage-member > form > table > tbody > tr:nth-child(3) > td > div > button"))
        )
        driver_incognito.execute_script("arguments[0].click();", verify_button)
        print("인증하기 버튼 클릭")

        # 확인 팝업의 버튼 클릭
        confirm_button = WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#modify > div:nth-child(2) > div > div > div.layer__container.alert.active > div.page__button > button"))
        )
        driver_incognito.execute_script("arguments[0].click();", confirm_button)
        print("확인 팝업 버튼 클릭")

        # 새 비밀번호 입력 필드에 값 입력
        new_password_input = WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#modify > div > div > div.mypage--right.mypage-member > form > table > tbody > tr:nth-child(4) > td > input"))
        )
        new_password_input.clear()  # 기존 값 지우기
        new_password_input.send_keys('2w2w2w2w2w')
        print("새 비밀번호 입력 완료")

        # 비밀번호 확인 입력 필드에 값 입력
        confirm_password_input = WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#modify > div > div > div.mypage--right.mypage-member > form > table > tbody > tr:nth-child(5) > td > input"))
        )
        confirm_password_input.clear()  # 기존 값 지우기
        confirm_password_input.send_keys('2w2w2w2w2w')
        print("비밀번호 확인 입력 완료")

        # 이메일 입력 필드에 값 입력
        email_input = WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#modify > div > div > div.mypage--right.mypage-member > form > table > tbody > tr:nth-child(7) > td > div > input:nth-child(1)"))
        )
        email_input.clear()  # 기존 값 지우기
        email_input.send_keys('seleniumeclass1')
        print("이메일 입력 완료")

        # 수정 완료 버튼 클릭
        submit_button = WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#modify > div > div > div.mypage--right.mypage-member > div.page__button > button.button-main.is--large.violet.width-240"))
        )
        driver_incognito.execute_script("arguments[0].click();", submit_button)
        print("수정 완료 버튼 클릭")

        # 확인 팝업의 버튼 클릭
        final_confirm_button = WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#modify > div:nth-child(2) > div > div > div.layer__container.alert.active > div.page__button > button"))
        )
        driver_incognito.execute_script("arguments[0].click();", final_confirm_button)
        print("최종 확인 팝업 버튼 클릭")

    except Exception as e:
        print(f"Fail: 회원정보 수정 실패 - {str(e)}")
        driver_incognito.save_screenshot("teacher_modify_failure.png")
        assert False, f"회원정보 수정 실패: {str(e)}"
