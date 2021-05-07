# Theme Saver
<p align="center">
  <img width="400" src="https://raw.githubusercontent.com/techcoder20/ThemeSaver/main/GUI/Icons/ThemeSaverLogo.png">  
</p>


<p align="center">
  <img src="https://img.shields.io/badge/Platform-GNU/Linux-orange?style=for-the-badge&logo=Linux">

  <img src="https://img.shields.io/badge/DE-XFCE/LXDE-blue?style=for-the-badge&logo=XFCE">

  <img alt="GitHub top language" src="https://img.shields.io/github/languages/top/techcoder20/themesaver?logo=Python&style=for-the-badge">

</p>

<p align="center">
<b> An app to help you save, load and share your different linux rices </b>
</p>

## What Is A Linux Rice ?
The term 'rice' is used to describe a person's unix desktop where someone has customized their desktop such as the icons, panels, or system interface. A great place to find different linux rice is the [r/unixporn](https://www.reddit.com/r/unixporn) subreddit.   

## Why Should You Use This App
Setting up a rice takes a lot of work. You need to install, copy the themes to their specific folders and if you find a rice you like it could be hard copying the file to the specific place if you're a noob in ricing. Wouldnt it be simple if you could just download one file which you can install on your system with one click without wasting your time copy pasting the several dotfiles. 

## Screenshots
![AllWindows](https://raw.githubusercontent.com/techcoder20/ThemeSaver/main/Screenshots/AllWindows.png)

### Main Window
The main window houses the four buttons the `NewSlot`, `ImportSlot`, `LoadSlot`, and the `Shop` (Coming Soon) button.    
![MainWindow](https://raw.githubusercontent.com/techcoder20/ThemeSaver/main/Screenshots/MainWindow.png)

### Save New Slot Window
The Save Slot Window houses one input text box and a confirm button. You can save the current rice by clicking on the confirm button. After you clicked the confirm button wait till you see the a window which says `Finished Saving`. If you try to save a slot with a name which that already exists you will get a popup asking you if you want to overwrite it.  
![SaveNewSlotWindow](https://raw.githubusercontent.com/techcoder20/ThemeSaver/main/Screenshots/SaveNewSlotWindow.png)

### Load Slots Window
The Load Slots Winow will help you browse through all your slots and perform different actions on them. Some of the actions which you can perform on the slots are, that you can delete the slot, you can export the slot to a specific slot which will give you a tar.gz archive and finally you can load the slot. If you have not saved any slots you will get a popup saying that `There Are No Saved Slots :(`  
![LoadSlotsWindow](https://raw.githubusercontent.com/techcoder20/ThemeSaver/main/Screenshots/LoadSlotsWindow.png)


## Installation
If the app has intrigued you you can install it by running this command in a terminal to install themesaver. ***Note***: This only works on `xfce` or `LXDE`.
```
wget -qO- https://raw.githubusercontent.com/techcoder20/ThemeSaver/main/install.sh | bash
```

<details>
<summary>To Install Manually</summary>
To manually install ThemeSaver:
 
```
git clone https://github.com/techcoer20/themesaver ~/ThemeSaver
~/ThemeSaver/install.sh
```
</details>

<details>
<summary>Uninstallation</summary>
If you dont like themesaver for some reason you can uninstall by running this command in a terminal.  

```
themesaver uninstall
```
</details>   

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

## Credits

<b>I got the icons for the app from flaticon.com so here are the attributes for them :)</b>   
<div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
<div>Icons made by <a href="https://www.flaticon.com/authors/bqlqn" title="bqlqn">bqlqn</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
<div>Icons made by <a href="https://www.flaticon.com/authors/chanut" title="Chanut">Chanut</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
<div>Icons made by <a href="https://www.flaticon.com/authors/kiranshastry" title="Kiranshastry">Kiranshastry</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
<div>Icons made by <a href="https://www.flaticon.com/authors/pixel-perfect" title="Pixel perfect">Pixel perfect</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>       
   
   
This app was inspired by: https://github.com/paju1986/PlasmaConfSaver

