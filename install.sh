#!/bin/bash

if [ ! -d ~/ThemeSaver ];then
    #Cloning github repo
    git clone https://github.com/techcoder20/themesaver ~/ThemeSaver
fi 
#Creating file which stores desktop entry name
echo $DESKTOP_SESSION > ~/ThemeSaver/DesktopEnvironment
DE=$(cat ~/ThemeSaver/DesktopEnvironment)
if [ $DE == 'xfce' ];then
    #Installing xfce4-panel-profiles
    sudo dpkg -i ~/ThemeSaver/xfce4-panel-profiles.deb
    #Fixing broken packages if any
    sudo apt -y install -f
fi
#Installing dependencies
sudo apt update
sudo apt -y install xdotool python-pil.imagetk python3-pil python3-pil.imagetk

#Copying Icon
sudo cp ~/ThemeSaver/ThemeSaver.png /usr/share/icons

#Creating Desktop Entry
echo "[Desktop Entry]
Type=Application
Terminal=false
Exec=python3 /home/$USER/ThemeSaver/gui.py
Name=ThemeSaver
Icon=ThemeSaver
Categories=Utility;" >> ~/.local/share/applications/ThemeSaver.desktop

#Creating alias for python script
echo "alias themesaver='python3 ~/ThemeSaver/ThemeSaver.py'" >> ~/.bashrc

bash
