from flask import Flask, request, render_template
import base64
import os
import time  # Added import for time module
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

# Initialize Flask app
app = Flask(__name__)

# Google Drive API setup
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate_google_drive():
    # Use the credentials.json file for OAuth authentication
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES
    )
    # Run the local server for authentication on port 8080
    credentials = flow.run_local_server(port=8080)
    return build('drive', 'v3', credentials=credentials)

# Authenticate and initialize Google Drive service
drive_service = authenticate_google_drive()

@app.route('/')
def signature_form():
    return render_template('form.html')  # Render the form.html template

@app.route('/submit', methods=['POST'])
def submit_form():
    signature_data = request.form.get('signature')  # Get the signature data from the form
    if signature_data:
        # Decode Base64 signature and save it as an image
        signature_base64 = signature_data.split(",")[1]
        unique_filename = f"signature_{int(time.time())}.png"  # Generate a unique filename using time
        filepath = os.path.join('uploads', unique_filename)

        # Ensure 'uploads' directory exists
        os.makedirs('uploads', exist_ok=True)
        with open(filepath, "wb") as signature_file:
            signature_file.write(base64.b64decode(signature_base64))
        
        # Upload the saved signature image to Google Drive
        file_metadata = {'name': unique_filename}
        media = MediaFileUpload(filepath, mimetype='image/png')
        drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        return f"Signature saved locally and uploaded to Google Drive as {unique_filename}!"

    return "No signature provided!", 400

if __name__ == "__main__":
    # Run the app on host 0.0.0.0 and port 8080
    app.run(host="0.0.0.0", port=8080)
