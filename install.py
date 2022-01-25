import os

if os.path.isfile("/usr/bin/pacman"):
    package_manager='pacman'
if os.path.isfile("/usr/bin/apt"):
    package_manager='apt'  
    
DE = os.environ["DESKTOP_SESSION"]

if not os.path.isfile("/usr/bin/wmctrl"):
    if package_manager == 'pacman':
        os.system('sudo pacman -S wmctrl --noconfirm --noprogressbar --needed')
    elif package_manager == 'apt':
        os.system('sudo apt -y install wmctrl')
    
WM = os.popen("wmctrl -m").read().split('\n')[0].replace('Name: ', '')    

SupportedDE_WM = ['xfce', 'xfwm4', 'plasma', 'kwin', 'qtile']

if not DE.lower() in SupportedDE_WM and WM.lower() in SupportedDE_WM:
        print("Your Desktop Environment/Window Manager Is Not Supported")        
        quit()

# Installing Dependencies
if package_manager == 'pacman':
    os.system("sudo pacman -S xdotool ttf-ubuntu-font-family imagemagick scrot --noconfirm --noprogressbar --needed")
elif package_manager == 'apt':    
    os.system("sudo apt update && sudo apt -y install xdotool fonts-ubuntu imagemagick scrot python3-pyqt5")

# Cloning Repo
if not os.path.isdir(f"{os.environ['HOME']}/.themesaver/"):
    os.system("git clone https://github.com/techcoder20/themesaver ~/.themesaver")

if DE == 'xfce':
    if package_manager == 'pacman':
        os.system('sudo pacman -S xfce4-panel-profiles --noconfirm --noprogressbar --needed')
    elif package_manager == 'apt':
        os.system('sudo dpkg -i ~/.themesaver/xfce4-panel-profiles.deb && sudo apt -y install -f')

# Creating Desktop Entry
os.system('mkdir ~/.local/share/icons')
os.system('sudo cp ~/.themesaver/GUI/Icons/OG/ThemeSaver.png ~/.local/share/icons')
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

os.system('mkdir ~/.config/ThemeSaver')
os.system('cp ~/.themesaver/config.env ~/.config/ThemeSaver/')

# Installing themesaver bin file
os.system('cd ~/.themesaver && pip install --editable .')


for path in os.environ['PATH'].split(':'):
    if path.endswith('/.local/bin'):
        quit()

shell = os.environ['SHELL'].strip().replace('/', '').replace('usr', '').replace('bin', '')
if shell == 'bash':
    os.system("echo 'export PATH=~/.local/bin/:$PATH' >> ~/.bashrc")
    
    
