import bcrypt
import jwt
import time
import pymysql
from jsonschema import *
from data_schema import *

MOMDB = pymysql.connect(
    user="momdba", passwd="*******", host="localhost", db="momdb", charset="utf8"
)
CURSOR = MOMDB.cursor(pymysql.cursors.DictCursor)
JWT_SALT = "goodsalt"
JWT_ALGO = "HS256"

# 빈 문자열을 파싱할 경우
def on_json_loading_failed_return_dict(e):
    return {}


# 정의 되지 않은 예외 오류메시지
def get_exception_message(e):
    if hasattr(e, "message"):
        result_msg = e.message  # Exception Message가 있으면 반환
    else:
        result_msg = str(e)
    return result_msg


# 패스위드 단방향 암호화
def encrypt_password(pw):
    pw = pw.encode("utf-8")
    pw = bcrypt.hashpw(pw, bcrypt.gensalt())
    return pw


# 성별 코드 변환
def convert_gender(gender):
    if gender == "여":
        return 2  # 여자
    else:
        return 1  # 남자


# REQUEST 체크
def check_request(request):
    request.on_json_loading_failed = on_json_loading_failed_return_dict
    # Body Data가 필요한 요청이지만 Content-Type이 없는 경우
    if request.method != "GET" and request.headers.get("Content-Length") is None:
        result_msg = "Missing Content-Length"
        result = {"result_msg": result_msg, "result_yn": False, "http_code": 400}
        return result

    if request.is_json is False:  # Content-Type이 application/json가 아님
        result_msg = "Content-Type Allow Only application/json"
        result = {"result_msg": result_msg, "result_yn": False, "http_code": 400}
        return result
    else:  # 올바른 Content-Type
        result = {"result_yn": True}
        return result


# INPUT DATA VALIDATION 체크
def input_data_validation(json, schema):
    try:
        validate(instance=json, schema=schema)
    except ValidationError as e:  # 400 Error 사용자 입력값 포맷이 올바르지 않음
        result = {"result_msg": e.message, "result_yn": False, "http_code": 400}
    except SchemaError as e:  # 500 Error JSON 스키마 정의가 올바르지 않음
        result = {"result_msg": e.message, "result_yn": False, "http_code": 500}
    except Exception as e:  # 500 Error 정의되지 않은 오류
        result_msg = "Validation Error :" + get_exception_message(e)
        result = {"result_msg": result_msg, "result_yn": False, "http_code": 500}
    else:  # 올바른 포맷
        result = {"result_yn": True}
    finally:
        return result


# 아이디 중복체크
def id_duplication_check(id):
    sql = "SELECT count(*) as count FROM users WHERE id=%s"

    try:
        CURSOR.execute(sql, id)
    except Exception as e:
        result_msg = "DB Error :" + get_exception_message(e)
        result = {"result_msg": result_msg, "result_yn": False, "http_code": 500}
    else:
        row = CURSOR.fetchone()
        if row["count"] > 0:
            result_msg = "이미 존재하는 아이디입니다."
            result = {"result_msg": result_msg, "result_yn": False, "http_code": 409}
        else:
            result = {"result_yn": True}
    finally:
        return result


# 시터회원 회원가입
def register_sitter(user):
    check = input_data_validation(user, REGISTER_SITTER_SCHEMA)  # 입력 포맷 확인
    if check["result_yn"] is False:
        return check

    check = id_duplication_check(user["id"])  # 아이디 중복체크
    if check["result_yn"] is False:
        return check

    user["type"] = 2  # 시터회원 TYPE
    user["gender"] = convert_gender(user["gender"])
    user["pw"] = encrypt_password(user["pw"])
    sql = "INSERT INTO users VALUES(NULL, %(type)s, %(name)s, %(birthday)s, %(gender)s, %(id)s, %(pw)s, %(email)s, NULL, '', %(possible_age)s, %(self_intro)s, now())"

    try:
        CURSOR.execute(sql, user)
    except Exception as e:
        result_msg = "DB Error :" + get_exception_message(e)
        result = {"result_msg": result_msg, "result_yn": False, "http_code": 500}
    else:
        MOMDB.commit()
        result_msg = "시터회원 가입이 완료되었습니다."
        result = {"result_msg": result_msg, "result_yn": True, "http_code": 201}
    finally:
        return result


