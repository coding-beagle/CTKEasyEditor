import customtkinter as ctk
import tkinter as tk
from icecream import ic
from CTkError import CTkError

class WidgetName(ctk.CTkFrame):
    def __init__(self, *args,
                 width: int = 200,
                 height: int = 40,
                 widget,
                 edit_button_cb,
                 delete_button_cb,
                 name_change_cb,
                 move_up_cb,
                 move_down_cb,
                 change_master_cb,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.columnconfigure(0, weight=5)  # Label column
        self.columnconfigure(1, weight=5)
        self.columnconfigure(2, weight=1)  # Expanding middle column
        self.columnconfigure(3, weight=0)  # Edit button column
        self.columnconfigure(4, weight=0)  # Delete button column

        self.masters = None
        self.change_master = change_master_cb

        self.widget_ref = widget

        self.mouse_left = False

        self.change_name = name_change_cb

        self.move_up = move_up_cb
        self.move_down = move_down_cb

        self.entry = ctk.CTkEntry(self, width=120)
        self.text = tk.StringVar(self.entry, self.widget_ref.get("widget_id"))
        self.old_name = self.widget_ref.get("widget_id")

        self.entry.configure(textvariable=self.text)
        self.entry.configure(state="disabled")
        self.entry.grid(column=0, row=0, sticky='w', columnspan=1, padx=5, rowspan=2)
        self.entry.bind('<Button-1>', self.edit_text)
        self.entry.bind('<Return>', self.stop_edit_text)
        self.entry.bind('<FocusOut>', self.stop_edit_text)

        self.edit_button = ctk.CTkButton(self, font=('roboto', -20),text="⛭", command=edit_button_cb, width=40, height=40)
        self.edit_button.grid(column=3, row=0, padx=2,pady=2, sticky='e', rowspan=2)
        
        self.remove_button = ctk.CTkButton(self, font=(('roboto', -25)), text="×", command=delete_button_cb, width=40, height=40)
        self.remove_button.grid(column=4, row=0, padx=2,pady=2, sticky='e', rowspan=2)

        self.optionmenu_masters = ctk.CTkOptionMenu(self, font=('roboto', -12), command=lambda e: self.switch_master(e), width=135, height=40, values=["root"],dynamic_resizing=False)
        self.optionmenu_masters.grid(column=1, row=0, padx=3, sticky='e', rowspan=2)

        self.up_button = ctk.CTkButton(self, font=('roboto', -10), text='⮝', width=20,height=10, command=self.move_up)
        self.up_button.grid(column=2, row=0, sticky='ne', pady=(2,0), padx=(0,1))

        self.down_button = ctk.CTkButton(self, font=('roboto', -10), text='⮟', width=20,height=10, command=self.move_down)
        self.down_button.grid(column=2, row=1, sticky='se', pady=(0,2), padx=(0,1))

    def switch_master(self, master):
        try:
            master_ref = [i for i in self.masters if i['Name'] == master][0]
            self.change_master(self.widget_ref, master_ref)
            self.optionmenu_masters.set(master)
        except TypeError:
            self.update_masters()
            self.optionmenu_masters.set(self.masters[0]['Name'])

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

            CTkError(self.master, button_1_text="Okay", error_message="Widgets cannot have the same name!",size_x=150, size_y=120)

        self.entry.configure(state="disabled")
    
    def get_widget(self):
        return self.widget_ref
    
    def update_masters(self):
        self.optionmenu_masters.configure(values=[i['Name'] for i in self.masters])
        try:
            master = [j['Name'] for j in self.masters if self.widget_ref['master'] == j['Name']][0]
            self.optionmenu_masters.set(master)
        except:
            pass


class WidgetHandler(ctk.CTkScrollableFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.scrollFrame = ctk.CTkScrollableFrame(self, height=kwargs.get("height"),width=kwargs.get("width"))
        self.active_widgets = []
        self.active_row_widgets = []
        self.columnconfigure(0, weight=10)

    def add_widget(self, widget, edit_cb, delete_cb, name_change_cb, move_up_cb, move_down_cb, masters_list, change_master_command):
        self.widget_data_dict = {"widget": widget,  "edit_cb": edit_cb, "delete_cb": delete_cb, "name_change_cb": name_change_cb, "move_up": move_up_cb, "move_down": move_down_cb}
        self.active_widgets.append(self.widget_data_dict)
        new_widget = WidgetName(self, height=30,width=300,widget=widget, edit_button_cb=edit_cb, delete_button_cb=delete_cb, name_change_cb=name_change_cb, move_up_cb=move_up_cb,move_down_cb=move_down_cb, change_master_cb=change_master_command)
        self.active_row_widgets.append(new_widget)
        new_widget.grid(row=len(self.active_widgets), sticky='ew')
        self.update_masters_list(masters_list)

    def update_masters_list(self, list):
        for widget in self.active_row_widgets:
            widget.masters = list
            widget.update_masters()

    # def update_grid(self):   # redraws the entire grid
    #     self.active_row_widgets = []
    #     self.clear_grid()
    #     for index,widget in enumerate(self.active_widgets):
    #         self.name = WidgetName(self, height=30,width=300,widget=widget.get("widget"), edit_button_cb=widget.get('edit_cb'), delete_button_cb=widget.get('delete_cb'), name_change_cb=widget.get("name_change_cb"), move_up_cb=widget.get("move_up"),move_down_cb=widget.get("move_down"))
    #         self.name.grid(row=index, sticky='ew')
    #         self.active_row_widgets.append((self.name))
    
    def clear_grid(self):
        for widget in self.active_row_widgets:
            widget.destroy()
        self.active_row_widgets = []
        self.active_widgets = []

    def remove_widget(self, widget):
        for index, row_widget in enumerate(self.active_row_widgets):
            if(row_widget.get_widget()["widget"] == widget):
                self.active_row_widgets[index].destroy()
                self.active_row_widgets.pop(index)
                return

    def swap_widget_from_to(self, from_index, to_index):
        self.active_row_widgets[from_index].grid(row=to_index, sticky='ew')
        self.active_row_widgets[to_index].grid(row=from_index, sticky='ew')
        self.active_row_widgets[from_index], self.active_row_widgets[to_index] = self.active_row_widgets[to_index], self.active_row_widgets[from_index]
        

    def check_widget(self, widget):
        output = False
        for active_widgets in self.active_widgets:
            if widget == active_widgets.get('widget').get('widget'):  # todo fiX 
                return True
        return output
        