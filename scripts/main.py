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
import json
from sys import platform
import math

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

def change_grid(tuple_up_down):
    if(tuple_up_down[0] and tuple_up_down[1]):
        if(export_preferences.get("Grid Count X:")["value"] > 1):
            export_preferences.get("Grid Count X:")["value"] -= 1
    elif(tuple_up_down[0] and not(tuple_up_down[1])):
        export_preferences.get("Grid Count X:")["value"] += 1
    elif(not(tuple_up_down[0]) and tuple_up_down[1]):
        if(export_preferences.get("Grid Count Y:")["value"] > 1):
            export_preferences.get("Grid Count Y:")["value"] -= 1
    elif(not(tuple_up_down[0]) and not(tuple_up_down[1])):
        export_preferences.get("Grid Count Y:")["value"] += 1
    
    toggle_grid()
    toggle_grid()

def toggle_grid(*args):
    global dragging
    if(not(dragging)):
        global background
        export_preferences.get("Grid Edit Mode:")["value"] = not(export_preferences.get("Grid Edit Mode:")["value"])
        if(export_preferences.get("Grid Edit Mode:").get("value")):
            height = int(entry_height.get())
            width = int(entry_width.get())
            grid_spacing_x = width / (int(export_preferences.get("Grid Count X:")["value"]) + 1)
            grid_spacing_y = height / (int(export_preferences.get("Grid Count Y:")["value"]) + 1)
            im = Image.new(mode = "RGBA", size = (width, height), color=(0,0,0, 0))
            draw = ImageDraw.Draw(im)
            for x in (range(1, int(export_preferences.get("Grid Count X:")["value"])+ 1)):
                draw.line([(int((x)*grid_spacing_x),0),(int((x)*grid_spacing_x), height)], (0, 128,128,255), 1)
            for y in (range(1, int(export_preferences.get("Grid Count Y:")["value"])+1)):
                draw.line([(0,int((y)*grid_spacing_y)),(width, int((y)*grid_spacing_y))], (0, 128,128, 255), 1)
            image = ctk.CTkImage(dark_image=im, size=(width,height))
            background = ctk.CTkLabel(app, image=image, text='', height=height, width=width)
            background.place(x=0,y=0)
            draw_widgets(app, update_widgets=True, delete_existing_widgets=True)
        else:
            background.destroy()

export_preferences = {
    "Grid Edit Mode:": {"value": False, "cb": toggle_grid},
    "Grid Count X:": {"value": 2, "cb": None},
    "Grid Count Y:": {"value": 2, "cb": None},
    "Snapping Sensitivity": {"value": 5, "cb": None},
    "Export as OOP?": {"value": True, "cb": None},
    "File Name:": {"value": "generated_file", "cb": None},
    "CustomTkinter Module Name:": {"value": "ctk", "cb": None},
    "Tkinter Module Name:": {"value": "tk", "cb": None},
    "Root Name:": {"value": "root", "cb": lambda: frame_widgets.update_masters_list(find_frames())},
    "Class Name (OOP Only):": {"value": "Root", "cb": None},
}

def find_widget_in_active_widgets(widget):  # this takes in a CTk Widget Object and finds its corresponding entry in the active_widgets dictionary
    for active_widget in active_widgets:
        if active_widget.get("widget") == widget:
            return active_widget

def set_theme_to_user_theme():
    theme = combo_theme_selector.get()
    theme = theme.replace(" ", "-")
    theme = theme.lower()
    ctk.set_default_color_theme(theme)

# def kill_snap_widget(arg):
#     global label_snap_lines_horizontal, label_snap_lines_vertical
#     if(label_snap_lines_vertical):
#         label_snap_lines_horizontal.forget()
#     if(label_snap_lines_horizontal):
#         label_snap_lines_vertical.forget()

def make_draggable(widget):
    widget.get("widget").bind("<Button-1>", on_drag_start)
    widget.get("widget").bind("<B1-Motion>", on_drag_motion)
    widget.get("widget").bind("<ButtonRelease-1>", on_drag_end)
    # widget.get("widget").bind("<ButtonRelease-1>", kill_snap_widget)

def on_drag_end(event):
    global dragging
    dragging = False

def on_drag_start(event):
    global dragging
    dragging = True
    widget = event.widget.master
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y

