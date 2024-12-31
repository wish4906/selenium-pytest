import pytest
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import random
import datetime
import time
import subprocess

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        logging.info("대시보드 프로필 이미지 클릭")

    except Exception as e:
        logging.error(f"Fail: 대시보드 프로필 이미지 클릭 실패 - {str(e)}")
        driver_incognito.save_screenshot("teacher_mypage_failure.png")
        assert False, f"대시보드 프로필 이미지 클릭 실패: {str(e)}"

    # 대시보드 > 마이페이지 접근 확인
    try:
        WebDriverWait(driver_incognito, 10).until(
            EC.url_contains("/v2/mypage/modify")
        )
        logging.info("교사가 대시보드 프로필로 마이페이지에 접근했습니다.")
    except TimeoutException:
        logging.error("Fail: 교사 대시보드 프로필로 마이페이지 접근 실패")
        driver_incognito.save_screenshot("teacher_dashboard_failure.png")
        assert False, "교사 대시보드 프로필로 마이페이지 접근 실패"

    # 마이페이지에서 뒤로가기 또는 /today로 진입
    try:
        # 뒤로가기
        driver_incognito.back()
        logging.info("뒤로가기 클릭")

        # 대시보드 페이지 접근 확인
        WebDriverWait(driver_incognito, 10).until(
            EC.url_contains("/today")  # /main 제거
        )
        logging.info("교사가 대시보드 페이지에 접근했습니다.")
    except TimeoutException:
        logging.error("Fail: 대시보드 접근 실패")
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
        logging.info("대시보드 프로필 이미지 클릭")

        # 드롭다운 팝업 확인
        WebDriverWait(driver_incognito, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "#gnb > div.header--wrapper > div.header--utill > div.header--utill__user > div > div > div"))
        )
        logging.info("드롭다운 팝업이 노출되었습니다.")

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
            logging.info(f"버튼이 정상적으로 노출되었습니다: {selector}")

        logging.info("모든 버튼이 정상적으로 노출되었습니다. - Pass")

    except Exception as e:
        logging.error(f"Fail: 버튼 노출 확인 실패 - {str(e)}")


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
        logging.info("나의 이력 버튼 클릭")

        # 나의 이력 페이지 확인
        WebDriverWait(driver_incognito, 10).until(
            EC.url_contains("/v2/mypage/record")  # 나의 이력 페이지 URL 확인
        )
        logging.info("나의 이력 페이지에 접근했습니다.")

        # 정보 수정 버튼 클릭
        info_modify_button = WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#record > div > div > div.mypage--left > div.mypage--left__menubox > div:nth-child(1) > div > a:nth-child(1)"))  # 정보 수정
        )
        driver_incognito.execute_script("arguments[0].click();", info_modify_button)
        logging.info("정보 수정 버튼 클릭")

        # 정보 수정 페이지 확인
        WebDriverWait(driver_incognito, 10).until(
            EC.url_contains("/v2/mypage/modify")  # 정보 수정 페이지 URL 확인
        )
        logging.info("정보 수정 페이지에 접근했습니다.")

    except Exception as e:
        logging.error(f"Fail: 나의 이력 페이지 접근 또는 정보 수정 페이지 접근 실패 - {str(e)}")
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
        logging.info("비밀번호 입력 완료")

        # 인증하기 버튼 클릭
        verify_button = WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#modify > div > div > div.mypage--right.mypage-member > form > table > tbody > tr:nth-child(3) > td > div > button"))
        )
        driver_incognito.execute_script("arguments[0].click();", verify_button)
        logging.info("인증하기 버튼 클릭")

        # 확인 팝업의 버튼 클릭
        confirm_button = WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#modify > div:nth-child(2) > div > div > div.layer__container.alert.active > div.page__button > button"))
        )
        driver_incognito.execute_script("arguments[0].click();", confirm_button)
        logging.info("확인 팝업 버튼 클릭")

        # 새 비밀번호 입력 필드에 값 입력
        new_password_input = WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#modify > div > div > div.mypage--right.mypage-member > form > table > tbody > tr:nth-child(4) > td > input"))
        )
        new_password_input.clear()  # 기존 값 지우기
        new_password_input.send_keys('2w2w2w2w2w')
        logging.info("새 비밀번호 입력 완료")

        # 비밀번호 확인 입력 필드에 값 입력
        confirm_password_input = WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#modify > div > div > div.mypage--right.mypage-member > form > table > tbody > tr:nth-child(5) > td > input"))
        )
        confirm_password_input.clear()  # 기존 값 지우기
        confirm_password_input.send_keys('2w2w2w2w2w')
        logging.info("비밀번호 확인 입력 완료")

        # 이메일 입력 필드에 값 입력
        email_input = WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#modify > div > div > div.mypage--right.mypage-member > form > table > tbody > tr:nth-child(7) > td > div > input:nth-child(1)"))
        )
        email_input.clear()  # 기존 값 지우기
        email_input.send_keys('seleniumeclass1')
        logging.info("이메일 입력 완료")

        # 수정 완료 버튼 클릭
        submit_button = WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#modify > div > div > div.mypage--right.mypage-member > div.page__button > button.button-main.is--large.violet.width-240"))
        )
        driver_incognito.execute_script("arguments[0].click();", submit_button)
        logging.info("수정 완료 버튼 클릭")

        # 확인 팝업의 버튼 클릭
        final_confirm_button = WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#modify > div:nth-child(2) > div > div > div.layer__container.alert.active > div.page__button > button"))
        )
        driver_incognito.execute_script("arguments[0].click();", final_confirm_button)
        logging.info("최종 확인 팝업 버튼 클릭")

    except Exception as e:
        logging.error(f"Fail: 회원정보 수정 실패 - {str(e)}")
        driver_incognito.save_screenshot("teacher_modify_failure.png")
        assert False, f"회원정보 수정 실패: {str(e)}"

