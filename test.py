# Import necessary modules from the flask library
from flask import Flask, render_template, request, redirect, jsonify
# Import os and csv modules
import os
import csv
import boto3
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError

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
            uploaded_files = request.files.getlist("filename")
            for file in uploaded_files:
                # Read the file as a CSV before uploading to S3
                csv_file = csv.reader(file.read().decode('utf-8').splitlines())
                # Reset file pointer to beginning before uploading to S3
                file.seek(0)
                s3.upload_fileobj(file, os.getenv('BUCKET_NAME'), file.filename)
            return jsonify({'message': 'Successfully sent'})
    return render_template('index.html')


@app.route('/show', methods=["GET"])
def show():
    bucket_name = os.getenv('BUCKET_NAME')
    file_name = 'Veevart Organizations Report test.csv'  
    try:
        s3.download_file(bucket_name, file_name, '/tmp/' + file_name)
    except NoCredentialsError:
        return jsonify({'error': 'No se encontraron las credenciales de AWS'})

    with open('/tmp/' + file_name, 'r') as f:
        csv_file = csv.reader(f)
        data = list(csv_file)

    return jsonify({'data': data})

@app.route('/delete', methods=["POST"])
def delete():
    file_name = 'Veevart Organizations Report test.csv'  
    bucket_name = os.getenv('BUCKET_NAME')
    try:
        s3.delete_object(Bucket=bucket_name, Key=file_name)
        return jsonify({'message': 'Archivo eliminado exitosamente'})
    except NoCredentialsError:
        return jsonify({'error': 'No se encontraron las credenciales de AWS'})

@app.route('/help')
def help():
    return render_template('help.html')

# If this script is run directly (not imported), start the Flask web server in debug mode
if __name__ == "__main__":
    app.run(debug=os.getenv('FLASK_DEBUG') == 'True')
