import picamera
import time

camera = picamera.PiCamera()

# 상하반전
camera.vflip = False
camera.hflip = False

camera.brightness = 60

# window 에 preview
camera.start_preview()
camera.preview.fullscreen = False
camera.preview.window = (0,0,640,480)

unique_filename = time.strftime("%Y%m%d-%H%M%S")

camera.capture(str(unique_filename)+'_pic.jpg') #사진촬영

for i in range(5):
    camera.capture(str(unique_filename)+'_tp'+str(i)+'.jpg')
    time.sleep(3)


camera.start_recording(str(unique_filename)+'.h264') #동영상촬영
time.sleep(10)

camera.stop_recording()
camera.close()
