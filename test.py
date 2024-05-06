# Import necessary modules from the flask library
from flask import Flask, render_template, request, redirect, jsonify
# Import os and csv modules
import os
import csv

# Create a new Flask web server
app = Flask(__name__)

# Define the main route which can handle both GET and POST requests
@app.route('/', methods=["GET", "POST"])
def index():
    data = []
    # If the request method is POST
    if request.method == 'POST':
        # If there are files in the request
        if request.files:
            # Get the uploaded file
            uploaded_file = request.files['filename']
            # Create the path where the file will be saved
            filepath = os.path.join(app.config['FILE_UPLOADS'], uploaded_file.filename)
            # Save the uploaded file to the specified path
            uploaded_file.save(filepath)
            # Open the saved file
            with open(filepath) as file:
                # Read the file as a CSV
                csv_file = csv.reader(file)
                # Get the headers from the first line of the CSV
                headers = next(csv_file)
                # For each row in the CSV, append it as a dictionary to the data list
                for row in csv_file:
                    data.append(dict(zip(headers, row)))
            # Return a success message and the data as a JSON response
            return jsonify({'message': 'Successfully sent', 'data': data})
    # If the request method is not POST, render the index.html template with the data
    return render_template('index.html', data=data)

# Define the help route which renders the help.html template
@app.route('/help')
def help():
    return render_template('help.html')

# Set the FILE_UPLOADS configuration to the specified path
app.config['FILE_UPLOADS'] = os.getenv('FILE_UPLOADS')

# If this script is run directly (not imported), start the Flask web server in debug mode
if __name__ == "__main__":
    app.run(debug=os.getenv('FLASK_DEBUG', True))
