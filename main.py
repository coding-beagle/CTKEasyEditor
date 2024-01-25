import os
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk
import customtkinter as ctk
from CTkMenuBar import *
from icecream import ic
import keyboard
from CTkTree import *
from ActiveWidgetHandler import *

widget_types = {
    "Add Widgets Here": None,
    "Button": ctk.CTkButton,
    "Label": ctk.CTkLabel,
    "Text Box": ctk.CTkTextbox,
    "Check Box": ctk.CTkCheckBox,
    "Combo Box": ctk.CTkComboBox,
    "Entry": ctk.CTkEntry,
    "Frame": ctk.CTkFrame,
    "Option Menu": ctk.CTkOptionMenu,
    "Progress Bar": ctk.CTkProgressBar,
    "Radio": ctk.CTkRadioButton,
    "Scrollable Frame": ctk.CTkScrollableFrame,
    "Scroll Bar": ctk.CTkScrollbar,
    # "Segment Button": ctk.CTkSegmentedButton,
    "Slider": ctk.CTkSlider,
    "Switch": ctk.CTkSwitch,
    # "Tab View": ctk.CTkTabview
}

def make_draggable(widget):
    widget.get("widget").bind("<Button-1>", on_drag_start)
    widget.get("widget").bind("<B1-Motion>", on_drag_motion)

def on_drag_start(event):
    widget = event.widget.master
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y

def on_drag_motion(event):
    widget = event.widget.master
    x = widget.winfo_x() - widget._drag_start_x + event.x
    y = widget.winfo_y() - widget._drag_start_y + event.y

    if(abs(widget.winfo_x() - widget._drag_start_x + event.x - int(app.winfo_width()) / 2) < app.winfo_width()/20 and not(keyboard.is_pressed("ctrl"))): # snapping x
        x = (app.winfo_width() - widget.winfo_width()) / 2
    
    if(abs(widget.winfo_y() - widget._drag_start_y + event.y - int(app.winfo_height()) / 2) < app.winfo_height()/20 and not(keyboard.is_pressed("ctrl"))):   # snapping y
        y = (app.winfo_height() - widget.winfo_height()) / 2

    widget.place(x=x, y=y)
    for active_widget in active_widgets:
        if widget == active_widget.get("widget"):
            active_widget['location'] = (x,y)
            break

def do_popup(event, frame, widget):
        global current_widget
        try: 
            frame.tk_popup(event.x_root, event.y_root)
            current_widget = widget
        finally: frame.grab_release()

def destroy_current_widget():
    global current_widget
    current_widget.destroy()
    for active_widget in active_widgets:
        if current_widget == active_widget.get('widget'):
            delete_widget_from_frame(active_widget)
            break
    
def create_app_window():
    global app
    app = ctk.CTkToplevel(editor_window)
    editor_size,editor_offset_x, editor_offset_y= editor_window.geometry().split("+")
    editor_size_x, _ = editor_size.split("x")
    app.geometry(f"500x400+{int(editor_offset_x)+int(editor_size_x) + 10}+{int(editor_offset_y)}")    # ensures the window always gets created next to the editor
    app.resizable(False, False)
    app.title("App")
    return app

def apply_window_settings(): # todo, maybe not repeating code here, app shOULDnt HAVE TO BE GLOBAl
    global app
    if(app == None or app.winfo_exists() == False):
        app = create_app_window()
        draw_widgets
    if(entry_width.get() + entry_height.get() != ""):
        app.geometry(f"{entry_width.get()}x{entry_height.get()}")
    if(entry_name.get() != ""):    
        app.title(f"{entry_name.get()}")
    if(entry_icon_file.get() != ""):
        icopath = ImageTk.PhotoImage(file=entry_icon_file.get())
        app.iconphoto(False, icopath)

def selectIcon():
    curr_dir = os.getcwd()
    path = filedialog.askopenfile(initialdir=curr_dir)
    if(path.name != ""):
        entry_icon_file.insert(0, str(path.name))

def delete_widget_from_frame(widget):
    widget.get('widget').destroy()
    frame_widgets.remove_widget(widget.get('widget'))
    active_widgets.remove(widget)

