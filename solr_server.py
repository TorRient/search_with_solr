import pysolr
import json
import os
from flask import Flask, jsonify, request, render_template
from werkzeug.utils import secure_filename

# Setup a Solr instance. The timeout is optional.
solr = pysolr.Solr('http://10.10.16.236:8983/solr/core_voccer', always_commit=True, timeout=100)

static_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'uploads/')

# Add data
@app.route('/add_data', methods=['GET'])
def add_data(path='./data'):
    list_json = os.listdir(path)
    for file_name in list_json:
        paths = os.path.join('./data',file_name)
        with open(paths) as json_file:
            data = json.load(json_file)
            solr.add(data)
    return jsonify("OK")

# Thêm data bằng file
@app.route('/add_data_file', methods=['GET','POST'])
def add_data_file():
    # if request.method == 'GET':
    #     return render_template('add_file.html')
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
    else :
        return jsonify('NOT FILE')

    with open(file_path) as json_file:
            data = json.load(json_file)
            solr.add(data)

    return jsonify("OK")
    
# Xóa data
@app.route('/delete_data', methods=['GET'])
def delete_data():
    solr.delete(q='*:*')
    return jsonify("OK")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)