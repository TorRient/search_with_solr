from word_similar import Word_Similar
import pysolr
import json
import os
from flask import Flask, jsonify, request, render_template
from werkzeug.utils import secure_filename
from pyvi import ViTokenizer

from solrq import Q

config = {
    'host': 'http://localhost',
    'port': '8983',
    'core_name': 'bkcv',
    'timeout': 10
}

# Setup a Solr instance. The timeout is optional.
solr = pysolr.Solr(config['host']+':'+config['port']+'/solr/' +
                   config['core_name'], always_commit=True, timeout=config['timeout'])

static_folder = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), 'static/')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'uploads/')

ws = Word_Similar()

# Add data
@app.route('/api/add_data', methods=['GET'])
def add_data(path='./data'):
    list_json = os.listdir(path)
    for file_name in list_json:
        paths = os.path.join(path, file_name)
        with open(paths) as json_file:
            data = json.load(json_file)
            data = list(data)
            for field in data:
                field["content"] = ViTokenizer.tokenize(field["content"]) if field['content'] else 'nothing'
                field["title"] = ViTokenizer.tokenize(field["title"]) if field['title'] else 'nothing'
                field["description"] = ViTokenizer.tokenize(field["description"]) if field['description'] else 'nothing'
                field["topic"] = ViTokenizer.tokenize(field["topic"]) if field['topic'] else 'nothing'
                field["author"] = field["author"].strip().replace(' ', '_') if (field['author'] and field['author'].strip()) else 'unknown'
                field['publish_date'] = field['publish_date'] if field['publish_date'] else 'unknown'
            
            solr.add(data)
    return jsonify("OK")

# Thêm data bằng file
@app.route('/add_data_file', methods=['GET', 'POST'])
def add_data_file():
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
    else:
        return jsonify('NOT FILE')

    with open(file_path) as json_file:
        data = json.load(json_file)
        data = list(data)
        for field in data:
            field["content"] = ViTokenizer.tokenize(field["content"])
            field["author"] = field["author"].strip().replace(' ', '_')
            field["title"] = ViTokenizer.tokenize(field["title"])
            field["description"] = ViTokenizer.tokenize(field["description"])
            field["topic"] = ViTokenizer.tokenize(field["topic"])
        solr.add(data)

    return jsonify("OK")


@app.route('/api/fulltext', methods=['POST'])
def fulltext():
    rows = request.json.get('rows')
    if rows == 'unlimited':
        rows = 34000

    full_text = request.json.get('full_text')

    weight_topic        = request.json.get('weight_topic')
    weight_title        = request.json.get('weight_title')
    weight_description  = request.json.get('weight_description')
    weight_content      = request.json.get('weight_content')
    weight_author      = request.json.get('weight_author')
    weight_publish_date = request.json.get('weight_publish_date')

    # print(weight_author)
    #define weight if it is unavaiable
    weight_topic        = weight_topic if weight_topic else 1
    weight_title        = weight_title if weight_title else 1
    weight_description  = weight_description if weight_description else 1
    weight_content      = weight_content if weight_content else 1
    weight_author      = weight_author if weight_author else 1
    weight_publish_date = weight_publish_date if weight_publish_date else 1
    
    full_text = full_text if full_text else ''

    full_text = full_text.replace('&&', 'AND')
    full_text = full_text.replace('&', 'AND')
    full_text =full_text.replace('and', 'AND')
    full_text =full_text.replace('or', 'OR')
    full_text = full_text.replace('||', 'OR')
    full_text =full_text.replace('|', 'OR')

    full_text_token = ''
    c_p = 0
    full_text_split = full_text.split()
    # print(full_text_split)
    for i,v in enumerate(full_text_split):
        if v == 'AND' or v == 'OR':
            tmp = ' '
            for text in full_text.split()[c_p:i]:
                tmp = tmp + text + ' '
            c_p = i + 1
            tmp = tmp.replace(' OR ', ' ')
            tmp = tmp.replace(' AND ', ' ')
            tmp = ViTokenizer.tokenize(tmp)
            full_text_token = full_text_token + tmp + ' '+  v + ' '

        if i+1 == len(full_text_split):
            tmp = ' '
            for text in full_text.split()[c_p:i+1]:
                tmp += text + ' '
            tmp = ViTokenizer.tokenize(tmp)
            full_text_token = full_text_token + tmp
    
    for i in range(len(full_text_token)):
        full_text_token = full_text_token.replace('  ', ' ')
    full_text_token = full_text_token.strip()
    print(full_text_token)

    result = solr.search(full_text_token, **{
        'rows': rows,
        'hl': 'true',
        'hl.method': 'original',
        'hl.simple.pre': '<mark style="background-color:#ffff0070;">',
        'hl.simple.post': '</mark>',
        'hl.highlightMultiTerm': 'true',
        'hl.fragsize': 100,
        'defType': 'edismax',
        'fl': '*, score',
        # 'bq':'{!func}linear(clicked, 0.01 ,0.0 )',
        'mm': 1,
        'ps': 3,
        'pf': 'topic^{} title^{} content^{} author^{} description^{} publish_date^{}' \
                .format(weight_topic, weight_title, weight_content, weight_author, weight_description, weight_publish_date),
        'qf': 'topic^{} title^{} content^{} author^{} description^{} publish_date^{}'\
                .format(weight_topic, weight_title, weight_content, weight_author, weight_description, weight_publish_date),
    })
    highlight = []
    for i in result.highlighting.values():
        highlight.append(i)
   
    return jsonify(results=list(result), hightlight=highlight)


