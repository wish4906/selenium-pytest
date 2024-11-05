@echo off
chcp 65001
echo 테스트 실행 시작...

echo 초등 테스트 실행 중...
start cmd /k "cd /d %~dp0 && chcp 65001 && pytest test_e.py -v && pause"

echo 중등 테스트 실행 중...
start cmd /k "cd /d %~dp0 && chcp 65001 && pytest test_m.py -v && pause"

echo 고등 테스트 실행 중...
start cmd /k "cd /d %~dp0 && chcp 65001 && pytest test_h.py -v && pause"

echo 모든 테스트가 별도의 창에서 실행됩니다.
echo 각 테스트 결과를 확인하려면 해당 창을 확인하세요.