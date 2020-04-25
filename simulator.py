import cv2
import numpy as np
import requests

from logger import Logger


class Simulator:
    def __init__(self, width=None, height=None, video_source=0, bg_path=None):
        self.logger = Logger.logger
        self.videocap = cv2.VideoCapture(video_source)
        if not width or not height:
            width, height = int(self.videocap.get(cv2.CAP_PROP_FRAME_WIDTH)), \
                            int(self.videocap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # width, height = 640, 480
        self.logger.info('Create a virtualwebcam with a solution of {}x{}'.format(width, height))

        # Configure Videocapture
        self.videocap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.videocap.set(cv2.CAP_PROP_FRAME_WIDTH, width)

        # Create a red background.
        background = cv2.imread(bg_path)
        self.background = cv2.resize(background, (width, height))

    def get_mask(self, frame, bodypix_url='http://localhost:9000'):
        _, data = cv2.imencode(".jpg", frame)
        r = requests.post(
            url=bodypix_url,
            data=data.tobytes(),
            headers={'Content-Type': 'application/octet-stream'})
        mask = np.frombuffer(r.content, dtype=np.uint8)
        mask = mask.reshape((frame.shape[0], frame.shape[1]))
        return mask

    def simulate(self):
        self.logger.info("Create a virtual webcam.")
        while True:
            ret, frame = self.videocap.read()
            cv2.imshow('Original', frame)
            mask = self.get_mask(frame)
            cv2.imshow('Mask', mask * 255)

            # Merge original frame and its mask.
            inv_mask = 1 - mask
            for c in range(frame.shape[2]):
                frame[:, :, c] = frame[:, :, c] * mask + self.background[:, :, c] * inv_mask

            cv2.imshow('Merged', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        self.videocap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    simulator = Simulator(width=640, height=480, bg_path='assets/background.png')
    simulator.simulate()
