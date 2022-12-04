from datetime import datetime
from flask import Flask, jsonify, request
from elasticsearch import Elasticsearch

es = Elasticsearch()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    results = es.get(index='scifi', doc_type='headings', id='my-new-slug')
    return jsonify(results['_source'])


@app.route('/insert_data', methods=['POST'])
# def insert_data():
#     heading = request.form['heading']
#     subheading = request.form['title']
#     para = request.form['content']

#     body = {
#         'slug': slug,
#         'title': title,
#         'content': content,
#         'timestamp': datetime.now()
#     }

#     result = es.index(index='contents', doc_type='title', id=slug, body=body)

#     return jsonify(result)

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']

    body = {
        "query": {
            "multi_match": {
                "query": keyword,
                "fields": ["headings", "subheadings"]
            }
        }
    }

    res = es.search(index="scifi", doc_type="headings", body=body)

    return jsonify(res['hits']['hits'])

app.run(port=5000, debug=True)