# 부모회원 회원가입
def register_parent(user):
    check = input_data_validation(user, REGISTER_PARENT_SCHEMA)  # 입력 포맷 확인
    if check["result_yn"] is False:
        return check

    check = id_duplication_check(user["id"])  # 아이디 중복체크
    if check["result_yn"] is False:
        return check

    user["type"] = 1  # 부모회원 TYPE
    user["gender"] = convert_gender(user["gender"])
    user["pw"] = encrypt_password(user["pw"])
    sql = "INSERT INTO users VALUES(NULL, %(type)s, %(name)s, %(birthday)s, %(gender)s, %(id)s, %(pw)s, %(email)s, %(req_age)s, %(req_detail)s, NULL, '', now())"

    try:
        CURSOR.execute(sql, user)
    except Exception as e:
        result_msg = "DB Error :" + get_exception_message(e)
        result = {"result_msg": result_msg, "result_yn": False, "http_code": 500}
    else:
        MOMDB.commit()
        result_msg = "부모회원 가입이 완료되었습니다."
        result = {"result_msg": result_msg, "result_yn": True, "http_code": 201}
    finally:
        return result


# 토큰 발행
def issuance_token(id):
    payload = dict()
    payload["id"] = id  # 토큰 발행대상
    payload["iat"] = int(time.time())  # 토큰 발행시간
    payload["exp"] = payload["iat"] + 3600  # 토큰 만료시간(유효 1시간)

    try:
        token = jwt.encode(payload, JWT_SALT, algorithm=JWT_ALGO)
    except Exception as e:  # 토큰 인코딩 실패(정의되지 않은 원인)
        result_msg = "Token Eecoding Error :" + get_exception_message(e)
        result = {"result_msg": result_msg, "result_yn": False, "http_code": 500}
    else:
        token = token.decode("utf-8")
        result_msg = "로그인 되었습니다."
        result = {"result_msg": result_msg, "result_yn": True, "http_code": 200, "token": token}
    finally:
        return result


# 토큰 체크
def check_token(id, token):
    token = token.split(" ")[1].encode("utf-8")  # "Bearer" 스트링 제거
    try:
        auth = jwt.decode(token, JWT_SALT, algorithms=JWT_ALGO)
    except jwt.exceptions.ExpiredSignatureError as e:  # 만료된 토큰
        result_msg = "만료된 토큰입니다."
        result = {"result_msg": result_msg, "result_yn": False, "http_code": 401}
    except jwt.exceptions.DecodeError as e:  # 토큰 Validation 실패
        result_msg = "유효하지 않는 토큰입니다."
        result = {"result_msg": result_msg, "result_yn": False, "http_code": 401}
    except Exception as e:  # 토큰 디코딩 실패(정의되지 않은 원인)
        result_msg = "Token Decoding Error :" + get_exception_message(e)
        result = {"result_msg": result_msg, "result_yn": False, "http_code": 500}
    else:
        if id != auth["id"]:  # ID와 Token 인증정보가 일치하지 않음
            result_msg = "ID와 Token 인증정보가 일치하지 않습니다."
            result = {"result_msg": result_msg, "result_yn": False, "http_code": 401}
        else:
            result = {"result_yn": True}
    finally:
        return result


# 토큰발행 회원정보 조회
def login_check_db(idpw):
    sql = "SELECT pw as encrypt_pw FROM users WHERE id=%s"

    try:
        CURSOR.execute(sql, idpw["id"])
    except Exception as e:
        result_msg = get_exception_message(e)
        result = {"result_msg": result_msg, "result_yn": False, "http_code": 500}
    else:
        row = CURSOR.fetchone()
        if row is None:  # 조회된 회원정보가 없음
            result_msg = "ID가 존재하지 않습니다."
            result = {"result_msg": result_msg, "result_yn": False, "http_code": 404}
        else:
            clear_pw = idpw["pw"].encode("utf-8")
            encrypt_pw = row["encrypt_pw"].encode("utf-8")
            if bcrypt.checkpw(clear_pw, encrypt_pw) is False:
                result_msg = "비밀번호가 일치하지 않습니다."
                result = {"result_msg": result_msg, "result_yn": False, "http_code": 403}
            else:
                result = {"result_yn": True}
    finally:
        return result


# 회원정보 불러오기
def get_user_info(id):
    sql = "SELECT * FROM users WHERE id=%s"

    try:
        CURSOR.execute(sql, id)
    except Exception as e:
        result_msg = "DB Error :" + get_exception_message(e)
        result = {"result_msg": result_msg, "result_yn": False, "http_code": 500}
    else:
        row = CURSOR.fetchone()
        if row is None:
            result_msg = "존재하지 않는 회원입니다."
            result = {"result_msg": result_msg, "result_yn": False, "http_code": 404}
        else:
            row.pop("PW")  # 비밀번호는 반환하지 않는다.
            row["BIRTHDAY"] = row["BIRTHDAY"].strftime("%Y%m%d")
            row["JOIN_DATE"] = row["JOIN_DATE"].strftime("%Y-%m-%d %H:%M:%S")
            row["GENDER"] = row["GENDER"] == 1 and "남" or "여"
            user_type = row.pop("TYPE")
            if user_type == 1:  # 부모회원
                result_msg = "부모회원 정보를 조회했습니다."
                row.pop("POSSIBLE_AGE")  # 부모회원은 케어최소연령이 없음
                row.pop("SELF_INTRO")  # 부모회원은 자기소개가 없음
            elif user_type == 2:  # 시터회원
                result_msg = "시터회원 정보를 조회했습니다."
                row.pop("REQ_AGE")  # 시터회원은 케어원하는나이가 없음
                row.pop("REQ_DETAIL")  # 시터회원은 신청내용이 없음
            else:
                result_msg = "부모+시터 회원정보를 조회했습니다."

            result = {"result_msg": result_msg, "result_yn": True, "users": row, "http_code": 200}
    finally:
        return result


