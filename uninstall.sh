#!/bin/bash

#Removing desktop entry
rm ~/.local/share/applications/ThemeSaver.desktop

#Removing icon
sudo rm /usr/share/icons/ThemeSaver.png

#Removing xfce4-panel-profiles
sudo apt -y purge xfce4-panel-profiles xdotool python-pil.imagetk python3-pil python3-pil.imagetk fonts-ubuntu
sudo apt install -f

#Removing ThemeSaver folder
rm -r ~/ThemeSaver

