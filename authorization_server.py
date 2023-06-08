from flask import Flask, redirect, request, url_for, jsonify
from authlib.integrations.flask_client import OAuth
from jose import jwt

app = Flask(__name__)

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='',
    client_secret='',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'}
)

@app.route("/")
def hello():
    return redirect(url_for('.login'))

@app.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

# @app.route("/login")
# def login_page():
#     return render_template("login.html")

@app.route('/authorize')
def authorize():
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    
    # create access token with user_info
    access_token = jwt.encode(user_info, '<your-secret-key>', algorithm='HS256')

    return jsonify(access_token=access_token)

if __name__ == "__main__":
    app.run()








# from flask import Flask, request, jsonify
# from jose import jwt
# import base64
# from datetime import datetime, timedelta
# import uuid

# app = Flask(__name__)

# # Replace these with your actual secret and public keys
# SECRET_KEY = "your_secret_key"
# PUBLIC_KEY = "your_public_key"

# CLIENTS = {
#     # client_id: client_secret
#     "client1": "secret1",
# }

# @app.route('/token', methods=['POST'])
# def token():
#     auth_header = request.headers.get('Authorization')
#     if not auth_header or 'Basic' not in auth_header:
#         return jsonify({"error": "Invalid client authentication, incorrect auth_header", "auth_header": auth_header}), 401

#     # Basic authentication: base64 encoded "client_id:client_secret"
#     client_id, client_secret = base64.b64decode(auth_header.split(" ")[1]).decode().split(":")
#     if client_id not in CLIENTS or CLIENTS[client_id] != client_secret:
#         return jsonify({"error": "Invalid client authentication or secret. " + "Client_Id: " + client_id + ", Client_Secret:" + client_secret}), 401
        
#     # Here we should also check the client's grant types, redirect URIs, etc.
#     # And also authenticate the user, if it's an authorization code or password grant
#     # But for simplicity, we'll skip those here

#     # Issue an access token
#     access_token = jwt.encode({
#         "iss": "your_authorization_server",
#         "sub": "user_id",  # The user's id
#         "aud": client_id,
#         "exp": datetime.utcnow() + timedelta(minutes=60),  # 1 hour expiry
#         "scopes": ["read", "write"],  # scopes granted to the client
#         "jti": str(uuid.uuid4()),  # unique identifier for the token
#     }, SECRET_KEY, algorithm="RS256")

#     return jsonify({
#         "access_token": access_token,
#         "token_type": "Bearer",
#         "expires_in": 3600,
#         "scope": "read write"
#     }), 200

# if __name__ == '__main__':
#     app.run(port=5001, debug=True)
