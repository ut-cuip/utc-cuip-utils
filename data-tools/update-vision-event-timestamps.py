from elasticsearch import Elasticsearch



elastichost = {"host": "scmgmt2.research.utc.edu", "port": 9200}
elastic_index = "cuip_vision_events"
es = Elasticsearch(hosts=[elastichost])
results = es.search(
    index=elastic_index, body={"query": {"match_all": {}}}, scroll="1m", size=1
)
scroll_id = results["_scroll_id"]
with open("scroll_ids.log", "a") as f:
    f.write(scroll_id + "\n")
documents = results["hits"]["hits"]
while True:
    for document in documents:
        # es.update(
        #     id=document["_id"],
        #     index=document["_index"],
        #     doc_type=document["_type"],
        #     body={
        #         "doc": {
        #             "timestamp": document["_source"]["timestamp"] - (3600 * 4)
        #         }
        #     },
        #     _source=True,
        # )
        print(document["_source"]["timestamp"])
    documents = es.scroll(scroll_id=scroll_id, scroll="100m")["hits"]["hits"]
    if len(documents) == 0:
        break

