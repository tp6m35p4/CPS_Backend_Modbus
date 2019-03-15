from functools import wraps
from flask import request, jsonify
def verification(f):
    @wraps(f)
    def verify(*args, **kwargs):
        if not doVerify(request.json):
            return jsonify(msg="verify failed")
        # print("verfied")
        return f(*args, **kwargs)
    return verify

def doVerify(data):
    return True