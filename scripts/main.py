import os
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image, ImageDraw
import customtkinter as ctk
from CTkMenuBar import *
from icecream import ic
import keyboard
from activewidgethandler import *
from boilerplate import *
from settingseditor import *
from CTkFileSelector import *
from preferenceshandler import *
from CTkImage import *
from CTkError import *

widget_types = {
    "Add Widgets Here": None,
    "Button": ctk.CTkButton,
    "Label": ctk.CTkLabel,
    "Image": CTkImageFrame,
    "Text Box": ctk.CTkTextbox,
    "Check Box": ctk.CTkCheckBox,
    "Combo Box": ctk.CTkComboBox,
    "Entry": ctk.CTkEntry,
    "Frame": ctk.CTkFrame,
    "Option Menu": ctk.CTkOptionMenu,
    "Progress Bar": ctk.CTkProgressBar,
    "Radio": ctk.CTkRadioButton,
    # "Scrollable Frame": ctk.CTkScrollableFrame, # Drag doesnt work for this
    "Scroll Bar": ctk.CTkScrollbar,
    # "Segment Button": ctk.CTkSegmentedButton, Drag is broken for this
    "Slider": ctk.CTkSlider,
    "Switch": ctk.CTkSwitch,
    # "Tab View": ctk.CTkTabview Drag is broken for this
}

# for a rainy day, also i'm not sure how this will play with the grid manager yet
# def toggle_grid():
#     global background
#     if(export_preferences.get("Grid Edit Mode:").get("value")):
#         height = int(entry_height.get())
#         width = int(entry_width.get())
#         grid_spacing_x = width / (int(export_preferences.get("Grid Count X:")["value"]) + 1)
#         grid_spacing_y = height / (int(export_preferences.get("Grid Count Y:")["value"]) + 1)
#         im = Image.new(mode = "RGB", size = (width, height), color=(36,36,36))
#         draw = ImageDraw.Draw(im)
#         for x in (range(1, int(export_preferences.get("Grid Count X:")["value"])+ 1)):
#             draw.line([(int((x)*grid_spacing_x),0),(int((x)*grid_spacing_x), height)], (0, 128,128,40), 1)
#         for y in (range(1, int(export_preferences.get("Grid Count Y:")["value"])+1)):
#             draw.line([(0,int((y)*grid_spacing_y)),(width, int((y)*grid_spacing_y))], (0, 128,128, 40), 1)
#         image = ctk.CTkImage(dark_image=im, size=(width,height))
#         background = ctk.CTkLabel(app, image=image, text='', height=height, width=width)
#         background.place(x=0,y=0)
#     else:
#         background.destroy()

export_preferences = {
    # "Grid Edit Mode:": {"value": False, "cb": toggle_grid "hotkey": []},
    # "Grid Count X:": {"value": 10, "cb": None},
    # "Grid Count Y:": {"value": 10, "cb": None},
    "Export as OOP?": {"value": True, "cb": None},
    "File Name:": {"value": "generated_file", "cb": None},
    "CustomTkinter Module Name:": {"value": "ctk", "cb": None},
    "Tkinter Module Name:": {"value": "tk", "cb": None},
    "Root Name:": {"value": "root", "cb": None},
    "Class Name (OOP Only):": {"value": "Root", "cb": None},
}

def find_widget_in_active_widgets(widget):  # this takes in a CTk Widget Object and finds its corresponding entry in the active_widgets dictionary
    for active_widget in active_widgets:
        if active_widget.get("widget") == widget:
            return active_widget

# def kill_snap_widget(arg):
#     global label_snap_lines_horizontal, label_snap_lines_vertical
#     if(label_snap_lines_vertical):
#         label_snap_lines_horizontal.forget()
#     if(label_snap_lines_horizontal):
#         label_snap_lines_vertical.forget()

