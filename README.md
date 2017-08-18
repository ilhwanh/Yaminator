Yaminator
=============
# 개요
야민정음 변환 모듈
# 개발환경
Python 3.5.3
Windows Anaconda 3
# 사용 예시
파이썬 코드

	import yamin
	ymn = yamin.Yaminator('db')
	print(ymn.transform(u'무대팀장'))

출력

	무머덤튽

python yamin.py 로 직접 실행하면 대화형식으로 야민정음을 변환해볼 수 있습니다.