# as long as i hide this function in my terminal everything is okay
# its responsibility is to return the x point of either the center line or a widget's center
# if it's x position is different by 20 pixels, same with y
# it achieves that through some black magic codde
def check_other_widgets(widget_x_mid, widget_y_mid, widget, test_x, widget_half_x, widget_half_y):
    snapping_sensitivity = int(export_preferences["Snapping Sensitivity"]["value"])
    for active_widget in active_widgets:
        if(widget == active_widget.get("widget") or active_widget['widget'].master == widget): 
            # ic(active_widget['master'])
            continue
        else:
            active_widget_x_midpoint, active_widget_y_midpoint = active_widget.get("location")
            active_widget_width, active_widget_height = active_widget.get("widget").cget("width"), active_widget.get("widget").cget("height")
            active_widget_x_midpoint += active_widget.get("widget").winfo_width() / 2
            if(not keyboard.is_pressed("shift")):
                if(test_x):
                    if(abs(widget_x_mid - active_widget_x_midpoint)) < snapping_sensitivity: return active_widget_x_midpoint - active_widget.get("widget").winfo_width()/2
                    if(abs((widget_x_mid) - active_widget_x_midpoint + active_widget_width)) < snapping_sensitivity: return active_widget_x_midpoint - active_widget_width - widget_half_x
                    if(abs((widget_x_mid) - active_widget_x_midpoint - active_widget_width)) < snapping_sensitivity: return active_widget_x_midpoint + active_widget_width - widget_half_x
                else:
                    if(abs(widget_y_mid - active_widget_y_midpoint - active_widget.get("widget").winfo_height() / 2)) < snapping_sensitivity: return active_widget_y_midpoint
                    if(abs((widget_y_mid - widget_half_y) - active_widget_y_midpoint - active_widget_height)) < snapping_sensitivity: return active_widget_y_midpoint + active_widget_height
                    if(abs((widget_y_mid - widget_half_y) - active_widget_y_midpoint + active_widget_height)) < snapping_sensitivity: return active_widget_y_midpoint - active_widget_height

    if(test_x and not(export_preferences["Grid Edit Mode:"]["value"])): # testing for app center line
        if(abs(widget_x_mid - app.winfo_width()/2) < snapping_sensitivity and not keyboard.is_pressed("alt")): return app.winfo_width()/2 - widget_half_x
        else: return False
    elif(not(export_preferences["Grid Edit Mode:"]["value"])):
        if(abs(widget_y_mid - app.winfo_height()/2) < snapping_sensitivity and not keyboard.is_pressed("alt")): return app.winfo_height()/2 - widget_half_y
        else: return False
    elif(test_x and (export_preferences["Grid Edit Mode:"]["value"])): # When Grid Mode is Active
        app_width = app.winfo_width()
        spacing_x = app_width/(export_preferences["Grid Count X:"]["value"] + 1)
        for i in range(0, export_preferences["Grid Count X:"]["value"]+1):
            if(abs(widget_x_mid - i*spacing_x) < snapping_sensitivity and not keyboard.is_pressed("alt")): return i*spacing_x - widget_half_x
            if(abs((widget_x_mid - widget_half_x) - i*spacing_x) < snapping_sensitivity and not keyboard.is_pressed("alt")): return i*spacing_x
            if(abs((widget_x_mid + widget_half_x) - i*spacing_x) < snapping_sensitivity and not keyboard.is_pressed("alt")): return i*spacing_x - 2*widget_half_x
        return False
    elif(not(test_x) and (export_preferences["Grid Edit Mode:"]["value"])): # When Grid Mode is Active
        app_height = app.winfo_height()
        spacing_y = app_height/(export_preferences["Grid Count Y:"]["value"] + 1)
        for i in range(0, export_preferences["Grid Count Y:"]["value"]+1):
            if(abs(widget_y_mid - i*spacing_y) < snapping_sensitivity and not keyboard.is_pressed("alt")): return i*spacing_y - widget_half_y
            if(abs((widget_y_mid - widget_half_y) - i*spacing_y) < snapping_sensitivity and not keyboard.is_pressed("alt")): return i*spacing_y
            if(abs((widget_y_mid + widget_half_y) - i*spacing_y) < snapping_sensitivity and not keyboard.is_pressed("alt")): return i*spacing_y - 2*widget_half_y
        return False
        
def on_drag_motion(event):
    widget = event.widget.master
    widget_half_height = widget.cget("height") / 2
    widget_half_width = widget.cget("width") / 2 
    x = widget.winfo_x() - widget._drag_start_x + event.x
    y = widget.winfo_y() - widget._drag_start_y + event.y

    widget_x_midpoint = x + widget_half_width 
    widget_y_midpoint = y + widget_half_height

    if(check_other_widgets(widget_x_midpoint, widget_y_midpoint, widget, True, widget_half_width,widget_half_height) and not(keyboard.is_pressed("ctrl"))): # snapping x
        x = check_other_widgets(widget_x_midpoint, widget_y_midpoint, widget, True, widget_half_width,widget_half_height)
    
    if(check_other_widgets(widget_x_midpoint, widget_y_midpoint, widget, False, widget_half_width,widget_half_height) and not(keyboard.is_pressed("ctrl"))):   # snapping y
        y = check_other_widgets(widget_x_midpoint, widget_y_midpoint, widget, False, widget_half_width,widget_half_height)

    widget.place(x=x, y=y)
    for active_widget in active_widgets:
        if widget == active_widget.get("widget"):
            active_widget['location'] = (int(x),int(y))
            break

