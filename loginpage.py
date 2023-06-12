from flask import Flask, render_template, make_response, redirect
import requests
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

app = Flask(__name__)

@app.route('/')
def home():
    # First render the template in a response
    response = make_response(render_template('home.html'))
    # Then set a cookie on the response
    response.set_cookie('my_cookie', 'cookie_value', samesite='Lax', secure=False)
    response.headers['Referrer-Policy'] = 'no-referrer-when-downgrade'
    # Then return the response
    return response

@app.route('/login')
def login():
    # The redirect URI is often on the same domain as the login route,
    # but it must be a route that your application handles.
    redirect_uri = "http://127.0.0.1:5001/"
    
    # The authorization URL is the URL you redirect the user to, in order
    # to authenticate with Google.
    authorization_url = "https://accounts.google.com/o/oauth2/v2/auth"
    
    # The values of these parameters depend on your OAuth 2.0 Client ID.
    params = {
        "response_type": "id_token",
        "client_id": "691013142486-m6ig3434oi8ghmavfggn0c9jmk7l4sjn.apps.googleusercontent.com",
        "redirect_uri": redirect_uri,
        "scope": "openid email profile",
        # "state": "your-state-value",  # optional, for CSRF protection
    }
    
    # You would normally use a library to construct this URL, but this
    # gives you the basic idea.
    url = f"{authorization_url}?{urlencode(params)}"
    
    return redirect(url)

@app.route('/callback', methods=['GET'])
def callback():
    code = request.args.get('code')
    if not code:
        return jsonify({"message": "No authorization code provided."}), 400

    token_endpoint = "https://oauth2.googleapis.com/token"
    client_id = "your-client-id"  # replace with your client ID
    client_secret = "your-client-secret"  # replace with your client secret

    payload = {
        "code": code,
        "client_id": os.environ.get('GOOGLE_CLIENT_ID'),
        "client_secret": os.environ.get('GOOGLE_CLIENT_SECRET'),
        "redirect_uri": "http://127.0.0.1:5001/callback",
        "grant_type": "authorization_code"
    }

    response = requests.post(token_endpoint, data=payload)
    if response.status_code == 200:
        token_response = response.json()
        access_token = token_response.get('access_token')
        if not access_token:
            return jsonify({"message": "No access token in token response."}), 401

        # Now you can use the access token to authorize requests to protected resources
        return jsonify({"message": "Access granted. Your access token is: " + access_token}), 200
    else:
        return jsonify({"message": "Failed to exchange code for token."}), 400


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)