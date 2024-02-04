# CTKEasyEditor

An easy GUI editor for CustomTkinter in Python - think of it as a boilerplate generation tool for your CustomTkinter projects.

I've found the most time consuming part of my app development using tkinter comes from repeatedly running and closing apps to check whether or not ui elements are positioned properly. This tool aims to fix this.

Thanks to Tom Schimansky for their CustomTkinter development. Find the original page for CustomTkinter here: https://customtkinter.tomschimansky.com/
The original documentation on CustomTkinter is excellent, and I recommend it for anyone starting off and struggling with the usage of this tool.

**Note** this is still a work in progress:

![Alt text](/screenshots/ss1.png "Example Screenshot")

Zip and Installer should be the most recent stable release, the python scripts are the most recent experimental releases.

Files, Windows Only (I can't figure out how to freeze to mac format). Just click on links and then press download:

- [Download Installer](https://github.com/coding-beagle/CTKEasyEditor/blob/main/Files/installer-windows/CTkEasyEditor-1.1-win64.msi)

- [Download As Zip](https://github.com/coding-beagle/CTKEasyEditor/blob/main/Files/zip-windows/ctkeasyeditor.zip)

Other platforms must donwload and run python code yourself (I can't figure out cx_freeze):

[Advanced Install Instructions](documentation\install.md)

Example Usage:

![Alt text](/screenshots/usage1.png "Usage Screenshot")

This tool is still in development, please report any bugs or issues under the issues tab.
Right now it seems to work okay, and the current implementation includes:

- Easy Application Window Settings Management
- Easy Active Widgets manager
- Dragging and snapping of widgets in relation to other widgets and center lines (can be adjusted based on hotkeys)
- Widget Editing 
- Use of Built In Themes for CTK
- Export to OOP and Procedural files (OOP by default)
- Preference Handler (i.e. names of modules, root element, etc)
- Saving and opening of projects

To be implemented soon:

- Custom Theme Support
- Some widgets don't play nice currently, namely CTkScrollableFrame, CTkTreeView and CTkSegmentedButton. I'll add these when I can get them to a stable version and playing nice.

Hotkeys & Shortcuts:

- CTRL --> Hold while dragging to prevent widget from snapping into place
- ALT --> Only snap widget to other widgets, not the app center lines
- Double Click --> Opens editor window on that widget
- Right Click --> Opens context menu on widget (edit, duplicate, delete)

- The standard save, save as and open hotkeys, i.e. ctrl+s, ctrl+shift+s, ctrl+o, etc

Yes, the UI looks bad right now. Yes, I will rework it using this tool when I make a version of it that works adequately.
