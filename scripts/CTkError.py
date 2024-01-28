import customtkinter as ctk

class CTkError(ctk.CTkFrame):
    def __init__(self, *args, title="Error",size_x=140, size_y=90,error_message, button_1_text, button_2_text="", **kwargs):
        super().__init__(*args)
        ## Geometry and Theme Settings

        self.top_level = ctk.CTkToplevel(self)

        self.top_level.geometry(f"{size_x}x{size_y}")
        self.top_level.title(title)
        self.top_level.resizable(False, False)

        self.Label_1 = ctk.CTkLabel(self.top_level,width=100,text=error_message,wraplength=100)
        self.Label_1.grid(row=0,column=0, padx=20,pady=10)

        if(button_1_text):
            self.Button_0 = ctk.CTkButton(self.top_level,corner_radius=20, width=100,text=button_1_text, command=lambda: self.destroy())
            self.Button_0.grid(row=1, column=0,pady=(0,20))

        if(button_2_text):
            self.Button_0 = ctk.CTkButton(self.top_level,corner_radius=20,text=button_2_text, command=lambda: self.destroy())
            self.Button_0.grid(row=1, column=2)