@app.route('/api/field', methods=['POST'])
def field():
    rows = int(request.json.get('rows'))

    word_similar = request.json.get('word_similar')

    topic = request.json.get('topic')
    title = request.json.get('title')
    description = request.json.get('description')
    content = request.json.get('content')
    author = request.json.get('author')
    publish_date = request.json.get('publish_date')

    # tokenizer and word similar
    topic = ViTokenizer.tokenize(topic.strip()) if topic else ''
    author = author.strip().replace(' ', '_') if (author and author.strip()) else ''
    publish_date = publish_date.strip() if publish_date else ''

    if word_similar == True:
        title = ws.find_word_similar(title.strip()) if title  else ""
        description = ws.find_word_similar(description.strip()) if description  else ""
        content = ws.find_word_similar(content.strip()) if content  else ""
    else:
        title = ViTokenizer.tokenize(title.strip()) if title  else ''
        description = ViTokenizer.tokenize(description.strip()) if description  else ''
        content = ViTokenizer.tokenize(content.strip()) if content else ''

    # convert to solrQ
    if topic == '':
        topic_q = Q(topic="*")
    else:
        topic_q = Q(topic=topic)

    if title == '':
        title_q = Q(title="*")
    else:
        title_q = Q(title=title)

    if description == '':
        description_q = Q(description="*")
    else:
        description_q = Q(description=description)

    if content == '':
        content_q = Q(content="*")
    else:
        content_q = Q(content=content)

    if author == '':
        author_q = Q(author="*")
    else:
        author_q = Q(author=author)

    if publish_date == '':
        publish_date_q = Q(publish_date="*")
    else:
        publish_date_q = Q(publish_date=publish_date)


    query = topic_q & title_q & author_q & description_q & content_q & publish_date_q

    query_q = str(query).replace('\\', '').replace('(', '').replace(')', '')
    print(query_q)
    result = solr.search(query_q, **{
        'rows': rows,
        'hl': 'true',
        'hl.method': 'original',
        'hl.simple.pre': '<mark style="background-color:#ffff0070;">',
        'hl.simple.post': '</mark>',
        'hl.highlightMultiTerm': 'true',
        'hl.fragsize': 100,
        'defType': 'edismax',
        'fl': '*, score',
        # 'bq': '{!func}linear(clicked, 0.01 ,0.0 )',
        'mm': 1,
        'ps': 3,
        'pf': 'topic^1 title^1 content^1 author^1 description^1 publish_date^1',
        'qf': 'topic^1 title^1 content^1 author^1 description^1 publish_date^1',
    })
    highlight = []
    for i in result.highlighting.values():
        highlight.append(i)
    
    # for i in highlight:
    #     print(i)
  
    return jsonify(results=list(result), hightlight=highlight)


# Xóa data


@app.route('/api/delete_data', methods=['GET'])
def delete_data():
    solr.delete(q='*:*')
    return jsonify("OK")


@app.route('/api/result_search/clicked', methods=['POST'])
def clicked_id():
    id = request.json.get('id')
    doc = {'id': id, 'clicked': 1}
    solr.add([doc], fieldUpdates={'clicked': 'inc'})
    return 'Ok'



if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
