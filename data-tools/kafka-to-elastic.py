import json
from datetime import datetime
from elasticsearch import Elasticsearch
from confluent_kafka import (
    Consumer,
    KafkaError,
    OFFSET_BEGINNING,
    OFFSET_END,
    TopicPartition,
)


kafka_config = {
    "group.id": "air_quality_ws_server",
    "auto.offset.reset": "latest",
    "bootstrap.servers": "sckafka1.simcenter.utc.edu,sckafka2.simcenter.utc.edu,sckafka3.simcenter.utc.edu",
}

kafka_topics = ["MLK_PEEPLES_AIR_QUALITY"]
kafka_partition = 0


elastichost = {"host": "scmgmt2.research.utc.edu", "port": 9200}

elastic_index = "mlk_peeples_air_quality"

elastic_doc_type = "air_quality_raw"

subcribed_topics = [
    TopicPartition(topic, partition=kafka_partition, offset=OFFSET_BEGINNING)
    for topic in kafka_topics
]

c = Consumer(kafka_config)
c.assign(subcribed_topics)

es = Elasticsearch(hosts=[elastichost])
es.delete_by_query(
    index=[elastic_index], doc_type=elastic_doc_type, body={"query": {"match_all": {}}}
)

while True:
    for msg in c.consume(100, 1):
        if msg and not msg.error():
            data = json.loads(msg.value().decode())
            # arbitrary transformations can be placed here:
            if (
                data["location"] == {"lat": 35.044624, "lon": -85.305542}
                or data["location"] == "35.044624, -85.305542"
            ):
                data["location"] = "35.042328, -85.298729"
            if "timestamp" not in data:
                data["timestamp"] = int(
                    1000
                    * datetime.strptime(
                        data["DateTime"], "%Y/%m/%dT%H:%M:%Sz"
                    ).timestamp()
                )
            # index operation is commented out to prevent accidental data ingestion
            # es.index(index=elastic_index, doc_type=elastic_doc_type, body=json.dumps(data))
        elif msg.error():
            if msg.error() == KafkaError._PARTITION_EOF:
                break
            else:
                print(msg.error())
