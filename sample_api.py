import cv2
import numpy as np
import requests

rcam = cv2.VideoCapture(0)
width, height = int(rcam.get(cv2.CAP_PROP_FRAME_WIDTH)), int(rcam.get(cv2.CAP_PROP_FRAME_HEIGHT))
width, height = 640, 480
rcam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
rcam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
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
    print(mask)
    return mask


while True:
    # Capture frame-by-frame
    ret, frame = rcam.read()
    cv2.imshow('Original', frame)
    mask = get_mask(frame)
    cv2.normalize(mask, 0, 255, cv2.NORM_MINMAX)
    cv2.imshow('Mask', mask * 255)
    cv2.imwrite('mask.jpg', mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
rcam.release()
cv2.destroyAllWindows()
