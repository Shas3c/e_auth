# E-Authentication-System
This project is about Authentication System which is built using Django Framework and can be used over a web application.

This E-Authentication System uses 2 Authentication Feature:

- Authentication using OTP

  <ul>
  1. User enter their login credentials and select 'Login with OTP'.<br>
  2. A 6-digit random OTP is generated and sent to user's registered email ID.<br>
  3. The user has to enter the correct OTP to get logged in to website.
  </ul>
  
- Authentication using QR

  <ul>
  1. User enter their login credential and select 'Login with QR'.<br>
  2. A random QR image is generated and sent to user's registered email ID and Web Scanner will be opened on your browser.<br>
  3. The user has to scan that QR image into scanner to get logged in to website.
  </ul>
  
**NOTE : Before running this application on your system, you are requested to change the sender email ID and password in settings.py file.**
