# Project Plan

## Web Frontend
### Create a User Interface with a Login Button
Develop a user interface featuring a login button for users to initiate the authentication process.
### Implement Google Redirect for User Login
Upon user’s click on the login button, the system should redirect to Google for user login.
### Receive ID-token from Google Post Login
Once the user logs into Google, the system must be capable of receiving the ID-token sent back by Google to the web frontend.

## Authorization Server:
### Develop an Authorization Server to Receive ID-token
The authorization server should be able to receive the ID-token from the web frontend.
### Verify ID-token using Google’s Public Keys
Implement functionality in the server to verify the ID-token using Google’s public keys.
### Generate and Dispatch Access Token Post Verification
If the ID-token is verified successfully, map the ID to permissions, generate an Access Token and send it back to the web frontend.

## Resource Server:
### Receive Access Token from Web Frontend
Develop functionality in the resource server to receive the Access Token from the web frontend.
### Implement Access Token Decoding
The resource server should be able to either decode the token using a Public Key from the Authorization Server or query the Authorization Server to get a decoded token.
### Validate Access Token and Scopes
Once the resource server has a decoded token, it should verify the freshness of the token and if it contains the correct permissions (known as “scopes”). If these conditions are met, the requested operation is allowed.
### Implement Response for Unauthorized Access
If conditions are not met, a 401 Unauthorized response should be returned.
### Compliance with OAuth 2.0 and OpenID Connect Protocols
Ensure best security practices by following the OAuth 2.0 and OpenID Connect protocols when implementing this solution.
### Use Secure Libraries and Tools for Token Generation and Validation
Use secure libraries and tools to manage tasks such as token generation and validation.