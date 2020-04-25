import time
from multiprocessing import Process

import cv2

import gui
from simulator import Simulator


class OwnYourCam:
    def __init__(self, vcam):
        self.vcam = vcam
        self.run()

    def run(self):
        simulator = Simulator(width=640, height=480, bg_path='assets/background.png')
        simulator.simulate(show_stream=True)


if __name__ == "__main__":

    # Process for reading the webcam and producing the virtual cam
    cam_p = Process(target=OwnYourCam)
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
