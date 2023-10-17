from flask import Flask, jsonify, render_template, make_response, redirect, request, url_for
import json
import os
import requests
from dotenv import load_dotenv
from cryptography.hazmat.primitives import serialization
from google.oauth2 import id_token # google.oauth2 library specifically verifies tokens that are issued by Google's OAuth2 authorization server.
import requests  # This is the common HTTP requests library
import google.auth.transport.requests as google_requests  # This is an alias to avoid the name collision
import time
import jwt as pyjwt
import datetime
from jwcrypto import jwe, jwk
from jwcrypto.common import json_encode, json_decode
from cryptography.hazmat.backends import default_backend

load_dotenv()  # take environment variables from .env.
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')

app = Flask(__name__)


# @app.route('/oauth/authorize', methods=['GET', 'POST'])
# @oauth.authorize_handler
# def authorize(*args, **kwargs):
#     if request.method == 'GET':
#         # Render a page for the user to grant access
#         pass
#     if request.method == 'POST':
#         # Read user decision from form data
#         pass
#     return True  # Assuming user grants access


permissions = {
   'me.2718281828@gmail.com' : 'project1',
   'robert@dahlborg.com': 'project1',
}





public_key = None
# Load the public key
with open("keys/public_key.pem", "rb") as key_file:
    public_key_pem = key_file.read()
    public_key = jwk.JWK.from_pem(public_key_pem)
assert public_key is not None


public_key_auth = None
# Load the public key
with open("keys/public_key_auth.pem", "rb") as key_file:
    public_key_auth_pem = key_file.read()
    public_key_auth = jwk.JWK.from_pem(public_key_auth_pem)
assert public_key_auth is not None


private_key_auth = None
# Load the private key
with open("keys/private_key_auth.pem", "rb") as key_file:
    private_key_auth = serialization.load_pem_private_key(
        key_file.read(),
        password=None,  # No password is set for the private key in the previous step
        backend=default_backend()
    )
assert private_key_auth is not None

# change to better signing algorithm, non symmetrical

# improve permission DB to include concept of Aud and scopes
# @oauth.token_handler
@app.route('/oauth/token', methods=['GET'])
def access_token(): # add query param for requested permission
    #?scopes=https://project1.avega.se/customer:read,https://project1.avega.se/order:readwrite

    # id X -> [https://project1.avega.se/customer:read, https://project1.avega.se/order:readwrite]
    # aud https://project1.avega.se -> [https://project1.avega.se/customer:read, https://project1.avega.se/order:readwrite]
    # aud https://project2.avega.se -> [https://project1.avega.se/customer:read, https://project1.avega.se/order:readwrite]
    idt = request.headers['Authorization']
    idt = idt.split('Bearer ')[1]
    try:
        id_payload = id_token.verify_oauth2_token(idt, google_requests.Request(), GOOGLE_CLIENT_ID)
        email = id_payload['email']
        user_permissions = permissions[email]
        # Payload (claims) that will be part of the access token
        payload = {
            "sub": email,  # Subject
            "iss": "Avega",  # Issuer
            "aud": ["https://project1.avega.se", "https://project2.avega.se"],  # Audience
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),  # Expiration time
            "scope": ["https://project1.avega.se/customer:read", "https://project1.avega.se/order:readwrite"]  # Custom scope (in this case, your original access token)
        }
        signed_encrypted_jwt = create_signed_encrypted_jwt(payload, "SECRET")
        print("Signed and encrypted JWT: " + signed_encrypted_jwt)
    except ValueError as e:        # Invalid token
        return jsonify({
            "message": "Invalid token",
            "error": str(e)  # Include the error message from the exception
        }), 400
    return signed_encrypted_jwt

def create_signed_encrypted_jwt(payload, secret_key):
    # Sign the JWT
    signed_access_token = pyjwt.encode(payload, private_key_auth, algorithm="RS256")
    # Encrypt the JWT
    protected_header = {
        "alg": "RSA-OAEP-256",
        "enc": "A256GCM"
    }
    jwetoken = jwe.JWE(plaintext=signed_access_token, protected=protected_header)
    jwetoken.add_recipient(public_key)
    
    return jwetoken.serialize()

private_key = None
# Load the private key
with open("keys/private_key.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,  # No password is set for the private key in the previous step
        backend=default_backend()
    )
assert private_key is not None

