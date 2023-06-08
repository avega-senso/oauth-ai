## Authorization Testing Instructions

These instructions guide you through the process of testing the authorization system using curl. The process involves making a POST request to the protected endpoint `/token`.

### Prerequisites

- You have curl installed on your machine.
- You have obtained a valid id token from the Identity Provider.

### Procedure using CURL

1. Open your command-line interface.

2. Paste the following command into the command line, replacing `your-token` with your actual access token:

```bash
curl -X POST \
  http://localhost:5000/token \
  -H 'Authorization: Basic Y2xpZW50MTpzZWNyZXQx'
```

### Procedure using REST Client for VSCode

```authenticate.http
POST http://localhost:5001/token HTTP/1.1
Content-Type: application/json
Authorization: token xxx

<request>
    <name>sample</name>
    <time>Wed, 21 Oct 2015 18:27:50 GMT</time>
</request>
```