@pytest.mark.e_test
def test_011_teacher_profile_picture(driver_incognito, base_url):
    """프로필 사진 변경 테스트"""

    try:
        # 기존 프로필 사진 요소 가져오기
        existing_profile_picture = WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#modify > div > div > div.mypage--left > div.mypage--left__profile > div > p"))  # 기존 프로필 사진의 CSS 선택자
        )
        
        # 기존 프로필 사진 상태 확인
        existing_image_class = existing_profile_picture.get_attribute("class")
        logging.info(f"기존 프로필 사진 클래스: {existing_image_class}")

        # 기존 이미지가 없을 경우
        if "avatar-no-image" in existing_image_class:
            existing_image_number = None
            logging.info("기존 프로필 사진이 없습니다.")
        else:
            # 기존 프로필 사진 URL 가져오기
            existing_image_style = existing_profile_picture.get_attribute("style")
            existing_image_url = existing_image_style.split("url(")[1].split(")")[0].replace("&quot;", "")  # 기존 이미지 URL
            existing_image_number = existing_image_url.split("/")[-1].split(".")[0]  # URL에서 숫자 부분 추출
            logging.info(f"기존 프로필 사진 URL: {existing_image_url}, 숫자: {existing_image_number}")

        # 프로필 사진 선택 버튼 클릭
        profile_picture_button = WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#modify > div > div > div.mypage--left > div.mypage--left__profile > div > button > p"))
        )
        driver_incognito.execute_script("arguments[0].click();", profile_picture_button)
        logging.info("프로필 사진 선택 버튼 클릭")

        # 팝업 확인
        try:
            popup = WebDriverWait(driver_incognito, 10).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "#contentsContainer > div.layer-area.modal-area.modal-confirm__popup.ele_ui > div.layer__container"))
            )
            logging.info("팝업이 나타났습니다.")

            # 확인 버튼 클릭 가능할 때까지 기다리기
            confirm_button = WebDriverWait(driver_incognito, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "#confirmPoupOk")
                )
            )
            driver_incognito.execute_script("arguments[0].click();", confirm_button)
            logging.info("확인 버튼 클릭")

            # 팝업이 닫힐 때까지 대기
            WebDriverWait(driver_incognito, 10).until(
                EC.invisibility_of_element_located(
                    (By.CSS_SELECTOR, "#contentsContainer > div.layer-area.modal-area.modal-confirm__popup.ele_ui > div.layer__container")
                )
            )
            logging.info("팝업이 닫혔습니다.")

            # 프로필 아이콘 다시 클릭
            profile_picture_button = WebDriverWait(driver_incognito, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#modify > div > div > div.mypage--left > div.mypage--left__profile > div > button > p"))
            )
            driver_incognito.execute_script("arguments[0].click();", profile_picture_button)
            logging.info("프로필 사진 선택 버튼 클릭")

        except TimeoutException:
            logging.warning("팝업이 나타나지 않았습니다. 계속 진행합니다.")

        # 파일 경로 설정 (상대 경로로 변경)
        current_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 파일의 디렉토리 경로
        inputfile_directory = os.path.join(current_dir, '..', 'inputfile','profile')  # inputfile 폴더의 상대 경로
        files = [f for f in os.listdir(inputfile_directory) if f.endswith(('.jpg', '.jpeg', '.png'))]  # 이미지 파일 목록 가져오기

        # 랜덤으로 파일 선택
        selected_file = random.choice(files)
        file_path = os.path.join(inputfile_directory, selected_file)  # 선택된 파일의 전체 경로
        logging.info(f"선택된 이미지 파일: {file_path}")

        # 파일 선택 대화상자에서 이미지 파일 선택
        file_input = WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[type='file']"))  # 파일 입력 필드 선택
            )
        
        file_input.send_keys(file_path)  # 랜덤으로 선택된 이미지 파일 경로 입력
        logging.info("이미지 파일 선택 완료")

        # 변경된 프로필 사진 요소 가져오기
        new_profile_picture = WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#modify > div > div > div.mypage--left > div.mypage--left__profile > div > p"))  # 변경된 프로필 사진의 CSS 선택자
            )
        
        
        # 변경된 프로필 사진이 로드될 때까지 대기
        WebDriverWait(driver_incognito, 10).until(
            lambda driver: new_profile_picture.get_attribute("style") != ""  # 스타일 속성이 비어있지 않을 때까지 대기
        )

        # 변경된 프로필 사진 상태 확인
        new_image_class = new_profile_picture.get_attribute("class")
        logging.info(f"변경된 프로필 사진 클래스: {new_image_class}")

        # 변경된 이미지가 없을 경우
        if "avatar-no-image" in new_image_class:
            new_image_number = None
            logging.info("변경된 프로필 사진이 없습니다.")
        else:
            # 변경된 프로필 사진 URL 가져오기
            new_image_style = new_profile_picture.get_attribute("style")
            new_image_url = new_image_style.split("url(")[1].split(")")[0].replace("&quot;", "")  # 변경된 이미지 URL
            new_image_number = new_image_url.split("/")[-1].split(".")[0]  # URL에서 숫자 부분 추출
            logging.info(f"변경된 프로필 사진 URL: {new_image_url}, 숫자: {new_image_number}")

        # 기존 이미지 숫자와 변경된 이미지 숫자 비교
        if existing_image_number is not None and new_image_number is not None and existing_image_number != new_image_number:
            logging.info("프로필 사진이 성공적으로 변경되었습니다.")
        elif existing_image_number is None and new_image_number is not None:
            logging.info("프로필 사진이 성공적으로 추가되었습니다.")
        else:
            logging.error("프로필 사진이 변경되지 않았습니다.")
            assert False, "프로필 사진이 변경되지 않았습니다."

    except Exception as e:
        logging.error(f"Fail: 프로필 사진 변경 실패 - {str(e)}")
        driver_incognito.save_screenshot("teacher_profile_picture_failure.png")
        assert False, f"프로필 사진 변경 실패: {str(e)}"

