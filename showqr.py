import tkinter as tk
import subprocess

root = tk.Tk()
root.title("Scan to Send File")
root.configure(bg="black")
root.geometry("500x550")

subprocess.run(["qrencode", "-o", "/home/joe/qr.png", "-s", "10", "http://10.42.0.1:8080"])

canvas = tk.Canvas(root, width=400, height=400, bg="black", highlightthickness=0)
canvas.pack(pady=20)

img = tk.PhotoImage(file="/home/joe/qr.png")
canvas.create_image(200, 200, image=img)

label = tk.Label(root, text="Connect to FileDrop WiFi then scan", fg="white", bg="black", font=("Arial", 13))
label.pack()

root.mainloop()
