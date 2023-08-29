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
   'me.2718281828@gmail.com' : 'project1'
}

@app.route('/oauth/token', methods=['GET'])
# @oauth.token_handler
def access_token():
    idt = request.headers['Authorization']
    idt = idt.split('Bearer ')[1]
    try:
        payload = id_token.verify_oauth2_token(idt, google_requests.Request(), GOOGLE_CLIENT_ID)
        email = payload['email']
        user_permissions = permissions[email]
        return jsonify({"access_token": user_permissions})
    except ValueError as e:
        # Invalid token
        return jsonify({
            "message": "Invalid token",
            "error": str(e)  # Include the error message from the exception
        }), 400
    return None


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
            token_reponse = "none"
            access_token = "none"
            if response.status_code == 200:
                token_response = response.json()
                access_token = token_response.get('access_token')
                # Use the access_token as needed
            else:
                # Handle error in token response
                print("Error fetching access token:", response.content)

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

            <p>Access Token: <pre>{json.dumps(access_token, indent=4)}</pre></p>
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