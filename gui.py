import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk

rcam = cv2.VideoCapture(0)
width, height = int(rcam.get(cv2.CAP_PROP_FRAME_WIDTH)), int(rcam.get(cv2.CAP_PROP_FRAME_HEIGHT))
rcam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
rcam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

root = tk.Tk()
root.resizable(False, False)

# Video View
video_area = tk.Frame(root, bg="white")
video_area.grid(column=0, row=0, columnspan=3)
label = tk.Label(video_area)
label.grid()

# PLAY Button
btn_play = tk.Button(root, text="PLAY")
btn_play.grid(column=2, row=1)

# STOP Button
btn_stop = tk.Button(root, text="STOP")
btn_stop.grid(column=0, row=1)

# PAUSE Button
btn_pause = tk.Button(root, text="PAUSE")
btn_pause.grid(column=1, row=1)

def update():
    ret, frame = rcam.read()
    if ret:
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = PIL.Image.fromarray(cv2image)
        imgtk = PIL.ImageTk.PhotoImage(image = img)
        label.imgtk = imgtk
        label.configure(image=imgtk)
    label.after(100, update)



if __name__ == "__main__":
    update()
    root.mainloop()
    
