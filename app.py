from flask import Flask, render_template, request, jsonify
import requests
from controllers.wpm import main as calculateWPM
from controllers.saw import main as calculateSAW
from werkzeug.utils import secure_filename
import os
import json

app = Flask(__name__)

@app.route('/')
def main() :
    return render_template("index.html")

@app.route('/updateMetode', methods = ['POST'])
def updateMetode() :
    # read file data.json
    file = open('data.json', 'r')
    data = json.load(file)

    data['type'] = request.form.get('metode')
    data['sorting'] = request.form.get('sorting')

    with open('data.json', 'w') as outfile :
        json.dump(data, outfile)

    return jsonify({"status": "success"})

@app.route('/setWeight', methods = ['POST'])
def setWeight() :
    # read file data.json
    file = open('data.json', 'r')
    data = json.load(file)

    data['W'] = request.form.getlist('weight[]')
    data['L'] = request.form.getlist('L[]')

    with open('data.json', 'w') as outfile :
        json.dump(data, outfile)

    return jsonify({"status": "success"})

@app.route('/setAlternatif', methods = ['POST'])
def setAlternatif() :
    # read file data.json
    file = open('data.json', 'r')
    data = json.load(file)

    file = request.files['file']

    data['A'] = []

    if file.filename == '' :
        data['K'] = request.form.getlist('alternatif_name[]')
        data['file'] = ""

        for i in range(len(request.form.getlist('alternatif_name[]'))) :
            data['A'].append(request.form.getlist('alternatif'+ str(i+1) +'[]'))
    else :
        filename = secure_filename(file.filename)
        data['file'] = filename
        file.save(filename)

    with open('data.json', 'w') as outfile :
        json.dump(data, outfile)

    return jsonify({"status": "success"})

@app.route('/getKriteria')
def getKriteria() :
    # read file data.json
    file = open('data.json', 'r')
    data = json.load(file)

    return jsonify({"data": len(data['L'])})

@app.route('/calculate')
def calculate_wpm() :
    file = open('data.json', 'r')
    data = json.load(file)

    if data['type'] == 'WPM' :
        return calculateWPM()
    elif data['type'] == 'SAW' :
        return calculateSAW()

if __name__ == "__main__" :
    app.run(debug=True)