from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from datetime import *
import logging

KEYSPACE = "sensordata"


log = logging.getLogger()
log.setLevel('DEBUG')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)


class CassandraClient():
    def __init__(self, CassandraClusterIP):

        self.Cassandra_ClusterIP = CassandraClusterIP
        self.cassandrasession = None



    def connectCassandra(self):
        cluster = Cluster([self.Cassandra_ClusterIP], port=9042)
        self.cassandrasession = cluster.connect()

        log.info("setting keyspace...")
        self.cassandrasession.set_keyspace(KEYSPACE)


    def saveToCassandra(self, camera_id, frame_id, timestamp, daydate, datavalue):
        self.cassandrasession.execute(
            "INSERT INTO cameradata (camera_id, frame_id, timestamp,daydate,value) VALUES (%s,%s,%s,%s,%s);",
            (camera_id, frame_id, int((timestamp), ), daydate, datavalue))
        print('Saved frame to DB: ' + frame_id)
        time.sleep(self.transmitdelay)