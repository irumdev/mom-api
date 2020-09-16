# debug mode run : FLASK_DEBUG=1 flask run --host=0.0.0.0
# normal mode run : flask run --host=0.0.0.0

from flask import *

from logic import *
from data_schema import *

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False


# 회원가입
@app.route("/users", methods=["POST"])
def api_register():
    check = check_request(request)  # REQUEST 확인
    if check["result_yn"] is False:
        http_code = check.pop("http_code")
        return jsonify(check), http_code

    check = input_data_validation(request.json, REGISTER_SCHEMA)  # 입력 포맷 확인
    if check["result_yn"] is False:
        http_code = check.pop("http_code")
        return jsonify(check), http_code

    if request.json["type"] == "S":
        register_result = register_sitter(request.json)  # 시터 회원 INSERT
    elif request.json["type"] == "P":
        register_result = register_parent(request.json)  # 부모 회원 INSERT

    http_code = register_result.pop("http_code")
    return jsonify(register_result), http_code


# 로그인
@app.route("/authorize", methods=["POST"])
def api_login():
    check = check_request(request)  # REQUEST 확인
    if check["result_yn"] is False:
        http_code = check.pop("http_code")
        return jsonify(check), http_code

    check = input_data_validation(request.json, LOGIN_INFO_SCHEMA)  # 입력 포맷 확인
    if check["result_yn"] is False:
        http_code = check.pop("http_code")
        return jsonify(check), http_code

    check = login_check_db(request.json)  # ID/PW DB CHECK
    if check["result_yn"] is False:
        http_code = check.pop("http_code")
        return jsonify(check), http_code

    issuance_result = issuance_token(request.json["id"])  # 토큰 발행
    http_code = issuance_result.pop("http_code")
    return jsonify(issuance_result), http_code


# 내 정보 업데이트
@app.route("/users/<id>", methods=["PUT"])
def api_update_user_info(id):
    check = check_request(request)  # REQUEST 확인
    if check["result_yn"] is False:
        http_code = check.pop("http_code")
        return jsonify(check), http_code

    check = input_data_validation(request.json, UPDATE_USERINFO_SCHEMA)  # 입력 포맷 확인
    if check["result_yn"] is False:
        http_code = check.pop("http_code")
        return jsonify(check), http_code

    check = check_token(id, request.headers.get("Authorization"))  # 토큰 유효성 확인
    if check["result_yn"] is False:
        http_code = check.pop("http_code")
        return jsonify(check), http_code

    update_result = update_user_info(id, request.json)  # 회원정보 UPDATE
    http_code = update_result.pop("http_code")
    return jsonify(update_result), http_code


# 내 정보 보기
@app.route("/users/<id>", methods=["GET"])
def api_get_user_info(id):
    check = check_request(request)  # REQUEST 확인
    if check["result_yn"] is False:
        http_code = check.pop("http_code")
        return jsonify(check), http_code

    check = check_token(id, request.headers.get("Authorization"))  # 토큰 유효성 확인
    if check["result_yn"] is False:
        http_code = check.pop("http_code")
        return jsonify(check), http_code

    user_result = get_user_info(id)  # 회원정보 DB 조회
    http_code = user_result.pop("http_code")
    return jsonify(user_result), http_code


# 부모로도 활동하기 / 시터로도 활동하기
@app.route("/users/<id>/type", methods=["PUT"])
def api_add_user_type(id):
    check = check_request(request)  # REQUEST 확인
    if check["result_yn"] is False:
        http_code = check.pop("http_code")
        return jsonify(check), http_code

    check = input_data_validation(request.json, ADD_TYPE_SCHEMA)  # 입력 포맷 확인
    if check["result_yn"] is False:
        http_code = check.pop("http_code")
        return jsonify(check), http_code

    check = check_token(id, request.headers.get("Authorization"))  # 토큰 유효성 확인
    if check["result_yn"] is False:
        http_code = check.pop("http_code")
        return jsonify(check), http_code

    if request.json["type"] == "P":
        add_result = add_parent_type(id, request.json)  # 부모로도 활동하기
    elif request.json["type"] == "S":
        add_result = add_sitter_type(id, request.json)  # 시터로도 활동하기

    http_code = add_result.pop("http_code")
    return jsonify(add_result), http_code


@app.errorhandler(404)
def not_found(e):
    result_msg = "Page Not Found"
    result = {"result_msg": result_msg, "result_yn": False}
    return result, 404


@app.errorhandler(405)
def not_allowed(e):
    result_msg = "Method Not Allowed"
    result = {"result_msg": result_msg, "result_yn": False}
    return result, 405


@app.errorhandler(500)
def undefined_error(e):
    result_msg = "정의되지 않은 오류"
    result = {"result_msg": result_msg, "result_yn": False}
    return result, 500
