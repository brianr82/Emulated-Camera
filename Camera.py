import cv2
from datetime import *
import time
import logging
import base64
import sys
import os, shutil


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

        self.camera_id = sys.argv[1]
        self.cassandra_cluster_ip = sys.argv[2]
        self.JPGQuality = int(sys.argv[3])
        self.transmitdelay = float(sys.argv[4])
        self.cassandrasession = None



        self.connectCassandra()
        start = time.time ()

    def cleanup(self):


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
        vidcap = cv2.VideoCapture ('black.mp4')
        success, image = vidcap.read ()
        count = 0
        success = True

        day_date= date.today()

        start = time.time ()

        while success:
            cv2.imwrite ("imagesout/frame%d.jpg" % count, image,[int(cv2.IMWRITE_JPEG_QUALITY), self.JPGQuality])  # save frame as JPEG file
            imageFileNameandPath =  ("imagesout/frame%d.jpg" % count)
            image_base64 = self.convertToBase64(imageFileNameandPath)
            success, image = vidcap.read ()
            #print ('Read a new frame: ', success)

            timestamp = str(int(time.time()))
            frame_id = timestamp+str(count)

            self.saveToCassandra (self.camera_id, frame_id, timestamp,day_date ,image_base64)
            count += 1


        end = time.time ()

        runtime_seconds = end - start

        print ('Experiment Runtime (seconds): ' + str(int(runtime_seconds)))
        print ('Images written per (second): ' + str(count/runtime_seconds))

    def connectCassandra(self):
        cluster = Cluster ([self.cassandra_cluster_ip], port=9042)
        self.cassandrasession = cluster.connect ()

        log.info ("setting keyspace...")
        self.cassandrasession.set_keyspace (KEYSPACE)



    def saveToCassandra(self, camera_id, frame_id, timestamp, daydate, datavalue):

        self.cassandrasession.execute ("INSERT INTO cameradata (camera_id, frame_id, timestamp,daydate,value) VALUES (%s,%s,%s,%s,%s);",(camera_id, frame_id, int((timestamp),), daydate,datavalue))
        print('Saved frame to DB: ' + frame_id)
        time.sleep(self.transmitdelay)

    def convertToBase64(self,fileNameandPath):

        with open (fileNameandPath, "rb") as imageFile:
            str = base64.b64encode (imageFile.read ())
        return str