def make_draggable(widget):
    widget.get("widget").bind("<Button-1>", on_drag_start)
    widget.get("widget").bind("<B1-Motion>", on_drag_motion)
    # widget.get("widget").bind("<ButtonRelease-1>", kill_snap_widget)

def on_drag_start(event):
    widget = event.widget.master
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y

# as long as i hide this function in my terminal everything is okay
# its responsibility is to return the x point of either the center line or a widget's center
# if it's x position is different by 20 pixels, same with y
# it achieves that through some black magic codde
def check_other_widgets(widget_x_mid, widget_y_mid, widget, test_x, widget_half_x, widget_half_y):
    # global label_snap_lines_vertical, label_snap_lines_horizontal
    # app_height = app.winfo_height()
    # app_width = app.winfo_width()

    # snap_lines_img_vertical = Image.new(mode = "RGBA", size = (1, 40), color=(0,0,0,128))
    # draw = ImageDraw.Draw(snap_lines_img_vertical)
    # draw.line([0, 0, 0, 40], (0,235,255,200), 1)

    # snap_lines_img_horizontal = Image.new(mode = "RGBA", size = (40, 1), color=(0,0,0,128))
    # draw2 = ImageDraw.Draw(snap_lines_img_horizontal)
    # draw2.line([0, 0, 40, 0], (0,235,255,200), 1)

    # image_vert = ctk.CTkImage(dark_image=snap_lines_img_vertical, size=(1,40))
    # image_horizontal = ctk.CTkImage(dark_image=snap_lines_img_vertical, size=(40,1))
    
    # label_snap_lines_horizontal = ctk.CTkLabel(widget, width=40, height=1, text='', image=image_horizontal)
    # label_snap_lines_vertical = ctk.CTkLabel(widget, width=1, height=40, text='', image=image_vert)
    
    for active_widget in active_widgets:
        if(widget == active_widget.get("widget")): continue
        else:
            active_widget_x_midpoint, active_widget_y_midpoint = active_widget.get("location")
            active_widget_x_midpoint += active_widget.get("widget").winfo_width() / 2
            if(test_x):
                if(abs(widget_x_mid - active_widget_x_midpoint)) < 10:
                    return active_widget_x_midpoint - active_widget.get("widget").winfo_width()/2
            else:
                if(abs(widget_y_mid - active_widget_y_midpoint - active_widget.get("widget").winfo_height() / 2)) < 10:
                    return active_widget_y_midpoint
                
    if(test_x): # testing for app center line
        if(abs(widget_x_mid - app.winfo_width()/2) < 10 and not keyboard.is_pressed("alt")): return app.winfo_width()/2 - widget_half_x
        else: return False
    else:
        if(abs(widget_y_mid - app.winfo_height()/2) < 10 and not keyboard.is_pressed("alt")): return app.winfo_height()/2 - widget_half_y
        else: return False

def on_drag_motion(event):
    widget = event.widget.master
    widget_half_height = widget.cget("height") / 2
    widget_half_width = widget.cget("width") / 2 
    x = widget.winfo_x() - widget._drag_start_x + event.x
    y = widget.winfo_y() - widget._drag_start_y + event.y

    widget_x_midpoint = widget.winfo_x() + widget_half_width - widget._drag_start_x + event.x
    widget_y_midpoint = widget.winfo_y() + widget_half_height - widget._drag_start_y + event.y

    if(check_other_widgets(widget_x_midpoint, widget_y_midpoint, widget, True, widget_half_width,widget_half_height) and not(keyboard.is_pressed("ctrl"))): # snapping x
        x = check_other_widgets(widget_x_midpoint, widget_y_midpoint, widget, True, widget_half_width,widget_half_height)
    
    if(check_other_widgets(widget_x_midpoint, widget_y_midpoint, widget, False, widget_half_width,widget_half_height) and not(keyboard.is_pressed("ctrl"))):   # snapping y
        y = check_other_widgets(widget_x_midpoint, widget_y_midpoint, widget, False, widget_half_width,widget_half_height)

    widget.place(x=x, y=y)
    for active_widget in active_widgets:
        if widget == active_widget.get("widget"):
            active_widget['location'] = (x,y)
            break

