# Import necessary modules from the flask library
from flask import Flask, render_template, request, redirect, jsonify
# Import os and csv modules
import os 
import glob
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
                # Read the file as a CSV
                csv_file = csv.reader(file.read().decode('utf-8').splitlines())
                # Specify the path where you want to save the file on your PC
                save_path = '/Users/juanestebanfloyd/Documents/testFlaskApp/data/' + file.filename
                # Save the file to the specified path
                file.save(save_path)
            return jsonify({'message': 'Successfully saved'})
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
    # Especifica la ruta donde están los archivos CSV
    save_path = '/Users/juanestebanfloyd/Documents/testFlaskApp/data/'
    # Encuentra todos los archivos CSV en la ruta especificada
    files = glob.glob(save_path + '*.csv')
    for file_name in files:
        # Elimina cada archivo
        os.remove(file_name)
    return jsonify({'message': 'Archivos eliminados exitosamente'})

@app.route('/help')
def help():
    return render_template('help.html')

# If this script is run directly (not imported), start the Flask web server in debug mode
if __name__ == "__main__":
    app.run(debug=os.getenv('FLASK_DEBUG') == 'True')
