# OAuthAI - OAuth2/OIDC Authentication and Authorization Project using ChatGPT 

OAuthAI is a comprehensive and secure project built with the primary objective of providing a hands-on, learning platform for individuals looking to delve into the world of OAuth 2.0, OpenID Connect protocols, and Google's authentication system. The project is implemented using the assistance of OpenAI's language model, ChatGPT, showcasing the potential of AI in software development, problem-solving and coding.

## Table of Contents
1. [Overview](#overview)
2. [Project Plan](./docs/PROJECTPLAN.md)
3. [Project Structure](#project-structure)
4. [Architecture](./docs/ARCHITECTURE.md)
5. [Key Concepts and Terminology](./docs/DEFINITIONS.md)
5. [Setup and Installation](#setup-and-installation)
6. [Google IdP Setup](./docs/GOOGLE.md)
7. [Usage](#usage)
8. [Contribute](#contribute)
9. [License](#license)

## Overview

This project includes the development of a Web Frontend, an Authorization Server, and a Resource Server. The Web Frontend initiates the login process by redirecting users to Google. The Authorization Server receives an ID-token from Google via the Web Frontend, verifies the token, and sends back an Access Token. The Resource Server receives the Access Token and verifies it. The requested operation is allowed if the token is valid and contains the right scopes.

## Project Structure

The project is divided into three main parts:

- **Web Frontend:** Contains the user interface and manages the interaction with Google for user login.
- **Authorization Server:** Handles ID-token verification and Access Token generation.
- **Resource Server:** Manages Access Token verification and operation authorization.

## Setup and Installation
### Installation

Here's a quick step by step guide on how to get the development env running:

1. Clone this repository:

    ```bash
    git clone https://github.com/avega-senso/oauth-ai.git
    ```
2. Setup a virtual environment

    ```bash
    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    ```

3. Install the requirements:

    ```bash
    cd oauth-ai
    pip install -r requirements.txt
    ```

### Prerequisites

- Python 3.x
- pip
- Flask
- PyJWT

## Usage

(Provide instructions on how to use the application, potentially with screenshots or video walkthroughs.)

## Contributing

Please read [CONTRIBUTING.md](./docs/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE.md](./docs/LICENSE.md) file for details.



# OAuth-AI

This project provides a simple Flask-based service to validate JWT tokens. 

## Getting Started




### Usage

1. Start the server:

    ```bash
    python app.py
    ```

2. Use `curl` to validate a JWT token:

    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"token":"your-jwt-token"}' http://127.0.0.1:5000/validate_token
    ```

    Replace `"your-jwt-token"` with a real JWT token.