def do_popup(event, frame, widget):
        global current_widget
        try: 
            ctk.set_default_color_theme('blue')
            frame.tk_popup(event.x_root, event.y_root)
            current_widget = find_widget_in_active_widgets(widget)
            set_theme_to_user_theme()
        finally: frame.grab_release()

def destroy_current_widget():
    global current_widget
    children_list = current_widget.get("widget").children.copy()
    if(children_list is not None):
        for children in children_list:
            try:
                child = find_widget_in_active_widgets((current_widget['widget'].nametowidget((children))))
                if(child is not None):
                    delete_widget_from_frame(child)
            except Exception as ex:
                ic(ex)

    current_widget.get("widget").destroy()
    ctk.set_default_color_theme('blue')
    delete_widget_from_frame(current_widget)
    set_theme_to_user_theme()

def update_size_vars(event):
    global window_width, window_height, app
    if event.widget.widgetName == "toplevel":
        if (window_width != event.width) and (window_height != event.height):
            window_width.set(event.width) 
            window_height.set(event.height)
        if (keyboard.is_pressed("ctrl")):
            width_rounded = math.ceil(event.width/10.0) * 10
            height_rounded = math.ceil(event.height/10.0) * 10
            window_width.set(width_rounded) 
            window_height.set(height_rounded)
            app.geometry(f"{width_rounded}x{height_rounded}")

def create_app_window():
    global app
    if(app is not None):
        app.destroy()
    app = ctk.CTkToplevel(editor_window)
    editor_size,editor_offset_x, editor_offset_y= editor_window.geometry().split("+")
    editor_size_x, _ = editor_size.split("x")
    app.geometry(f"{entry_width.get()}x{entry_height.get()}+{int(editor_offset_x)+int(editor_size_x) + 10}+{int(editor_offset_y)}")    # ensures the window always gets created next to the editor
    if(switch_resizable_window.get()):
        app.resizable(True, True)
    else:
        app.resizable(False, False)
    app.title(entry_name.get())

    app.bind("<Configure>", update_size_vars)

    return app

def apply_window_settings(): # todo, maybe not repeating code here, app shOULDnt HAVE TO BE GLOBAl
    global app
    if(app == None or app.winfo_exists() == False):
        app = create_app_window()
    if(combo_theme_selector.get() != ""): 
        global theme
        set_theme_to_user_theme()
        app = create_app_window()
        if(file_selector.get_path() != ""):
            app.after(200, lambda: app.iconbitmap(file_selector.get_path()))
        draw_widgets(app, True)
    if(entry_width.get() + entry_height.get() != ""):
        app.geometry(f"{entry_width.get()}x{entry_height.get()}")
    if(entry_name.get() != ""):    
        app.title(f"{entry_name.get()}")
    if(file_selector.get_path() != ""):
        if platform.startswith("win"):
            app.after(200, lambda: app.iconbitmap(file_selector.get_path()))
    
def delete_widget_from_frame(widget):
    widget.get('widget').destroy()
    frame_widgets.remove_widget(widget.get('widget'))
    active_widgets.remove(widget)

def find_widget_reference_with_name(name):
    for widget in active_widgets:
        if(widget['widget_id'] == name):
            return widget['widget']
    return None

def move_widget_up_in_frame(widget):
    ctk.set_default_color_theme('blue')
    global active_widgets
    widget_index = 0
    for active_widget in active_widgets:
        if(active_widget.get("widget") == widget.get("widget")):
            break
        widget_index += 1
    if(widget_index == 0):
        return
    elif(editor_window.nametowidget(active_widgets[widget_index-1]['widget']) != find_widget_reference_with_name(active_widgets[widget_index]['master'])):
        active_widgets[widget_index], active_widgets[widget_index - 1] = active_widgets[widget_index - 1], active_widgets[widget_index]
        frame_widgets.swap_widget_from_to(widget_index, widget_index-1)
    else:
        CTkError(editor_window, error_message=f"Widget {active_widgets[widget_index]['widget_id']} cannot be above master {active_widgets[widget_index - 1]['widget_id']}!", button_1_text="Okay", size_x=150, size_y=100)
        return
    set_theme_to_user_theme()
    draw_widgets(app, update_widgets=True, delete_existing_widgets=True)
    
