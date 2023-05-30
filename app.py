from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)

# Secret key for JWT token verification
app.config['SECRET_KEY'] = 'your-secret-key'

@app.route('/validate_token', methods=['POST'])
def validate_token():
    token = request.json['token']

    try:
        # Verify and decode the JWT token
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        
        # Access the payload data
        user_id = decoded_token['user_id']
        
        # Add your additional validation logic here
        # ...

        return jsonify(valid=True, user_id=user_id)
    except jwt.ExpiredSignatureError:
        return jsonify(valid=False, error='Token has expired')
    except jwt.InvalidTokenError:
        return jsonify(valid=False, error='Invalid token')

if __name__ == '__main__':
    app.run(debug=True)
