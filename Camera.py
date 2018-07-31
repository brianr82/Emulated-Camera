import cv2

import logging
import datetime
import time

import base64


log = logging.getLogger()
log.setLevel('DEBUG')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

KEYSPACE = "sensordata"

class Camera():
    def __init__(self):

        self.camera_id = 'test_cam_1'
        self.sensorType = 'iot_camera'
        self.cassandra_cluster_ip = '10.12.7.5'



    def cleanup(self):

        import os, shutil
        folder = 'imagesout'
        for the_file in os.listdir (folder):
            file_path = os.path.join (folder, the_file)
            try:
                if os.path.isfile (file_path):
                    os.unlink (file_path)
                # elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print (e)

    def processVideoStream(self):
        vidcap = cv2.VideoCapture ('video/video.mov')
        success, image = vidcap.read ()
        count = 0
        success = True

        day_date= datetime.date.today().strftime("%Y") + datetime.date.today().strftime("%m")+ datetime.date.today().strftime("%d")

        while success:
            cv2.imwrite ("imagesout/frame%d.jpg" % count, image)  # save frame as JPEG file
            imageFileNameandPath =  ("imagesout/frame%d.jpg" % count)
            self.convertToBase64(imageFileNameandPath)
            success, image = vidcap.read ()
            print ('Read a new frame: ', success)
            #self.saveToCassandra (self.camera_id + str(count), self.sensorType,str(int(time.time())),day_date ,'blob data here')
            count += 1


    def saveToCassandra(self, camera_id, sensorType, timestamp, daydate, value):
        cluster = Cluster ([self.cassandra_cluster_ip], port=9042)
        session = cluster.connect ()


        log.info ("setting keyspace...")
        session.set_keyspace (KEYSPACE)


        query = SimpleStatement ("""INSERT INTO cameradata (camera_id, sensorType, timestamp,daydate,value) VALUES (%(key)s, %(a)s, %(b)s) """, consistency_level=ConsistencyLevel.ONE)

        prepared = session.prepare ("""INSERT INTO mytable (thekey, col1, col2) VALUES (?, ?, ?)""")

        for i in range (10):
            log.info ("inserting row %d" % i)
            session.execute (query, dict (key="key%d" % i, a='a', b='b'))
            session.execute (prepared.bind (("key%d" % i, 'b', 'b')))



        # session.execute("DROP KEYSPACE " + KEYSPACE)


    def convertToBase64(self,fileNameandPath):

        with open (fileNameandPath, "rb") as imageFile:
            str = base64.b64encode (imageFile.read ())
        print (str)


