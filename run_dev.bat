@echo off
chcp 65001
echo DEV 환경 테스트 실행 시작..
echo 초등 테스트 실행 중...
start cmd /k "cd /d %~dp0 && set "TEST_ENV=dev" && pytest test_e.py -v --html=reports/dev/elementary_report_%date:~0,4%%date:~5,2%%date:~8,2%.html && pause"

echo 중등 테스트 실행 중...
start cmd /k "cd /d %~dp0 && set "TEST_ENV=dev" && pytest test_m.py -v --html=reports/dev/middle_report_%date:~0,4%%date:~5,2%%date:~8,2%.html && pause"

echo 고등 테스트 실행 중...
start cmd /k "cd /d %~dp0 && set "TEST_ENV=dev" && pytest test_h.py -v --html=reports/dev/high_report_%date:~0,4%%date:~5,2%%date:~8,2%.html && pause"

echo 모든 테스트가 별도의 창에서 실행됩니다.
echo 각 테스트 결과를 확인하려면 해당 창을 확인하세요.
echo 상세 리포트는 reports/dev 폴더에서 확인할 수 있습니다.