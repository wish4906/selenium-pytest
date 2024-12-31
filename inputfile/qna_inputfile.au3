; AutoIt 스크립트 시작

; 명령줄 인자로 파일 경로 받기
Local $filePath = $CmdLine[1]

; 파일 업로드 대화 상자가 나타날 때까지 대기
WinWaitActive("열기") ; "열기"는 파일 선택 대화 상자의 제목입니다. 시스템 언어에 따라 다를 수 있습니다.

; 파일 경로 입력
Send($filePath)

; Enter 키를 눌러 파일 선택
Send("{ENTER}")