import shutil
import os
from icecream import ic

class BoilerPlateHandler():
    def __init__(self):
        self.preferences = {}
        self.ctk_module = ""
        self.tk_module = ""
        self.need_images = False
        self.need_commands = False

    def set_preferences(self, dict):
        self.preferences = dict
        self.ctk_module = self.preferences.get('CustomTkinter Module Name:')['value']
        self.tk_module = self.preferences.get('Tkinter Module Name:')['value']
        self.root = self.preferences.get('Root Name:')['value']
        self.export_oop = self.preferences.get("Export as OOP?")['value']
        self.classname = self.preferences.get("Class Name (OOP Only):")['value']

        if(self.export_oop and self.classname == ""):
            self.classname = f"{self.root[:-1].upper()}{self.root[:1]}"
    
    def check_for_images(self, active_widgets_list, icon_path):  # this flag determines whether or not we need to include the PIL Image libraries
        if(icon_path):
            self.need_images = True
            return
        for active_widget in active_widgets_list:
            if("image_path" in active_widget):
                self.need_images = True
                return
        else:
            self.need_images = False

    def check_for_commands(self, active_widgets_list):  # this flag determines whether or not we need to write out the functions for the command of buttons
        for active_widget in active_widgets_list:
            try:
                if('command_name' in active_widget):
                    self.need_commands = True
                    return
            except KeyError:
                pass
        self.need_commands = False
        return

    def write_callbacks(self, active_widgets_list):
        text = ''
        if(self.need_commands):
            for active_widget in active_widgets_list:
                if("command_name" in active_widget and active_widget["command_name"] is not None):
                    command_to_write = active_widget.get("command_name")
                    command_to_write = command_to_write.replace(" ", "_")
                else:
                    command_to_write = None

                if(command_to_write is not None and text.find(str(command_to_write)) == -1):   # check if widget has a command= property associated to it, or if the command callback already exists
                    text += f"""{'    ' if self.export_oop else ''}def {command_to_write} ({'self' if self.export_oop else ''}):
{'      ' if self.export_oop else '  '} ## callback code goes here
{'      ' if self.export_oop else '  '}return\n"""
        
        return text

    def imports(self):
        text = f"import customtkinter as {self.ctk_module}\n"
        if(self.need_images):
            text += f"from PIL import ImageTk, Image\n"     
        text += f"import tkinter as {self.tk_module}\n"
        return text

    def basic_app_window(self,size_x, size_y, icon_path, output_src, title="app", theme='blue', active_widgets_list=[]):
        if(title == ''): title = self.root
        callbacks = self.write_callbacks(active_widgets_list)
        self.callback_text = f"\n{callbacks}\n"
        if(self.export_oop):
            text = f"""
class {self.classname}({self.ctk_module}.CTk): {self.callback_text if self.callback_text != "" else ''}
    def __init__(self):
        super().__init__()
        ## Geometry and Theme Settings
        {self.ctk_module}.set_appearance_mode("dark")     # todo add these
        {self.ctk_module}.set_default_color_theme("{theme}")

        self.geometry("{size_x}x{size_y}")
        self.title("{title}")"""
            if(icon_path):
                filename = icon_path.split("/")[-1]
                try:
                    shutil.copyfile(icon_path, f"{output_src}/assets/{filename}")
                except FileNotFoundError:
                    os.makedirs(f"{output_src}/assets")
                    shutil.copyfile(icon_path, f"{output_src}/assets/{filename}")
                except shutil.SameFileError:
                    pass    # file exists in directory where we're trying to write to, so we don't care
                text += f"""
        ## Icon gets set here        
        self.icon_path = ImageTk.PhotoImage(file="{output_src}/assets/{filename}")
        self.wm_iconbitmap()
        self.iconphoto(True, self.icon_path)"""
            return f"{text}\n"
        else:
            text =f"""
{self.write_callbacks(active_widgets_list)}
            
## Geometry and Theme Settings
{self.ctk_module}.set_appearance_mode("dark")     # todo add these
{self.ctk_module}.set_default_color_theme("dark-blue")

{self.root} = {self.ctk_module}.CTk()
{self.root}.geometry("{size_x}x{size_y}")
{self.root}.title("{title}")"""
        if(icon_path):
            filename = icon_path.split("/")[-1]
            try:
                shutil.copyfile(icon_path, f"{output_src}/assets/{filename}")
            except FileNotFoundError:
                os.makedirs(f"{output_src}/assets")
                shutil.copyfile(icon_path, f"{output_src}/assets/{filename}")
            except shutil.SameFileError:
                pass    # file exists in directory where we're trying to write to, so we don't care
            text += f"""
## Icon gets set here        
icon_path = ImageTk.PhotoImage(file="{output_src}/assets/{filename}")
{self.root}.wm_iconbitmap()
{self.root}.iconphoto(True, icon_path)"""
        return text + "\n"
    

    def widget_code(self, widget, output_src): # take in widget, create an instance of it using its name, configure all of its kwargs,
        text = ""
        kwargs = widget.get("kwargs")

        arguments = f"master={self.root}"
        self.image_exists = False

        widget_name = widget.get("widget_id")
        widget_name = widget_name.replace(" ", "_")

        if("image_path" in widget):
            self.image_exists = True
            arguments += f",image={'self.' if self.export_oop else ''}image_{widget_name}"

        for key, arg in kwargs.items():
            arguments += ","
            arguments += str(key)
            arguments += "="
            if isinstance(arg, str):
                arguments += f'"{arg}"'  # Add quotation marks around the string
            else:
                arguments += str(arg)

        if(self.image_exists):
            image_path = widget["image_path"]
            filename = image_path.split("/")[-1]
            im_x, im_y = widget["image_size"]
            try:
                shutil.copyfile(image_path, f"{output_src}/assets/{filename}")     # copy image file to new directory
            except FileNotFoundError: # assets folder doesn't exist, so we make one
                os.makedirs(f"{output_src}/assets")
                shutil.copyfile(image_path, f"{output_src}/assets/{filename}") 
            except shutil.SameFileError:
                pass
            text += f"\n{'        self.' if self.export_oop else ''}image_{widget_name} = {self.ctk_module}.CTkImage(dark_image=Image.open('{output_src}/assets/{filename}'), size=({im_x}, {im_y}))"

        if(self.export_oop):
            arguments = arguments.replace( f"master={self.root}", "self")

        x,y = widget.get("location")

        widget_type = widget.get("widget_type").split(".")[-1][:-2]
        if(widget_type == 'CTkImageFrame'):
            widget_type = 'CTkLabel'
            arguments += ',text=""'
        
        if("command_name" in widget and widget["command_name"] is not None):
            widget_command = widget.get('command_name').replace(' ', '_')
        else:
            widget_command = None

        text += f"""
{"        self." if self.export_oop else ""}{widget_name} = {self.ctk_module}.{widget_type}({arguments}{f",command={'self.' if self.export_oop else ''}{widget_command}" if widget_command is not None else ""})
{"        self." if self.export_oop else ""}{widget_name}.place(x={x}, y={y})\n"""
        return text

    def main_loop(self):
        text = "\n"
        if(self.export_oop):
            text += f"{self.root} = {self.classname}()"
        text += f"\n{self.root}.mainloop()"
        return text

