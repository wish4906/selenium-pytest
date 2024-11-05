from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# 사용자 프로필 경로 설정
user_data_dir = "C:/Users/Admin/AppData/Local/Google/Chrome/User Data"

# 드라이버 설정
options = Options()
options.add_argument(f"user-data-dir={user_data_dir}")  # 사용자 데이터 디렉토리 추가
options.add_argument("--profile-directory=Profile 2")  # 사용할 프로필 지정
# options.add_argument('--headless')  # 필요시 헤드리스 모드 활성화
driver = webdriver.Chrome(options=options)

try:
    driver.get("https://hi.goe.go.kr/")  # 실제 테스트할 웹사이트로 변경

    # 페이지가 로드될 때까지 대기
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # 화면 축소 테스트
    def test_zoom_out(times):
        for _ in range(times):
            ActionChains(driver)\
                .key_down(Keys.CONTROL)\
                .send_keys(Keys.SUBTRACT)\
                .key_up(Keys.CONTROL)\
                .perform()
            print("화면을 축소했습니다.")

    # 축소를 5번 실행
    test_zoom_out(5)

    # 드라이버 종료를 하지 않음
    input("Press Enter to exit...")  # 사용자가 Enter를 누를 때까지 대기

finally:
    driver.quit()  # 드라이버 종료
