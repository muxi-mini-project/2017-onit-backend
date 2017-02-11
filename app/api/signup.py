from . import api
from flask import request
from flask import jsonify

@api.route('/signup/', methods=['POST'])
def signup():
    if request.method == 'POST':
        un = request.get_json.get('username')
        passwd = request.get_json.get('password')

        user = User.query.filter_by('username'=un).first()
        if user:
            return jsonify({}), 400
        new_user = User(
                username=un,
                role_id=3
                )
        new_user.password(passwd)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'created': new_user.id}), 200
