from flask import jsonify
from flask import request

# Authorization: Basic base64(un:password)
@api.route('/signin/', methods=['POST'])
def signin1():
    un = request.get_json.get('username')
    password = request.get_json.get('password')
    try:
        user = User.query.filter_by(username=un).first()
    except:
        user = None
        user_id = None
    if not user:
        return jsonfy({}), 403
    else:
        if user.verify_password(password):
            return jsonify ({
                'uid': user.uid
                }), 200
        else:
            return jsonify({}), 502//对嘛
        
