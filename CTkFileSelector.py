import customtkinter as ctk
from tkinter import filedialog
import os

class CTkFileSelector(ctk.CTkFrame):
    def __init__(self, *args, label, select_button_width=10, select_button_height=25, entry_text="file/path", entry_padding, **kwargs):
        super().__init__(*args, *kwargs)
        self.configure(fg_color="transparent")
        self.entry_file_path = ctk.CTkEntry(self, placeholder_text=entry_text)
        self.entry_file_path.grid(column=1, row=0,padx=entry_padding)
        self.label_entry_name = ctk.CTkLabel(self, text=label)
        self.label_entry_name.grid(column=0, row=0, sticky='w')
        self.button_select_icon = ctk.CTkButton(self, text="...", width=select_button_width, height=select_button_height, command=self.set_path)
        self.button_select_icon.grid(column=2, row=0)

    def set_path(self):
        self.currdir = os.getcwd()
        self.path = filedialog.askopenfile(initialdir=self.currdir)
        if(self.path is not None):
            self.entry_file_path.insert(0, str(self.path.name))
    
    def get_path(self):
        return self.entry_file_path.get()