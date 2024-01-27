import shutil
from icecream import ic


class BoilerPlateHandler():
    def __init__(self):
        self.preferences = {}
        self.ctk_module = ""
        self.tk_module = ""

    def set_preferences(self, dict):
        self.preferences = dict
        self.ctk_module = self.preferences.get('CustomTkinter Module Name:')
        self.tk_module = self.preferences.get('Tkinter Module Name:')
        self.root = self.preferences.get('Root Name:')

    def imports(self):
        text = f"import customtkinter as {self.ctk_module}\n"
        text += f"from PIL import ImageTk, Image\n"     # probably a smart way of detecting whether or not images exist
        text += f"import tkinter as {self.tk_module}\n"
        return text

    def basic_app_window(self,size_x, size_y, icon_path, output_src, title="app"):
        text =f"""
## Geometry and Theme Settings
{self.ctk_module}.set_appearance_mode("dark")     # todo add these
{self.ctk_module}.set_default_color_theme("dark-blue")

{self.root} = {self.ctk_module}.CTk()
{self.root}.geometry("{size_x}x{size_y}")
{self.root}.title("{title}")"""
        if(icon_path):
            filename = icon_path.split("/")[-1]
            try:
                shutil.copyfile(icon_path, f"{output_src}/{filename}")
            except shutil.SameFileError:
                pass    # file exists in directory where we're trying to write to, so we don't care
            text += f"""
## Icon gets set here        
icon_path = ImageTk.PhotoImage(file="{output_src}/{filename}")
{self.root}.wm_iconbitmap()
{self.root}.iconphoto(True, icon_path)
    """
        return text + "\n"


    def widget_code(self, widget, output_src): # take in widget, create an instance of it using its name, configure all of its kwargs,
        text = ""
        kwargs = widget.get("kwargs")

        arguments = f"master={self.root}"
        image_exists = False

        widget_name = widget.get("widget_id")
        widget_name = widget_name.replace(" ", "_") 

        if(image_exists):
            image_path = kwargs.get('image_path')
            filename = image_path.split("/")[-1]
            shutil.copyfile(image_path, f"{output_src}/{filename}")
            text += f"image_{widget_name} = {self.ctk_module}.CTkImage(dark_image=Image.open('{output_src}/{filename}'), size=({kwargs.get('image_size_x')}, {kwargs.get('image_size_y')}))"

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

        x,y = widget.get("location")

        text += f"""
{widget_name} = {self.ctk_module}.{widget.get("widget_type").split(".")[-1][:-2]}({arguments})
{widget_name}.place(x={x}, y={y})\n
"""
        return text

    def main_loop(self):
        return f"{self.root}.mainloop()"
