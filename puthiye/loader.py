from elasticsearch import Elasticsearch

import json

es = Elasticsearch(hosts=["http://127.0.0.1:9200"])

print(f"Connected to ElasticSearch cluster `{es.info().body['cluster_name']}`")

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

with open('./scrapped.json') as f:
    data = json.load(f)

docs = data["key"]

for doc in docs:
    document = {
        "headings" : doc["headings"],
        "subheadings" : doc["subheadings"],
        "paras" : doc["paras"]
    }
    es.index(index="scififilms", document=document)
