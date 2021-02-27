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
#Installing xdotool
sudo apt update
sudo apt -y install xdotool
#Creating alias for python script
echo "alias themesaver='python3 ~/ThemeSaver/ThemeSaver.py'" >> ~/.bashrc

bash
