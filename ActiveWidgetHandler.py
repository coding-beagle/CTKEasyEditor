import customtkinter as ctk
from icecream import ic

class WidgetName(ctk.CTkFrame):
    def __init__(self, *args,
                 width: int = 200,
                 height: int = 40,
                 name: str = "",
                 edit_button_cb,
                 delete_button_cb,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.columnconfigure(0, weight=10)  # Label column
        self.columnconfigure(1, weight=1)  # Expanding middle column
        self.columnconfigure(2, weight=0)  # Edit button column
        self.columnconfigure(3, weight=0)  # Delete button column

        self.text = ctk.CTkLabel(self, text=name)
        self.text.grid(column=0, row=0, sticky='w', columnspan=1, padx=5)

        self.edit_button = ctk.CTkButton(self, font=('helvetica', -15),text="⛭", command=edit_button_cb, width=30, height=30)
        self.edit_button.grid(column=2, row=0, padx=2,pady=2, sticky='e')
        
        self.remove_button = ctk.CTkButton(self, font=(('helvetica', -20)), text="×", command=delete_button_cb, width=30, height=30)
        self.remove_button.grid(column=3, row=0, padx=2,pady=2, sticky='e')


class WidgetHandler(ctk.CTkScrollableFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.scrollFrame = ctk.CTkScrollableFrame(self, height=kwargs.get("height"),width=kwargs.get("width"))
        self.active_widgets = []
        self.active_row_widgets = []
        self.columnconfigure(0, weight=10)

    def add_widget(self, widget, name, edit_cb, delete_cb):
        self.widget_data_dict = {"widget": widget, "name": str(name), "edit_cb": edit_cb, "delete_cb": delete_cb}
        self.active_widgets.append(self.widget_data_dict)
        self.update_grid()

    def update_grid(self):
        self.clear_grid()
        for index,widget in enumerate(self.active_widgets):
            self.name = WidgetName(self, height=30,width=300,name=widget.get('name'), edit_button_cb=widget.get('edit_cb'), delete_button_cb=widget.get('delete_cb'))
            self.name.grid(row=index, stick='ew')
            self.active_row_widgets.append(self.name)
    
    def clear_grid(self):
        for active_row in self.active_row_widgets:
            active_row.destroy()

    def remove_widget(self, widget):
        for index, active_widget in enumerate(self.active_widgets):
            if(widget == active_widget.get('widget')):
                self.active_widgets.pop(index)
                break
        self.update_grid()

    def check_widget(self, widget):
        output = False
        for active_widgets in self.active_widgets:
            if widget == active_widgets.get('widget'):
                return True
        return output
        