def move_widget_down_in_frame(widget):
    ctk.set_default_color_theme('blue')
    global active_widgets
    widget_index = 0
    for active_widget in active_widgets:
        if(active_widget.get("widget") == widget.get("widget")):
            break
        widget_index += 1
    # ic(widget_index)
    if(widget_index == len(active_widgets) - 1):
        return
    elif(editor_window.nametowidget(active_widgets[widget_index]['widget']) != find_widget_reference_with_name(active_widgets[widget_index + 1]['master'])):
        active_widgets[widget_index], active_widgets[widget_index + 1] = active_widgets[widget_index + 1], active_widgets[widget_index]
        frame_widgets.swap_widget_from_to(widget_index, widget_index+1)
    else:
        CTkError(editor_window, error_message=f"Widget {active_widgets[widget_index]['widget_id']} cannot be below child {active_widgets[widget_index + 1]['widget_id']}!", button_1_text="Okay", size_x=150, size_y=100)
        return
    set_theme_to_user_theme()
    draw_widgets(app, update_widgets=True, delete_existing_widgets=True)
    
def change_master_overall(widget, new_master):
    if(widget['widget'] == new_master['Reference']):
        CTkError(editor_window, button_1_text="Okay",error_message="Widget Master Cannot Be Itself!", size_x=150, size_y=100)
        raise TypeError("Cannot Set Widget Master To Itself!")
        return
    
    new_master_index = 0
    widget_index = 0
    for index, active_widget in enumerate(active_widgets):
        if(active_widget['widget'] == widget['widget']):
            widget_index = index
        if(active_widget['widget'] == new_master["Reference"]):
            new_master_index = index

    if(new_master_index > widget_index):
        CTkError(editor_window, button_1_text="Okay",error_message="Widget master cannot be drawn after child!", size_x=150, size_y=100)
        raise TypeError("Widget Master is Lower than Child!")
        return
    # ic(widget, new_master)
    widget['widget'].destroy()
    # ic(new_master['Reference'])
    widget['master'] = new_master['Name']
    widget['location'] = (0, 0)
    draw_widgets(app, delete_existing_widgets=True, update_widgets=True)
    frame_widgets.update_masters_list(find_frames())

def find_frames():
    frames = []
    frames.append({"Name": export_preferences.get("Root Name:")['value'], "Reference": app})
    for widget in active_widgets:
        if(isinstance(widget['widget'], ctk.CTkFrame)):
            frames.append({"Name":widget['widget_id'],"Reference": widget['widget']})
    return frames

def add_bindings(draw=True, updated_menu=None):
    for widget_instance in active_widgets:           # we want to call these everytime a new widget is added
        if(frame_widgets.check_widget(widget_instance.get('widget')) == False):
            ctk.set_default_color_theme('blue')
            frame_widgets.add_widget(widget_instance,name_change_cb=change_widget_id ,edit_cb=lambda w=widget_instance: open_editor_window(w), masters_list=find_frames(), delete_cb=lambda w=widget_instance: delete_widget_from_frame(w), move_up_cb=lambda w=widget_instance: move_widget_up_in_frame(w), move_down_cb=lambda w=widget_instance: move_widget_down_in_frame(w), change_master_command=change_master_overall)
            set_theme_to_user_theme()
        if(not(widget_instance.get("has_bindings"))):
            widget_instance.get('widget').bind("<Button-3>", lambda event, w=widget_instance.get('widget'): do_popup(event, widget=w, frame=new_right_click_menu(w._nametowidget(w.winfo_parent()))))
            widget_instance.get('widget').bind("<Double-Button-1>", lambda event, w=widget_instance: open_editor_window(w))
            make_draggable(widget_instance)
            widget_instance["has_bindings"] = True
    if(draw):
        draw_widgets()

