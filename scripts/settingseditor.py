import customtkinter as ctk
from CTkFileSelector import *
from icecream import ic
from CTkColorPicker import *
import tkinter as tk

class AttributeEditorWindow(ctk.CTkFrame):
    editable_attributes = {
                        "Spacer": None,
                        "Width": {"type": int, "value": 0,"kwarg":"width", "flags": ["px"]},
                        "Height": {"type": int, "value": 0, "kwarg":"height", "flags": ["px"]},
                        "Corner Radius": {"type": int, "value": 0,"kwarg":"corner_radius", "flags": ["px"]},
                        "Border Width": {"type": int, "value": 0,"kwarg":"border_width", "flags": ["px"]},
                        "Border Spacing": {"type": int, "value": 0,"kwarg":"border_spacing", "flags": ["px"]},
                        "Checkbox Width": {"type": int, "value": 0,"kwarg":"checkbox_width", "flags": ["px"]},
                        "Checkbox Height": {"type": int, "value": 0,"kwarg":"checkbox_height", "flags": ["px"]},
                        "Switch Width": {"type": int, "value": 0,"kwarg":"switch_width", "flags": ["px"]},
                        "Switch Height": {"type": int, "value": 0,"kwarg":"switch_height", "flags": ["px"]},
                        "Radio Width": {"type": int, "value": 0,"kwarg":"radiobutton_width", "flags": ["px"]},
                        "Radio Height": {"type": int, "value": 0,"kwarg":"radiobutton_height", "flags": ["px"]},
                        "Border Width Checked": {"type": int, "value": 0,"kwarg":"border_width_checked", "flags": ["px"]},
                        "Border Width Unchecked": {"type": int, "value": 0,"kwarg":"border_width_unchecked", "flags": ["px"]},
                        "Minimum Pixel Length": {"type": int, "value": 0,"kwarg":"minimum_pixel_length", "flags": ["px"]},
                        "Foreground Colour": {"type": int, "value": 0,"kwarg":"fg_color", "flags": ["colour"]},
                        "Hover Colour": {"type": int, "value": 0,"kwarg":"hover_color", "flags": ["colour"]},
                        "Border Colour": {"type": int, "value": 0,"kwarg":"border_color", "flags":  ["colour"]},
                        "Text Colour": {"type": int, "value": 0,"kwarg":"text_color", "flags":  ["colour"]},
                        "Text Colour Disabled": {"type": int, "value": 0,"kwarg":"text_color_disabled", "flags":  ["colour"]},
                        "Placeholder Text Colour": {"type": int, "value": 0,"kwarg":"placeholder_text_color", "flags":  ["colour"]},
                        "Button Colour": {"type": int, "value": 0,"kwarg":"button_color", "flags":  ["colour"]},
                        "Button Hover Colour": {"type": int, "value": 0,"kwarg":"button_hover_color", "flags":  ["colour"]},
                        "Scrollbar Button Colour": {"type": int, "value": 0,"kwarg":"scrollbar_button_colour", "flags":  ["colour"]},
                        "Scrollbar Button Hover Colour": {"type": int, "value": 0,"kwarg":"scrollbar_button_hover_colour", "flags":  ["colour"]},
                        "Dropdown Foreground Colour": {"type": int, "value": 0,"kwarg":"dropdown_fg_color", "flags":  ["colour"]},
                        "Dropdown Hover Colour": {"type": int, "value": 0,"kwarg":"dropdown_hover_color", "flags":  ["colour"]},
                        "Progress Colour": {"type": int, "value": 0,"kwarg":"progress_color", "flags":  ["colour"]},
                        "Dropdown Text Colour": {"type": int, "value": 0,"kwarg":"dropdown_text_color", "flags":  ["colour"]},
                        "Text": {"type": str, "kwarg":"text", "value": "","flags": []},
                        "Placeholder Text": {"type": str, "kwarg":"placeholder_text", "value": "","flags": []},
                        "Font": {"type": tuple, "value": ("Roboto", 0),"kwarg":"font", "flags": [{"dropdown": ["Roboto", "Comic Sans MS","Calibri", "Roman", "Script", "Courier", "Tekton", "Hobot Std"]}, "px"]},
                        "Dropdown Font": {"type": tuple, "value": (0,0),"kwarg":"dropdown_font", "flags": [{"dropdown": ["Roboto", "Comic Sans MS","Calibri", "Roman", "Script", "Courier", "Tekton", "Hobot Std"]}, "px"]},
                        "Callback Name": {"type": str, "value": "","kwarg":"command", "flags":  ["dontupdate"]},
                        "Image": {"type": str, "value": "","kwarg": "image_path", "flags": ["dontupdate", "image_path"]},
                        "Image Width": {"type": int, "value": 0,"kwarg":"image_width","flags":["px"]},
                        "Image Height": {"type": int, "value": 0,"kwarg":"image_height","flags":["px"]},
                        "Justify": {"type": str, "value": "", "kwarg": "justify", "flags": [{"dropdown": ["left", "center", "right"]}]},
                        "Compound": {"type": str, "value": "", "kwarg": "compound", "flags": [{"dropdown": ["top", "bottom", "left", "right"]}]},
                        "Pad X": {"type": int, "value": 0,"kwarg":"padx", "flags": ["px"]},
                        "Pad Y": {"type": int, "value": 0, "kwarg":"pady", "flags": ["px"]},
                        "From": {"type": int, "value": 0, "kwarg":"from_", "flags": []},
                        "To": {"type": int, "value": 0, "kwarg":"to", "flags": []},
                        "Number of Steps": {"type": int, "value": 0, "kwarg":"number_of_steps", "flags": []},
                        "Hover": {"type": bool, "value": True, "kwarg":"hover", "flags": []},
                        "Dynamic Resizing": {"type": bool, "value": True, "kwarg":"dynamic_resizing", "flags": []},
                        "Activate Scrollbars": {"type": bool, "value": True, "kwarg":"activate_scrollbars", "flags": []},
                        "Anchor": {"type": str, "value": "", "kwarg": "anchor", "flags": [{"dropdown": ["n", "s", "e", "w","center"]}]},
                        "Orientation": {"type": str, "value": "", "kwarg": "orientation", "flags": [{"dropdown": ["horizontal", "vertical"]}]},
                        "Mode": {"type": str, "value": "", "kwarg": "mode", "flags": [{"dropdown": ["determinate", "indeterminate"]}]},
                        "Text Wrapping": {"type": str, "value": "", "kwarg": "wrap", "flags": [{"dropdown": ["char","word", "none"]}]},
                        }

    edit_dict = {
        "Button": ["Width", "Height", "Corner Radius", "Border Width", "Spacer", "Text", "Font", "Spacer", "Callback Name", "Spacer", "Image", "Image Width", "Image Height", "Spacer", "Foreground Colour","Hover Colour", "Border Colour", "Text Colour", "Spacer"],
        "Label": ["Width", "Height", "Corner Radius", "Spacer", "Text", "Font", "Spacer", "Image", "Image Width", "Image Height", "Spacer", "Foreground Colour", "Text Colour", "Spacer", "Justify", "Compound", "Spacer","Pad X", "Pad Y", "Spacer"],
        "Check Box": ["Width", "Height", "Corner Radius", "Border Width", "Spacer", "Text", "Font", "Spacer", "Checkbox Width", "Checkbox Height", "Spacer", "Foreground Colour", "Hover Colour", "Border Colour", "Text Colour", "Spacer"],
        "Entry": ["Width", "Height", "Corner Radius", "Spacer", "Text","Placeholder Text", "Font", "Spacer", "Foreground Colour", "Text Colour", "Placeholder Text Colour", "Spacer"],
        "Combo Box": ["Width", "Height", "Corner Radius", "Border Width", "Spacer", "Hover", "Justify","Font", "Spacer", "Foreground Colour", "Border Colour","Text Colour", "Text Colour Disabled", "Button Colour", "Button Hover Colour", "Dropdown Foreground Colour", "Dropdown Hover Colour", "Dropdown Text Colour" ,"Spacer"],
        "Frame": ["Width", "Height", "Border Width", "Spacer", "Foreground Colour", "Border Colour","Spacer"],
        "Option Menu": ["Width", "Height", "Corner Radius", "Spacer", "Hover", "Dynamic Resizing", "Anchor","Font", "Spacer", "Callback Name", "Spacer", "Foreground Colour", "Border Colour","Text Colour", "Text Colour Disabled", "Button Colour", "Button Hover Colour", "Dropdown Foreground Colour", "Dropdown Hover Colour", "Dropdown Text Colour","Spacer"],
        "Progress Bar": ["Width", "Height", "Corner Radius", "Border Width", "Spacer", "Mode", "Foreground Colour", "Border Colour", "Progress Colour","Spacer"],
        "Radio": ["Width", "Height", "Corner Radius", "Spacer", "Radio Width", "Radio Height", "Border Width Checked", "Border Width Unchecked","Spacer","Text", "Font", "Spacer", "Callback Name","Spacer"],
        "Image": ["Image", "Image Width", "Image Height", "Spacer"],
        "Scroll Bar": ["Width", "Height", "Corner Radius", "Border Spacing", "Spacer", "Callback Name", "Hover", "Minimum Pixel Length", "Spacer", "Foreground Colour", "Button Colour", "Button Hover Colour", "Spacer"],
        "Slider": ["Width", "Height", "Border Width", "Spacer", "Callback Name", "From", "To", "Number of Steps", "Hover", "Spacer", "Foreground Colour", "Progress Colour", "Border Colour", "Button Colour", "Button Hover Colour","Spacer" ],
        "Switch": ["Width", "Height", "Corner Radius", "Border Width", "Spacer", "Switch Width", "Switch Height", "Callback Name", "Text","Font","Spacer", "Foreground Colour", "Border Colour", "Progress Colour", "Button Colour", "Button Hover Colour", "Hover Colour", "Text Colour","Spacer"],
        "Text Box": ["Width", "Height", "Corner Radius", "Border Width", "Border Spacing", "Spacer", "Text Wrapping","Font","Spacer", "Foreground Colour", "Border Colour", "Text Colour", "Scrollbar Button Colour", "Scrollbar Button Hover Colour","Spacer"],
    }

    def __init__(self,*args,widget_to_edit,apply_settings_cb, app_pos,**kwargs):
        super().__init__(*args, **kwargs)
        self.widget_being_edited = widget_to_edit
        self.cb_to_apply = apply_settings_cb

        self.app_position = app_pos
        self.app_geometry = (self.app_position.split("+"))
        self.app_width, self.app_height = self.app_geometry[0].split("x")
        self.editor_offset_x = int(self.app_width) + int(self.app_geometry[1])
        self.editor_offset_y = self.app_geometry[2]
        self.widget_being_edited = widget_to_edit
        self.widget_type = str(widget_to_edit.get("widget_name"))
        
        self.attributes_to_edit = self.edit_dict.get((self.widget_type))

        self.kwarg_list = {}

        self.toplevel = ctk.CTkToplevel()
        self.toplevel.attributes('-topmost', 'true')
        self.toplevel.title(f"Widget Properties Editor")
        self.toplevel.resizable(False, False)

        self.size_x = 300
        self.size_y = 50
        
        self.label_widget_type = ctk.CTkLabel(self.toplevel,width=50, text=f"Edit {self.widget_being_edited.get('widget_id')}")
        self.label_widget_type.cget("font").configure(size=20)
        self.label_widget_type.place(x=10,y=10)
        
        self.button_apply = ctk.CTkButton(self.toplevel, text='Apply Settings', height=30, width=50, corner_radius=10, command=self.update_attributes)
        self.button_apply.place(x=190, y=10)
        
        self.check_attributes(self.attributes_to_edit)

        editor_size, editor_offset_x, editor_offset_y = self.master.geometry().split("+")
        # _, editor_size_y = editor_size.split("x")
        self.toplevel.geometry(f"{self.size_x}x{self.size_y}+{int(editor_offset_x)+10}+{int(editor_offset_y)}")    # ensures the window always gets created below to the editor
    
        # self.populate_existing_fields()        
    def update_attributes(self):

        # ic(self.kwarg_list)

        for (value,kwarg) in self.kwarg_list.items():
            self.widget_being_edited["kwargs"].update({value:kwarg})

        self.cb_to_apply(self.widget_being_edited)
    
    def change_edited_widget(self, widget_to_edit):
        self.widget_being_edited = widget_to_edit
        self.widget_type = (self.widget_being_edited.get("widget_name"))
        self.attributes_to_edit = self.edit_dict.get(self.widget_type)
        # ic(self.kwarg_list)
        self.kwarg_list = {}
        self.kwarg_list = self.widget_being_edited['kwargs']
        # ic(self.kwarg_list)
        # ic(self.widget_being_edited['kwargs'])

        self.size_x = 300
        self.size_y = 50
        try:
            self.toplevel.geometry(f"300x50")
        except:
            self.toplevel = ctk.CTkToplevel()
            self.toplevel.title(f"Widget Properties Editor")
            self.toplevel.resizable(False, False)

            editor_size,editor_offset_x, editor_offset_y = self.master.geometry().split("+")
            _, editor_size_y = editor_size.split("x")

            self.toplevel.geometry(f"{self.size_x}x{self.size_y}+{int(editor_offset_x) + 200}+{int(editor_offset_y) + 200}")

        for widget in self.winfo_children():
            widget.destroy()

        self.label_widget_type = ctk.CTkLabel(self.toplevel,width=50, text=f"Edit {self.widget_being_edited.get('widget_id')}")
        self.label_widget_type.cget("font").configure(size=20)
        self.label_widget_type.place(x=10,y=10)
        
        self.button_apply = ctk.CTkButton(self.toplevel, text='Apply Settings', height=30, width=50, corner_radius=10, command=self.update_attributes)
        self.button_apply.place(x=190, y=10)
    
        self.kwarg_list = self.widget_being_edited["kwargs"]

        # ic(self.widget_being_edited['widget_id'])
    
        self.check_attributes(self.attributes_to_edit)
        self.toplevel.geometry(f"{self.size_x}x{self.size_y}")

    def check_attributes(self, attributes_to_edit):
        attributes_to_add = []
        temp_frame_height = 0
        # self.kwarg_list = {}
        # self.kwarg_list = self.widget_being_edited['kwargs']

        for attribute in attributes_to_edit:
            attribute_info = self.editable_attributes.get(attribute)
            if(attribute != "Spacer"):      # build up list of attributes to place
                attributes_to_add.append(attribute)
                if(attribute_info["type"] == tuple):
                    temp_frame_height += 50
                else:
                    temp_frame_height += 25
            else:           # clear list of attributes to place
                frame = ctk.CTkFrame(self.toplevel, width=280, height=temp_frame_height+12)
                frame.place(x=10, y=self.size_y)
                for index,additional_attribute in enumerate(attributes_to_add):
                    info = self.editable_attributes.get(additional_attribute)
                    y_val = (index*25+5)
                    flags = self.editable_attributes[additional_attribute]["flags"]
                    if(info.get('type') == int):
                        label = ctk.CTkLabel(frame, text=additional_attribute)
                        label.place(x=10, y=y_val)
                        textVar = tk.StringVar()
                        if(info["kwarg"] in self.widget_being_edited['kwargs']):    # string var cb logic
                            textVar.set(self.widget_being_edited['kwargs'][info['kwarg']])
                        textVar.trace_add(mode='write', callback=lambda name, mode, index, inf=info, tvar=textVar: self.set_value(inf['kwarg'], (tvar.get()), inf['type'], inf["flags"]))
                        entry = ctk.CTkEntry(frame, placeholder_text=f"{additional_attribute.split(' ')[-1]}", width=50, height=10, textvariable=textVar)

                        if("px" in info.get('flags')):
                            entry.place(x=205, y=y_val+3)
                            label_px = ctk.CTkLabel(frame, text="px")
                            label_px.place(x=260, y=y_val)
                        elif(("colour") in info.get('flags')):
                            entry = ctk.CTkEntry(frame, placeholder_text=f"#RRGGBB", width=50, height=10, textvariable=textVar)
                            entry.place(x=200, y=y_val+3)
                            button_ask_color = ctk.CTkButton(master=frame, text="...", width=20,height=10, command=lambda e=entry: self.set_color(e))
                            button_ask_color.place(x=255, y=y_val+3)
                        else:
                            entry = ctk.CTkEntry(frame, placeholder_text=f"{additional_attribute.lower()}", width=70, height=10)
                            entry.place(x=205, y=y_val+3)
                    elif(info.get('type') == str):
                        label = ctk.CTkLabel(frame, text=additional_attribute)
                        label.place(x=10, y=y_val)

                        textVar = tk.StringVar()
                        if(info["kwarg"] in self.widget_being_edited['kwargs']):
                            textVar.set(self.widget_being_edited['kwargs'][info['kwarg']])
                        textVar.trace_add(mode='write', callback=lambda name, mode, index, inf=info, tvar=textVar: self.set_value(inf['kwarg'], (tvar.get()), inf['type']))
                        if(any("dropdown" in flag for flag in flags)):
                            optionmenu = ctk.CTkOptionMenu(frame, width=120, height=17, values=info['flags'][0].get('dropdown'), anchor='w',dynamic_resizing=False)
                            optionmenu.configure(command= lambda value,inf=info: self.set_value(inf['kwarg'], value, inf['type']))
                            
                            optionmenu.place(x=154, y=y_val+3)
                
                        elif("image_path" in info.get('flags')):
                            entry = ctk.CTkEntry(frame, placeholder_text=f"path/to/img", width=50, height=10, textvariable=textVar)
                            entry.place(x=200, y=y_val+3)
                            if("image_path" in self.widget_being_edited):
                                textVar.set(self.widget_being_edited["image_path"])
                            button_ask_file = ctk.CTkButton(frame, text="...", width=20, height=10, command=lambda e = entry: self.pick_img(e))
                            button_ask_file.place(x=255, y=y_val+3) 

                        else:
                            entry = ctk.CTkEntry(frame, placeholder_text=f"{additional_attribute.split(' ')[-1]}", width=70, height=10, textvariable=textVar)
                            entry.place(x=205, y=y_val+3)
                    elif(info.get('type') == tuple):
                        if(info.get("kwarg") == "font"):
                            label = ctk.CTkLabel(frame, text="Font Face")
                            label.place(x=10, y=y_val)
                            
                            optionmenu = ctk.CTkOptionMenu(frame, width=120, height=17, values=info['flags'][0].get('dropdown'), anchor='w',dynamic_resizing=False)
                            optionmenu.configure(command= lambda value,inf=info: self.set_value(inf['kwarg'], value, inf['type']))
                            optionmenu.place(x=154, y=y_val+3)

                            label = ctk.CTkLabel(frame, text="Font Size")
                            label.place(x=10, y=y_val+25)

                            textVar = tk.StringVar()
                            if(info["kwarg"] in self.widget_being_edited['kwargs']):
                                textVar.set(str(abs(int(self.widget_being_edited['kwargs'][info['kwarg']][1]))))
                                optionmenu.set(self.widget_being_edited['kwargs'][info['kwarg']][0])
                            textVar.trace_add(mode='write', callback=lambda name, mode, index, inf=info, tvar=textVar: self.set_value(inf['kwarg'], (tvar.get()), inf['type']))

                            entry = ctk.CTkEntry(frame, placeholder_text="Font Size", width=70, height=10, textvariable=textVar)
                            entry.place(x=205, y=y_val+25)                            
                    elif(info.get('type') == bool):
                        label = ctk.CTkLabel(frame, text=additional_attribute)
                        label.place(x=10, y=y_val)
                        var = tk.BooleanVar()
                        if(info['kwarg'] in self.widget_being_edited['kwargs']):
                            var.set(self.widget_being_edited['kwargs'])
                        
                        switch = ctk.CTkSwitch(frame, width=30, height=10,text="", variable=var)
                        switch.place(x=240, y=y_val+3)

                        var.trace_add(mode='write', callback=lambda name,mode,index, v=var, inf=info: self.set_value(inf['kwarg'], bool(v.get()), inf['type']))

                self.size_y += temp_frame_height + 20
                temp_frame_height = 0
                attributes_to_add = []

    def pick_img(self, entry):
        currdir = os.getcwd()
        file_path = filedialog.askopenfile(initialdir=currdir)
        if(file_path is not None):
            entry.delete(0, 'end')
            entry.insert(0, file_path.name)

    def set_value(self, key_to_set, value_to_set, vartype, flag=[]):
        try:
            if(vartype == int and not "dontupdate" in flag and value_to_set):
                if('colour' in flag):           # todo, check if colour is empty, if it is then pass the default colour value of the theme
                    # if(value_to_set == ""):           
                    #     self.kwarg_list[f"{key_to_set}"] = "DELETEME"
                    self.kwarg_list[f"{key_to_set}"] = str(value_to_set)
                else:
                    self.kwarg_list[f"{key_to_set}"] = int(value_to_set)
            elif(vartype == str and not "dontupdate" in flag and value_to_set):
                if(key_to_set == "command_name"):
                    self.widget_being_edited["command_name"] = value_to_set
                else:
                    self.kwarg_list[f"{key_to_set}"] = (value_to_set)
            elif(vartype == tuple and not "dontupdate" in flag and value_to_set):
                if(key_to_set == "font" and not value_to_set.isdigit()):
                    if("font" in self.kwarg_list):
                        self.kwarg_list[f"{key_to_set}"] = (value_to_set, self.kwarg_list["font"][1])
                    else:
                        self.kwarg_list[f"{key_to_set}"] = (value_to_set, 13)
                elif(key_to_set == "font" and value_to_set.isdigit()):
                    if("font" in self.kwarg_list):
                        self.kwarg_list[f"{key_to_set}"] = (self.kwarg_list["font"][0], -int(value_to_set))
                    else:  
                        self.kwarg_list[f"{key_to_set}"] = ("roboto", -int(value_to_set))
            elif(vartype == bool and not "dontupdate" in flag):
                self.kwarg_list[f"{key_to_set}"] = bool(value_to_set) 
            self.widget_being_edited["kwargs"] = self.kwarg_list        ## THIS LINE BREAKS EVERYTHIGN FOR SOME REASOGSDJGsdjkgksn
        except ValueError:
            pass

    def get_current_widget(self):
        return self.widget_being_edited

    def set_color(self, entry_widget):
        color = AskColor()
        entry_widget.delete(0, 'end')
        entry_widget.insert(0, color.get())