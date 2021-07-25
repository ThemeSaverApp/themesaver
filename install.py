import os

if os.path.isfile("/usr/bin/pacman"):
    package_manager='pacman'
if os.path.isfile("/usr/bin/apt"):
    package_manager='apt'  
    
if "DESKTOP_SESSION" in os.environ:
    Desktop_Environment = os.environ["DESKTOP_SESSION"]
else:    
    Is_Installed=False
    if not os.path.isfile("/usr/bin/wmctrl"):
        os.system('sudo pacman -S wmctrl')
    Desktop_Environment = os.popen("wmctrl -m").read().split('\n')[0].replace('Name: ', '')    
 

SupportedDesktopWindowEnvironments = ['xfce', 'lxde-pi', 'lxde', 'awesome', 'qtile']
if not Desktop_Environment.lower() in SupportedDesktopWindowEnvironments:
        print("Your Desktop Environment/Window Manager Is Not Supported")        
        quit()

# Installing Dependencies
if package_manager == 'pacman':
    os.system("sudo pacman -S xdotool ttf-ubuntu-font-family imagemagick python-pyqt5 scrot --noconfirm --noprogressbar --needed")
elif package_manager == 'apt':    
    os.system("sudo apt update && sudo apt -y install xdotool fonts-ubuntu imagemagick python3-pyqt5 scrot")

if Desktop_Environment == 'xfce':
    if package_manager == 'pacman':
        os.system('sudo pacman -S xfce4-panel-profiles --noconfirm --noprogressbar --needed')
    elif package_manager == 'apt':
        os.system('sudo dpkg -i ~/ThemeSaver/xfce4-panel-profiles.deb && sudo apt -y install -f')
    
# Cloning Repo
if not os.path.isdir(f"{os.environ['HOME']}/.themesaver/"):
    os.system("git clone https://github.com/techcoder20/themesaver ~/.themesaver")

# Creating Desktop Entry
os.system("mkdir ~/.local/share/applications")
os.system('touch ~/.local/share/applications/ThemeSaver.desktop')
with open(f"{os.environ['HOME']}/.local/share/applications/ThemeSaver.desktop", "w") as DesktopFile:
    DesktopFile.write(
'''[Desktop Entry]
Type=Application
Terminal=false
Exec=themesaver gui
Name=ThemeSaver
Icon=ThemeSaver
Categories=Utility;
'''
)

#Creating Binary
os.system('sudo touch /usr/local/bin/themesaver')
os.system(f'sudo chown $USER:$USER /usr/local/bin/themesaver')
os.system(f'sudo chmod +x /usr/local/bin/themesaver')
with open(f"/usr/local/bin/themesaver", "w") as BinaryFile:
    BinaryFile.write(
'''
#!/bin/bash
python3 ~/.themesaver/ThemeSaver.py "$1" "$2" "$3"
'''
)

os.system('sudo rm -f ~/.themesaver/xfce4-panel-profiles.deb')
