## Authentication Testing Instructions

These instructions guide you through the process of testing the authentication and authorization system using curl. The process involves making a GET request to the protected endpoint `/resource`.

### Prerequisites

- You have curl installed on your machine.
- You have obtained a valid access token from the Authorization Server.

### Procedure using CURL

1. Open your command-line interface.

2. Paste the following command into the command line, replacing `your-token` with your actual access token:

```bash
curl -X GET http://localhost:5000/resource -H 'Authorization: Bearer your-token'
```

### Procedure using REST Client for VSCode

```authenticate.http
GET http://localhost:5000/resource HTTP/1.1
Content-Type: application/json
Authorization: token xxx

<request>
    <name>sample</name>
    <time>Wed, 21 Oct 2015 18:27:50 GMT</time>
</request>
```