def do_popup(event, frame, widget):
        global current_widget
        try: 
            frame.tk_popup(event.x_root, event.y_root)
            current_widget = find_widget_in_active_widgets(widget)
        finally: frame.grab_release()

def destroy_current_widget():
    global current_widget
    current_widget.get("widget").destroy()
    delete_widget_from_frame(current_widget)
    
def create_app_window():
    app = ctk.CTkToplevel(editor_window)
    editor_size,editor_offset_x, editor_offset_y= editor_window.geometry().split("+")
    editor_size_x, _ = editor_size.split("x")
    app.geometry(f"500x500+{int(editor_offset_x)+int(editor_size_x) + 10}+{int(editor_offset_y)}")    # ensures the window always gets created next to the editor
    app.resizable(False, False)
    app.title("App")
    return app

def apply_window_settings(): # todo, maybe not repeating code here, app shOULDnt HAVE TO BE GLOBAl
    global app
    if(app == None or app.winfo_exists() == False):
        app = create_app_window()
        draw_widgets(app, True)
    if(entry_width.get() + entry_height.get() != ""):
        app.geometry(f"{entry_width.get()}x{entry_height.get()}")
    if(entry_name.get() != ""):    
        app.title(f"{entry_name.get()}")
    if(file_selector.get_path() != ""):
        icopath = ImageTk.PhotoImage(file=file_selector.get_path())
        app.iconphoto(False, icopath)
    # todo: fix this - Current limitation is that set_default_color_theme applies to the entire window, not the app
    # and also it doesn't update the app appearance in real time. One way would be to adjust the colours of the drawn
    # widgets in real time i.e. fg_color = current_theme col, but then that would get sent to boilerplate generator.
    # ill come back to this when im wiser 
    if(combo_theme_selector.get() != ""): 
        global theme
        theme = combo_theme_selector.get()
        theme = theme.replace(" ", "-")
        theme = theme.lower()
        ctk.set_default_color_theme(theme)
        app = create_app_window()
        draw_widgets(app, True)

def delete_widget_from_frame(widget):
    widget.get('widget').destroy()
    frame_widgets.remove_widget(widget.get('widget'))
    active_widgets.remove(widget)

def add_bindings(draw=True, updated_menu=None):
    for widget_instance in active_widgets:           # we want to call these everytime a new widget is added
        if(frame_widgets.check_widget(widget_instance.get('widget')) == False):
            theme = "blue"
            ctk.set_default_color_theme(theme)
            frame_widgets.add_widget(widget_instance,name_change_cb=change_widget_id ,edit_cb=lambda w=widget_instance: open_editor_window(w), delete_cb=lambda w=widget_instance: delete_widget_from_frame(w))
        if(not(widget_instance.get("has_bindings"))):
            widget_instance.get('widget').bind("<Button-3>", lambda event, w=widget_instance.get('widget'): do_popup(event, widget=w, frame=new_right_click_menu(w._nametowidget(w.winfo_parent()))))
            widget_instance.get('widget').bind("<Double-Button-1>", lambda event, w=widget_instance: open_editor_window(w))
            make_draggable(widget_instance)
            widget_instance["has_bindings"] = True
    if(draw):
        draw_widgets()

