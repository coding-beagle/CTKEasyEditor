import customtkinter as ctk
from CTkFileSelector import *

class AttributeEditorWindow(ctk.CTkFrame):
     
    attributes = {
    "Button": ["size_adjustments", "text_adjustments"],
    "Label": ["size_adjustments", "text_adjustments"],
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
        self.toplevel.title(f"Widget Properties Editor")
        self.toplevel.resizable(False, False)

        self.size_x = 300
        self.size_y = 50
        
        self.label_widget_type = ctk.CTkLabel(self.toplevel,width=50, text=f"Edit {self.widget_being_edited.get('widget_id')}")
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
            self.size_y += 150
            self.frame_text_adjustments = ctk.CTkFrame(self.toplevel, width=280, height = 140)
            self.frame_text_adjustments.place(x=10, y=self.current_y)

            self.label_text = ctk.CTkLabel(self.frame_text_adjustments, text="Text")
            self.label_text.place(x=10, y=5)
            self.entry_text = ctk.CTkEntry(self.frame_text_adjustments, placeholder_text="text", width=70, height=10)
            self.entry_text.place(x=205, y=8)

            self.label_font_size = ctk.CTkLabel(self.frame_text_adjustments, text="Font Size")
            self.label_font_size.place(x=10, y=30)
            self.entry_font_size = ctk.CTkEntry(self.frame_text_adjustments, placeholder_text="font size", width=70, height=10)
            self.entry_font_size.place(x=205, y=33)

            self.image_sel = CTkFileSelector(self.frame_text_adjustments, entry_padding=(100,5), entry_width=100, entry_height=20, select_button_height=17, select_button_width=17, label="Image")
            self.image_sel.place(x=10, y=55)

            self.label_image_size_x = ctk.CTkLabel(self.frame_text_adjustments, text="Image Width")
            self.label_image_size_x.place(x=10, y=80)
            self.entry_image_size_x = ctk.CTkEntry(self.frame_text_adjustments, placeholder_text="width", width=70, height=10)
            self.entry_image_size_x.place(x=205, y=83)
            self.label_image_size_x_px = ctk.CTkLabel(self.frame_size_adjustments, text="px")
            self.label_image_size_x_px.place(x=260, y=80)

            self.label_image_size_y = ctk.CTkLabel(self.frame_text_adjustments, text="Image Height")
            self.label_image_size_y.place(x=10, y=105)
            self.entry_image_size_y = ctk.CTkEntry(self.frame_text_adjustments, placeholder_text="height", width=70, height=10)
            self.entry_image_size_y.place(x=205, y=108)
            self.label_image_size_y = ctk.CTkLabel(self.frame_size_adjustments, text="px")
            self.label_image_size_y.place(x=260, y=105)
            
        editor_size,editor_offset_x, editor_offset_y = self.master.geometry().split("+")
        _, editor_size_y = editor_size.split("x")
        self.toplevel.geometry(f"{self.size_x}x{self.size_y}+{int(editor_offset_x)}+{int(editor_offset_y) + int(editor_size_y) + 40}")    # ensures the window always gets created below to the editor
    
    def update_attributes(self):
        # Mapping of property names to their corresponding Tkinter entry widgets
        property_entries = {
            "height": {"entry": self.entry_height, "type": int},
            "width": {"entry": self.entry_width, "type": int},
            "corner_radius": {"entry": self.entry_corner_radius, "type": int},
            "text": {"entry": self.entry_text, "type": str},
            "image_path": {"entry": self.image_sel.get_path(), "type": str}, # todo definitely rework
            "image_size_x": {"entry": self.entry_image_size_x, "type": int},
            "image_size_y": {"entry": self.entry_image_size_y, "type": int}
        }


        kwargs = {}
        for prop, info in property_entries.items():
            if(prop == "image_path"):   # rework this?
                value = self.image_sel.get_path()
            else:
                value = info["entry"].get().strip()
            if info["type"] == int and value.isdigit():
                kwargs[prop] = int(value)
            elif info["type"] == str and value:
                kwargs[prop] = str(value)

        # Update widget properties only if there are valid changes
        if kwargs:
            self.widget_being_edited["kwargs"] = kwargs
        else:
            print("No valid inputs to update.")

        self.cb_to_apply(self.widget_being_edited)

