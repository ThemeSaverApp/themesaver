import os

CleanUpCommands = [
'rm ~/.local/share/applications/ThemeSaver.desktop',
'rm ~/.local/share/icons/ThemeSaver.png',
'pip3 uninstall -y themesaver',
'rm ~/.local/bin/themesaver',
 'sudo rm -r ~/.themesaver',
]

for command in CleanUpCommands:
    os.system(command)

if os.path.isfile("/usr/bin/pacman"):
    os.system('sudo pacman -R xdotool ttf-ubuntu-font-family imagemagick xfce4-panel-profiles')
if os.path.isfile("/usr/bin/apt"):  
    os.system('sudo apt -y purge xfce4-panel-profiles xdotool python-pil.imagetk python3-pil python3-pil.imagetk fonts-ubuntu && sudo apt install -f && sudo apt -y autoremove')

