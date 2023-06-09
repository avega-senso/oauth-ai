import os
from flask import Flask, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key"  # Replace with your secret key
# app.config["GOOGLE_OAUTH_CLIENT_ID"] = "359656154300-aund08jegp7qo42imfk0gjh66g4h2e4o.apps.googleusercontent.com"  # Replace with your Google OAuth Client ID
# app.config["GOOGLE_OAUTH_CLIENT_SECRET"] = "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"  # Replace with your Google OAuth Client Secret
app.config["GOOGLE_OAUTH_CLIENT_ID"] = "691013142486-m6ig3434oi8ghmavfggn0c9jmk7l4sjn.apps.googleusercontent.com"  # Replace with your Google OAuth Client ID
app.config["GOOGLE_OAUTH_CLIENT_SECRET"] = "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"  # Replace with your Google OAuth Client Secret

google_bp = make_google_blueprint(scope=["https://www.googleapis.com/auth/userinfo.profile", "openid"])
app.register_blueprint(google_bp, url_prefix="/login")

@app.route("/")
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v1/userinfo")
    assert resp.ok, resp.text
    return "You are {name} on Google".format(name=resp.json()["name"])

if __name__ == "__main__":
    app.run(debug=True)