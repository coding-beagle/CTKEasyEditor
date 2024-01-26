import shutil
from icecream import ic

def imports(ctkmodulename="ctk", tkmodulename="tk"):
    text = f"import customtkinter as {ctkmodulename}\n"
    text += f"from PIL import ImageTk, Image\n"     # probably a smart way of detecting whether or not images exist
    text += f"import tkinter as {tkmodulename}\n"
    return text
    
def basic_app_window(size_x, size_y, icon_path, output_src, title="app", modulename="ctk"):
    text =f"""
## Geometry and Theme Settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")
root = {modulename}.CTk()
root.geometry("{size_x}x{size_y}")
root.title("{title}")"""
    if(icon_path):
        filename = icon_path.split("/")[-1]
        try:
            shutil.copyfile(icon_path, f"{output_src}/{filename}")
        except shutil.SameFileError:
            pass    # file exists in directory where we're trying to write to, so we don't care
        text += f"""
## Icon gets set here        
icon_path = ImageTk.PhotoImage(file="{output_src}/{filename}")
root.wm_iconbitmap()
root.iconphoto(True, icon_path)
"""
    return text + "\n"
        

def widget_code(widget, modulename="ctk"): # take in widget, create an instance of it using its name, configure all of its kwargs,
    text = ""
    kwargs = widget.get("kwargs")

    arguments = "master=root"
    image_exists = False
    
    widget_name = widget.get("widget_id")
    widget_name = widget_name.replace(" ", "_") 

    for key, arg in kwargs.items():
        if(key == "image_path" or key == "image_size_x" or key == "image_size_y"):
            image_exists = True
            if(arguments.find(",image=image") == -1):
                arguments += f",image=image_{widget_name}"
            continue
        arguments += ","
        arguments += str(key)
        arguments += "="
        if isinstance(arg, str):
            arguments += f'"{arg}"'  # Add quotation marks around the string
        else:
            arguments += str(arg)

    if(image_exists):
        text += f"image_{widget_name} = {modulename}.CTkImage(dark_image=Image.open('{kwargs.get('image_path')}'), size=({kwargs.get('image_size_x')}, {kwargs.get('image_size_y')}))"

    x,y = widget.get("location")
    
    text += f"""
{widget_name} = {modulename}.{widget.get("widget_type").split(".")[-1][:-2]}({arguments})
{widget_name}.place(x={x}, y={y})\n
"""
    return text

def main_loop():
    return "root.mainloop()\n"
