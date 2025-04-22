# Capital City Time API

This is a simple Flask API. It provides the current time and UTC offset for specified capital cities, protected by token-based authentication.

## Base URL

The API is hosted on a Google Cloud VM and is accessible at:

`http://35.245.217.124:5000/`

**(Note: Please ensure the Flask application `app.py` is running on the VM for the API to be accessible.)**

## Authentication

Most endpoints require Bearer Token authentication. You must include an `Authorization` header in your requests with a valid token.

**Token:** `supersecrettoken123`

**Example Header:**
`Authorization: Bearer supersecrettoken123`

Requests without a valid token to protected endpoints will receive a `401 Unauthorized` error.

## Endpoints

### 1. Hello World (Public)

* **URL:** `/api/hello`
* **Method:** `GET`
* **Authentication:** None required
* **Description:** A simple test endpoint.
* **Success Response (200):**
    ```json
    {
        "message": "Hello, world!"
    }
    ```

### 2. Secure Data (Protected)

* **URL:** `/api/secure-data`
* **Method:** `GET`
* **Authentication:** Bearer Token required
* **Description:** A test endpoint demonstrating token authentication[cite: 1].
* **Success Response (200):**
    ```json
    {
        "secret": "This is protected info!"
    }
    ```
* **Error Response (401):**
    ```json
    {
        "error": "Unauthorized",
        "message": "Valid Bearer token required."
    }
    ```

### 3. Capital City Time (Protected)

* **URL:** `/api/time/<capital_city>`
* **Method:** `GET`
* **Authentication:** Bearer Token required
* **URL Parameters:**
    * `capital_city` (string): The name of the capital city (e.g., `London`, `Tokyo`). Case-insensitive.
* **Description:** Returns the current time, timezone name, and UTC offset for the specified capital city, if supported.
* **Success Response (200):**
    ```json
    {
        "city": "London",
        "local_time": "10:30:45", // Example time
        "timezone": "Europe/London",
        "utc_offset": "+0100" // Example offset (+HHMM format)
    }
    ```
* **Error Response (404 - City Not Found):**
    ```json
    {
        "error": "City not found",
        "message": "Time data for 'UnknownCity' is not available."
    }
    ```
* **Error Response (401 - Unauthorized):**
    ```json
    {
        "error": "Unauthorized",
        "message": "Valid Bearer token required."
    }
    ```

## How to Call the API (Example using cURL)

To get the time for London:

```bash
curl -H "Authorization: Bearer supersecrettoken123" [http://35.245.217.124:5000/api/time/London](http://35.245.217.124:5000/api/time/London)
