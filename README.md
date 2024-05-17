# Smart Switch Controller for Eufy Cameras with Push Notification Forwarding

## Overview

I recently installed several smart switches around my house, including one for the front porch light. My goal was to set up the front porch light to turn on when my doorbell or garage cameras detect someone. However, my Eufy cameras do not support API notifications. To work around this limitation, I found an Android app called "Push Notification Forward HTTP," which forwards push notifications as HTTP requests.

I then developed a small API in Python to handle these HTTP requests from that app and control the smart switches. I then hosted this small python program on a Raspberry Pi and keeps it running 24/7. This program can be expanded to other use cases such as backyard light, bedroom light, etc.

**Pros:**
- Integrates smart devices without official development APIs (e.g., Eufy).
- Free and suitable for small home projects.
- No need for complex setup or cloud server expenses.

**Cons:**
- Latency: The average delay to turn on the light is about 4 seconds, which can be reduced by using a dedicated old phone in the same network as the switch for forwarding notifications only.

## Program Description

The Python program uses the Flask framework to create a web server that listens for POST requests. When a POST request is received with specific keywords ("doorbell" or "garage") in the title, the program turns on a smart switch for a specified duration (default is 2 minutes). The program also includes basic API key authentication to enhance security.

## How to Set Up

1. **Install Dependencies**:
   ```bash
   pip install Flask pyHS100

2. **Run the program**:
   ```bash
   python app.py

3. **Configure Push Notification Forwarding:**:
   - Install the "Push Notification Forward HTTP" app on your Android phone.
    - Set up the app to forward notifications from your Eufy camera app to the endpoint `http://<your_server_ip>:69/push-notification`.
    - Include the API key in the request form.
   ![request_form](https://github.com/cusinbs/smart-switch-api/assets/20715034/9efdeaa8-2fc8-4af5-b809-d202f396b04e)

3. **Set Up Static IP and Port Forwarding:**:
   - Ensure your Raspberry Pi or hosting device has a static IP address to maintain consistent access.
    - Depending on your router, configure port forwarding for the hosting device to allow external access to your dedicated port.
    ![Portforward](https://github.com/cusinbs/smart-switch-api/assets/20715034/765282d6-4f7c-4013-98eb-446f4210df60)

## Security Considerations

During testing, I noticed some malicious attempts to spoof the endpoints. To mitigate this, ensure that:

- The API endpoint is secured with a strong, random API key.
- If possible, use a dedicated old phone using your home network for forwarding notifications to reduce latency and avoid exposing your primary device.

## Potential Improvements

For those seeking more advanced integrations, you might explore using the [eufy-security-client](https://github.com/bropat/eufy-security-client) repository, which offers more direct control over Eufy devices but requires a more complex setup and potentially cloud services.

By using the "Push Notification Forward HTTP" app, you can achieve a functional and cost-effective solution for your smart home project.
