import tkinter as tk
from PIL import ImageTk, Image
import envPi

root = tk.Tk()

image = ImageTk.PhotoImage(file="sunny.jpg")

background = tk.Label(root, image=image)
background.place(x=0, y=0, relwidth=1, relheight=1)

temperature = tk.StringVar()
temperature.set(envPi.just_right_temp + " °C")

humidity = tk.StringVar()
humidity.set("70" + " %")

temperatureLabel = tk.Label(root, fg="white", background="#00dbde", textvariable=temperature,
                            font=("Helvetica", 40, "bold"))
temperatureLabel.place(x=580, y=100)

humidityLabel = tk.Label(root, fg="white", background="#00dbde", textvariable=humidity,
                         font=("Helvetica", 40, "bold"))
humidityLabel.place(x=580, y=200)

root.attributes("-fullscreen", True)
root.bind("<1>", exit)


def exit():
    root.quit()


root.mainloop()
