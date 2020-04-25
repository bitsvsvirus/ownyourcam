import time

import cv2
import numpy as np
import requests

rcam = cv2.VideoCapture(0)
width, height = int(rcam.get(cv2.CAP_PROP_FRAME_WIDTH)), int(rcam.get(cv2.CAP_PROP_FRAME_HEIGHT))
fgbg = cv2.createBackgroundSubtractorKNN()


def denoise(frame):
    frame = cv2.medianBlur(frame, 5)
    frame = cv2.GaussianBlur(frame, (5, 5), 0)

    return frame


def get_mask(frame, bodypix_url='http://localhost:9000'):
    _, data = cv2.imencode(".jpg", frame)
    r = requests.post(
        url=bodypix_url,
        data=data.tobytes(),
        headers={'Content-Type': 'application/octet-stream'})
    # convert raw bytes to a numpy array
    # raw data is uint8[width * height] with value 0 or 1
    mask = np.frombuffer(r.content, dtype=np.uint8)
    mask = mask.reshape((frame.shape[0], frame.shape[1]))
    return mask


while True:
    # Capture frame-by-frame
    ret, frame = rcam.read()
    # frame = fgbg.apply(frame)
    # get the foreground
    print(time.time())
    cv2.imshow('Original', frame)
    cv2.imshow('Mask', get_mask(frame))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
rcam.release()
cv2.destroyAllWindows()
