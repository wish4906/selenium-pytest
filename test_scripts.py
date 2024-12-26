import pytest
import importlib
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
from datetime import datetime
from fpdf import FPDF

@pytest.mark.e_test

class TestHigh:
    network_errors = []

    @pytest.fixture(scope="session")
    def browser_manager(self, selenium_url):
        class BrowserManager:
            def __init__(self):
                self.drivers = {}
                self.selenium_url = selenium_url
                
                # 브라우저 설정 및 생성
                incognito_options = Options()
                incognito_options.add_argument("--incognito")
                normal_options = Options()
                
                self.drivers['incognito'] = webdriver.Remote(
                    command_executor=self.selenium_url,
                    options=incognito_options
                )
                self.drivers['normal'] = webdriver.Remote(
                    command_executor=self.selenium_url,
                    options=normal_options
                )
                print("일반 모드 브라우저 생성됨")
                
                # 화면 배치
                screen_width = self.drivers['normal'].execute_script("return window.screen.availWidth;")
                screen_height = self.drivers['normal'].execute_script("return window.screen.availHeight;")
                
                self.drivers['incognito'].set_window_position(0, 0)
                self.drivers['incognito'].set_window_size(screen_width // 2, screen_height)
                
                self.drivers['normal'].set_window_position(screen_width // 2, 0)
                self.drivers['normal'].set_window_size(screen_width // 2, screen_height)
                    
                # 네트워크 에러 모니터링 설정
                for driver in self.drivers.values():
                    driver.execute_script("""
                        window.networkErrors = [];
                        const originalFetch = window.fetch;
                        window.fetch = async (...args) => {
                            try {
                                const response = await originalFetch(...args);
                                if (!response.ok) {
                                    window.networkErrors.push({
                                        url: args[0],
                                        status: response.status,
                                        timestamp: new Date().toISOString()
                                    });
                                }
                                return response;
                            } catch (error) {
                                window.networkErrors.push({
                                    url: args[0],
                                    error: error.message,
                                    timestamp: new Date().toISOString()
                                });
                                throw error;
                            }
                        };
                    """)
            
        manager = BrowserManager()
        yield manager
        
        print("브라우저 정리 시작")
        if self.network_errors:
            self.create_pdf_report()
        for driver in manager.drivers.values():
            driver.quit()

    @pytest.mark.parametrize('test_func_name', [
        name for module in sorted(os.listdir('test_script'))
        if module.startswith('test_') and module.endswith('.py')
        for name in dir(importlib.import_module(f"test_script.{module[:-3]}"))
        if name.startswith('test_')
    ])
    def test_run_all(self, test_func_name, login_data, browser_manager, test_type):
        """테스트 실행"""
        assert test_type == 'test_script'  # 올바른 테스트 타입인지 확인
        for module in sorted(os.listdir('test_script')):
            if module.startswith('test_') and module.endswith('.py'):
                test_module = importlib.import_module(f"test_script.{module[:-3]}")
                if hasattr(test_module, test_func_name):
                    test_func = getattr(test_module, test_func_name)
                    
                    # base_url 설정
                    base_url = login_data['teacher'][0]
                    
                    # login 테스트만 특별 처리
                    if 'login' in test_func_name:
                        if 'teacher' in test_func_name:
                            test_func(browser_manager.drivers['incognito'], login_data['teacher'])
                        else:
                            test_func(browser_manager.drivers['normal'], login_data['student'])
                    else:  # login이 아닌 모든 테스트
                        if 'teacher' in test_func_name:
                            test_func(browser_manager.drivers['incognito'], base_url)
                        else:
                            test_func(browser_manager.drivers['normal'], base_url)

    @classmethod
    def create_pdf_report(cls):
        """네트워크 에러 PDF 리포트 생성"""
        if not cls.network_errors:
            return

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        pdf.cell(200, 10, txt=f"Network Error Report - {datetime.now()}", ln=True, align='C')
        
        for error in cls.network_errors:
            pdf.cell(200, 10, txt=f"Test: {error['test']}", ln=True)
            pdf.cell(200, 10, txt=f"Browser: {error['browser']}", ln=True)
            pdf.cell(200, 10, txt=f"URL: {error['url']}", ln=True)
            pdf.cell(200, 10, txt=f"Timestamp: {error['timestamp']}", ln=True)
            if 'status' in error:
                pdf.cell(200, 10, txt=f"Status: {error['status']}", ln=True)
            if 'error' in error:
                pdf.cell(200, 10, txt=f"Error: {error['error']}", ln=True)
            pdf.cell(200, 10, txt="-" * 50, ln=True)

        pdf.output(f"network_errors_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")

