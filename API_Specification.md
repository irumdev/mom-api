# API Specification

1. [Authentication](#Authentication)
2. [회원가입](#회원가입)
3. [로그인](#로그인)
4. [내 정보 업데이트](#내-정보-업데이트)
5. [부모로도 활동하기 / 시터로도 활동하기](#부모로도-활동하기--시터로도-활동하기)
6. [내 정보 보기](#내-정보-보기)

---

## Authentication

몇몇 인증이 필요한 API는 호출시 Token이 필요합니다.  
아래와 같이 Request Header에 인증토큰을 포함하여 주세요.  
Token은 [로그인](#로그인) API를 호출하여 발급받을 수 있습니다.

```
Authorization: Bearer {Token}
```

---

## 회원가입

회원정보를 받아서 회원가입을 수행합니다.

- **URL**  
  /users

- **Method**  
  `POST`

- **Data Params**
  |Name|Type|Required / Optional|Description|
  |:---:|:---:|:---:|:---:|
  |type|string|required|회원타입 (부모이면 "P", 시터이면 "S")|
  |name|string|required|이름|
  |birthday|string|required|생년월일 (YYYYMMDD)|
  |gender|string|required|성별("남" or "여")|
  |id|string|required|아이디|
  |pw|string|required|비밀번호 (영어,숫자,특수문자 1자 이상 포함하여 8자리 이상, 20자리 이하)|
  |email|string|required|이메일|
  |req_age|number|conditionality required|케어를 원하는 아이 나이 (type이 "P"이면 필수)|
  |req_detail|string|conditionality required|신청 내용 (type이 "P"이면 필수)|
  |possible_age|number|conditionality required|케어 가능한 아이 최소 연령 (type이 "S"이면 필수)|
  |self_intro|string|conditionality required|자기소개 (type이 "S"이면 필수)|

- **Request example**

  ```
  POST /users HTTP/1.1
  Host: run.kzz.kr:5000
  Content-Type: application/json

  {
    "type" : "P",
    "name" : "김부모",
    "birthday" : "19940713",
    "gender" : "남",
    "id" : "testuser123",
    "pw" : "testuser123!",
    "email" : "testuser123@gmail.com",
    "req_age" : 3,
    "req_detail" : "하루에 2시간 정도 한글놀이를 해 줄 수 있는 시터를 찾습니다 :)"
  }
  ```

- **Response example**

  ```
  HTTP/1.0 201 CREATED
  Content-Type: application/json
  Content-Length: 80

  {
    "result_msg" : "부모회원 가입이 완료되었습니다.",
    "result_yn" : true
  }
  ```

  OR

  ```
  HTTP/1.0 409 CONFLICT
  Content-Type: application/json
  Content-Length: 75

  {
    "result_msg" : "이미 존재하는 아이디입니다.",
    "result_yn" : false
  }
  ```

---

## 로그인

ID, PW를 확인하고 인증 TOKEN을 발행합니다.

- **URL**  
  /authorize

- **Method**  
  `POST`

- **Data Params**
  |Name|Type|Required / Optional|Description|
  |:---:|:---:|:---:|:---:|
  |id|string|required|아이디|
  |pw|string|required|비밀번호|
  <br>

- **Request example**

  ```
  POST /authorize HTTP/1.1
  Host: run.kzz.kr:5000
  Content-Type: application/json

  {
    "id" : "testuser123",
    "pw" : "testuser123!"
  }
  ```

- **Response example**

  ```
  HTTP/1.0 200 OK
  Content-Type: application/json
  Content-Length: 225

  {
    "result_msg" : "로그인 되었습니다.",
    "result_yn" : true,
    "token" : "eyJ0eXAiOiJJ9.eyJpZCI6ITB9.ZPuwhkRyJo"
  }
  ```

  OR

  ```
  HTTP/1.0 403 FORBIDDEN
  Content-Type: application/json
  Content-Length: 78

  {
    "result_msg" : "비밀번호가 일치하지 않습니다.",
    "result_yn" : false
  }
  ```

---

## 내 정보 업데이트

한가지 이상의 회원정보를 수정합니다.  
이 API를 호출하기 위해서는 TOKEN이 필요합니다.

- **URL**  
   /users/{id}
- **Method**  
   `PUT`
- **URL Params**
  |Name|Description|
  |:---:|:---:|
  |id|회원정보를 수정할 대상 회원 ID|
  <br>

- **Data Params**
  |Name|Type|Required / Optional|Description|
  |:---:|:---:|:---:|:---:|
  |name|string|optional|이름|
  |birthday|string|optional|생년월일 (YYYYMMDD)|
  |gender|string|optional|성별 ("남" or "여")|
  |id|string|optional|아이디|
  |pw|string|optional|패스워드 (영어,숫자,특수문자 1자 이상 포함하여 8자리 이상, 20자리 이하)|
  |email|string|optional|이메일|
  |req_age|number|optional|케어를 원하는 아이 나이|
  |req_detail|string|optional|신청내용|
  |possible_age|number|optional|케어 가능한 아이 최소 연령|
  |self_intro|string|optional|자기소개|
  <br>
- **Request example**

  ```
  PUT /users/testuser123 HTTP/1.1
  Host: run.kzz.kr:5000
  Content-Type: application/json
  Authorization: Bearer eyJ0eXAiOiJJ9.eyJpZCI6ITB9.ZPuwhkRyJo

  {
    "name" : "홍길동",
    "birthday" : "20001212",
    "pw" : "test123!"
  }
  ```

- **Response example**

  ```
  HTTP/1.0 200 OK
  Content-Type: application/json
  Content-Length: 70

  {
    "result_msg" : "회원정보를 수정했습니다.",
    "result_yn" : true
  }
  ```

  OR

  ```
  HTTP/1.0 401 UNAUTHORIZED
  Content-Type: application/json
  Content-Length: 62

  {
    "result_msg" : "만료된 토큰입니다.",
    "result_yn" : false
  }
  ```

---

## 부모로도 활동하기 / 시터로도 활동하기

회원타입을 추가합니다.  
이 API를 호출하기 위해서는 TOKEN이 필요합니다.

- **URL**  
  /users/{id}/type
- **Method**  
  `PUT`

- **URL Params**
  |Name|Description|
  |:---:|:---:|
  |id|타입을 추가할 대상 회원 ID|
  <br>

- **Data Params**
  |Name|Type|Required / Optional|Description|
  |:---:|:---:|:---:|:---:|
  |type|string|required|추가 할 회원 타입 (부모로도 활동하기이면 "P", 시터로도 활동하기이면 "S")|
  |req_age|number|conditionality required|케어를 원하는 아이 나이 (type이 "P"이면 필수)|
  |req_detail|string|conditionality required|신청 내용 (type이 "P"이면 필수)|
  |possible_age|number|conditionality required|케어 가능한 아이 최소 연령 (type이 "S"이면 필수)|
  |self_intro|string|conditionality required|자기소개 (type이 "S"이면 필수)|
  <br>

- **Request example**

  ```
  PUT /users/testuser123/type HTTP/1.1
  Host: run.kzz.kr:5000
  Content-Type: application/json
  Authorization: Bearer eyJ0eXAiOiJJ9.eyJpZCI6ITB9.ZPuwhkRyJo

  {
    "type" : "S",
    "possible_age" : 2,
    "self_intro" : "유아교육과를 전공중인 대학생 시터입니다! 사촌 동생들을 많이 돌본 경험이 있어서 아이랑 잘 놀아줄 수 있어요."
  }
  ```

- **Response example**

  ```
  HTTP/1.0 200 OK
  Content-Type: application/json
  Content-Length: 77

  {
    "result_msg" : "시터회원 타입을 추가했습니다.",
    "result_yn" : true
  }
  ```

  OR

  ```
  HTTP/1.0 409 CONFLICT
  Content-Type: application/json
  Content-Length: 73

  {
    "result_msg" : "이미 부모+시터 회원입니다.",
    "result_yn" : false
  }
  ```

---

## 내 정보 보기

나의 회원정보를 조회합니다.  
이 API를 호출하기 위해서는 TOKEN이 필요합니다.

- **URL**  
  /users/{id}
- **Method**  
  `GET`
- **URL Params**  
   |Name|Description|
  |:---:|:---:|
  |id|정보를 조회할 대상 회원 ID|
  <br>

- **Request example**

  ```
  GET /users/testuser123 HTTP/1.1
  Host: run.kzz.kr:5000
  Content-Type: application/json
  Authorization: Bearer eyJ0eXAiOiJJ9.eyJpZCI6ITB9.ZPuwhkRyJo
  ```

- **Response example**

  ```
  HTTP/1.0 200 OK
  Content-Type: application/json
  Content-Length: 540

  {
    "result_msg":"부모+시터 회원정보를 조회했습니다.",
    "result_yn":true,
    "users": {
      "no" : 79,
      "id" : "testuser123",
      "birthday" : "20001212",
      "email" : "testuser123@gmail.com",
      "gender" : "남",
      "join_date" : "2020-09-16 13:18:54",
      "name" : "홍길동",
      "possible_age" : 2,
      "req_age" : 3,
      "req_detail" : "하루에 2시간 정도 한글놀이를 해 줄 수 있는 시터를 찾습니다 :)",
      "self_intro" : "유아교육과를 전공중인 대학생 시터입니다! 사촌 동생들을 많이 돌본 경험이 있어서 아이랑 잘 놀아줄 수 있어요."
    }
  }
  ```

  OR

  ```
  HTTP/1.0 401 UNAUTHORIZED
  Content-Type: application/json
  Content-Length: 72

  {
    "result_msg" : "유효하지 않는 토큰입니다.",
    "result_yn" : false
  }
  ```
