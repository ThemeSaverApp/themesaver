#!/bin/bash

sudo dpkg -i ~/ThemeSaver/xfce4-panel-profiles.deb
sudo apt install -f
sudo apt install xdotool
echo "alias themesaver='python ~/ThemeSaver/ThemeSaver.py'" >> ~/.bashrc
bash