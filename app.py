from flask import Flask, jsonify, render_template, make_response, redirect, request, url_for
import json
import os
import requests
from dotenv import load_dotenv
from cryptography.hazmat.primitives import serialization
from google.oauth2 import id_token # google.oauth2 library specifically verifies tokens that are issued by Google's OAuth2 authorization server.
from google.auth.transport import requests


load_dotenv()  # take environment variables from .env.
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')

app = Flask(__name__)

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

        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
            userid = idinfo['sub']
            payload = idinfo
            picture_url = idinfo.get('picture', '')  # Extract the profile picture URL
            
            # Now include the picture_url in your response.
            html = f"""
            <html>
            <body>
            <h1>Token is valid</h1>
            <p>UserID: {userid}</p>
            <img src="{picture_url}" alt="Profile Picture">
            <p>JWT Token: <pre>{token}</pre></p>
            <p><a href="https://jwt.io/#id_token={token}"><img src="http://jwt.io/img/badge.svg" alt="JWT.io"></a></p>
            <p>Payload: <pre>{json.dumps(idinfo, indent=4)}</pre></p>
            <!-- Add a button to return to the home page -->
            <button onclick="location.href='{url_for('home')}'" type="button">
                Return to home
            </button>
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
    app.run(host='localhost', port=5001, debug=True)