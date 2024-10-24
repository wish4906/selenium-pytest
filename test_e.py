import pytest
import importlib
import os

@pytest.mark.e_test
@pytest.mark.usefixtures("setup_drivers")
class TestElementary:
    @pytest.fixture(autouse=True)
    def setup_method(self, login_data):
        self.login_data = login_data

    @pytest.mark.parametrize('test_func_name', [
        name
        for module in os.listdir('e_tests')
        if module.startswith('test_') and module.endswith('.py')
        for name in dir(importlib.import_module(f"e_tests.{module[:-3]}"))
        if name.startswith('test_')
    ])
    def test_run_all(self, test_func_name):
        for module in os.listdir('e_tests'):
            if module.startswith('test_') and module.endswith('.py'):
                test_module = importlib.import_module(f"e_tests.{module[:-3]}")
                if hasattr(test_module, test_func_name):
                    test_func = getattr(test_module, test_func_name)
                    test_func((self.driver_normal, self.driver_incognito), self.login_data)
                    break

    @classmethod
    def teardown_class(cls):
        if hasattr(cls, 'driver_normal'):
            cls.driver_normal.quit()
        if hasattr(cls, 'driver_incognito'):
            cls.driver_incognito.quit()
