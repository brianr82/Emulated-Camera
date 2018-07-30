import cv2
print(cv2.__version__)


def cleanup():
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


cleanup()


vidcap = cv2.VideoCapture('video/video.mov')
success,image = vidcap.read()
count = 0
success = True



while success:
  cv2.imwrite("imagesout/frame%d.jpg" % count, image)     # save frame as JPEG file
  success,image = vidcap.read()
  print ('Read a new frame: ', success)
  count += 1

