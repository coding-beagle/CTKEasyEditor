import customtkinter as ctk
import tkinter as tk
from icecream import ic

# this class handles all of the export preferences
# it has a dict with all of the export preferences that we can retrieve
# we pass this dict as an argument to the export handler functions
class ExportPreferenceHandler(ctk.CTkFrame):
    def __init__(self, *args, pref_dict=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.export_settings = pref_dict
        self.number_of_settings = len(self.export_settings)

        self.set_cb = None

        self.toplevel = ctk.CTkToplevel()
        self.toplevel.geometry(f"300x{self.number_of_settings*30 + 60}")
        self.toplevel.attributes('-topmost', 'true')
        
        self.frame_export_settings = ctk.CTkFrame(self.toplevel, width=280, height=self.number_of_settings*30 + 10)
        self.frame_export_settings.place(x=10, y=40)

        self.button_set_preferences = ctk.CTkButton(self.toplevel, text="Set Preferences")
        self.button_set_preferences.place(x=150, y=5)

        for index, (key, value) in enumerate(self.export_settings.items()):
            label = ctk.CTkLabel(self.frame_export_settings, text=f"{key}")
            y_val = (index * 30)+5
            label.place(x=10, y=y_val)
            if(type(value) == bool):
                switch = ctk.CTkSwitch(self.frame_export_settings, text="", command=lambda k=key: self.set_value(k, bool(switch.get())))
                switch.place(x=230, y=y_val)
                if(value == True):
                    switch.select()
            if(type(value) == str):
                textVar = tk.StringVar(value=str(value))
                entry = ctk.CTkEntry(self.frame_export_settings, textvariable=textVar, width=70)
                entry.place(x=200, y=y_val)
                textVar.trace_add('write', callback=lambda name, index, mode, k=key, t=textVar: self.set_value(k, t.get()))
    
    def set_value(self, key_to_set, value_to_set):
        self.export_settings[f"{key_to_set}"] = value_to_set
    
    def set_set_preferences_cb(self, cb):
        self.button_set_preferences.configure(command=cb)

    def get_preferences_dict(self):
        return self.export_settings
                

