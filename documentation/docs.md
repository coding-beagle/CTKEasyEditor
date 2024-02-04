This is going to sound like the ramblings of a mad man. That's what python does to someone.

**main.py**

<ins>Responsibilities</ins>

- Bring together every element of the app.

</ins>How it accomplishes this</ins>

Editor Window:

- editor_window is the root element
- - The window settings get drawn in the first iteration when running the app.
- - We populate it with all of the different widgets for editing, i.e. all of the entry for window setting, the menubar, the menubar callbacks

App window:

- The App preview window is a ctk.CTkTopLevel widget with master being editor_window. It is created on app start up, and whenever 'apply settings' is pressed.
- - When 'apply settings' is pressed, we check to see if an app element exists, as the toplevel is stored in the global variable 'app'. If it does not, then we create a new instance of 'app' using the create_app_window() function.
- - create_app_window() returns a ctk.CTkTopLevel widget based on the parameters present in frame_window_settings. These values are defaulted to (500, 500, title="", icopath = "") the app window always appears to the right of the editor.
- we then call draw_widgets() to populate the app with widgets (if they exist)

Widget handling

- Widgets are as stored as a dictionary, as part of a global list titled "active_widgets". This stores the fields:
    - "widget" = the actual instance of the ctk widget
    - "location" = a tuple with the x,y coordinates of the widget relative to the app position
    - "wiget_name" = a string of what is used to display in the create widget options (explained later)
    - "widget_type" = a string reference of the ctk widget type, i.e. !ctk.ctkbutton
    - "kwargs" = a dictionary of key value pairs used to generate the boilerplate code and also update attributes of each widget
    - "widget_id" = a string of what the widget is called in the generated code. can be changed by the user
    - "has bindings" = a bool of whether or not the widget instance has bindings, such as right click bindings, drag bindings, etc
    - "image_path" = a string of the path to the image used for the widget (empty if unused)
    - "image_size" = a tuple of the dimensions of the image
    - "image" = the ctk.Image object

- widget_class is a dictionary that maps readable names to the equivalent ctk reference.
- - e.g. Button gets mapped to "ctk.CTkButton"

- create_widget() takes this readable name, as well as optional parameters to be explained later, in order to instatiate an instance of the equivalent ctk type. This is because the option menu (the drop down widget used to add widgets) calls its command= callback with the argument of the option that is selected.
- - e.g. create_widget("Button") is called when the user selects button from the drop down list.
- - this is how we infer to create the correct type, using the widget_class dict.
- - create_widget() then adds an instance of this widget to the middle of the screen and populates the rest of the dictionary with relevant information.
- create_widget() optionally takes the parameters of bool duplicate, widget_to_duplicate and kwarg_list, all of which are used to create duplicates of existing elements
- - When we duplicate widgets, we create a widget of the same type as the widget to be duplicated (which is why we store widget_name, so we can pass in widget.get("widget_name")). This can be improved in the future.
- the created_widget is then added to the list of global active_widgets, where add_bindings() is then called.
  
- add_bindings()