def create_widget(widget_type, duplicate=False, widget_to_duplicate=None, kwarg_list=[],from_file=False, from_file_dict={}, widget_command=None, master=None,**kwargs):
    set_theme_to_user_theme()
    # Get the widget class from the dictionary
    widget_class = widget_types.get(widget_type)
    # If the widget type is valid, create the widget and do all the code necessary
    if widget_class is not None:
        location_x, location_y = ((app.winfo_width()-widget_class(app, **kwargs).cget("width"))/2, (app.winfo_height()-widget_class(app, **kwargs).cget("height"))/2) if not duplicate else widget_to_duplicate.get("location")   # if it is duplicated, set the location to middle, otherwise duplicated it on top of the current widget
        number_of_same_widgets = 0

        list_of_widgets_names = []
        for active_widget in active_widgets:
            list_of_widgets_names.append(active_widget["widget_id"])

        for active_widget in active_widgets:
            if(active_widget.get("widget_type")) == str(widget_class):
                number_of_same_widgets += 1
                if(f"{widget_type} {number_of_same_widgets}" not in list_of_widgets_names):
                    break
        
        created_widget = {
            "widget": None,
            "location": (location_x, location_y),
            "widget_name": str(widget_type),  # todo check why we need this
            "widget_type": str(widget_class),
            "kwargs": kwargs,
            "widget_id": f"{widget_type} {number_of_same_widgets}",
            "has_bindings": False,
            "master": None
        }

        if(master is not None):
            created_widget["widget"] = widget_class(find_widget_reference_with_name(master), **kwargs)
            created_widget["master"] = master  
        else:
            created_widget["widget"] = widget_class(app, **kwargs)
            created_widget["master"] = export_preferences.get("Root Name:")["value"] 

        if(widget_type == "Option Menu"):
            created_widget.get("widget").configure(state="disabled")
        if(duplicate):
            created_widget["location"] = (location_x+10, location_y+10)
            created_widget["kwargs"] = kwarg_list.copy()   # this is needed because image is part of kwargs for some reason
            created_widget["command_name"] = widget_command
            if("image" in widget_to_duplicate):
                created_widget["image_path"] = widget_to_duplicate["image_path"]
                created_widget["image_size"] = widget_to_duplicate["image_size"]
            edit_widget_attributes(created_widget)
        if(from_file):
            created_widget["location"] = from_file_dict["location"]
            created_widget["kwargs"] = from_file_dict["kwargs"]
            created_widget["widget_id"] = from_file_dict["widget_id"]
            if("image_path" in from_file_dict):
                created_widget["image_path"] = from_file_dict["image_path"]
                created_widget["image_size"] = from_file_dict["image_size"]
            if("command_name" in from_file_dict):
                created_widget["command_name"] = from_file_dict["command_name"]
            edit_widget_attributes(created_widget)
    
        active_widgets.append(created_widget)
        add_bindings()

        return created_widget

def bring_up_a_layer():
    global current_widget
    move_widget_down_in_frame(current_widget)

def bring_down_a_layer():
    global current_widget
    move_widget_up_in_frame(current_widget)

def new_right_click_menu(master):    
    RightClickMenu = tk.Menu(master, tearoff=False, background='#565b5e', fg='white', borderwidth=0, bd=0)
    RightClickMenu.add_command(label="Duplicate", command=duplicate_current_widget)
    RightClickMenu.add_command(label="Edit", command=edit_current_widget)
    RightClickMenu.add_command(label="Delete", command=destroy_current_widget)
    RightClickMenu.add_command(label="Bring Up One Layer", command=bring_up_a_layer)        # todo these are currently reversed in viewport, e.g. higher in active_widgets == drawn first, whereas it should be the opposite
    RightClickMenu.add_command(label="Bring Down One Layer", command=bring_down_a_layer)

    return RightClickMenu

def draw_widgets(new_canvas = None, update_widgets = False, delete_existing_widgets=False):
    global background
    try:
        background
    except:
        background = None
    if(new_canvas):
        right_click_menu=new_right_click_menu(new_canvas)

    if(delete_existing_widgets):
        for app_widgets in app.winfo_children():
            if((app_widgets.nametowidget(app_widgets) != background)):
                app_widgets.destroy()
    # ic(export_preferences.get('Root Name:')['value'])

    app_ref = new_canvas

    for widget in active_widgets:
        if(new_canvas):
            kwargs = widget.get('kwargs')
            # ic(widget.get('master'))
            
            if(widget.get('master') != export_preferences.get('Root Name:')['value']):
                temp = [i.get('widget') for i in active_widgets if i['widget_id'] == widget.get('master')][0] # reference of master widget
                new_canvas = app.nametowidget(str(temp))
                
            else:
                # ic("check passed!")
                new_canvas = app_ref
            # ic(new_canvas)
            widget['widget'] = None
            widget['widget'] = widget_types.get((widget.get('widget_name')))(new_canvas, **kwargs)
            if('image' in widget):
                widget['widget'].configure(image=widget["image"])
            if(widget['widget_name'] == "Option Menu"):
                widget['widget'].configure(state="disabled")
            widget['has_bindings'] = False
            widget.get('widget').unbind("<Button-3>")
            widget.get('widget').unbind("<Button-1>")
            widget.get('widget').unbind("<B1-Motion>")
            widget.get('widget').unbind("<Double-Button-1>")
                        
        x,y = widget.get('location')
        widget.get('widget').place(x=x,y=y)
    if(update_widgets and not new_canvas):
        add_bindings(draw=False)
    if(update_widgets and new_canvas):
        add_bindings(draw=False, updated_menu=right_click_menu)
        
