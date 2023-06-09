from flask import Flask, render_template, make_response, redirect

app = Flask(__name__)

@app.route('/')
def home():
    # First render the template in a response
    response = make_response(render_template('home.html'))
    # Then set a cookie on the response
    response.set_cookie('my_cookie', 'cookie_value', samesite='Lax', secure=False)
    # Then return the response
    return response

@app.route('/login')
def login():
    # The redirect URI is often on the same domain as the login route,
    # but it must be a route that your application handles.
    redirect_uri = "http://127.0.0.1:5000/callback"
    
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
    app.run(debug=True)
