import customtkinter as ctk
from PIL import ImageTk, Image
import tkinter as tk

class Root(ctk.CTk):
    def __init__(self):
        super().__init__()
        ## Geometry and Theme Settings
        ctk.set_appearance_mode("dark")     # todo add these
        ctk.set_default_color_theme("dark-blue")

        self.geometry("500x400")
        self.title("")


        self.Button_0 = ctk.CTkButton(self,text="123")
        self.Button_0.place(x=180.0, y=186.0)

        self.Button_1 = ctk.CTkButton(self,text="5")
        self.Button_1.place(x=180.0, y=225)

        self.Button_2 = ctk.CTkButton(self,width=46,text="3")
        self.Button_2.place(x=227.0, y=262)

        self.Button_3 = ctk.CTkButton(self,width=46,text="3")
        self.Button_3.place(x=227.0, y=300)
root = Root()
root.mainloop()