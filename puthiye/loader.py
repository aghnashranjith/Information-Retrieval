from elasticsearch import Elasticsearch

import json

es = Elasticsearch(hosts=["http://127.0.0.1:9200"])

print(f"Connected to ElasticSearch cluster `{es.info().body['cluster_name']}`")
es.indices.delete(index='scififilms2', ignore=[400, 404])
es.indices.delete(index='scififilms3', ignore=[400, 404])

# with open("./Car details v3.csv", "r") as f:
#     reader = csv.reader(f)

#     for i, line in enumerate(reader):
#         document = {
#             "name": line[0],
#             "engine": line[9],
#             "year": line[1],
#             "price": line[2],
#         }
#         es.index(index="cars", document=document)

with open('./withlinks.json') as f:
    data = json.load(f)

docs = data["key"]

for doc in docs:
    document = {
        "headings" : doc["headings"],
        "subheadings" : doc["subheadings"],
        "paras" : doc["paras"],
        "link" : doc["link"]
    }
    es.index(index="scififilms2", document=document)

# index for tfidf queries
docs = data["key"]

for doc in docs:
    document = {
        "headings" : doc["headings"],
        "subheadings" : doc["subheadings"],
        "paras" : doc["paras"],
        "link" : doc["link"]
    }
    es.index(index="scififilms3", document=document)

cl = es.indices.close(index = "scififilms3")
  
sett = es.indices.put_settings(index = "scififilms3", settings={"settings": {
    "similarity": {
      "default": {
        "type": "LMDirichlet"
        }
      }
    } })
op = es.indices.open(index="scififilms3")
# resp = es.search(index="scififilms3", body={"query":payload}, size=MAX_SIZE)