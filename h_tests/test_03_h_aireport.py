import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains
import time

@pytest.mark.h_test

def test_007_teacher_aireport(driver_incognito, base_url):
    """AI 리포트 - 과목리포트 진입"""

    try: # AI 리포트 탭 클릭
        ai_report_button = WebDriverWait(driver_incognito, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#gnb > div.header--wrapper > div.header--menu__box > ul > li:nth-child(4) > a"))
        )
        ai_report_button.click()
        print("AI 리포트 탭 클릭")

        subject_report_button = WebDriverWait(driver_incognito, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#gnb > div.header--wrapper > div.header--menu__box > ul > li:nth-child(4) > div > div > a:nth-child(1)"))
        )
        subject_report_button.click()
        print("과목 리포트 클릭")

    except Exception as e:
        print(f"Fail: AI 리포트 클릭 실패 - {str(e)}")
        driver_incognito.save_screenshot("teacher_aireport_failure.png")
        assert False, f"AI 리포트 클릭 실패: {str(e)}"


    try: # 과목 리포트 접근 확인
        WebDriverWait(driver_incognito, 5).until(
            EC.url_contains("/aireport/monthly")
        )
        print("교사가 과목 리포트에 접근했습니다.")
    except TimeoutException:
        print("Fail: 교사 과목 리포트에 접근 실패")
        driver_incognito.save_screenshot("teacher_subject-report_failure.png")
        assert False, "교사 과목 리포트에 접근 실패"


    try: # 과목 리포트 툴팁 클릭
        title_tooltip_button = WebDriverWait(driver_incognito, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#contentsContainer > div:nth-child(10) > div > div.container > div.contents--title.no-bg > div > div.contents--title__text > div > button > p"))
        )
        title_tooltip_button.click()
        print("과목 리포트 툴팁 클릭")

        # 툴팁이 노출 되었는지 확인
        WebDriverWait(driver_incognito, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#contentsContainer > div:nth-child(10) > div > div.container > div.contents--title.no-bg > div > div.contents--title__text > div > div > div > div > p > strong")  # 과목 리포트 페이지에서 고유한 요소의 선택자
            )
        )
        print("과목 리포트 툴팁 확인")
    except Exception as e:
        print(f"Fail: 과목 리포트 툴팁 클릭 실패 - {str(e)}")
        driver_incognito.save_screenshot("teacher_aireport_failure.png")
        assert False, f"과목 리포트 툴팁 클릭 실패: {str(e)}"



    try: # 이전 달 이동
        month_move_button = WebDriverWait(driver_incognito, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#contentsContainer > div:nth-child(10) > div > div.container > div.contents--title.no-bg > div > div.contents--title__right > div > button.date--button-prev.button-icon > p"))
        )
        month_move_button.click()
        print("이전 달 이동 클릭")

    except Exception as e:
        print(f"Fail: 이전 달 이동 클릭 실패 - {str(e)}")
        # driver_incognito.save_screenshot("teacher_aireport_failure.png")
        assert False, f"이전 달 이동 클릭 실패: {str(e)}"



    try: # 과목 탭 찾기 & 삭제 클릭
        subject_tag_button = WebDriverWait(driver_incognito, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#draggable > div:nth-child(2) > div"))
        )

        if subject_tag_button.is_displayed():  # 중복 로그인 - 팝업 노출 확인
            print("과목탭이 있는지 확인")

            # '삭제' 버튼이 노출되도록 해당 요소 위로 마우스 호버
            actions = ActionChains(driver_incognito)
            actions.move_to_element(subject_tag_button).perform()
            print("마우스를 삭제 버튼 위로 이동")

            delete_button = WebDriverWait(driver_incognito, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#draggable > div:nth-child(2) > button > p"))
            )
            delete_button.click()
            print("삭제 버튼 클릭 완료")

        else:
            print("과목탭 확인 불가능.")

    except Exception as e:
        print(f"Fail: 삭제 버튼 클릭 실패 - {str(e)}")
        # driver_incognito.save_screenshot("delete_button_failure.png")
        assert False, f"삭제 버튼 클릭 실패: {str(e)}"



    try:  # 과목 탭 추가하기
        find_plus_button = WebDriverWait(driver_incognito, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#contentsContainer > div:nth-child(10) > div > div.container > div.contents-area > div > div:nth-child(1) > div.tab-tags--wrapper.is--scroll > div > div:nth-child(1) > button > p"))
        )
        if find_plus_button.is_displayed():
            print("[+] 버튼 확인")

                # [+] 버튼 클릭
            plus_button = WebDriverWait(driver_incognito, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            "#contentsContainer > div:nth-child(10) > div > div.container > div.contents-area > div > div:nth-child(1) > div.tab-tags--wrapper.is--scroll > div > div:nth-child(1) > button > p"))
            )
            plus_button.click()
            print("[+] 버튼 클릭 완료")

            # 과목탭 추가하기
            plus_subject_button = WebDriverWait(driver_incognito, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            "#contentsContainer > div:nth-child(10) > div > div.container > div.contents-area > div > div:nth-child(1) > div.tab-tags--wrapper.is--scroll.open > div > div.tab-tags--box.tags-select > div > button:nth-child(1)"))
            )
            plus_subject_button.click()
            print("과목탭 추가 성공")

            # 추가하기 페이지 종료
            exist_subject_button = WebDriverWait(driver_incognito, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            "#contentsContainer > div:nth-child(10) > div > div.container > div.contents-area > div > div:nth-child(1) > div.tab-tags--wrapper.is--scroll.open > div > div.tab-tags--box.tags-select > button > p"))
            )
            exist_subject_button.click()
            print("추가하기 페이지 종료 성공")
        else:
            print("[+] 버튼 노출되지 않음.")
    except Exception as e:
        print(f"Fail: 과목 탭 추가하기 클릭 실패 - {str(e)}")
        # driver_incognito.save_screenshot("delete_button_failure.png")
        assert False, f"과목 탭 추가하기 클릭 실패: {str(e)}"



    try:  # 학생 리포트 바로가기 클릭 후 돌아오기
        find_report_move = WebDriverWait(driver_incognito, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#contentsContainer > div:nth-child(10) > div > div.container > div.contents-area > div > div:nth-child(1) > div.box-bg__white.report-month__badgebox > div > div.month__status.width-432 > div > button"))
        )
        if find_report_move.is_displayed():
            print("학생 리포트 바로가기 찾기")

                # 학생 리포트 바로가기 버튼 클릭
            report_move_button = WebDriverWait(driver_incognito, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            "#contentsContainer > div:nth-child(10) > div > div.container > div.contents-area > div > div:nth-child(1) > div.box-bg__white.report-month__badgebox > div > div.month__status.width-432 > div > button"))
            )
            report_move_button.click()
            print("학생 리포트 바로가기 클릭")

            # 10초 대기
            time.sleep(3)

            # 뒤로가기
            driver_incognito.back()

            print("뒤로가기 클릭")
        else:
            print("학생 리포트 바로가기 노출 안됨")
    except Exception as e:
        print(f"Fail: 학생 리포트 바로가기 클릭 실패 - {str(e)}")
        # driver_incognito.save_screenshot("delete_button_failure.png")
        assert False, f"학생 리포트 바로가기 클릭 실패: {str(e)}"


    try: # 과목별 리포트 과목 탭
        find_second_subject_button = WebDriverWait(driver_incognito, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "#contentsContainer > div:nth-child(10) > div > div.container > div.contents-area > div > div:nth-child(2) > div > div.tab-box.tab-fit > button:nth-child(2)"))
        )
        if find_second_subject_button.is_displayed():

            second_subject_button = WebDriverWait(driver_incognito, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR,
                     "#contentsContainer > div:nth-child(10) > div > div.container > div.contents-area > div > div:nth-child(2) > div > div.tab-box.tab-fit > button:nth-child(2)"))
            )
            second_subject_button.click()
        else:
            print("과목별 리포트 과목 탭 노출 안됨")

            # 데이터 있는지 체크
        find_data_check = WebDriverWait(driver_incognito, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR,
                 "#contentsContainer > div:nth-child(10) > div > div.container > div.contents-area > div > div:nth-child(2) > div > div.tab--contents.is--bg.active > div.month-subject__total > div.box-bg__lightgray.month__status > ul > li:nth-child(1) > div > strong > div > button > p"))
        )
        if find_data_check.is_displayed():

            # 문제풀이 학습량 툴팁 클릭
            learning_amount_tooltip = WebDriverWait(driver_incognito, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR,
                     "#contentsContainer > div:nth-child(10) > div > div.container > div.contents-area > div > div:nth-child(2) > div > div.tab--contents.is--bg.active > div.month-subject__total > div.box-bg__lightgray.month__status > ul > li:nth-child(1) > div > strong > div > button > p"))
            )
            learning_amount_tooltip.click()
            print("문제풀이 학습량 툴팁 클릭 성공")

            time.sleep(3)

            # # 문제풀이 정답률 툴팁 클릭
            # correct_answers_tooltip = WebDriverWait(driver_incognito, 10).until(
            #     EC.element_to_be_clickable(
            #         (By.CSS_SELECTOR,
            #          "#contentsContainer > div:nth-child(10) > div > div.container > div.contents-area > div > div:nth-child(2) > div > div.tab--contents.is--bg.active > div.month-subject__total > div.box-bg__lightgray.month__status > ul > li:nth-child(2) > div > strong > div > button > p"))
            # )
            # correct_answers_tooltip.click()
            # print("문제풀이 정답률 툴팁 클릭 성공")

        else:
            print("과목별 리포트 과목 탭 노출 안됨")


    except Exception as e:
        print(f"Fail: 과목별 리포트 과목 탭 클릭 실패 - {str(e)}")
        driver_incognito.save_screenshot("teacher_aireport_failure.png")
        assert False, f"과목별 리포트 과목 탭 클릭 실패: {str(e)}"


















