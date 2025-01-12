import picamera
from time import sleep
camera = picamera.PiCamera()
camera.capture('./image.jpg') #사진촬영
#camera.resolution = (1920,1080)
#camera.resolution = (1280,720)
camera.resolution = (800,600)
#camera.resolution = (640,480)

# window 에 preview
camera.start_preview()
camera.preview.fullscreen = False
camera.preview.window = (0,0,640,480)

# 상하반전
# camera.vflip = False
camera.vflip = True
camera.hflip = False

camera.brightness = 60
camera.start_recording('./video.h264') #동영상촬영
sleep(1) # 5 second
camera.stop_recording()
camera.close()

#except KeyboardInterrupt:
#    camera.stop_recording()
#    camera.close()
#    break


