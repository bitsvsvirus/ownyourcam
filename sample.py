import cv2
import pyfakewebcam
from multiprocessing import Process
import time
import gui

# video_device = '/dev/video1'

# rcam = cv2.VideoCapture(0)
# width, height = int(rcam.get(cv2.CAP_PROP_FRAME_WIDTH)), int(rcam.get(cv2.CAP_PROP_FRAME_HEIGHT))
# vcam = pyfakewebcam.FakeWebcam(video_device, width, height)



class Sample:

    def __init__(self, rcam, vcam):
        self.rcam = rcam
        self.vcam = vcam
        self.run()


    def run(self):
        while True:
            ret, frame = self.rcam.read()

            # Convert RGB to BGR
            frame = frame[..., ::-1]

            self.vcam.schedule_frame(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        self.rcam.release()

    def stop(self):
        self.rcam.release()



if __name__ == "__main__":

    # set the devices
    video_device = '/dev/video1'
    rcam = cv2.VideoCapture(0)
    width, height = int(rcam.get(cv2.CAP_PROP_FRAME_WIDTH)), int(rcam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    vcam = pyfakewebcam.FakeWebcam(video_device, width, height)

    # Process for reading the webcam and producing the virtual cam
    cam_p = Process(target=Sample, args=[rcam, vcam])
    cam_p.start()

    time.sleep(1)

    # Process for projecting the virtual cam to gui
    webcam = cv2.VideoCapture(1)
    gui_p = Process(target=gui.App, args=[webcam])
    gui_p.start()

    # If the Gui gets closed terminate the cam process
    while True:
        if not gui_p.is_alive():
            cam_p.terminate()
            break