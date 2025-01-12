# contiunse capture and recording 
import picamera
import time

camera = picamera.PiCamera()
# Default 1280,720
#camera.resolution = (1920,1080)
camera.resolution = (800,600)
#camera.resolution = (640,480)

# 상하반전
camera.vflip = False
camera.hflip = False

camera.brightness = 60

# window 에 preview
#camera.start_preview()
#camera.preview.fullscreen = False
#camera.preview.window = (0,0,640,480)

unique_filename = time.strftime("%Y%m%d-%H%M%S")

camera.start_recording(str(unique_filename)+'.h264') #동영상촬영

#for i in range(8640):
#    camera.capture(str(unique_filename)+'_tp'+str(i)+'.jpg')
#    time.sleep(5)
time.sleep(1)

#debug
#for i in range(1):
#    camera.capture(str(unique_filename)+'_tp'+str(i)+'.jpg')
#    time.sleep(1)

camera.stop_recording()
camera.close()

