from flask import Flask, request, render_template
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=["http://127.0.0.1:9200"])
print(f"Connected to ElasticSearch cluster `{es.info().body['cluster_name']}`")

app = Flask(__name__)

MAX_SIZE = 15

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search")
def search_autocomplete():
    query = request.args["q"].lower()
    # print(request.args)
    tokens = query.split(" ")

    # ranking_fn = request.form.gzet('ranker')
    # print(ranking_fn)
    if(value=='BM25'):
         ranker = 1
    else: 
        ranker = 0

    
    if ranker == 1:
        indexx = "scififilms2"
    else:
        indexx = "scififilms3"

    clauses = [
        {
            "span_multi": {
                "match": {"fuzzy": {"headings": {"value": i, "fuzziness": "AUTO"}}},
                "match": {"fuzzy": {"subheadings": {"value": i, "fuzziness": "AUTO"}}},
                "match": {"fuzzy": {"paras": {"value": i, "fuzziness": "AUTO"}}},
            }
        }
        for i in tokens
    ]

    payload = {
        "bool": {
            "must": [{"span_near": {"clauses": clauses, "slop": 0, "in_order": False}}]
        }
    }

    resp = es.search(index=indexx, query=payload, size=MAX_SIZE)
    # print(resp)
    resultlist = []
    for result in resp['hits']['hits']:
        res = []
        res.append(result['_source']['headings'])
        res.append(result['_source']['link'])
        resultlist.append(res)
    return resultlist
    # return [result['_source']['link'] for result in resp['hits']['hits']]


if __name__ == "__main__":
    app.run(debug=True)