def generate_file(path, export_preferences):
    boiler_handler = BoilerPlateHandler()
    boiler_handler.set_preferences(export_preferences)
    app_height = entry_height.get()
    app_width = entry_width.get()
    
    boiler_handler.check_for_images(active_widgets, file_selector.get_path())
    boiler_handler.check_for_commands(active_widgets)

    file_data = ""
    try:
        if(app_height != "" and app_width != ""):
            file_data += boiler_handler.imports()
        else:
            CTkError(editor_window,error_message="App Dimensions Cannot Be Empty!", button_1_text="Okay")
            return

        theme = combo_theme_selector.get().lower()
        theme = theme.replace(" ", "-")

        file_data += boiler_handler.basic_app_window(app_width, app_height, file_selector.get_path(), path, entry_name.get(), theme, active_widgets_list=active_widgets)

        for widget in active_widgets:
            file_data += (str(boiler_handler.widget_code(widget, path)))

        file_data += boiler_handler.main_loop()

        with open(f"{path}/{export_preferences.get('File Name:')['value']}.py", 'w') as f:   # separate f.write functions to not clog down this file any more than it needs to be
            f.write(file_data)
            CTkError(editor_window,title="Successful!",size_x= 150,size_y=180, error_message=f"Successful write at {path}/{export_preferences.get('File Name:')['value']}.py", button_1_text="Okay")
    except Exception as ex:
        CTkError(editor_window,error_message=f"Error occured: {ex}\n Please Report On Github", button_1_text="okay", size_x=150, size_y=180)

def save_logic():
    global export_preferences
    curr_dir = os.getcwd()
    path = filedialog.askdirectory(initialdir=curr_dir)
    if(path != ""):
        generate_file(path, export_preferences)

def find_children(widget):
    output = []
    for widgets in active_widgets:
        # ic(widgets["master"])
        if(widgets['master'] == widget["widget_id"]):
            output.append(widgets)
    # ic(output)
    return output

def duplicate_current_widget():
    global current_widget
    duplicate = create_widget(current_widget.get("widget_name"), True, current_widget, kwarg_list=current_widget.get("kwargs"), widget_command=current_widget.get("command_name"))
    if(current_widget['widget_name'] == "Frame"):
        for widget in find_children(current_widget):
            ic(widget)
            create_widget(widget.get("widget_name"), True, widget, kwarg_list=widget["kwargs"], master=duplicate["widget_id"])

def edit_widget_attributes(widget):
    properties = widget.get("kwargs")
    if("image_path" in properties):
        widget["image_path"] = properties["image_path"]
        properties.pop("image_path")
    if("image_height" in properties or "image_width" in properties):
        widget["image_size"] = (properties["image_width"], properties["image_height"])
        properties.pop("image_width")
        properties.pop("image_height")
    if("command" in properties):
        widget["command_name"] = properties["command"]
        properties.pop("command")

    try:
        widget.get("widget").configure(**properties)
    except Exception as ex:
        CTkError(editor_window, error_message=f"Error occured: {ex}\n Please Report On Github", button_1_text="Okay", size_x=150, size_y=180)
    
    if(widget.get("image_path") is not None):
        image = ctk.CTkImage(dark_image=Image.open(widget.get("image_path")), size=(widget.get("image_size")))
        widget["image"] = image 
        widget["widget"].configure(image=image)

def open_editor_window(widget):
    ctk.set_default_color_theme('blue')
    global attribute_editor_window
    if(attribute_editor_window):
        # ic("Cheeck")
        attribute_editor_window.change_edited_widget(widget)
    else:
        # ic("FooBar")
        attribute_editor_window = AttributeEditorWindow(editor_window, widget_to_edit=widget, apply_settings_cb=edit_widget_attributes, app_pos = (app.winfo_geometry()))
    set_theme_to_user_theme()

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
    theme = 'blue'
    ctk.set_default_color_theme(theme)
    export = ExportPreferenceHandler(editor_window, pref_dict=export_preferences)
    export.set_set_preferences_cb(lambda: set_preferences(export.get_preferences_dict()))  # the button needs a reference to the function to update the export preferences

def save_as_project(args=None):
    global save_path
    curr_dir = os.getcwd()
    files = [('Json File', '*.json'), ('All Files', '*.*')]

    save_path = (filedialog.asksaveasfile(initialdir=curr_dir, defaultextension=files, filetypes=files, title="Save Project As"))
    if(save_path is None):
        return
    else:
        save_path = save_path.name
    if(save_path.split('.')[-1] != "json"):
        CTkError(editor_window,title="Are you sure?", error_message="Saved type is not a .json. Are you sure what you're doing is worth it?", button_1_text="Yes", size_x=150, size_y=150)
        return
    if(save_path != ""):
        save_project()
    