@pytest.mark.e_test
def test_012_teacher_record(driver_incognito, base_url):
    """나의 이력 버튼 클릭 및 페이지 접근 확인"""
    
    try:
        # 나의 이력 버튼 클릭 (XPath 사용)
        mypage_record_button = WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class, 'mypage--left__menubox')]//a[contains(text(), '나의 이력')]")  # '나의 이력' 텍스트를 포함하는 링크
            )
        )
        driver_incognito.execute_script("arguments[0].click();", mypage_record_button)
        logging.info("나의 이력 버튼 클릭")

        # 나의 이력 페이지 확인
        WebDriverWait(driver_incognito, 10).until(
            EC.url_contains("/v2/mypage/record")  # 나의 이력 페이지 URL 확인
        )
        logging.info("나의 이력 페이지에 정상적으로 접근했습니다.")

    except Exception as e:
        logging.error(f"Fail: 나의 이력 페이지 접근 실패 - {str(e)}")
        driver_incognito.save_screenshot("mypage_record_failure.png")
        assert False, f"나의 이력 페이지 접근 실패: {str(e)}"

@pytest.mark.e_test
def test_013_teacher_qna(driver_incognito, base_url):
    """1:1 문의 버튼 클릭 및 페이지 접근 확인"""
    
    try:
        # 1:1 문의 버튼 클릭 (XPath 사용)
        logging.info("Attempting to click 1:1 문의 버튼...")
        mypage_qna_button = WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class, 'mypage--left__menubox')]//a[contains(text(), '1:1 문의')]")
            )
        )
        driver_incognito.execute_script("arguments[0].click();", mypage_qna_button)
        logging.info("1:1 문의 버튼 클릭")

        # 1:1 문의 페이지 확인
        logging.info("Checking 1:1 문의 페이지 접근...")
        WebDriverWait(driver_incognito, 10).until(
            EC.url_contains("/v2/mypage/qna")
        )
        logging.info("1:1 문의 페이지에 정상적으로 접근했습니다.")

        # Q&A 등록 프로세스 시작
        logging.info("Starting Q&A registration process...")
        register_button = WebDriverWait(driver_incognito, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#qnaList > div > div > div.mypage--right.mypage-service > div > div.box--search > button.button-main.is--small.line"))
        )
        register_button.click()
        logging.info("등록 버튼 클릭")

        # 제목 입력란에 오늘 날짜와 현재 시간 기입
        logging.info("Entering title...")
        title_input = WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#qnaWrite > div > div > div.mypage--right.mypage-service > div > div.box--edit > div:nth-child(1) > dl > dd > input"))
        )
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        title_input.send_keys(current_time)
        logging.info(f"제목 입력란에 '{current_time}' 입력")

        # 카테고리 드롭다운에서 랜덤 선택
        logging.info("Selecting category...")
        category_buttons = [
            "#qnaWrite > div > div > div.mypage--right.mypage-service > div > div.box--edit > div:nth-child(2) > dl > dd > div > div > button:nth-child(1)",
            "#qnaWrite > div > div > div.mypage--right.mypage-service > div > div.box--edit > div:nth-child(2) > dl > dd > div > div > button:nth-child(2)",
            "#qnaWrite > div > div > div.mypage--right.mypage-service > div > div.box--edit > div:nth-child(2) > dl > dd > div > div > button:nth-child(3)"
        ]
        
        category_dropdown_button = WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.dropdown--select[data-guide='선택']"))
        )
        driver_incognito.execute_script("arguments[0].click();", category_dropdown_button)
        logging.info("카테고리 드롭다운 클릭")

        selected_category = random.choice(category_buttons)
        category_button = WebDriverWait(driver_incognito, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selected_category))
        )
        category_button.click()
        logging.info("카테고리 선택 완료")

        # 파일 첨부 버튼 클릭
        logging.info("Clicking file upload button...")
        file_upload_button = WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#qnaWrite > div > div > div.mypage--right.mypage-service > div > div.box--edit > div:nth-child(3) > dl > dd > div.button--file.width-140 > button"))
        )
        driver_incognito.execute_script("arguments[0].scrollIntoView(true);", file_upload_button)
        driver_incognito.execute_script("arguments[0].click();", file_upload_button)
        logging.info("파일 첨부 버튼 클릭")

        # 랜덤 파일 선택 및 AutoIt 스크립트 실행
        # 상위 디렉토리로 이동하여 경로 설정
        file_directory = os.path.join(os.path.dirname(__file__), "..", "inputfile", "book")
        if not os.path.exists(file_directory):
            raise FileNotFoundError(f"Directory does not exist: {file_directory}")

        files = os.listdir(file_directory)
        random_file = random.choice(files)
        random_file_path = os.path.join(file_directory, random_file)

        logging.info(f"Selected random file: {random_file_path}")

        # AutoIt 스크립트 경로 확인
        autoit_script_path = os.path.join(os.path.dirname(__file__), "..","inputfile", "qna_inputfile.au3")
        if not os.path.exists(autoit_script_path):
            raise FileNotFoundError(f"AutoIt script does not exist: {autoit_script_path}")

        subprocess.run([
            "C:\\Program Files (x86)\\AutoIt3\\AutoIt3.exe",  # AutoIt 설치 경로
            autoit_script_path,  # AutoIt 스크립트 경로
            random_file_path  # 선택된 파일 경로
        ])
        logging.info("AutoIt 스크립트 실행 완료")

        # 파일 첨부 후 대기
        WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body.cke_editable"))
        )
        logging.info("파일 첨부 완료")

        # 텍스트 입력란에 제목과 동일한 텍스트 입력
        logging.info("Clicking and entering text in contenteditable body...")
        # iframe으로 전환
        iframe = WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#cke_qstSbst iframe"))
        )
        driver_incognito.switch_to.frame(iframe)
        
        # .cke_editable 요소 클릭
        editable_area = WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".cke_editable"))
        )
        editable_area.click()
        logging.info("Clicked on .cke_editable area")

        # html 요소에 텍스트 입력
        html_body = WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "html"))
        )
        html_body.send_keys(current_time)
        logging.info(f"html body에 '{current_time}' 입력")
        driver_incognito.switch_to.default_content()

        # 취소 버튼 클릭
        logging.info("Clicking cancel button...")
        cancel_button = WebDriverWait(driver_incognito, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#qnaWrite > div > div > div.mypage--right.mypage-service > div > div.page__button.is--small > button.button-main.gray"))
        )
        cancel_button.click()
        logging.info("취소 버튼 클릭")

        # 팝업 확인
        logging.info("Checking for confirmation popup...")
        WebDriverWait(driver_incognito, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#qnaWrite > div:nth-child(2) > div > div > div.layer__container.confirm.active"))
        )
        logging.info("팝업이 노출되었습니다.")

        # 팝업에서 취소 버튼 클릭
        logging.info("Clicking cancel button on popup...")
        popup_cancel_button = WebDriverWait(driver_incognito, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#qnaWrite > div:nth-child(2) > div > div > div.layer__container.confirm.active > div.page__button > button.button-main.is--large.gray"))
        )
        WebDriverWait(driver_incognito, 10).until(
            lambda driver: popup_cancel_button.is_displayed() and popup_cancel_button.is_enabled()
        )
        popup_cancel_button.click()
        logging.info("팝업에서 취소 버튼 클릭")

        # 등록 버튼 클릭
        logging.info("Clicking register button...")
        register_button = WebDriverWait(driver_incognito, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#qnaWrite > div > div > div.mypage--right.mypage-service > div > div.page__button.is--small > button.button-main.violet"))
        )
        register_button.click()
        logging.info("등록 버튼 클릭")

    except Exception as e:
        logging.error(f"Fail: 1:1 문의 페이지 접근 실패 - {str(e)}")
        driver_incognito.save_screenshot("mypage_qna_failure.png")
        assert False, f"1:1 문의 페이지 접근 실패: {str(e)}"
    
# @pytest.mark.e_test
# def test_014_teacher_agree(driver_incognito, base_url):
#     """이용약관 버튼 클릭 및 페이지 접근 확인"""
    
#     try:
#         # 이용약관 버튼 클릭 (XPath 사용)
#         mypage_agree_button = WebDriverWait(driver_incognito, 10).until(
#             EC.presence_of_element_located(
#                 (By.XPATH, "//div[contains(@class, 'mypage--left__menubox')]//a[contains(text(), '이용약관')]")  # '이용약관' 텍스트를 포함하는 링크
#             )
#         )
#         driver_incognito.execute_script("arguments[0].click();", mypage_agree_button)
#         print("이용약관 버튼 클릭")

#         # 이용약관 페이지 확인
#         WebDriverWait(driver_incognito, 10).until(
#             EC.url_contains("/v2/mypage/agree")  # 이용약관 페이지 URL 확인
#         )
#         print("이용약관 페이지에 정상적으로 접근했습니다.")

   