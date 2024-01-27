# CTKEasyEditor

An easy GUI editor for CustomTkinter in Python - think of it as a boilerplate generation tool for your CustomTkinter projects.

I've found the most time consuming part of my app development using tkinter comes from repeatedly running and closing apps to check whether or not ui elements are positioned properly. This tool aims to fix this.

Thanks to Tom Schimansky for their CustomTkinter development. Find the original page for CustomTkinter here: https://customtkinter.tomschimansky.com/
The original documentation on CustomTkinter is excellent, and I recommend it for anyone starting off and struggling with the usage of this tool.

**Note** this is still a work in progress:

![Alt text](/screenshots/ss1.png "Example Screenshot")

To install and run (assuming you have git and pip):

```
$ git clone https://github.com/coding-beagle/ctkeasyeditor.git
```

Navigate to scripts, e.g.

```
$ cd ctkeasyeditor
```

Recommended: start a new python virtual environment in this directory:

```
$ python -m venv venv
$ venv/scripts/activate.ps1
```

Install the required packages:

```
$ pip install -r requirements.txt
```

Navigate to scripts and run main.py

```
$ cd scripts
$ python main.py
```

Usage:

![Alt text](/screenshots/usage1.png "Usage Screenshot")

Currently this is just the skeleton and I am experimenting with the design of different elements.
Right now it seems to work okay, and the current implementation includes:

- Easy Application Window Settings Management
- Easy Active Widgets manager
- Drag, and (limited) snapping capability on added widgets
- Widget Editing (without theme management yet)
- Export to OOP and Procedural (OOP by default)
- Preference Handler (i.e. names of modules, root element, etc)

To be implemented soon:

- Some basic theme management
- Improve user-friendliness, e.g. Undos, Save Projects, Improved Snapping Functionality

Hotkeys & Shortcuts:

- CTRL --> Hold while dragging to prevent widget from snapping into place
- ALT --> Only snap widget to other widgets, not the app center lines
- Double Click --> Opens editor window on that widget
- Right Click --> Opens context menu on widget (edit, duplicate, delete)

Yes, the UI looks bad right now. Yes, I will rework it using this tool when I make a version of it that works adequately.

I will add an installer and freeze this into a .exe when I get the tool up to a state when I am happy.