def create_widget(widget_type, duplicate=False, widget_to_duplicate=None, kwarg_list=[],**kwargs):
    theme = combo_theme_selector.get()
    theme = theme.replace(" ", "-")
    theme = theme.lower()
    ctk.set_default_color_theme(theme)
    # Get the widget class from the dictionary
    widget_class = widget_types.get(widget_type)
    # If the widget type is valid, create the widget and do all the code necessary
    if widget_class and widget_class != None:
        location_x, location_y = ((app.winfo_width()-widget_class(app, **kwargs).cget("width"))/2, (app.winfo_height()-widget_class(app, **kwargs).cget("height"))/2) if not duplicate else widget_to_duplicate.get("location")   # if it is duplicated, set the location to middle, otherwise duplicated it on top of the current widget
        number_of_same_widgets = 0
        for active_widget in active_widgets:
            if(active_widget.get("widget_type")) == str(widget_class):
                number_of_same_widgets += 1
        created_widget = {"widget":widget_class(app, **kwargs),
                          "location": (location_x, location_y),
                          "widget_name": str(widget_type),  # todo check why we need this
                          "widget_type": str(widget_class),
                          "kwargs": kwargs,
                          "widget_id": f"{widget_type} {number_of_same_widgets}",
                          "has_bindings": False}  
        if(widget_type == "Option Menu"):
            created_widget.get("widget").configure(state="disabled")
        if(duplicate):
            created_widget["location"] = (location_x+10, location_y+10)
            created_widget["kwargs"] = kwarg_list   # this is needed because image is part of kwargs for some reason
            edit_widget_attributes(created_widget)
    
    active_widgets.append(created_widget)
    add_bindings()

def new_right_click_menu(master):
    RightClickMenu = tk.Menu(master, tearoff=False, background='#565b5e', fg='white', borderwidth=0, bd=0)
    RightClickMenu.add_command(label="Duplicate", command=duplicate_current_widget)
    RightClickMenu.add_command(label="Edit", command=edit_current_widget)
    RightClickMenu.add_command(label="Delete", command=destroy_current_widget)
    return RightClickMenu

def draw_widgets(new_canvas = None, update_widgets = False):
    for widget in active_widgets:
        if(new_canvas):
            kwargs = widget.get('kwargs')
            widget['widget'] = widget_types.get((widget.get('widget_name')))(new_canvas, **kwargs)
            widget['has_bindings'] = False
            widget.get('widget').unbind("<Button-3>")
            widget.get('widget').unbind("<Button-1>")
            widget.get('widget').unbind("<B1-Motion>")
            widget.get('widget').unbind("<Double-Button-1>")
            
            right_click_menu=new_right_click_menu(new_canvas)
            
        x,y = widget.get('location')
        widget.get('widget').place(x=x,y=y)
    if(update_widgets):
        add_bindings(draw=False, updated_menu=right_click_menu)
   
def generate_file(path, export_preferences):
    with open(f"{path}/{export_preferences.get('File Name:')['value']}.py", 'w') as f:   # separate f.write functions to not clog down this file any more than it needs to be
        boiler_handler = BoilerPlateHandler()
        boiler_handler.set_preferences(export_preferences)
        app_height = entry_height.get()
        app_width = entry_width.get()
        if(app_height != "" and app_width != ""):
            f.write(boiler_handler.imports())
            theme = combo_theme_selector.get().lower()
            theme = theme.replace(" ", "-")
            f.write(boiler_handler.basic_app_window(app_width, app_height, file_selector.get_path(), path, entry_name.get(), theme))
        else:
            CTkError(editor_window,error_message="App Dimensions Cannot Be Empty!", button_1_text="Okay")
            try:
                os.remove(f"{path}/{export_preferences.get('File Name:').get('value')}.py")
            except FileNotFoundError:
                pass
        
        for widget in active_widgets:
            f.write(str(boiler_handler.widget_code(widget, path)))

        f.write(boiler_handler.main_loop())

        CTkError(editor_window,title="Successful!",size_y=140, error_message=f"Successful write at {path}/{export_preferences.get('File Name:')['value']}.py", button_1_text="Okay")

def save_logic():
    global export_preferences
    curr_dir = os.getcwd()
    path = filedialog.askdirectory(initialdir=curr_dir)
    if(path != ""):
        generate_file(path, export_preferences)

