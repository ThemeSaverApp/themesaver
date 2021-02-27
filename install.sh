#!/bin/bash

#Cloning github repo if not present
if [ ! -d '~/ThemeSaver' ]; then
    git clone https://github.com/techcoder20/themesaver ~/ThemeSaver
fi

#Installing xfce4-panel-profiles
sudo dpkg -i ~/ThemeSaver/xfce4-panel-profiles.deb
#Fixing broken packages if any
sudo apt install -f
#Installing xdotool
sudo apt install xdotool
#Creating alias for python script
echo "alias themesaver='python ~/ThemeSaver/ThemeSaver.py'" >> ~/.bashrc

bash
