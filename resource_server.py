import requests
from flask import Flask, request, jsonify
from jose import jwt
from jose.exceptions import JWTError


app = Flask(__name__)

# Replace this with the correct public key from your Authorization Server
# Fetch Google's public keys
response = requests.get('https://www.googleapis.com/oauth2/v3/certs')
keys = response.json()
PUBLIC_KEY = keys.get(header['kid'])

# Used to validate using symmetric keys using HS256 algorithm 
SECRET = '12345'

@app.route('/resource', methods=['GET'])
def protected_resource():
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return jsonify({"message": "No authorization header provided."}), 401

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token."}), 401

    # Distinguish between an ID token and an Access Token
    if 'sub' in payload and 'iat' in payload:
        # return jsonify({"message": "This is an ID token, not an access token."}), 401
        return jsonify({"message": "Welcome " + str(payload['name']) + "! You are passing an ID token, not an access token. The ID token is not meant to provide access to resources. it's meant to provide information about the authenticated user to the client. Your id token contains:" + str(payload)}), 401

    # Check the scopes in payload['scopes'] to decide whether to allow the operation
    if 'desired-scope' not in payload['scopes']:
        return jsonify({"message": "Access denied."}), 403

    return jsonify({"message": "Access granted. Your access token contains:" + str(payload)})
    
if __name__ == '__main__':
    app.run(port=5000, debug=True)