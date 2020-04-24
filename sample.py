import cv2
import pyfakewebcam

video_device = '/dev/video1'

rcam = cv2.VideoCapture(0)
width, height = int(rcam.get(cv2.CAP_PROP_FRAME_WIDTH)), int(rcam.get(cv2.CAP_PROP_FRAME_HEIGHT))
vcam = pyfakewebcam.FakeWebcam(video_device, width, height)

while True:
    ret, frame = rcam.read()

    # Convert RGB to BGR
    frame = frame[..., ::-1]

    vcam.schedule_frame(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
rcam.release()
cv2.destroyAllWindows()
