# toyGPT
<p>사용자의 단 한줄 입력 만으로 </br>
'글, 요약문, 사진, 태그' 등의 정보를 포함한 블로그(Tistory) 게시글을 작성할 수 있는 사이트입니다. </br>
내용이 마음에 들지 않으면 수정하여 포스팅 할 수 있습니다.</p>

*python/flask/jinja2, openAI-API, gcloud-API-Translate, Tistory-API, unsplash-API를 사용합니다.*

<p>사용시 주의 : 최초 입력한 'prompt'를 기준으로 파일명이 결정되니 title(수정된 prompt)와 혼동하지 않도록합니다</p>

### 진행
1. (Ver1.1.x) 웹서버 연결 후 기본 서비스페이지 제작 </br>
    *(프롬프트 입력(create) - 결과확인(read) - 결과수정(update) - 결과포스팅(Tistory - API))*
    * 1.1.0 결과확인(ai연동) : 성공
    * 1.1.1 결과수정(로컬 csv파일 연동) : 성공
    * 1.1.2 결과포스팅(블로그 연동) : 성공
    * 1.1.3 tag형변환 함수 추상화 : 성공
    * 1.1.4 동적 textarea(summary부분) : 성공
    * 1.1.5 로컬이미지 포함 업로드 : 성공

### 목표
2. (Ver1.2.x) DB연동
3. (Ver1.3.x) 로그인 기능+, 개인 API-KEY 적용, 포스팅 세부조건 설정옵션(카테고리 등)
4. (ver1.4.x) 보안 , client-ip추적(5회사용시 차단? 등)
5. (ver2.0.0) aws연동-배포


* 왜 파이썬인가?
* 왜 티스토리인가?
* 왜 flask인가?

*5.참고*
    안녕, 나는 파이썬으로 웹서버를 설계중이야.
    이 서비스를 임의의 사용자에게 배포하려 하는데, 이들이 내 서비스를 과도하게 사용해서 내 서버가 부하될까 걱정이야. 나는 이를 해결하기 위해서 방법을 생각해봤는데,
    1. 사용자가 request를 보내면 ip를 수집한다.
    2. 해당ip를 변수로 만들고 request 1번에 count가 1개씩 증가하는 로직을 만든다.
    3. count가 10이 되면 해당ip로 나의 서버에 접근할 수 없도록 차단한다.

    이 내용으로 파이선 코드를 작성할 수 있니?