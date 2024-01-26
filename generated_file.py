import customtkinter as ctk
from PIL import ImageTk, Image
import tkinter as tk

## Geometry and Theme Settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")
root = ctk.CTk()
root.geometry("600x600")
root.title("")
image_Label_0 = ctk.CTkImage(dark_image=Image.open('D:/Codes/wait im goated/IMG_20211225_081900_857.jpg'), size=(300, 500))
Label_0 = ctk.CTkLabel(master=root,image=image_Label_0)
Label_0.place(x=150.0, y=46)

root.mainloop()
