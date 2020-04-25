import tkinter as tk
from tkinter import filedialog
import cv2
import PIL.Image, PIL.ImageTk


class App:

    def __init__(self, webcam):
        self.rcam = webcam

        root = tk.Tk()
        root.resizable(False, False)

        self.build_ui(root)
        vframe = self.build_video_frame(root)
        self.update(vframe)
        root.mainloop()


    def build_video_frame(self, rootTk):
        video_area = tk.Frame(rootTk, bg="white")
        video_area.grid(column=0, row=0, columnspan=3)
        label = tk.Label(video_area)
        label.grid()
        return label

    def build_ui(self, rootTk):
        # FileChooser
        labelFrame = tk.LabelFrame(rootTk, text="Change your background")
        labelFrame.grid(column=0, row=2, columnspan=3, sticky="ew", pady=20, padx=10)

        btn_fc = tk.Button(labelFrame, text="Browse..", command=self.file_dialog)
        btn_fc.grid(column=1, row=1)

        # Info Labels
        infoLabelFrame = tk.LabelFrame(rootTk, text="Virtual Camera Name")
        infoLabelFrame.grid(column=0, row=3, columnspan=3, sticky="ew", pady=20, padx=10)
        # infoLabel = tk.Label(infoLabelFrame, text=self.rcam.get(cv2.))

        # Video View
        video_area = tk.Frame(rootTk, bg="white")
        video_area.grid(column=0, row=0)
        label = tk.Label(video_area)
        label.grid()

        # PLAY Button
        btn_play = tk.Button(rootTk, text="PLAY")
        btn_play.grid(column=2, row=1)

        # STOP Button
        btn_stop = tk.Button(rootTk, text="STOP")
        btn_stop.grid(column=0, row=1)

        # PAUSE Button
        btn_pause = tk.Button(rootTk, text="PAUSE")
        btn_pause.grid(column=1, row=1)
        


    def update(self, label):
        ret, frame = self.rcam.read()
        
        if ret:
            frame = cv2.flip(frame, 1)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = PIL.Image.fromarray(cv2image)
            imgtk = PIL.ImageTk.PhotoImage(image = img)
            label.imgtk = imgtk
            label.configure(image=imgtk)
        label.after(15, self.update, label)

    def file_dialog(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select Background", filetypes=[("Image", "*.jpg")])
        print(filename)

    def __exit__():
        self.rcam.release()  
