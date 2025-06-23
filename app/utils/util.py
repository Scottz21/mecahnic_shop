import jwt
from datetime import datetime, timezone, timedelta
from functools import wraps
from flask import request, jsonify


SECRET_KEY = "super secret secrets"

def encode_token(customer_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(hours=1),
        'iat': datetime.now(timezone.utc),
        'sub': str(customer_id)  
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            print("AUTH HEADER RAW:", auth_header)  # 👈 debug log
            parts = auth_header.split()

            if len(parts) != 2 or parts[0] != "Bearer":
                return jsonify({'message': 'Invalid token format'}), 400

            token = parts[1]
            try:
                data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                print("DECODED JWT:", data)  # 👈 debug log

                # ✅ Convert customer_id back to int after decoding
                customer_id = int(data['sub'])

            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired!'}), 400
            except jwt.InvalidTokenError as e:
                print("JWT ERROR:", e)  # 👈 log the exact JWT error
                return jsonify({'message': 'Invalid token!'}), 400

            return f(customer_id, *args, **kwargs)

        return jsonify({'message': 'Authorization header missing'}), 400

    return decorated

        
            
            