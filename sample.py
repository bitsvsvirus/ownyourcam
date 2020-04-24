import cv2
import pyfakewebcam

width, height = 1280, 720
video_device = '/dev/video1'

camera = pyfakewebcam.FakeWebcam(video_device, width, height)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

while True:
    ret, frame = cap.read()

    # Convert RGB to BGR
    frame = frame[...,::-1]

    camera.schedule_frame(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
