import cv2
import numpy as np
import requests

from logger import Logger


class Simulator:
    def __init__(self, width=None, height=None, video_source=0, bg_path=None, vcam_source='/dev/video1',
                 stream_to_vam=True):
        self.logger = Logger.logger
        self.stream_to_vcam = stream_to_vam
        self.videocap = cv2.VideoCapture(video_source)
        if not width or not height:
            width, height = int(self.videocap.get(cv2.CAP_PROP_FRAME_WIDTH)), \
                            int(self.videocap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.logger.info('Create a virtualwebcam with a solution of {}x{}'.format(width, height))

        # Configure Videocapture
        self.videocap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.videocap.set(cv2.CAP_PROP_FRAME_WIDTH, width)

        # Configure background from passed bg_path
        background = cv2.imread(bg_path)
        self.background = cv2.resize(background, (width, height))

        if stream_to_vam:
            from pyfakewebcam import pyfakewebcam
            self.vcam = pyfakewebcam.FakeWebcam(vcam_source, width, height)

    def get_mask(self, frame, bodypix_url='http://localhost:9000'):
        _, data = cv2.imencode(".jpg", frame)
        r = requests.post(
            url=bodypix_url,
            data=data.tobytes(),
            headers={'Content-Type': 'application/octet-stream'})
        mask = np.frombuffer(r.content, dtype=np.uint8)
        mask = mask.reshape((frame.shape[0], frame.shape[1]))
        return mask

    def simulate(self, show_stream=False):
        self.logger.info("Create a virtual webcam.")
        while True:
            ret, frame = self.videocap.read()
            mask = self.get_mask(frame)

            # Merge original frame and its mask.
            inv_mask = 1 - mask
            merged = np.copy(frame)
            for c in range(frame.shape[2]):
                merged[:, :, c] = merged[:, :, c] * mask + self.background[:, :, c] * inv_mask

            if show_stream:
                cv2.imshow('Original', frame)
                cv2.imshow('Mask', mask * 255)
                cv2.imshow('Merged', merged)

            # Write image to virtual cam input.
            if self.stream_to_vcam:
                self.vcam.schedule_frame(merged)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        self.videocap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    simulator = Simulator(width=640, height=480, bg_path='assets/background.png')
    simulator.simulate(show_stream=True)
