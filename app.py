# app.py
import os
from flask import Flask, jsonify, request
from datetime import datetime
import pytz # You'll need to install this: pip install pytz
from functools import wraps # Import wraps

app = Flask(__name__)

# --- Token Authentication Setup (from PDF) ---
# Use an environment variable for the token in production, but hardcode for now
API_TOKEN = "supersecrettoken123" #

def token_required(f): #
    @wraps(f) # Use wraps to preserve function metadata
    def decorator(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            if token == API_TOKEN:
                return f(*args, **kwargs)
        return jsonify({"error": "Unauthorized", "message": "Valid Bearer token required."}), 401 #
    return decorator

# --- Capital City Timezone Data ---
# You'll need to expand this dictionary with the capitals you want to support.
# The keys are lowercase city names for easier lookup, values are standard timezone names.
CAPITAL_TIMEZONES = {
    "london": "Europe/London",
    "tokyo": "Asia/Tokyo",
    "washington": "America/New_York", # Washington D.C. uses Eastern Time
    "paris": "Europe/Paris",
    "canberra": "Australia/Canberra",
    "ottawa": "America/Toronto", # Ottawa uses Eastern Time, often represented by Toronto
    "moscow": "Europe/Moscow"
    # Add more capitals and their corresponding pytz timezone names here
}

# --- API Endpoints ---

@app.route('/api/hello', methods=['GET']) # Basic endpoint from PDF
def hello():
    return jsonify({"message": "Hello, world!"}) #

@app.route('/api/secure-data', methods=['GET']) # Protected endpoint from PDF
@token_required
def secure_data():
    return jsonify({"secret": "This is protected info!"}) #

@app.route('/api/time/<string:capital_city>', methods=['GET'])
@token_required # Protect this endpoint
def get_capital_time(capital_city):
    """
    Returns the current time and UTC offset for a supported capital city.
    Requires Bearer token authentication.
    """
    city_lower = capital_city.lower() # Convert input to lowercase for lookup

    if city_lower not in CAPITAL_TIMEZONES:
        return jsonify({"error": "City not found", "message": f"Time data for '{capital_city}' is not available."}), 404

    try:
        tz_name = CAPITAL_TIMEZONES[city_lower]
        city_tz = pytz.timezone(tz_name)
        now_utc = datetime.now(pytz.utc) # Get current time in UTC
        now_local = now_utc.astimezone(city_tz) # Convert to the city's local time

        # Format time and offset
        local_time_str = now_local.strftime('%H:%M:%S')
        utc_offset = now_local.strftime('%z') # Gets offset like +0100 or -0400
        # Add colon to offset for readability if needed: utc_offset_formatted = utc_offset[:3] + ":" + utc_offset[3:]


        return jsonify({
            "city": capital_city.capitalize(), # Return original capitalization
            "timezone": tz_name,
            "local_time": local_time_str,
            "utc_offset": utc_offset # Returns offset like +HHMM or -HHMM
        })

    except pytz.UnknownTimeZoneError:
         return jsonify({"error": "Invalid timezone", "message": f"The timezone '{tz_name}' configured for '{capital_city}' is invalid."}), 500
    except Exception as e:
        # Catch unexpected errors
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


# --- Run the App ---
if __name__ == '__main__':
    # Use port 5000 and host 0.0.0.0 to make it accessible externally
    app.run(host='0.0.0.0', port=5000, debug=True) # Set debug=False for production