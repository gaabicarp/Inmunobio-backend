# def token_required(func):
#    def wraper():
#       token = None

#       if 'token' in request.headers:
#          token = request.headers['x-access-tokens']

#       if not token:
#          return jsonify({'message': 'a valid token is missing'})

#       try:
#          data = jwt.decode(token, app.config[SECRET_KEY])
#          current_user = Users.query.filter_by(public_id=data['public_id']).first()
#       except:
#          return jsonify({'message': 'token is invalid'})

#         return f(current_user, *args, **kwargs)
#    return decorator