# 회원정보 수정
def update_user_info(id, user):
    if "id" in user:  # ID 변경불가
        result_msg = "아이디는 변경할 수 없습니다."
        result = {"result_msg": result_msg, "result_yn": False, "http_code": 403}
        return result

    if "pw" in user:
        user["pw"] = encrypt_password(user["pw"])

    options = list()
    for prop in user:  # SQL SET문 생성
        tmp = prop + "=%(" + prop + ")s"
        options.append(tmp)
    sql = "UPDATE users SET " + ",".join(options) + " WHERE id=%(id)s"
    user["id"] = id  # ID KEY 할당
    if "gender" in user:
        user["gender"] = convert_gender(user["gender"])

    try:
        CURSOR.execute(sql, user)
    except Exception as e:
        result_msg = "DB Error :" + get_exception_message(e)
        result = {"result_msg": result_msg, "result_yn": False, "http_code": 500}
    else:
        MOMDB.commit()
        result_msg = "회원정보를 수정했습니다."
        result = {"result_msg": result_msg, "result_yn": True, "http_code": 200}
    finally:
        return result


# 타입추가 전 타입체크
def usertype_check(id, add_type):
    sql = "SELECT type FROM users WHERE id=%s"

    try:
        CURSOR.execute(sql, id)
    except Exception as e:
        result_msg = "DB Error:" + get_exception_message(e)
        result = {"result_msg": result_msg, "result_yn": False, "http_code": 500}
    else:
        row = CURSOR.fetchone()
        if row["type"] == 3:
            result_msg = "이미 부모+시터 회원입니다."
            result = {"result_msg": result_msg, "result_yn": False, "http_code": 409}
        elif row["type"] == add_type:
            type_name = add_type == 1 and "부모" or "시터"
            result_msg = "이미 " + type_name + " 회원입니다."
            result = {"result_msg": result_msg, "result_yn": False, "http_code": 409}
        else:
            result = {"result_yn": True}
    finally:
        return result


# 부모로도 활동하기
def add_parent_type(id, user):
    check = input_data_validation(user, ADD_PARENT_TYPE_SCHEMA)  # 입력 포맷 확인
    if check["result_yn"] is False:
        return check

    add_type = 1  # 부모 타입(지금 추가하려는 타입)
    check = usertype_check(id, add_type)  # 타입 체크
    if check["result_yn"] is False:
        return check

    user["type"] = 3  # 부모+시터 회원 TYPE
    user["id"] = id  # ID KEY 할당
    sql = "UPDATE users SET type=%(type)s, req_age=%(req_age)s, req_detail=%(req_detail)s WHERE id=%(id)s"

    try:
        CURSOR.execute(sql, user)
    except Exception as e:
        result_msg = "DB Error :" + get_exception_message(e)
        result = {"result_msg": result_msg, "result_yn": False, "http_code": 500}
    else:
        MOMDB.commit()
        result_msg = "부모회원 타입을 추가했습니다."
        result = {"result_msg": result_msg, "result_yn": True, "http_code": 200}
    finally:
        return result


# 시터로도 활동하기
def add_sitter_type(id, user):
    check = input_data_validation(user, ADD_SITTER_TYPE_SCHEMA)  # 입력 포맷 확인
    if check["result_yn"] is False:
        return check

    add_type = 2  # 시터 타입(지금 추가하려는 타입)
    check = usertype_check(id, add_type)  # 타입 체크
    if check["result_yn"] is False:
        return check

    user["type"] = 3  # 부모+시터 회원 TYPE
    user["id"] = id  # ID KEY 할당
    sql = "UPDATE users SET type=%(type)s, possible_age=%(possible_age)s, self_intro=%(self_intro)s WHERE id=%(id)s"

    try:
        CURSOR.execute(sql, user)
    except Exception as e:
        result_msg = "DB Error :" + get_exception_message(e)
        result = {"result_msg": result_msg, "result_yn": False, "http_code": 500}
    else:
        MOMDB.commit()
        result_msg = "시터회원 타입을 추가했습니다."
        result = {"result_msg": result_msg, "result_yn": True, "http_code": 200}
    finally:
        return result
