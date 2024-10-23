# test_selenium.py

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor, as_completed

# 각 PC의 Selenium 서버 URL
url_pc1 = 'http://192.168.0.72:4444/wd/hub'
url_pc2 = 'http://192.168.0.18:4444/wd/hub'
url_pc3 = 'http://192.168.0.106:4444/wd/hub'

# 각 PC에서 열 URL 및 로그인 정보 설정
urls = {
    url_pc1: ("https://tb-edu.ontactedu.co.kr/office/goe", "teacher", "QAE001", "2w2w2w2w2w", "QWER", "student_num1"),
    url_pc2: ("https://tb-edu.ontactedu.co.kr/office/goe", "teacher", "jw01", "2w2w2w2w2w", "test", "student_num2"),
    url_pc3: ("https://tb-edu.ontactedu.co.kr/office/goe", "teacher", "watest9", "2w2w2w2w2w", "mmm", "student_num3"),
}


@pytest.mark.parametrize("url, credentials", urls.items())
def test_login(url, credentials):
    website, role, user_id, password, school_name, student_num = credentials

    # 일반 모드 (교사 로그인)
    driver_normal = webdriver.Remote(
        command_executor=url,
        options=webdriver.ChromeOptions()  # 일반 모드용
    )

    try:
        # 해당 웹사이트 열기 (일반 모드)
        driver_normal.get(website)

        # 로그인 과정 (교사)
        driver_normal.find_element(By.CSS_SELECTOR, ".login--item:nth-child(2) > .login--item-button").click()
        driver_normal.find_element(By.ID, "mbrId").send_keys(user_id)
        driver_normal.find_element(By.ID, "loginPw").send_keys(password)
        driver_normal.find_element(By.CSS_SELECTOR, ".margin-t-29").click()

        # 시크릿 모드 (학생 로그인)
        options = webdriver.ChromeOptions()
        options.add_argument('--incognito')  # 시크릿 모드 옵션 추가
        driver_incognito = webdriver.Remote(
            command_executor=url,
            options=options  # 시크릿 모드용
        )

        # 해당 웹사이트 열기 (시크릿 모드)
        driver_incognito.get(website)

        # 로그인 과정 (학생)
        driver_incognito.find_element(By.CSS_SELECTOR, ".login--item:nth-child(1) > .login--item-button").click()
        driver_incognito.find_element(By.ID, "schoolFind").send_keys(school_name)
        driver_incognito.find_element(By.ID, "schFindBtn").click()
        driver_incognito.find_element(By.ID, "000270").click()  # 학교 선택
        driver_incognito.find_element(By.ID, "schSelectBtn").click()  # 선택 완료
        driver_incognito.find_element(By.ID, "selectedStdnNum").send_keys(student_num)  # 학생 번호 입력
        driver_incognito.find_element(By.ID, "stdn_loginPw").send_keys(password)  # 비밀번호 입력
        driver_incognito.find_element(By.CSS_SELECTOR, ".login--button").click()  # 로그인 버튼 클릭

        # 잠시 대기 (테스트 진행을 위한 대기)
        driver_incognito.implicitly_wait(5)  # 5초 대기

    finally:
        # 각 드라이버 종료
        driver_normal.quit()
        driver_incognito.quit()
