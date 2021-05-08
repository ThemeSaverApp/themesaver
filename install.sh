#!/bin/bash

if [ $DESKTOP_SESSION != 'xfce' ] && if [ $DESKTOP_SESSION != 'LXDE-pi' ]
then
    echo "Your Desktop Environment is not supported"
    exit 1
fi

if [ ! -d ~/ThemeSaver ];then
    #Cloning github repo
    git clone https://github.com/techcoder20/themesaver ~/ThemeSaver
fi 

if [ $DESKTOP_SESSION == 'xfce' ];then
    if command -v apt &> /dev/null
    then
        #Installing xfce4-panel-profiles
        sudo dpkg -i ~/ThemeSaver/xfce4-panel-profiles.deb
        #Fixing broken packages if any
        sudo apt -y install -f
    elif command -v pacman &> /dev/null
    then
        sudo pacman -S xfce4-panel-profiles
    fi
fi

#Installing dependencies
if command -v apt &> /dev/null
then
    sudo apt update
    sudo apt -y install xdotool fonts-ubuntu imagemagick python-pyqt5
elif command -v pacman &> /dev/null
then
    sudo pacman -S xdotool ttf-ubuntu-font-family imagemagick xfce4-panel-profiles python-pyqt5
fi

#Copying Icon
sudo cp ~/ThemeSaver/GUI/Icons/ThemeSaverLogo.png /usr/share/icons/ThemeSaver.png

mkdir ~/ThemeSaver/Slots

#Creating Desktop Entry And Binary
echo "[Desktop Entry]
Type=Application
Terminal=false
Exec=python3 $HOME/ThemeSaver/GUI/MainWindow.py
Name=ThemeSaver
Icon=ThemeSaver
Categories=Utility;" > ~/.local/share/applications/ThemeSaver.desktop

echo '#!/bin/bash
python3 ~/ThemeSaver/ThemeSaver.py "$1" "$2" "$3"'  | sudo tee /usr/local/bin/themesaver > /dev/null

sudo chmod +x /usr/local/bin/themesaver

