def code_0(data, msg=""):
    return {
        "code": 0,
        "data": data,
        "msg": msg,
    }


def internal_error(msg):
    return {
        "code": 405,
        "data": None,
        "msg": msg,
    }
