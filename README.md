# toyGPT
python과 openAI를 활용하여 csv파일 생성 및 블로그 연동

### 목표
1. (Ver1.1.x) 웹서버 연결 후 기본 서비스페이지 제작 *(프롬프트 입력(create) - 결과확인(read) - 결과수정(update) - 결과포스팅(Tistory - API))*
2. (Ver1.2.x) DB연동
3. (Ver1.3.x) 로그인 기능+, 개인 API-KEY 적용
4. (ver1.4.x) 보안 , client-ip추적(5회사용시 차단? 등)
5. (ver2.0.0) aws연동-배포


*왜 파이썬인가?  -  왜 티스토리인가?  -  왜 flask인가?

* 5.참고
안녕, 나는 파이썬으로 웹서버를 설계중이야.
이 서비스를 임의의 사용자에게 배포하려 하는데, 이들이 내 서비스를 과도하게 사용해서 내 서버가 부하될까 걱정이야. 나는 이를 해결하기 위해서 방법을 생각해봤는데,
1. 사용자가 request를 보내면 ip를 수집한다.
2. 해당ip를 변수로 만들고 request 1번에 count가 1개씩 증가하는 로직을 만든다.
3. count가 10이 되면 해당ip로 나의 서버에 접근할 수 없도록 차단한다.

이 내용으로 파이선 코드를 작성할 수 있니?