# Key Concepts and Terminology in OAuth 2.0 and OpenID Connect

### OAuth 2.0
An authorization framework that enables a third-party application to obtain limited access to an HTTP service.

### OpenID Connect (OIDC)
An authentication layer built on top of OAuth 2.0, which allows clients to verify the identity of the end-user.

### Authorization Server
The server that authenticates the resource owner and issues access tokens after getting proper authorization.

### Resource Server
The server that hosts the protected user data and accepts requests for this data. These requests must be accompanied by an access token.

### Client 
An application making protected resource requests on behalf of the resource owner and with its authorization.

### Resource Owner
The entity capable of granting access to a protected resource. Often this is the end-user.

### Access Token
A credential that can be used by an application to access an API. It denotes the scopes and duration of access.

### Refresh Token
A credential that can be used to obtain a new access token when the current access token expires.

### Scopes
The extent of access that has been granted, which can include details such as read or write access, access to certain resources, or any other particular permissions.

### Authorization Code
A temporary code that the client will exchange for an access token. The code itself does not allow any access to the user's data.

### Implicit Flow
A flow in OAuth where the access token is transmitted directly to the client without an intermediary step of exchanging an authorization code.

### Authorization Code Flow
A flow in OAuth where the client gets an authorization code as an intermediary step, which is then exchanged for an access token.

### PKCE (Proof Key for Code Exchange)
A protocol used to mitigate the threat of having the authorization code intercepted. It's used in public clients, which cannot hold the client secret confidential.

### ID Token
A token used in OpenID Connect to communicate about the authentication of the end-user. It's a JWT and contains claims about the authentication event.

### JWT (JSON Web Token)
A compact, URL-safe means of representing claims to be transferred between two parties. The claims in a JWT are encoded as a JSON object that is used as the payload of a JSON Web Signature (JWS) structure, enabling the claims to be digitally signed or MACed.

### JWS (JSON Web Signature)
A standard part of the JOSE (JavaScript Object Signing and Encryption) framework. It provides a mechanism to digitally sign or Message Authentication Code (MAC) a JSON payload. In essence, it's used to ensure the integrity and authenticity of the data payload.

### Bearer Token

A type of access token that can be used by the "bearer" of the token to access resources. With OAuth 2.0, when a client application gets an access token, it's a Bearer Token. The client can use this token to authenticate requests to the resource server. It's called a Bearer Token because it doesn't require the client to prove possession of cryptographic material (a key). Any party in possession of a bearer token (a "bearer") can use it to get access to the associated resources (without demonstrating possession of a cryptographic key).

