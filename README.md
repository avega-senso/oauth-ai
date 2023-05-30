# OAuth-AI

# Flask JWT Validation Service

This project provides a simple Flask-based service to validate JWT tokens. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.x
- pip
- Flask
- PyJWT

### Installation

Here's a quick step by step guide on how to get the development env running:

1. Clone this repository:

    ```bash
    git clone https://github.com/yourusername/flask-jwt-validation.git
    ```

2. Install the requirements:

    ```bash
    cd flask-jwt-validation
    pip install -r requirements.txt
    ```

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

## API

**POST /validate_token**

Validates a JWT token.

- Request:

    ```json
    {
        "token": "your-jwt-token"
    }
    ```

- Response:

    ```json
    {
        "valid": true,
        "user_id": "user_id_from_decoded_token"
    }
    ```

    or

    ```json
    {
        "valid": false,
        "error": "error_message"
    }
    ```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
