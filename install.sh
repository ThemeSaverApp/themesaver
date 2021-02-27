#!/bin/bash

#Cloning github repo if not present
if [ ! -d '/home/$USER/ThemeSaver' ]; then
    git clone https://github.com/techcoder20/themesaver

#Installing xfce4-panel-profiles
sudo dpkg -i ~/ThemeSaver/xfce4-panel-profiles.deb
#Fixing broken packages if any
sudo apt install -f
#Installing xdotool
sudo apt install xdotool
#Creating alias for python script
echo "alias themesaver='python ~/ThemeSaver/ThemeSaver.py'" >> ~/.bashrc

bash