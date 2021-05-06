# Theme Saver
This is a python program whose aim is to help you save, load and share your different linux rices. 

## What Is A Linux Rice 
What is a linux rice you may ask ? The term 'rice' is used to describe a person's unix deskton where someone has customized their desktop such as the icons, panels, or system interface. A great place to find different linux rice is the r/unixporn subreddit. 

## Why Should You Use The App
Now why should you use the themesaver app ? Setting up a rice takes a lot of work. You need to install the themes copy themes to the specific folders and if you find a rice you like it could be a little hard copying the file to the specific place if your a noob to ricing. Wont it be simple if you could just link to one file which you can install on your system with one click without wasting your time copy pasting the several dotfiles. 

## Installation
If the app has intrigued you you can install it by running this command in a terminal to install themesaver. ***Note***: This only works on `xfce` or `LXDE`.
```
wget -qO- https://raw.githubusercontent.com/techcoder20/ThemeSaver/main/install.sh | bash
```

## Uninstallation
If you dont like themesaver for some reason you can uninstall by running this command in a terminal.
```
themesaver uninstall
```

## Features/Terminal Usage
These are a list of features which can use and also the syntax you need to use while running the commands in a terminal.
1. `themesaver save [SlotName]`   
Save any new slot

2. `themesaver load [SlotName]`   
Load any saved slot

3. `themesaver del [SlotName]`  **or** `themesaver delete [SlotName]`  
Delete any saved slot

4. `themesaver ls`  **or** `themesaver list`  
List all saved slots

5. `themesaver gui`   
Loads gui for themesaver. There is a desktop shortcut too.

5. `themesaver help`  
Prints list of available arguments

6. `themesaver import [FilePath]`  
Import a slot (Does not work on LXDE)

7. `themesaver export [SlotName] [FilePath]`  
Export existing slot (Does not work on LXDE)

