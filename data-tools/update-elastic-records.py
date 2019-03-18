from elasticsearch import Elasticsearch


sensors = [
    {
        "topic": "MLK_PEEPLES_AIR_QUALITY",
        "mac": "84:f3:eb:91:44:38",
        "nicename": "mlk-peeples",
    },
    {
        "topic": "MLK_CENTRAL_AIR_QUALITY",
        "mac": "84:f3:eb:44:d8:24",
        "nicename": "mlk-central",
    },
    {
        "topic": "MLK_DOUGLAS_AIR_QUALITY",
        "mac": "84:f3:eb:91:44:60",
        "nicename": "mlk-douglas",
    },
    {
        "topic": "MLK_MAGNOLIA_AIR_QUALITY",
        "mac": "84:f3:eb:45:1a:53",
        "nicename": "mlk-magnolia",
    },
    {
        "topic": "MLK_GEORGIA_AIR_QUALITY",
        "mac": "84:f3:eb:45:1a:66",
        "nicename": "mlk-georgia",
    },
    {
        "topic": "MLK_LINDSAY_AIR_QUALITY",
        "mac": "84:f3:eb:45:31:54",
        "nicename": "mlk-lindsay",
    },
    {
        "topic": "MLK_HOUSTON_AIR_QUALITY",
        "mac": "84:f3:eb:45:23:4c",
        "nicename": "mlk-houston",
    },
]

mac_nicename_map = {item["mac"]: item["nicename"] for item in sensors}

elastichost = {"host": "scmgmt2.research.utc.edu", "port": 9200}
elastic_index = "mlk_lindsay_air_quality"
es = Elasticsearch(hosts=[elastichost])
results = es.search(
    index=elastic_index, body={"query": {"match_all": {}}}, scroll="1m", size=1000
)
scroll_id = results["_scroll_id"]
documents = results["hits"]["hits"]
while True:
    for document in documents:
        if not "nicename" in document["_source"]:
            es.update(
                id=document["_id"],
                index=document["_index"],
                doc_type=document["_type"],
                body={
                    "doc": {
                        "nicename": mac_nicename_map[document["_source"]["SensorId"]]
                    }
                },
                _source=True,
            )
    documents = es.scroll(scroll_id=scroll_id, scroll="1m")["hits"]["hits"]
    if len(documents) == 0:
        break

