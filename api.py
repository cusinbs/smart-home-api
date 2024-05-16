from datetime import datetime
from flask import Flask, request, jsonify
from pyHS100 import SmartPlug, SmartDeviceException
import threading
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

API_KEY = "018f83d0-b896-710c-b0b2-3bef02463ac5"  # Replace with your actual API key

class SmartSwitchController:
    def __init__(self, ip_address, on_duration=120):
        self.plug = SmartPlug(ip_address)
        self.lock = threading.Lock()
        self.timer = None
        self.on_duration = on_duration

    def turn_on_for_duration(self):
        with self.lock:
            try:
                if self.plug.state == "OFF":
                    self.plug.turn_on()
                    logging.info(f"Smart switch turned ON at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

                # Cancel the existing timer if there is one
                if self.timer:
                    self.timer.cancel()

                # Set a new timer
                self.timer = threading.Timer(self.on_duration, self.turn_off)
                self.timer.start()
            except SmartDeviceException as e:
                logging.error(f"Failed to turn on the smart switch: {e}")

    def turn_off(self):
        with self.lock:
            try:
                if self.plug.state == "ON":
                    self.plug.turn_off()
                    logging.info(f"Smart switch turned OFF at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            except SmartDeviceException as e:
                logging.error(f"Failed to turn off the smart switch: {e}")

# Initialize SmartSwitchController with IP address and duration
porch_light_switch = SmartSwitchController("192.168.68.72") #Replace with your actual smart switch IP

@app.route('/push-notification', methods=['POST'])
def push_notification():
    # Validate the request
    if not request.form:
        logging.error("No form data in request")
        return jsonify({"error": "Bad Request - No form data"}), 400

    # Get the form data sent in the request
    form_data = request.form.to_dict()

    # Validate API key
    api_key = form_data.get("apikey", "").lower()
    if api_key != API_KEY:
        logging.error("Invalid API key")
        return jsonify({"error": "Unauthorized"}), 401
    
    # Check if the title contains the word "Doorbell" or "Garage"
    title = form_data.get("title", "").lower()
    if title in ["garage", "doorbell"]:
        porch_light_switch.turn_on_for_duration()

    # Return 200 OK without form data
    return '', 200

@app.errorhandler(400)
def bad_request_error(error):
    # Log the request data
    logging.error(f"Bad Request Data: {request.data}")
    logging.error(f"Bad Request JSON: {request.get_json()}")
    return jsonify({"error": "Bad Request"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=69)
