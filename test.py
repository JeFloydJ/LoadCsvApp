# Import necessary modules from the flask library
from flask import Flask, render_template, request, redirect, jsonify
# Import os and csv modules
import os
import csv
import boto3
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Read AWS credentials from environment variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        if request.files:
            uploaded_file = request.files['filename']
            # Read the file as a CSV before uploading to S3
            csv_file = csv.reader(uploaded_file.read().decode('utf-8').splitlines())
            # Reset file pointer to beginning before uploading to S3
            uploaded_file.seek(0)
            s3.upload_fileobj(uploaded_file, os.getenv('BUCKET_NAME'), uploaded_file.filename)
            return jsonify({'message': 'Successfully sent'})
    return render_template('index.html')

@app.route('/help')
def help():
    return render_template('help.html')

# If this script is run directly (not imported), start the Flask web server in debug mode
if __name__ == "__main__":
    app.run(debug=os.getenv('FLASK_DEBUG') == 'True')