@app.route('/resource', methods=['GET'])# This service has audience https://project1.avega.se
def get_resource():
    auth_header = request.headers.get('Authorization', None)
    if not auth_header:
        return jsonify({'error': 'No Authorization header'}), 401

    parts = auth_header.split()

    if parts[0].lower() != 'bearer':
        return jsonify({'error': 'Invalid Authorization header format'}), 401
    if len(parts) == 1:
        return jsonify({'error': 'Token missing'}), 401
    elif len(parts) > 2:
        return jsonify({'error': 'Authorization header must be Bearer token'}), 401

    encrypted_access_token = parts[1]
    # decrypt token with resource server private key


    # Convert the private key to JWK format
    jwk_key = jwk.JWK.from_pem(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

    # Deserialize and decrypt the JWE token
    print("encrypted_access_token", encrypted_access_token)
    encrypted_token = jwe.JWE()
    encrypted_token.deserialize(encrypted_access_token)
    encrypted_token.decrypt(jwk_key)
    signed_access_token = encrypted_token.payload
    print("decrypted jwt", signed_access_token)
    try:
        # Here we decode and verify the JWT
        payload = pyjwt.decode(signed_access_token, public_key_auth, algorithms=['RS256'], audience='https://project1.avega.se')
        print("decoded jwt", payload)
    except pyjwt.ExpiredSignatureError:
        print("expired jwt")
        return jsonify({'error': 'Token has expired'}), 401
    except pyjwt.InvalidTokenError as e:
        print("Detailed error:", str(e))
        return jsonify({'error': 'Invalid token'}), 401

    # If JWT is valid, respond with a protected resource
    return jsonify({
        'data': 'This is a protected resource',
        'user': payload['sub']
    })

@app.route('/')
def home():
    # First render the template in a response
    response = make_response(render_template('home.html'))
    # Then set a cookie on the response
    response.set_cookie('my_cookie', 'cookie_value', samesite='Lax', secure=False)
    response.headers['Referrer-Policy'] = 'no-referrer-when-downgrade'
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin-allow-popups' 
    response.headers['Content-Security-Policy-Report-Only'] = 'script-src https://accounts.google.com/gsi/client; frame-src https://accounts.google.com/gsi/; connect-src https://accounts.google.com/gsi/;'
    return response

@app.route('/callback', methods=['GET', 'POST']) # a.k.a /auth, /redirect, or /return
def validate(): # https://developers.google.com/identity/gsi/web/guides/verify-google-id-token
    if request.method == 'POST':
        token = request.form.get('credential')  # Get the JWT from the form data
#         index = len(token) // 2
#         bad_token = token[:index] + str(1) + token[index + 1:]
        try:
            time.sleep(1.01)
            idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), GOOGLE_CLIENT_ID)
            userid = idinfo['sub']
            payload = idinfo
            picture_url = idinfo.get('picture', '')  # Extract the profile picture URL

           # Exchange authorization code for access token (example for authorization_code grant type)
            token_endpoint = "http://localhost:5001/oauth/token"

            response = requests.get(token_endpoint, headers={'Authorization': 'Bearer ' + token})
            encrypted_access_token = "none"
            if response.status_code == 200:
                encrypted_access_token = response.text
                # Use the access_token as needed
            else:
                # Handle error in token response
                print("Error fetching access token:", response.content)

            # Call resource serverAPI with token
            resource_endpoint = "http://localhost:5001/resource"
            response = requests.get(resource_endpoint, headers={'Authorization': 'Bearer ' + encrypted_access_token})
            resource_data = response.json() if response.status_code == 200 else {"error": "Failed to fetch resource"}
            # Now include the picture_url in your response.
            html = f"""
            <html>
            <body>
            <h1>Token is valid</h1>
            <p>UserID: {userid}</p>
            <img src="{picture_url}" alt="Profile Picture">
            <p>JWT Token: <pre>{token}</pre></p>
            <p><a href="https://jwt.io/#id_token={token}"><img src="http://jwt.io/img/badge.svg" alt="JWT.io"></a></p>
            <button onclick="location.href='{url_for('home')}'" type="button">
                Return to home
            </button>
            <p>Payload: <pre>{json.dumps(idinfo, indent=4)}</pre></p>

            <p>JWE Token: <pre>{json.dumps(encrypted_access_token, indent=4)}</pre></p>

            <p>Resource Data: <pre>{json.dumps(resource_data, indent=4)}</pre></p>

            <div>
                <h3>iss</h3>
                <p>This stands for issuer. It tells you who issued this token. In this case, the issuer is https://accounts.google.com, which means that the token was issued by Google's authentication server.</p>

                <h3>nbf</h3>
                <p>This stands for not before. It tells you the time before which the token must not be accepted for processing. The time is represented as the number of seconds since 1970-01-01T0:0:0Z as measured in UTC.</p>

                <h3>aud</h3>
                <p>This stands for audience. It tells you the ID of the audience that the ID token is intended for. It must match the client ID of your application.</p>

                <h3>sub</h3>
                <p>This stands for subject. It's an identifier for the user, unique among all Google accounts and never reused.</p>

                <h3>hd</h3>
                <p>This is the hosted domain parameter. If present, it indicates the hosted domain of the user. This is provided only if the user belongs to a hosted domain.</p>

                <h3>email</h3>
                <p>This is the email address of the user.</p>

                <h3>email_verified</h3>
                <p>This tells you whether the email address has been verified as belonging to the user.</p>

                <h3>azp</h3>
                <p>This stands for authorized party. In certain scenarios, this claim is needed to ensure that the token is intended for the expected recipient.</p>

                <h3>name</h3>
                <p>This is the full name of the user.</p>

                <h3>picture</h3>
                <p>This is the URL of the user's profile picture.</p>

                <h3>given_name</h3>
                <p>This is the given name (first name) of the user.</p>

                <h3>family_name</h3>
                <p>This is the family name (last name) of the user.</p>

                <h3>iat</h3>
                <p>This stands for issued at. It tells you when the token was issued. Like nbf, the time is represented as the number of seconds since 1970-01-01T0:0:0Z as measured in UTC.</p>

                <h3>exp</h3>
                <p>This stands for expiration time. It tells you when the token expires. After this time, the token must not be accepted for processing.</p>

                <h3>jti</h3>
                <p>This stands for JWT ID. It's a unique identifier for the token, can be used to prevent the JWT from being replayed.</p>

                <p>The values in "sub", "aud", "azp" are specific to your application and the user. The URLs, names, and times will vary based on the specifics of your application and the user who has authenticated.</p>
            </div>
            </body>
            </html>
            """
            return html
        
            # return jsonify({"message": "Token is valid", "payload": idinfo}), 200
        except ValueError as e:
            # Invalid token
            return jsonify({
                "message": "Invalid token",
                "error": str(e)  # Include the error message from the exception
            }), 400
            pass
            
    # this will be returned if no valid POST request is received
    return jsonify({"message": "Unexpected request"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)