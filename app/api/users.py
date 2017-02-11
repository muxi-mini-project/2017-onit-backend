#读取用户信息
@api.route('/user/show_profile/', method=['GET'])
def show_profile():
    username = request.args.get('username')
   
   return jsonify({ 
        'uid': [post.to_json()],

        })
