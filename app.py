from flask import Flask, request, render_template
import base64

app = Flask(__name__)

# Route for the form
@app.route('/')
def signature_form():
    return render_template('form.html')  # This will load the HTML form

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit_form():
    signature_data = request.form['signature']  # Get the Base64 signature
    if signature_data:
        # Remove the prefix and save the signature as an image
        signature_base64 = signature_data.split(",")[1]
        with open("signature.png", "wb") as signature_file:
            signature_file.write(base64.b64decode(signature_base64))

    return "Signature saved successfully!"

# Correct indentation for the main block
if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)

