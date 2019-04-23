import cv2
from datetime import *
import time
import logging
import base64
import sys
import os, shutil
import CassandraClient
from KafkaClient import *


log = logging.getLogger()
log.setLevel('DEBUG')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)




class Camera():
    def __init__(self,camera_id,destination_cluster_ip,JPGQuality,transmitdelay):

        '''

        self.camera_id = sys.argv[1]
        self.destination_cluster_ip = sys.argv[2]
        self.JPGQuality = int(sys.argv[3])
        self.transmitdelay = float(sys.argv[4])
        start = time.time()

        '''

        self.camera_id = camera_id
        self.destination_cluster_ip = destination_cluster_ip
        self.JPGQuality = JPGQuality
        self.transmitdelay = transmitdelay
        start = time.time()

        '''uncomment this section for debugging locally'''

        '''
        self.camera_id = "0001"
        self.destination_cluster_ip = "192.168.0.3"
        self.JPGQuality = 5
        self.transmitdelay = 1.0
        start = time.time ()
        '''



        #to use cassandra as a sink
        #self.cassandraclient = CassandraClient(self.destination_cluster_ip)
        #self.cassandraclient.connectCassandra()


        #to use kafka as a sink
        self.kafkaclient = KafkaClient(self.destination_cluster_ip)
        self.kafkaclient.connectKafka()



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
            imageFileNameandPath =  ("app/frame%d.jpg" % count)
            image_base64 = self.convertToBase64(imageFileNameandPath)
            success, image = vidcap.read ()
            #print ('Read a new frame: ', success)

            timestamp = str(int(time.time()))
            frame_id = timestamp+str(count)

            #self.cassandraclient.saveToCassandra(self.camera_id, frame_id, timestamp,day_date ,image_base64)
            self.kafkaclient.saveToKafka(self.camera_id, frame_id, timestamp, day_date, image_base64)

            count += 1


        end = time.time ()

        runtime_seconds = end - start

        print ('Experiment Runtime (seconds): ' + str(int(runtime_seconds)))
        print ('Images written per (second): ' + str(count/runtime_seconds))

        self.cleanup()


    def convertToBase64(self,fileNameandPath):

        with open (fileNameandPath, "rb") as imageFile:
            str = base64.b64encode (imageFile.read ())
        return str


