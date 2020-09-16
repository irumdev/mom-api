REGISTER_SCHEMA = {
    "type": "object",
    "properties": {
        "type" : {
            "type" : "string",
            "enum": ["P", "S"]
        },
        "name": {
            "type": "string",
            "maxLength" : 30
        },
        "birthday": {
            "type": "string",
            "pattern": "^(19|20)\d{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[0-1])$",
            "maxLength" : 8
        },
        "gender" : {
            "type" : "string",
            "enum": ["남", "여"]
        },
        "id" : {
            "type" : "string",
            "pattern" : "^[a-zA-Z0-9]{4,20}$"
        },
        "pw" : {
            "type" : "string",
            "pattern" : "^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,20}$"
        },
        "email" : {
            "type" : "string",
            "pattern" : "^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$"
        }
    },
    "required" : ["type", "name", "birthday", "gender", "id", "pw", "email"]
}

REGISTER_PARENT_SCHEMA = {
    "type": "object",
    "properties": {
        "req_age" : {
            "type" : ["string", "number"],
            "pattern" : "^[0-9]{1,2}$"
        },
        "req_detail" : {
            "type" : "string",
            "pattern" : "",
            "maxLength" : 255
        }
    },
    "required" : ["req_age", "req_detail"]
}

REGISTER_SITTER_SCHEMA = {
    "type": "object",
    "properties": {
        "possible_age" : {
            "type" : ["string", "number"],
            "pattern" : "^[0-9]{1,2}$"
        },
        "self_intro" : {
            "type" : "string",
            "pattern" : "",
            "maxLength" : 255
        }
    },
    "required" : ["possible_age", "self_intro"]
}

LOGIN_INFO_SCHEMA = {
    "type" : "object",
    "properties" : {
        "id" : {
            "type" : "string",
            "pattern" : "^[a-zA-Z0-9]{4,20}$"
        },
        "pw" : {
            "type" : "string",
            "pattern" : ""
        }
    },
    "required" : ["id", "pw"]
}

UPDATE_USERINFO_SCHEMA = {
    "type": "object",
    "minProperties" : 1,
    "properties": {
        "name": {
            "type": "string",
            "maxLength" : 30
        },
        "birthday": {
            "type": "string",
            "pattern": "^(19|20)\d{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[0-1])$",
        },
        "gender" : {
            "type" : "string",
            "enum": ["남", "여"]
        },
        "id" : {
            "type" : "string",
            "pattern" : "^[a-zA-Z0-9]{4,20}$"
        },
        "pw" : {
            "type" : "string",
            "pattern" : "^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$"
        },
        "email" : {
            "type" : "string",
            "pattern" : "^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$"
        },
        "req_age" : {
            "type" : ["string", "number"],
            "pattern" : "^[0-9]{1,2}$"
        },
        "req_detail" : {
            "type" : "string",
            "pattern" : "",
            "maxLength" : 255
        },
        "possible_age" : {
            "type" : ["string", "number"],
            "pattern" : "^[0-9]{1,2}$"
        },
        "self_intro" : {
            "type" : "string",
            "pattern" : "",
            "maxLength" : 255
        }
    },
    "additionalProperties": False,
}

ADD_TYPE_SCHEMA = {
    "type": "object",
    "properties": {
        "type": {
            "type": "string",
            "enum": ["P", "S"]
        },
    },
    "required" : ["type"]
}

ADD_PARENT_TYPE_SCHEMA = {
    "type": "object",
    "properties": {
        "req_age" : {
            "type" : ["string", "number"],
            "pattern" : "^[0-9]{1,2}$"
        },
        "req_detail" : {
            "type" : "string",
            "pattern" : "",
            "maxLength" : 255
        }
    },
    "required" : ["req_age", "req_detail"]
}

ADD_SITTER_TYPE_SCHEMA = {
    "type": "object",
    "properties": {
        "possible_age" : {
            "type" : ["string", "number"],
            "pattern" : "^[0-9]{1,2}$"
        },
        "self_intro" : {
            "type" : "string",
            "pattern" : "",
            "maxLength" : 255
        }
    },
    "required" : ["possible_age", "self_intro"]
}