SELENIUM_URLS = {
    'e_test': 'http://192.168.0.72:4444/wd/hub',
    'm_test': 'http://192.168.0.18:4444/wd/hub',
    'h_test': 'http://192.168.0.106:4444/wd/hub'
}

LOGIN_DATA = {
    'e_test': {
        'teacher': ("https://hi.goe.go.kr/", "qae2", "2w2w2w2w2w"),
        'student': ("https://hi.goe.go.kr/", "qae", "student_num1", "2w2w2w2w2w")
    },
    'm_test': {
        'teacher': ("https://hi.goe.go.kr/", "seleniummclass1", "2w2w2w2w2w"),
        'student': ("https://hi.goe.go.kr/", "seleniumm", "student_num2", "2w2w2w2w2w")
    },
    'h_test': {
        'teacher': ("https://hi.goe.go.kr/", "seleniumhclass1", "2w2w2w2w2w"),
        'student': ("https://hi.goe.go.kr/", "seleniumh", "student_num3", "2w2w2w2w2w")
    }
}