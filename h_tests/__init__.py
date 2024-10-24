import os
import importlib

print("Loading h_tests package")

# 현재 디렉토리의 모든 테스트 파일을 동적으로 import
for filename in sorted(os.listdir(os.path.dirname(__file__))):
    if filename.startswith('test_') and filename.endswith('.py'):
        module_name = f"h_tests.{filename[:-3]}"
        importlib.import_module(module_name)
