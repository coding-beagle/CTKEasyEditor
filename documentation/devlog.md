**19-03-2024**

Todo:

- Frames not snapping properly?

**11-03-2024**

Todo:

- Errors get thrown if widget is below master in active_widgets
  - I.e. Button gets created first, then frame. When button master is set to frame, we delete everything, and then redraw a new. Button gets created before frame is drawn, which gives error.
- Similarly, when master widget is deleted, children widgets are not deleted from active_widgets

Completed:

- Added window resizing functionality
- Refactored CTkError to display in middle of screen
- Made good headway into resolving issues with widget height reordering

**01-03-2024**

**06-03-2024**

Todo:

- Errors get thrown if widget is below master in active_widgets
  - I.e. Button gets created first, then frame. When button master is set to frame, we delete everything, and then redraw a new. Button gets created before frame is drawn, which gives error.
- Similarly, when master widget is deleted, children widgets are not deleted from active_widgets

Completed:

- Added basic functionality for master switching

**01-03-2024**

Todo: 

- Fix widgets editing others

Completed:
- Fixed duplicate widget editing 

**03-02-2024**
Todo:

-Complete documentation

Bugs:

- **(Fixed)** files saving as "None" when no path was selected

Completed:
- Added all new widget properties
- Changed widget properties window placement

**02-02-2024**
Todo:
- Add all of the new properties to widgets

Completed:
- Refactored settingseditor.py

**30-01-2024**
Todo:

- Refactor settingseditor.py to have more granular control over widget properties
- Might need to add custom theme support tomorrow

Bugs:

- **(Fixed)** First widget was not being loaded on new file

Completed:

- Refactored how widgets handle images
- Subsequently fixed shifting layer of images
- Reworked saving and opening file logic, now generates text first and if errors occur we don't write the file.
- Frozen file and added to .exe

**29-01-2024**

Completed:

- Active Widget Handler optimised

**28-01-2024**

Todo:

- Add custom theme support
- Active Widget Handler needs some optimisations

Bugs encountered:

- **(Fixed)** Lots of error messages but the app still seems to work fine
- **(Fixed)** The error messages were because the app was not working fine.
- **(Fixed)** Error messages were being caused by app window being duplicated in create_app_window() function
- Icon not working now

Completed:

- Fixed editor window of elements opening a new window when clicked
- Changed the widget IDs to be based on the numer of those elements, instead of number of total elements
- 'Apply Settings' now correctly reloads all of the widgets when the app window is closed (wasn't working before)
- boilerplate.py indenting issues for image objects
- Added basic theme management
- Added element rearranging (this is currently backwards compared to photoshop or other standard, in theory widgets should have higher draw priority the more they are on top)
- Added project saving

**27-01-2024**

Todo:

- Add user friendliness features, i.e. being able to rearrange element hierarchy
- Theme editor / theme selector implementation
- r/therewasanattempt to try and add line drawings to show snap

Bugs encountered:

- **(FIXED)** Duplicate on widgets with images, 'image_path', 'image_size_x', 'image_size_y' are being unpacked
- **(FIXED)** Duplicate on widgets with different font sizes causes other properties to not be inherited (likely as a result of the font size handling in settingseditor.py)

Completed:

- Added preference window with dynamic element adjusting
- OOP export implemented
- Added snapping to other widgets (needs to be fine tuned)

**26-01-2024**

Big progress day, uni exams are done

Todo:

- Continue adding the editing menus for each widget (the specific ones are annoying)
- Add Edit -> Preferences
- - Preferences should contain things like export type (OOP mode or Procedural, etc),
- - Also things like what is the ctk library called
- Add Editor saving system, i.e. File -> save, File -> open etc, (unsure of implementation)
- Active widget hierarchy adjustments (one fears the thought of touching activewidgethandler.py)
- Theme editor implementation

Bugs encountered:

- **(FIXED)** Need to reopen window with all drawn elemnts when it is closed
- Not a bug, but figure out a way to only import PIL libraries if it is needed, e.g. if there is an image object or something

Completed:

- Added dynamic system for adding widget editing
- Completed a few of the important widgets
- Added export to .py (only for procedural)

**25-01-2024**

Todo:

- God please fix the code why is it so messy and bad and ill have to go through and reformat it again why did i choose python devleopemneinodjkosjopisdojiiogio;sg
- Segmented button doesn't have drag functionality implemented (not in creation list for now)
- TabView not implemented yet either
- Finish widget editing functionality
- Add logic to do naming (i.e. click on widget in active widgets and then rename that)
- Add logic to move around active widgets in active tab (more drag and drop????)

Bugs encountered:

- Scrollable Frame doesn't delete properly

Completed:

- Fixed widget handler
- Added a simple file selector widget
- Added widget creation functionality
- Added export to .py for basic root boilerplate
- Started with widget editing functionality

**24-01-2024**

Todo:

- Fix Widget Handler

Bugs encountered:

- **(FIXED)** Right click menu not completed functionality
- **(FIXED)** Need to add widget adding functionality
- **(FIXED)** Improve Widget Handler

Completed:

- Dragging elements
- Right Click Menu Implemented

**23-01-2024**

Todo:

- Fix dragging elements (probably need to refactor the mouse moving code)

Bugs encountered:

- **(FIXED)** Fix lag on clicking top bar

Completed:

- Added basic functionality