def save_project(args=None):
    if(save_path == ""):
        save_as_project()
        if(save_path is None):
            return
    
    data_to_save = []

    try:
        data_to_save = ["This is some data regarding a custom tkinter application"]
        data_to_save.append(f"The file has dimensions of ({entry_width.get()}x{entry_height.get()}) and a title of {entry_name.get()}, and has a theme of {combo_theme_selector.get()}. It has an icon path of {file_selector.get_path()}")
        for active_widget in active_widgets:
            save = [active_widget["widget_name"], active_widget["widget_id"], active_widget["location"], active_widget["kwargs"]]
            if("command_name" in active_widget):
                save.append(active_widget["command_name"])
            else:
                save.append(None)
            if("image_path" in active_widget):
                save.append(active_widget["image_path"])
                save.append(active_widget["image_size"])
            save.append(active_widget["master"])
            data_to_save.append(save)
    except Exception as ex:
        CTkError(error_message=f"Error occured: {ex}\n Please Report On Github", button_1_text="okay", size_x=200, size_y=120)
        return
    # so we don't overwrite files if the data isn't generated properly
    with open(f"{save_path}", "w") as write_file:
        json.dump(data_to_save, write_file, indent=2)

def open_project(args=None):
    global active_widgets
    curr_dir = os.getcwd()
    file_path = filedialog.askopenfile(initialdir=curr_dir, filetypes=[("Json File","*.json")])
    if(file_path is not None):
        with open (str(file_path.name), "r") as file:
            try:
                new_data = json.load(file)
            except json.decoder.JSONDecodeError:
                CTkError(editor_window, error_message="Bad File!",button_1_text="Okay")                
            if(new_data[0] != "This is some data regarding a custom tkinter application"):
                CTkError(editor_window, error_message="This file is not correct!",button_1_text="Okay")
                return
            else:
                active_widgets = []
                frame_widgets.clear_grid()

                width, height = new_data[1].split("(")[1].split(")")[0].split('x')      # dealing with window settings data
                entry_width.delete(0, (len(str(width)) -1 ))
                entry_width.insert(0, int(width))
                entry_width.delete(len(str(entry_width.get())) - 1, tk.END)
                entry_height.delete(0, (len(str(height)) -1 ))
                entry_height.insert(0, int(height))
                entry_height.delete(len(str(entry_height.get())) - 1, tk.END)

                title, theme = new_data[1].split("title of ")[1].split(', and has a theme of ')
                theme = theme.split(".")[0]
                entry_name.delete(0, tk.END)
                entry_name.insert(0, title)
                combo_theme_selector.set(theme)
                ico_path = new_data[1].split("path of ")[1]
                try:
                    if(ico_path != ""):
                        file_selector.get_entry_element().delete(0, tk.END)
                        file_selector.get_entry_element().insert(0, ico_path)
                except IndexError:  # backwards compatibility
                    pass

                apply_window_settings()         # deal with themes

                for item in new_data[2:]: # rest of data is widgets
                    if(len(item) == 5):
                        item_dict = {"widget_id": item[1], "location":item[2],"kwargs": item[3]}
                    elif(len(item)==6):
                        item_dict = {"widget_id": item[1], "location":item[2],"kwargs": item[3], "command_name": item[4]}
                    else:
                        item_dict = {"widget_id": item[1], "location":item[2],"kwargs": item[3], "command_name": item[4], "image_path": item[5], "image_size": tuple(item[6])}
                    if("font" in item_dict["kwargs"]):
                        item_dict["kwargs"]["font"] = tuple(item_dict["kwargs"]["font"])
                    if(find_widget_reference_with_name(item[-1]) is not None):
                        create_widget(item[0], False, None, from_file=True, from_file_dict=item_dict, master = item[-1])
                    else:
                        create_widget(item[0], False, None, from_file=True, from_file_dict=item_dict)        
                
    else:
        return    

