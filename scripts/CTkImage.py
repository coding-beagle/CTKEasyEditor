import customtkinter as ctk

class CTkImageFrame(ctk.CTkLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.configure(text="")