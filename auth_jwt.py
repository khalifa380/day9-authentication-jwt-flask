from flask import Flask, request, jsonify
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'

# Dummy user for demonstration
USER_DATA = {
    "username": "shaik",
    "password": "khalifa123"
}

# Token-required decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(*args, **kwargs)
    return decorated

# Login route
@app.route('/login', methods=['POST'])
def login():
    auth = request.json
    if auth and auth['username'] == USER_DATA['username'] and auth['password'] == USER_DATA['password']:
        token = jwt.encode({'user': auth['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token})
    return jsonify({'message': 'Invalid credentials'}), 401

# Protected route
@app.route('/protected', methods=['GET'])
@token_required
def protected():
    return jsonify({'message': 'Welcome! This is a protected route.'})

if __name__ == '__main__':
    app.run(debug=True)
    {
  "username": "admin",
  "password": "admin123"
}

