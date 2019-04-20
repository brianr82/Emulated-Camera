
from confluent_kafka import Producer

import time
import json

class KafkaClient():
    def __init__(self, KafkaClusterIP):

        self.Kafka_ClusterIP = KafkaClusterIP
        self.ProducerClient = None

    def connectKafka(self):

        conf = {'bootstrap.servers': self.Kafka_ClusterIP}
        self.ProducerClient = Producer(**conf)


    def saveToKafka(self, camera_id, frame_id, timestamp, daydate, datavalue):
        #self.cassandrasession.execute(
        #    "INSERT INTO cameradata (camera_id, frame_id, timestamp,daydate,value) VALUES (%s,%s,%s,%s,%s);",
        #    (camera_id, frame_id, int((timestamp), ), daydate, datavalue))
        #print('Saved frame to DB: ' + frame_id)
        #time.sleep(self.transmitdelay)

        self.ProducerClient.poll(0)

        payload = {"camera_id": camera_id, "frame_id": frame_id, "timestamp": timestamp, "daydate": daydate, "datavalue": datavalue}

        # Asynchronously produce a message, the delivery report callback
        # will be triggered from poll() above, or flush() below, when the message has
        # been successfully delivered or failed permanently.

        json_payload = json.dumps(payload, indent=4, sort_keys=True, default=str)

        self.ProducerClient.produce('camera_data', json_payload)

        # Wait for any outstanding messages to be delivered and delivery report
        # callbacks to be triggered.
        self.ProducerClient.flush()



    def delivery_report(err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))