def validate(action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        # if value_if_allowed:
        #     try:
        #         int(value_if_allowed)
        #         return True
        #     except ValueError:
        #         return False
        # else:
        #     return False
    return True

def toggle_resize(*args):
    if(args):
        if(switch_resizable_window.get()):
            switch_resizable_window.deselect()
        else:
            switch_resizable_window.select()
    global app
    if(switch_resizable_window.get()):
        app.resizable(True, True)
    else:
        app.resizable(False, False)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

theme = "blue"

editor_window = ctk.CTk()
editor_window.geometry("400x530")
editor_window.resizable(width=False, height=False)
editor_window.title("CTKEasyEditor")
icon = ImageTk.PhotoImage(file = 'scripts/assets/icon.png')
editor_window.after(200, lambda: editor_window.iconphoto(False, icon))

# menubar settings starts
menu = CTkMenuBar(master=editor_window)

menubar_button_file = menu.add_cascade("File")
menubar_button_edit = menu.add_cascade("Edit")

dropdown_file = CustomDropdownMenu(widget=menubar_button_file, corner_radius=0)
dropdown_file.add_option(option="Save                           (ctrl + S)", command=save_project)
editor_window.bind_all("<Control-s>", save_project)
dropdown_file.add_option(option="Save As...       (ctrl + shift + S)", command=save_as_project)
editor_window.bind_all("<Control-Shift-S>", save_as_project)
dropdown_file.add_option(option="Open Project...         (ctrl + O)", command=open_project)
editor_window.bind_all("<Control-o>", open_project)
dropdown_file.add_separator()
dropdown_file.add_option(option="Export as .py", command=save_logic)

editor_window.bind_all("<Control-g>", toggle_grid)
editor_window.bind_all("<Control-Right>", lambda e: change_grid((True, False)))
editor_window.bind_all("<Control-Left>", lambda e: change_grid((True, True)))
editor_window.bind_all("<Control-Down>", lambda e: change_grid((False, True)))
editor_window.bind_all("<Control-Up>", lambda e: change_grid((False, False)))

dragging = False

save_path = ""

dropdown_file = CustomDropdownMenu(widget=menubar_button_edit, corner_radius=0)
dropdown_file.add_option(option="Preferences...", command=export_preferences_editor)
# menubar settings end

# windows settings starts
label_window_settings = ctk.CTkLabel(editor_window, text="Window Settings")
label_window_settings.pack(anchor="w", padx=15)

frame_window_settings = ctk.CTkFrame(editor_window, width=380, height=170)

vcmd = (editor_window.register(validate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

window_width = tk.Variable()
window_height = tk.Variable()

label_entry_width = ctk.CTkLabel(frame_window_settings, text="px")
label_entry_width.place(x=200, y=10)
label_left_entry_width = ctk.CTkLabel(frame_window_settings, text="Width")
label_left_entry_width.place(x=10, y=10)
entry_width = ctk.CTkEntry(frame_window_settings,placeholder_text = "Width of Window", validate = 'key', validatecommand=vcmd, textvariable=window_width)
entry_width.place(x=55, y=10)
entry_width.insert(0, 500)

entry_height = ctk.CTkEntry(frame_window_settings, placeholder_text= "Height of Window", validate = 'key', validatecommand=vcmd, textvariable=window_height)
entry_height.place(x=55, y=40)
label_left_entry_height = ctk.CTkLabel(frame_window_settings, text="Height")
label_left_entry_height.place(x=10, y=40)
label_entry_width = ctk.CTkLabel(frame_window_settings, text="px")
label_entry_width.place(x=200, y=40)
entry_height.insert(0, 500)

entry_name = ctk.CTkEntry(frame_window_settings, placeholder_text= "App Name")
entry_name.place(x=55, y=70)
label_left_name = ctk.CTkLabel(frame_window_settings, text="Title")
label_left_name.place(x=10, y=70)

file_selector = CTkFileSelector(frame_window_settings,entry_width=115, entry_padding=(20, 5), label="Icon")
file_selector.place(x=10, y=100)

label_theme_selection = ctk.CTkLabel(frame_window_settings, text="Select a theme:")
label_theme_selection.place(x=250, y=70)
combo_theme_selector = ctk.CTkSegmentedButton(frame_window_settings, values=["Blue", "Dark Blue", "Green"],height=30)
combo_theme_selector.place(x=215, y=100)

combo_theme_selector.set('Blue')

button_apply_settings = ctk.CTkButton(frame_window_settings, text="Apply Settings", width=100, height = 60, corner_radius=20, command=apply_window_settings)
button_apply_settings.place(x=250, y = 10)

switch_resizable_window = ctk.CTkSwitch(frame_window_settings, text="Window Resizable? // Only Editing Window, not final app", command=toggle_resize)
switch_resizable_window.place(x=10, y= 140)

editor_window.bind_all("<Control r>", toggle_resize)

frame_window_settings.pack(pady=0)
# windows settings end

app = None
app = create_app_window()

# active widgets ui begins, will reimplement as a tree later: https://github.com/TomSchimansky/CustomTkinter/discussions/524
label_active_widgets = ctk.CTkLabel(editor_window, text="Active Widgets")
label_active_widgets.place(x=15, y=230)
optionmenu_add_widget = ctk.CTkOptionMenu(editor_window, values=[item for item in widget_types.keys()], width = 30, height=20, command=create_widget)
optionmenu_add_widget.place(x=390, y = 243, anchor="e")

frame_widgets = WidgetHandler(editor_window, width=355, height=250)

active_widgets = []

frame_widgets.place(x=10,y=260)
# active widgets ui ends

current_widget = None

# Right Click Menu Begins
RightClickMenu = new_right_click_menu(app)
# Right Click Menu Ends

attribute_editor_window = None
attributes_is_active = False

app.bind("<1>", lambda event: event.widget.focus_set())

editor_window.mainloop()