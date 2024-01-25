import customtkinter as ctk

class AttributeEditorWindow(ctk.CTkFrame):
     
    attributes = {
    "Button": ["size_adjustments", "text_adjustments"],
    # "Label": ctk.CTkLabel,
    # "Text Box": ctk.CTkTextbox,
    # "Check Box": ctk.CTkCheckBox,
    # "Combo Box": ctk.CTkComboBox,
    # "Entry": ctk.CTkEntry,
    # "Frame": ctk.CTkFrame,
    # "Option Menu": ctk.CTkOptionMenu,
    # "Progress Bar": ctk.CTkProgressBar,
    # "Radio": ctk.CTkRadioButton,
    # "Scrollable Frame": ctk.CTkScrollableFrame,
    # "Scroll Bar": ctk.CTkScrollbar,
    # "Segment Button": ctk.CTkSegmentedButton,
    # "Slider": ctk.CTkSlider,
    # "Switch": ctk.CTkSwitch,
    # "Tab View": ctk.CTkTabview
    }

    def __init__(self,*args,widget_to_edit,apply_settings_cb,**kwargs):
        super().__init__(*args, **kwargs)
        self.widget_being_edited = widget_to_edit
        self.cb_to_apply = apply_settings_cb
        self.widget_type = str(widget_to_edit.get("widget_name"))
        self.attributes_to_edit = self.attributes.get(str(self.widget_type))
        self.toplevel = ctk.CTkToplevel()
        self.toplevel.attributes('-topmost', 'true')
        self.toplevel.resizable(False, False)

        self.size_x = 300
        self.size_y = 50
        
        self.label_widget_type = ctk.CTkLabel(self.toplevel,width=50, text=f"Edit {self.widget_type}")
        self.label_widget_type.cget("font").configure(size=20)
        self.label_widget_type.place(x=10,y=10)
        
        self.button_apply = ctk.CTkButton(self.toplevel, text='Apply Settings', height=30, width=50, corner_radius=10, command=self.update_attributes)
        self.button_apply.place(x=190, y=10)
        
        if("size_adjustments" in self.attributes_to_edit):
            self.current_y = self.size_y
            self.size_y += 100
            self.frame_size_adjustments = ctk.CTkFrame(self.toplevel, width=280, height = 90)
            self.frame_size_adjustments.place(x=10, y=self.current_y)

            self.label_width = ctk.CTkLabel(self.frame_size_adjustments, text="Width")
            self.label_width.place(x=10, y=5)
            self.entry_width = ctk.CTkEntry(self.frame_size_adjustments, placeholder_text="width", width=50, height=10)
            self.entry_width.place(x=205, y=8)
            self.label_width_px = ctk.CTkLabel(self.frame_size_adjustments, text="px")
            self.label_width_px.place(x=260, y=5)

            self.label_height = ctk.CTkLabel(self.frame_size_adjustments, text="Height")
            self.label_height.place(x=10, y=30)
            self.entry_height = ctk.CTkEntry(self.frame_size_adjustments, placeholder_text="height", width=50, height=10)
            self.entry_height.place(x=205, y=33)
            self.label_height_px = ctk.CTkLabel(self.frame_size_adjustments, text="px")
            self.label_height_px.place(x=260, y=30)

            self.label_corner_radius = ctk.CTkLabel(self.frame_size_adjustments, text="Corner Radius")
            self.label_corner_radius.place(x=10, y=55)
            self.entry_corner_radius = ctk.CTkEntry(self.frame_size_adjustments, placeholder_text="radius", width=50, height=10)
            self.entry_corner_radius.place(x=205, y=58)
            self.label_height_px = ctk.CTkLabel(self.frame_size_adjustments, text="px")
            self.label_height_px.place(x=260, y=55)

        if("text_adjustments" in self.attributes_to_edit):
            self.current_y = self.size_y       # these windows always get added at the bottom
            self.size_y += 100
            self.frame_text_adjustments = ctk.CTkFrame(self.toplevel, width=280, height = 90)
            self.frame_text_adjustments.place(x=10, y=self.current_y)

            self.label_text = ctk.CTkLabel(self.frame_text_adjustments, text="Text")
            self.label_text.place(x=10, y=5)
            self.entry_text = ctk.CTkEntry(self.frame_text_adjustments, placeholder_text="text", width=70, height=10)
            self.entry_text.place(x=205, y=8)

            self.label_font = ctk.CTkLabel(self.frame_text_adjustments, text="Font")
            self.label_font.place(x=10, y=30)
            self.menu_font = ctk.CTkOptionMenu(self.frame_text_adjustments, values=["Font 1", "Font 2", "Font 3"], width=70, height=10)
            self.menu_font.place(x=205, y=33)
            
        editor_size,editor_offset_x, editor_offset_y = self.master.geometry().split("+")
        _, editor_size_y = editor_size.split("x")
        self.toplevel.geometry(f"{self.size_x}x{self.size_y}+{int(editor_offset_x)}+{int(editor_offset_y) + int(editor_size_y) + 40}")    # ensures the window always gets created below to the editor
    
    def update_attributes(self):
        # Mapping of property names to their corresponding Tkinter entry widgets
        property_entries = {
            "height": {"entry": self.entry_height, "type": int},
            "width": {"entry": self.entry_width, "type": int},
            "corner_radius": {"entry": self.entry_corner_radius, "type": int},
            "text": {"entry": self.entry_text, "type": str}
            
        }


        kwargs = {}
        for prop, info in property_entries.items():
            value = info["entry"].get().strip()
            if info["type"] == int and value.isdigit():
                kwargs[prop] = int(value)
            elif info["type"] == str and value:
                kwargs[prop] = value

        # Update widget properties only if there are valid changes
        if kwargs:
            self.widget_being_edited["kwargs"] = kwargs
        else:
            print("No valid inputs to update.")

        self.cb_to_apply(self.widget_being_edited)

