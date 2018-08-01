import logging

from  datetime import *

import time
from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

KEYSPACE = "sensordata"

log = logging.getLogger()
log.setLevel('DEBUG')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

class CassandraTesting():

    def __init__(self):
        self.camera_id = 'test_cam_'
        self.sensortype = 'iot_camera'
        self.cassandra_cluster_ip = '10.12.7.5'


    def run(self):
        #day_date = date.today().strftime ("%Y") + date.today ().strftime ("%m") + date.today().strftime ("%d")


        for count in range(0,5):
            self.saveToCassandra (self.camera_id + str (count), self.sensortype, str (int (time.time ())), date.today(), 'blob data here')



    def saveToCassandra(self, camera_id, sensortype, timestamp, daydate, datavalue):
        cluster = Cluster ([self.cassandra_cluster_ip], port=9042)
        session = cluster.connect ()

        log.info ("setting keyspace...")
        session.set_keyspace (KEYSPACE)


        session.execute ("INSERT INTO cameradata (camera_id, sensortype, timestamp,daydate,value) VALUES (%s,%s,%s,%s,%s);",(camera_id, sensortype, int((timestamp),), daydate,datavalue))


        # session.execute("DROP KEYSPACE " + KEYSPACE)