def duplicate_current_widget():
    global current_widget
    create_widget(current_widget.get("widget_name"), True, current_widget, kwarg_list=current_widget.get("kwargs"))

def edit_widget_attributes(widget):
    try:
        properties = widget.get("kwargs")
        widget.get("widget").configure(**properties)
    except ValueError:
        if(widget.get("kwargs").get("image_path")):
            image = ctk.CTkImage(dark_image=Image.open(widget.get("kwargs").get("image_path")), size=(widget.get("kwargs").get("image_size_x"), widget.get("kwargs").get("image_size_y")))
            widget.get("widget").configure(image=image)

def open_editor_window(widget):
    global attribute_editor_window
    if(attribute_editor_window):
        attribute_editor_window.change_edited_widget(widget)
    else:
        attribute_editor_window = AttributeEditorWindow(editor_window, widget_to_edit=widget, apply_settings_cb=edit_widget_attributes)

def change_widget_id(widget, id):
    for widgets in active_widgets:
        if (widgets.get("widget_id") == id and widgets != widget):
            raise NameError ("There is already an item with this name!")
        else:
            widget["widget_id"] = id

def edit_current_widget():
    global current_widget
    open_editor_window(current_widget)

def set_preferences(dictionary):
    global export_preferences
    export_preferences = dictionary

def export_preferences_editor():
    export = ExportPreferenceHandler(editor_window, pref_dict=export_preferences)
    export.set_set_preferences_cb(lambda: set_preferences(export.get_preferences_dict()))  # the button needs a reference to the function to update the export preferences

def save_project():
    pass
 
def open_project():
    pass

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

theme = "blue"

editor_window = ctk.CTk()
editor_window.geometry("400x500")
editor_window.resizable(width=False, height=False)
editor_window.title("CTk EasyEditor")

app = create_app_window()

# menubar settings starts
menu = CTkMenuBar(master=editor_window)

menubar_button_file = menu.add_cascade("File")
menubar_button_edit = menu.add_cascade("Edit")

dropdown_file = CustomDropdownMenu(widget=menubar_button_file, corner_radius=0)
dropdown_file.add_option(option="Export as .py", command=save_logic)

dropdown_file = CustomDropdownMenu(widget=menubar_button_edit, corner_radius=0)
dropdown_file.add_option(option="Preferences...", command=export_preferences_editor)
# menubar settings end

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
entry_width.insert(0, 500)

entry_height = ctk.CTkEntry(window_settings_frame, placeholder_text= "Height of Window")
entry_height.place(x=55, y=40)
label_left_entry_height = ctk.CTkLabel(window_settings_frame, text="Height")
label_left_entry_height.place(x=10, y=40)
label_entry_width = ctk.CTkLabel(window_settings_frame, text="px")
label_entry_width.place(x=200, y=40)
entry_height.insert(0, 500)


entry_name = ctk.CTkEntry(window_settings_frame, placeholder_text= "App Name")
entry_name.place(x=55, y=70)
label_left_name = ctk.CTkLabel(window_settings_frame, text="Title")
label_left_name.place(x=10, y=70)

file_selector = CTkFileSelector(window_settings_frame, entry_padding=(20, 5), label="Icon")
file_selector.place(x=10, y=100)

# see function apply_window_settings for why this isn't implemented yet
label_theme_selection = ctk.CTkLabel(window_settings_frame, text="Select a theme:")
label_theme_selection.place(x=250, y=70)
combo_theme_selector = ctk.CTkSegmentedButton(window_settings_frame, values=["Blue", "Dark Blue", "Green"],height=30)
combo_theme_selector.place(x=215, y=100)

combo_theme_selector.set('Blue')

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

# Right Click Menu Begins
RightClickMenu = new_right_click_menu(app)
# Right Click Menu Ends

attribute_editor_window = None
attributes_is_active = False

app.bind("<1>", lambda event: event.widget.focus_set())

editor_window.mainloop()