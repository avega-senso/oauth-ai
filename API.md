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
