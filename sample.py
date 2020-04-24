# see red_blue.py in the examples dir
import time

import numpy as np
import pyfakewebcam

width, height = 640, 480

blue = np.zeros((height, width, 3), dtype=np.uint8)
blue[:, :, 2] = 255

red = np.zeros((height, width, 3), dtype=np.uint8)
red[:, :, 0] = 255

video_device = '/dev/video1'
camera = pyfakewebcam.FakeWebcam(video_device, width, height)

while True:
    camera.schedule_frame(red)
    time.sleep(1 / 30.0)

    camera.schedule_frame(blue)
    time.sleep(1 / 30.0)
