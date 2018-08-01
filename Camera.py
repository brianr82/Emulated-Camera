import cv2
from datetime import *
import time
import logging
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
        self.cassandra_cluster_ip = '10.12.7.5'
        self.cassandrasession = None

        self.connectCassandra()



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

        day_date= date.today()

        while success:
            cv2.imwrite ("imagesout/frame%d.jpg" % count, image)  # save frame as JPEG file
            imageFileNameandPath =  ("imagesout/frame%d.jpg" % count)
            image_base64 = self.convertToBase64(imageFileNameandPath)
            success, image = vidcap.read ()
            print ('Read a new frame: ', success)

            timestamp = str(int(time.time()))
            frame_id = timestamp+str(count)

            self.saveToCassandra (self.camera_id, frame_id, timestamp,day_date ,image_base64)
            count += 1


    def connectCassandra(self):
        cluster = Cluster ([self.cassandra_cluster_ip], port=9042)
        self.cassandrasession = cluster.connect ()

        log.info ("setting keyspace...")
        self.cassandrasession.set_keyspace (KEYSPACE)



    def saveToCassandra(self, camera_id, frame_id, timestamp, daydate, datavalue):

        self.cassandrasession.execute ("INSERT INTO cameradata (camera_id, frame_id, timestamp,daydate,value) VALUES (%s,%s,%s,%s,%s);",(camera_id, frame_id, int((timestamp),), daydate,datavalue))
        print('Saved frame' + frame_id)

    def convertToBase64(self,fileNameandPath):

        with open (fileNameandPath, "rb") as imageFile:
            str = base64.b64encode (imageFile.read ())
        return str


