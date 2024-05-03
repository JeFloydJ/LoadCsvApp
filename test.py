from flask import Flask, render_template, request, redirect, jsonify
import os
import csv

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    data = []
    if request.method == 'POST':
        if request.files:
            uploaded_file = request.files['filename']
            filepath = os.path.join(app.config['FILE_UPLOADS'], uploaded_file.filename)
            uploaded_file.save(filepath)
            with open(filepath) as file:
                csv_file = csv.reader(file)
                headers = next(csv_file)
                for row in csv_file:
                    data.append(dict(zip(headers, row)))
            return jsonify({'message': 'Enviado exitosamente', 'data': data})
    return render_template('index.html', data=data)

@app.route('/help')
def help():
    return render_template('help.html')

app.config['FILE_UPLOADS'] = "/Users/juanestebanfloyd/Documents/testFlaskApp"

if __name__ == "__main__":
    app.run(debug=True)
