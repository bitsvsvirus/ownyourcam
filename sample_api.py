import cv2
import numpy as np
import requests

videocap = cv2.VideoCapture(0)
width, height = int(videocap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(videocap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# width, height = 640, 480

# Configure Videocapture
videocap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
videocap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
fgbg = cv2.createBackgroundSubtractorKNN()


def get_mask(frame, bodypix_url='http://localhost:9000'):
    _, data = cv2.imencode(".jpg", frame)
    r = requests.post(
        url=bodypix_url,
        data=data.tobytes(),
        headers={'Content-Type': 'application/octet-stream'})
    mask = np.frombuffer(r.content, dtype=np.uint8)
    mask = mask.reshape((frame.shape[0], frame.shape[1]))
    return mask


# Create a red background.
background = np.zeros((height, width, 3), dtype=np.uint8)
background[:, :, 2] = 255

while True:
    ret, frame = videocap.read()
    cv2.imshow('Original', frame)
    mask = get_mask(frame)
    cv2.imshow('Mask', mask * 255)

    # Merge original frame and its mask.
    inv_mask = 1 - mask
    for c in range(frame.shape[2]):
        frame[:, :, c] = frame[:, :, c] * mask + background[:, :, c] * inv_mask

    cv2.imshow('Merged', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
videocap.release()
cv2.destroyAllWindows()