def update_active_widgets():
    for widget in active_widgets:           # we want to call these everytime a new widget is added
        if(frame_widgets.check_widget(widget.get('widget')) == False):
            frame_widgets.add_widget(widget.get('widget'),name=widget.get('widget_name'),edit_cb=lambda:print("Edit"), delete_cb=lambda w=widget: delete_widget_from_frame(w))
            widget.get('widget').bind("<Button-3>", lambda event, w=widget: do_popup(event, widget=w.get('widget'), frame=RightClickMenu))
            make_draggable(widget)
    draw_widgets()

def create_widget(widget_type, **kwargs):
    # Get the widget class from the dictionary
    widget_class = widget_types.get(widget_type)

    # If the widget type is valid, create the widget and do all the code necessary
    if widget_class and widget_class != None:
        created_widget = {"widget":widget_class(app, **kwargs),
                          "location": (app.winfo_width()/2, app.winfo_height()/2),
                          "widget_name": str(widget_type)}
        if(widget_type == "Option Menu"):
            created_widget.get("widget").configure(state="disabled")
        active_widgets.append(created_widget)
        update_active_widgets()

def draw_widgets():
    for widget in active_widgets:
        x,y = widget.get('location')
        widget.get('widget').place(x=x,y=y)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

editor_window = ctk.CTk()
editor_window.geometry("400x500")
editor_window.resizable(width=False, height=False)
editor_window.title("CTk EasyEdit")

app = create_app_window()

menu = CTkMenuBar(master=editor_window)
menu.add_cascade("File")
menu.add_cascade("Edit")

# windows settings starts
label_window_settings = ctk.CTkLabel(editor_window, text="Window Settings")
label_window_settings.pack(anchor="w", padx=15)

window_settings_frame = ctk.CTkFrame(editor_window, width=380, height=140)

label_entry_width = ctk.CTkLabel(window_settings_frame, text="px")
label_entry_width.place(x=200, y=10)
label_left_entry_width = ctk.CTkLabel(window_settings_frame, text="Width")
label_left_entry_width.place(x=10, y=10)
entry_width = ctk.CTkEntry(window_settings_frame, placeholder_text = "Width of Window")
entry_width.place(x=55, y=10)

entry_height = ctk.CTkEntry(window_settings_frame, placeholder_text= "Height of Window")
entry_height.place(x=55, y=40)
label_left_entry_height = ctk.CTkLabel(window_settings_frame, text="Height")
label_left_entry_height.place(x=10, y=40)
label_entry_width = ctk.CTkLabel(window_settings_frame, text="px")
label_entry_width.place(x=200, y=40)

entry_name = ctk.CTkEntry(window_settings_frame, placeholder_text= "App Name")
entry_name.place(x=55, y=70)
label_left_name = ctk.CTkLabel(window_settings_frame, text="Title")
label_left_name.place(x=10, y=70)

entry_icon_file = ctk.CTkEntry(window_settings_frame, placeholder_text= "Path/to/Icon")
entry_icon_file.place(x=55, y=100)
label_left_entry_icon = ctk.CTkLabel(window_settings_frame, text="Icon")
label_left_entry_icon.place(x=10, y=100)
button_select_icon = ctk.CTkButton(window_settings_frame, text="...", width=10, height=25, command=selectIcon)
button_select_icon.place(x=200, y=102)

button_apply_settings = ctk.CTkButton(window_settings_frame, text="Apply Settings", width=100, height = 60, corner_radius=20, command=apply_window_settings)
button_apply_settings.place(x=250, y = 10)

window_settings_frame.pack(pady=0)
# windows settings end


# active widgets ui begins, will reimplement as a tree later: https://github.com/TomSchimansky/CustomTkinter/discussions/524
label_active_widgets = ctk.CTkLabel(editor_window, text="Active Widgets")
label_active_widgets.place(x=15, y=200)
optionmenu_add_widget = ctk.CTkOptionMenu(editor_window, values=[item for item in widget_types.keys()], width = 30, height=20, command=create_widget)
optionmenu_add_widget.place(x=390, y = 214, anchor="e")

frame_widgets = WidgetHandler(editor_window, width=355, height=250)

active_widgets = []

frame_widgets.place(x=10,y=230)
# active widgets ui ends

current_widget = None

RightClickMenu = tk.Menu(app, tearoff=False, background='#565b5e', fg='white', borderwidth=0, bd=0)
RightClickMenu.add_command(label="Duplicate", command=lambda: print("Duplicate Logic"))
RightClickMenu.add_command(label="Delete", command=lambda: destroy_current_widget())

app.bind("<1>", lambda event: event.widget.focus_set())

editor_window.mainloop()