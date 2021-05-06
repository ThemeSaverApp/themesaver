#!/bin/bash

#Removing All ThemeSaver Files
rm ~/.local/share/applications/ThemeSaver.desktop
sudo rm -r ~/ThemeSaver
sudo rm /usr/share/icons/ThemeSaver.png
sudo rm /usr/local/bin/themesaver

#Removing xfce4-panel-profiles and other dependencies
if command -v apt &> /dev/null
then
    sudo apt -y purge xfce4-panel-profiles xdotool python-pil.imagetk python3-pil python3-pil.imagetk fonts-ubuntu
    sudo apt install -f
    sudo apt -y autoremove
elif command -v pacman &> /dev/null
then
    sudo pacman -R xdotool ttf-ubuntu-font-family imagemagick xfce4-panel-profiles
    fi
    