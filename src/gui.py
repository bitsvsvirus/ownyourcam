import tkinter as tk

root = tk.Tk()

frame = tk.Frame(bg="#008888", height=400, width=600)
frame.grid(column=0, row=0, columnspan=3)

btn_play = tk.Button(root, text="PLAY")
btn_play.grid(column=2, row=1)

btn_stop = tk.Button(root, text="STOP")
btn_stop.grid(column=0, row=1)

btn_pause = tk.Button(root, text="PAUSE")
btn_pause.grid(column=1, row=1)

root.mainloop()
