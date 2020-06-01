import pysolr
import json
import os
from flask import Flask, jsonify, request, render_template
from werkzeug.utils import secure_filename
from pyvi import ViTokenizer
config = {
    'host': 'http://localhost',
    'port': '8983',
    'core_name': 'bkcv',
    'timeout': 100
}

# Setup a Solr instance. The timeout is optional.
solr = pysolr.Solr(config['host']+':'+config['port']+'/solr/'+config['core_name'], always_commit=True, timeout=config['timeout'])

static_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'uploads/')

# from word_similar import Word_Similar
# ws = Word_Similar()

# Add data
@app.route('/add_data', methods=['GET'])
def add_data(path='./data'):
    list_json = os.listdir(path)
    count = 0
    for file_name in list_json:
        paths = os.path.join('./data',file_name)
        with open(paths) as json_file:
            data = json.load(json_file)
            data = list(data)
            for field in data:
                field["content"] = ViTokenizer.tokenize(field["content"])
                field["author"] = ViTokenizer.tokenize(field["author"])
                field["title"] = ViTokenizer.tokenize(field["title"])
                field["description"] = ViTokenizer.tokenize(field["description"])
                field["topic"] = ViTokenizer.tokenize(field["topic"])
            solr.add(data)
        # break
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
            data = list(data)
            for field in data:
                field["content"] = ViTokenizer.tokenize(field["content"])
                field["author"] = ViTokenizer.tokenize(field["author"])
                field["title"] = ViTokenizer.tokenize(field["title"])
                field["description"] = ViTokenizer.tokenize(field["description"])
                field["topic"] = ViTokenizer.tokenize(field["topic"])
            solr.add(data)

    return jsonify("OK")

@app.route('/fulltext', methods=['POST'])
def fulltext():
    general_text = request.args.get('general_text')
    word_similar = request.args.get('word_similar')
    if word_similar == True: # Nếu có feature từ đồng nghĩa
        general_text = ws.find_word_similar(general_text)

    results = solr.search(general_text, **{
        'rows':10,
        'hl':'true',
        'hl.method':'original',
        'hl.simple.pre':'<mark style="background-color:#ffff0070;">',
        'hl.simple.post':'</mark>',
        'hl.highlightMultiTerm':'true',
        'hl.fragsize':100,
        'defType' : 'dismax',
        'fl' : '*, score',
        # 'bq':'{!func}linear(clicked, 0.01 ,0.0 )',
        # # 'bq':'{!func}log(linear(clicked, 20 ,0.0 ))',
        'mm':1,
        'ps':3,
        'pf': 'title^1.0 description^1.0 content^2.0',
        'qf':'topic^1 title^3.0 description^1.0 content^1.0',
    })
    return jsonify("OK")

@app.route('/field', methods=['POST'])
def fulltextws():
    # general_text        = request.args.get('general_text')
    topic               = request.args.get('topic')
    bool_1              = request.args.get('bool_1')
    # weight_topic        = request.args.get('weight_topic')

    title               = request.args.get('title')
    bool_2              = request.args.get('bool_2')
    # weight_title        = request.args.get('weight_title')
    
    description         = request.args.get('description')
    bool_3              = request.args.get('bool_3')
    # weight_description  = request.args.get('weight_description')
    
    content             = request.args.get('content')
    bool_4              = request.args.get('bool_4')
    # weight_content      = request.args.get('weight_content')
    
    author              = request.args.get('author')
    bool_5              = request.args.get('bool_5')
    # weight_author       = request.args.get('weight_author')
    
    publish_date        = request.args.get('publish_date')
    # weight_publish_date = request.args.get('weight_publish_date')
    print(description)
    title             = "title:"  + ws.find_word_similar(title) if title != "" else ""
    description       = "description:"  + ws.find_word_similar(description) if description != "" else ""
    content           = "content:"  + ws.find_word_similar(content) if content != "" else ""
    bool_1 = "&&"
    print(topic)
    print(title)
    print(description)
    print(content)
    print(author)
    query = topic + " " + bool_1 + " " +\
            title + " " + bool_1 + " " +\
            description + " " + bool_1 + " " +\
            content + " " + bool_1 + " " +\
            "'" + author + "'" + " " + bool_1 + " " + publish_date
    
    result = solr.search(query, **{
        'rows':1,
        'hl':'true',
        'hl.method':'original',
        'hl.simple.pre':'<mark style="background-color:#ffff0070;">',
        'hl.simple.post':'</mark>',
        'hl.highlightMultiTerm':'true',
        'hl.fragsize':100,
        'defType' : 'dismax',
        'fl' : '*, score',
        # 'bq':'{!func}linear(clicked, 0.01 ,0.0 )',
        # # 'bq':'{!func}log(linear(clicked, 20 ,0.0 ))',
        'mm':1,
        'ps':3,
        'pf': 'title^1.0 description^1.0 content^2.0',
        'qf':'topic^1 title^3.0 description^1.0 content^1.0',
    })
    for i in result:
        print(i)
    return jsonify("ok")

# Xóa data
@app.route('/delete_data', methods=['GET'])
def delete_data():
    solr.delete(q='*:*')
    return jsonify("OK")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)