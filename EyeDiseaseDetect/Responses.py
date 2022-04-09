def code_0(data):
    return {
        "code": 0,
        "data": data,
        "msg": "",
    }


def internal_error(msg):
    return {
        "code": 405,
        "data": None,
        "msg": msg,
    }
