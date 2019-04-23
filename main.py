from Camera import *

camera_id = sys.argv[1]
destination_cluster_ip = sys.argv[2]
JPGQuality = int(sys.argv[3])
transmitdelay = float(sys.argv[4])


c1 = Camera(camera_id,destination_cluster_ip,JPGQuality,transmitdelay)
c1.cleanup()
while True:
    c1.processVideoStream()


