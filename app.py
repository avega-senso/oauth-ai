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
def validate():
    if request.method == 'POST':
        token = request.form.get('credential')  # Get the JWT from the form data

        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)

            # Or, if multiple clients access the backend server:
            # idinfo = id_token.verify_oauth2_token(token, requests.Request())
            # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
            #     raise ValueError('Could not verify audience.')

            # If auth request is from a G Suite domain:
            # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
            #     raise ValueError('Wrong hosted domain.')

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            userid = idinfo['sub']
            payload = idinfo
            picture_url = idinfo.get('picture', '')  # Extract the profile picture URL
            
                        # Now include the picture_url in your response.
            # Here's an example of how you could create a simple HTML page displaying the picture.
            html = f"""
            <html>
            <body>
            <h1>Token is valid</h1>
            <p>UserID: {userid}</p>
            <img src="{picture_url}" alt="Profile Picture">
            <p>Payload: <pre>{json.dumps(idinfo, indent=4)}</pre></p>
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