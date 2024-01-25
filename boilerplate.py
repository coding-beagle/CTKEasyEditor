import shutil

def imports(ctkmodulename="ctk", tkmodulename="tk"):
    text = f"import customtkinter as {ctkmodulename}\n"
    text += f"from PIL import ImageTk\n"
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
        

def widget_code(widget): # take in widget, create an instance of it using its name, configure all of its kwargs,
    text = f"""

"""

def main_loop():
    return "root.mainloop()\n"
