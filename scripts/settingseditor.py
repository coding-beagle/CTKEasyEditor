import customtkinter as ctk
from CTkFileSelector import *
from icecream import ic

class AttributeEditorWindow(ctk.CTkFrame):
     
    attributes = {
    "Button": ["size_adjustments", "command_options","image_adjustments","text_adjustments"],
    "Label": ["size_adjustments", "image_adjustments","text_adjustments"],
    "Text Box": ["size_adjustments", "textbox"], # uncomplete
    "Check Box": ["size_adjustments", "text_adjustments", "checkbox"],
    "Combo Box": ["size_adjustments"],
    "Entry": ["size_adjustments", "placeholder_text"],
    "Frame": ["size_adjustments"],
    "Option Menu": ["size_adjustments"],
    "Progress Bar": ["size_adjustments"],
    "Radio": ["size_adjustments", "text_adjustments"],
    # "Scrollable Frame": ["size_adjustments", "scroll_dir"],
    "Scroll Bar": ["size_adjustments", "scroll_dir"],
    # "Segment Button": ctk.CTkSegmentedButton,
    "Slider": ["size_adjustments", "scroll_dir"],
    "Switch": ["size_adjustments", "text_adjustments", "switch_adjustments"],
    # "Tab View": ctk.CTkTabview
    "Image": ["image_adjustments"]
    }

    def __init__(self,*args,widget_to_edit,apply_settings_cb,**kwargs):
        super().__init__(*args, **kwargs)
        self.widget_being_edited = widget_to_edit
        self.cb_to_apply = apply_settings_cb

        self.widget_being_edited = widget_to_edit
        self.widget_type = str(widget_to_edit.get("widget_name"))
        self.attributes_to_edit = self.attributes.get(str(self.widget_type))

        self.toplevel = ctk.CTkToplevel()
        self.toplevel.attributes('-topmost', 'true')
        self.toplevel.title(f"Widget Properties Editor")
        self.toplevel.resizable(False, False)

        self.property_entries = {}

        self.size_x = 300
        self.size_y = 50
        
        self.label_widget_type = ctk.CTkLabel(self.toplevel,width=50, text=f"Edit {self.widget_being_edited.get('widget_id')}")
        self.label_widget_type.cget("font").configure(size=20)
        self.label_widget_type.place(x=10,y=10)
        
        self.button_apply = ctk.CTkButton(self.toplevel, text='Apply Settings', height=30, width=50, corner_radius=10, command=self.update_attributes)
        self.button_apply.place(x=190, y=10)
        
        self.check_attributes(self.attributes_to_edit)

        editor_size,editor_offset_x, editor_offset_y = self.master.geometry().split("+")
        _, editor_size_y = editor_size.split("x")
        self.toplevel.geometry(f"{self.size_x}x{self.size_y}+{int(editor_offset_x)}+{int(editor_offset_y) + int(editor_size_y) + 40}")    # ensures the window always gets created below to the editor
    
        self.populate_existing_fields()

    def populate_existing_fields(self):
        for key, value in self.widget_being_edited.get("kwargs").items():
            if(key == "font"):
                self.property_entries[key]["entry"].insert(0, abs(value[1]))
                continue
            self.property_entries[key]["entry"].insert(0, value)
        try:
            command = self.widget_being_edited["command"]
            self.property_entries["command"]["entry"].insert(0, str(command))
        except KeyError:
            return

    def update_attributes(self):
        kwargs = {}
        for prop, info in self.property_entries.items():
            if(prop == "image_path"):   # rework this?
                value = self.image_sel.get_path()
            elif(prop == "font"):
                value = ("roboto", info["entry"].get())
            else:
                value = info["entry"].get()
            if info["type"] == int and value.isdigit():
                kwargs[prop] = int(value)
            elif info["type"] == str and value or prop=="show":
                kwargs[prop] = str(value)
            elif info["type"] == bool:
                kwargs[prop] = bool(value)
            elif info["type"] == tuple and value[0] and value[1]:
                kwargs[prop] = (str(value[0]), -int(value[1]))
        # Update widget properties only if there are valid changes
        if "command" in kwargs:
            self.widget_being_edited["command"] = kwargs["command"]
            kwargs.pop("command")       # we don't actually want to attach the callback for the widget in our editor window
        if kwargs:
            self.widget_being_edited["kwargs"] = kwargs
        

        self.cb_to_apply(self.widget_being_edited)
    
    def change_edited_widget(self, widget_to_edit):
        self.widget_being_edited = widget_to_edit
        self.widget_type = str(widget_to_edit.get("widget_name"))
        self.attributes_to_edit = self.attributes.get(str(self.widget_type))
        
        self.size_x = 300
        self.size_y = 50
        try:
            self.toplevel.geometry(f"300x50")
            self.property_entries = {}
        except:

            self.toplevel = ctk.CTkToplevel()
            self.toplevel.attributes('-topmost', 'true')
            self.toplevel.title(f"Widget Properties Editor")
            self.toplevel.resizable(False, False)

            editor_size,editor_offset_x, editor_offset_y = self.master.geometry().split("+")
            _, editor_size_y = editor_size.split("x")

            self.toplevel.geometry(f"{self.size_x}x{self.size_y}+{int(editor_offset_x)}+{int(editor_offset_y) + int(editor_size_y) + 40}")
            self.property_entries = {}

        for widget in self.toplevel.winfo_children():
            widget.destroy()

        self.label_widget_type = ctk.CTkLabel(self.toplevel,width=50, text=f"Edit {self.widget_being_edited.get('widget_id')}")
        self.label_widget_type.cget("font").configure(size=20)
        self.label_widget_type.place(x=10,y=10)
        
        self.button_apply = ctk.CTkButton(self.toplevel, text='Apply Settings', height=30, width=50, corner_radius=10, command=self.update_attributes)
        self.button_apply.place(x=190, y=10)

        self.check_attributes(self.attributes_to_edit)

        self.toplevel.geometry(f"{self.size_x}x{self.size_y}")

        self.populate_existing_fields()
    
    def check_attributes(self, attributes_to_edit):
        if("size_adjustments" in attributes_to_edit):
            self.current_y = self.size_y
            self.size_y += 125
            self.frame_size_adjustments = ctk.CTkFrame(self.toplevel, width=280, height = 115)
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

            self.label_border_width = ctk.CTkLabel(self.frame_size_adjustments, text="Border Width")
            self.label_border_width.place(x=10, y=80)
            self.entry_border_width = ctk.CTkEntry(self.frame_size_adjustments, placeholder_text="width", width=50, height=10)
            self.entry_border_width.place(x=205, y=83)
            self.label_border_width_px = ctk.CTkLabel(self.frame_size_adjustments, text="px")
            self.label_border_width_px.place(x=260, y=80)

            self.property_entries["height"] = {"entry": self.entry_height, "type": int}
            self.property_entries["width"] = {"entry": self.entry_width, "type": int}
            self.property_entries["corner_radius"] = {"entry": self.entry_corner_radius, "type": int}
            self.property_entries["border_width"] = {"entry": self.entry_border_width, "type": int}

        if("text_adjustments" in attributes_to_edit):
            self.current_y = self.size_y       # these windows always get added at the bottom
            self.size_y += 70
            self.frame_text_adjustments = ctk.CTkFrame(self.toplevel, width=280, height = 60)
            self.frame_text_adjustments.place(x=10, y=self.current_y)

            self.label_text = ctk.CTkLabel(self.frame_text_adjustments, text="Text")
            self.label_text.place(x=10, y=5)
            self.entry_text = ctk.CTkEntry(self.frame_text_adjustments, placeholder_text="text", width=70, height=10)
            self.entry_text.place(x=205, y=8)

            self.label_font_size = ctk.CTkLabel(self.frame_text_adjustments, text="Font Size")
            self.label_font_size.place(x=10, y=30)
            self.entry_font_size = ctk.CTkEntry(self.frame_text_adjustments, placeholder_text="size", width=50, height=10)
            self.entry_font_size.place(x=205, y=33)
            self.label_font_size_px = ctk.CTkLabel(self.frame_text_adjustments, text="px")
            self.label_font_size_px.place(x=260, y=30)

            self.property_entries["text"] = {"entry": self.entry_text, "type": str}
            self.property_entries["font"] = {"entry": self.entry_font_size, "type": tuple}

        if("textbox" in attributes_to_edit):
            self.current_y = self.size_y       # these windows always get added at the bottom
            self.size_y += 95
            self.frame_textbox_adjustments = ctk.CTkFrame(self.toplevel, width=280, height = 85)
            self.frame_textbox_adjustments.place(x=10, y=self.current_y)

            self.label_border_width = ctk.CTkLabel(self.frame_textbox_adjustments, text="Border Spacing")
            self.label_border_width.place(x=10, y=5)
            self.entry_border_width = ctk.CTkEntry(self.frame_textbox_adjustments, placeholder_text="spacing", width=50, height=10)
            self.entry_border_width.place(x=205, y=8)
            self.entry_border_width_px = ctk.CTkLabel(self.frame_textbox_adjustments, text="px")
            self.entry_border_width_px.place(x=260, y=8)

            self.label_scrollbars = ctk.CTkLabel(self.frame_textbox_adjustments, text="Activate Scroll Bars")
            self.label_scrollbars.place(x=10, y=30)
            self.switch_scrollbars = ctk.CTkSwitch(self.frame_textbox_adjustments, text='')
            self.switch_scrollbars.place(x=240, y=30)
            
            self.label_wrapping = ctk.CTkLabel(self.frame_textbox_adjustments, text="Word Wrapping")
            self.label_wrapping.place(x=10, y=55)
            self.menu_wrapping = ctk.CTkOptionMenu(self.frame_textbox_adjustments, values=["char", "word", "none"], width=60, height=20)
            self.menu_wrapping.place(x=210, y=55)

            self.property_entries["border_spacing"] = {"entry": self.entry_border_width, "type": int}
            self.property_entries["activate_scrollbars"] = {"entry": self.switch_scrollbars, "type": bool}
            self.property_entries["wrap"] = {"entry": self.menu_wrapping, "type": str}
        
        if("command_options" in attributes_to_edit):
            self.current_y = self.size_y       # these windows always get added at the bottom
            self.size_y += 50
            self.frame_command = ctk.CTkFrame(self.toplevel, width=280, height = 40)
            self.frame_command.place(x=10, y=self.current_y)

            self.label_command_cb_name = ctk.CTkLabel(self.frame_command, text="Command Callback Name:")
            self.label_command_cb_name.place(x=10, y=5)
            self.entry_cb_name = ctk.CTkEntry(self.frame_command, placeholder_text="cb name", width=90, height=10)
            self.entry_cb_name.place(x=185, y=8)

            self.property_entries["command"] = {"entry": self.entry_cb_name, "type": str}

        if("image_adjustments" in attributes_to_edit):
            self.current_y = self.size_y       # these windows always get added at the bottom
            self.size_y += 100

            self.frame_image_adjustments = ctk.CTkFrame(self.toplevel, width=280, height = 90)
            self.frame_image_adjustments.place(x=10, y=self.current_y)

            self.image_sel = CTkFileSelector(self.frame_image_adjustments, entry_padding=(100,5), entry_width=100, entry_height=20, select_button_height=17, select_button_width=17, label="Image")
            self.image_sel.place(x=10, y=5)

            self.label_image_size_x = ctk.CTkLabel(self.frame_image_adjustments, text="Image Width")
            self.label_image_size_x.place(x=10, y=30)
            self.entry_image_size_x = ctk.CTkEntry(self.frame_image_adjustments, placeholder_text="width", width=50, height=10)
            self.entry_image_size_x.place(x=205, y=33)
            self.label_image_size_x_px = ctk.CTkLabel(self.frame_image_adjustments, text="px")
            self.label_image_size_x_px.place(x=260, y=30)

            self.label_image_size_y = ctk.CTkLabel(self.frame_image_adjustments, text="Image Height")
            self.label_image_size_y.place(x=10, y=55)
            self.entry_image_size_y = ctk.CTkEntry(self.frame_image_adjustments, placeholder_text="height", width=50, height=10)
            self.entry_image_size_y.place(x=205, y=58)
            self.label_image_size_y_px = ctk.CTkLabel(self.frame_image_adjustments, text="px")
            self.label_image_size_y_px.place(x=260, y=55)

            self.property_entries["image_path"] = {"entry": self.image_sel.get_entry_element, "type": str}
            self.property_entries["image_size_x"] = {"entry": self.entry_image_size_x, "type": int}
            self.property_entries["image_size_y"] = {"entry": self.entry_image_size_y, "type": int}

        if("checkbox" in attributes_to_edit):
            self.current_y = self.size_y       # these windows always get added at the bottom
            self.size_y += 70
            self.frame_checkbox_adjustments = ctk.CTkFrame(self.toplevel, width=280, height = 60)
            self.frame_checkbox_adjustments.place(x=10, y=self.current_y)

            self.label_checkbox_width = ctk.CTkLabel(self.frame_checkbox_adjustments, text="Checkbox Width")
            self.label_checkbox_width.place(x=10, y=5)
            self.entry_checkbox_width = ctk.CTkEntry(self.frame_checkbox_adjustments, placeholder_text="width", width=70, height=10)
            self.entry_checkbox_width.place(x=205, y=8)
            self.label_checkbox_width_px = ctk.CTkLabel(self.frame_size_adjustments, text="px")
            self.label_checkbox_width_px.place(x=260, y=5)

            self.label_checkbox_height = ctk.CTkLabel(self.frame_checkbox_adjustments, text="Checkbox Height")
            self.label_checkbox_height.place(x=10, y=30)
            self.entry_checkbox_height = ctk.CTkEntry(self.frame_checkbox_adjustments, placeholder_text="height", width=70, height=10)
            self.entry_checkbox_height.place(x=205, y=33)
            self.label_checkbox_height_px = ctk.CTkLabel(self.frame_size_adjustments, text="px")
            self.label_checkbox_height_px.place(x=260, y=30)

            self.property_entries["checkbox_width"] = {"entry": self.entry_checkbox_width, "type": int}
            self.property_entries["checkbox_height"] = {"entry": self.entry_checkbox_height, "type": int}

        if("switch_adjustments" in attributes_to_edit):
            self.current_y = self.size_y       # these windows always get added at the bottom
            self.size_y += 70
            self.frame_switch_adjustments = ctk.CTkFrame(self.toplevel, width=280, height = 60)
            self.frame_switch_adjustments.place(x=10, y=self.current_y)

            self.label_switch_width = ctk.CTkLabel(self.frame_switch_adjustments, text="Switch Width")
            self.label_switch_width.place(x=10, y=5)
            self.entry_switch_width = ctk.CTkEntry(self.frame_switch_adjustments, placeholder_text="width", width=70, height=10)
            self.entry_switch_width.place(x=205, y=8)
            self.label_switch_width_px = ctk.CTkLabel(self.frame_size_adjustments, text="px")
            self.label_switch_width_px.place(x=260, y=5)

            self.label_switch_height = ctk.CTkLabel(self.frame_switch_adjustments, text="Switch Height")
            self.label_switch_height.place(x=10, y=30)
            self.entry_switch_height = ctk.CTkEntry(self.frame_switch_adjustments, placeholder_text="height", width=70, height=10)
            self.entry_switch_height.place(x=205, y=33)
            self.label_switch_height = ctk.CTkLabel(self.frame_size_adjustments, text="px")
            self.label_switch_height.place(x=260, y=30)

            self.property_entries["switch_width"] = {"entry": self.entry_switch_width, "type": int}
            self.property_entries["switch_height"] = {"entry": self.entry_switch_height, "type": int}

        if("placeholder_text" in attributes_to_edit):
            self.current_y = self.size_y       # these windows always get added at the bottom
            self.size_y += 70
            self.frame_placeholder_text = ctk.CTkFrame(self.toplevel, width=280, height = 60)
            self.frame_placeholder_text.place(x=10, y=self.current_y)

            self.label_placeholder_text = ctk.CTkLabel(self.frame_placeholder_text, text="Placeholder Text")
            self.label_placeholder_text.place(x=10, y=5)
            self.entry_placeholder_text = ctk.CTkEntry(self.frame_placeholder_text, placeholder_text="text", width=70, height=10)
            self.entry_placeholder_text.place(x=205, y=8)

            self.label_hidetext = ctk.CTkLabel(self.frame_placeholder_text, text="Hide inputs (*)")
            self.label_hidetext.place(x=10, y=30)
            self.checkbox_hidetext = ctk.CTkCheckBox(self.frame_placeholder_text,text=" ", width=70, height=10, onvalue='*', offvalue='')
            self.checkbox_hidetext.place(x=250, y=33)

            self.property_entries["placeholder_text"] = {"entry": self.entry_placeholder_text, "type": str}
            self.property_entries["show"] = {"entry": self.checkbox_hidetext, "type": str}

        if("scroll_dir" in attributes_to_edit):
            self.current_y = self.size_y       # these windows always get added at the bottom
            self.size_y += 40
            self.frame_scroll_direction = ctk.CTkFrame(self.toplevel, width=280, height = 30)
            self.frame_scroll_direction.place(x=10, y=self.current_y)

            self.label_scroll_dir = ctk.CTkLabel(self.frame_scroll_direction, text="Scroll Direction")
            self.label_scroll_dir.place(x=10, y=5)
            self.menu_scroll_dir = ctk.CTkOptionMenu(self.frame_scroll_direction, values=["vertical", "horizontal"], width=80, height=20)
            self.menu_scroll_dir.place(x=190, y=5)
            
            self.property_entries["orientation"] = {"entry": self.menu_scroll_dir, "type": str}      # for some reason this doesn't change on demand, only on duplicating widget

    def get_current_widget(self):
        return self.widget_being_edited


