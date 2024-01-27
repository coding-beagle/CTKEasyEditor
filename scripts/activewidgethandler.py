import customtkinter as ctk
import tkinter as tk
from icecream import ic

class WidgetName(ctk.CTkFrame):
    def __init__(self, *args,
                 width: int = 200,
                 height: int = 40,
                 widget,
                 edit_button_cb,
                 delete_button_cb,
                 name_change_cb,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.columnconfigure(0, weight=10)  # Label column
        self.columnconfigure(1, weight=1)  # Expanding middle column
        self.columnconfigure(2, weight=0)  # Edit button column
        self.columnconfigure(3, weight=0)  # Delete button column

        self.widget_ref = widget

        self.mouse_left = False

        self.change_name = name_change_cb

        self.entry = ctk.CTkEntry(self)
        self.text = tk.StringVar(self.entry, self.widget_ref.get("widget_id"))
        self.old_name = self.widget_ref.get("widget_id")

        self.entry.configure(textvariable=self.text)
        self.entry.configure(state="disabled")
        self.entry.grid(column=0, row=0, sticky='w', columnspan=1, padx=5)
        self.entry.bind('<Button-1>', self.edit_text)
        self.entry.bind('<Return>', self.stop_edit_text)
        self.entry.bind('<FocusOut>', self.stop_edit_text)

        self.edit_button = ctk.CTkButton(self, font=('roboto', -15),text="⛭", command=edit_button_cb, width=30, height=30)
        self.edit_button.grid(column=2, row=0, padx=2,pady=2, sticky='e')
        
        self.remove_button = ctk.CTkButton(self, font=(('roboto', -20)), text="×", command=delete_button_cb, width=30, height=30)
        self.remove_button.grid(column=3, row=0, padx=2,pady=2, sticky='e')

    def edit_text(self, event):
        self.entry.configure(state="normal")
        self.old_name = self.entry.get()

    def mouse_enter(self, event):
        self.mouse_is_on = True

    def mouse_left(self, event):
        self.mouse_is_on = False

    def stop_edit_text(self, event):
        try:
            self.change_name(self.widget_ref, self.entry.get())
        except NameError:       ## add toplevel error here
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.old_name)

            self.top_level_error = ctk.CTkToplevel()
            self.top_level_error.geometry("250x100")
            self.top_level_error.attributes('-topmost', 'true')
            self.top_level_error.title(f"Error")
            self.top_level_error.resizable(False, False)
            self.text_top_level_error = ctk.CTkLabel(self.top_level_error,text="Widget names cannot\nbe the same!")
            self.text_top_level_error.pack(pady=(20,10))
            self.button_top_level_error = ctk.CTkButton(self.top_level_error, text="Okay", command=lambda: self.top_level_error.destroy())
            self.button_top_level_error.pack(pady=(0,20))

        self.entry.configure(state="disabled")


class WidgetHandler(ctk.CTkScrollableFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.scrollFrame = ctk.CTkScrollableFrame(self, height=kwargs.get("height"),width=kwargs.get("width"))
        self.active_widgets = []
        self.active_row_widgets = []
        self.columnconfigure(0, weight=10)

    def add_widget(self, widget, edit_cb, delete_cb, name_change_cb):
        self.widget_data_dict = {"widget": widget,  "edit_cb": edit_cb, "delete_cb": delete_cb, "name_change_cb": name_change_cb}
        self.active_widgets.append(self.widget_data_dict)
        self.update_grid()

    def update_grid(self):
        self.clear_grid()
        for index,widget in enumerate(self.active_widgets):
            self.name = WidgetName(self, height=30,width=300,widget=widget.get("widget"), edit_button_cb=widget.get('edit_cb'), delete_button_cb=widget.get('delete_cb'), name_change_cb=widget.get("name_change_cb"))
            self.name.grid(row=index, stick='ew')
            self.active_row_widgets.append(self.name)
    
    def clear_grid(self):
        for active_row in self.active_row_widgets:
            active_row.destroy()

    def remove_widget(self, widget):
        for index, active_widget in enumerate(self.active_widgets):
            if(widget == active_widget.get('widget').get('widget')):
                self.active_widgets.pop(index)
                break
        self.update_grid()

    def check_widget(self, widget):
        output = False
        for active_widgets in self.active_widgets:
            if widget == active_widgets.get('widget').get('widget'):  # todo fiX 
                return True
        return output
        