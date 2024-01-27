# CTKEasyEditor

An easy GUI editor for CustomTKinter in Python

**Note** this is still a work in progress:

![Alt text](/screenshots/ss1.png "Example Screenshot")

To install and run (assuming you have git and pip):

```
$ git clone https://github.com/coding-beagle/ctkeasyeditor.git
$ pip install -r requirements.txt
$ python main.py
```

Usage:

![Alt text](/screenshots/usage1.png "Usage Screenshot")

Currently this is just the skeleton and I am experimenting with the design of different elements.
Right now it seems to work okay, and the current implementation includes:

- Easy Application Window Settings Management
- Easy Active Widgets manager
- Drag, and (limited) snapping capability on added widgets
- The groundwork for adding all of the editing functionality (only some widgets implemented)
- Export to OOP and Procedural (OOP by default)
- Preference Handler (i.e. names of modules, root element, etc)

To be implemented soon:

- Some basic theme management
- Improve user-friendliness, e.g. Undos, Save Projects, Etc

Yes, the UI looks bad right now. Yes, I will rework it using this tool when I make a version of it that works adequately.
