import os
import sys
import click

installDependencies = True

if len(sys.argv) > 1:
    if sys.argv[1] == '-nd':
        installDependencies = False

if os.path.isfile("/usr/bin/pacman"):
    package_manager='pacman'
if os.path.isfile("/usr/bin/apt"):
    package_manager='apt'  

DE = os.environ['XDG_CURRENT_DESKTOP'].lower().strip()
if len(DE.split(':')) != 1:
    DE = DE.split(':')[1]

click.echo(click.style('\nChecking if your Desktop environment and Window manager is supported', fg='blue'))
if not os.path.isfile("/usr/bin/wmctrl") and installDependencies:
    if package_manager == 'pacman':
        os.system('sudo pacman -S wmctrl --noconfirm --noprogressbar --needed')
    elif package_manager == 'apt':
        os.system('sudo apt -y install wmctrl')

WM = os.popen("wmctrl -m").read().split('\n')[0].replace('Name: ', '').lower()
if DE.strip() == '':
    DE = WM

SupportedDE_WM = ['xfce', 'xfwm4', 'plasma', 'kde','kwin','qtile', 'lg3d', 'gnome', 'gnome shell']

if not DE in SupportedDE_WM or not WM in SupportedDE_WM:      
        click.echo(click.style(f'The Desktop Environment {DE} and Window Manager {WM} Is Not Supported', fg='red')) 
        quit()

click.echo(click.style('Your Desktop Environment and Window Manager Is Supported', fg='green')) 

# Installing Dependencies
if package_manager == 'pacman' and installDependencies:
    click.echo(click.style('\n=========[ Installing Dependencies ]=========', fg='green'))
    os.system("sudo pacman -S xdotool ttf-ubuntu-font-family imagemagick scrot python-pip --noconfirm --noprogressbar --needed")
elif package_manager == 'apt' and installDependencies:    
    os.system("sudo apt update && sudo apt -y install xdotool fonts-ubuntu imagemagick scrot python3-pyqt5 python3-pip gnome-shell-extensions gnome-tweaks")

if DE == 'xfce' and installDependencies:
    if package_manager == 'pacman':
        os.system('sudo pacman -S xfce4-panel-profiles --noconfirm --noprogressbar --needed')
    elif package_manager == 'apt':
        os.system('sudo dpkg -i ~/.themesaver/xfce4-panel-profiles.deb && sudo apt -y install -f')

click.echo(click.style('\n=========[ Generating Required Files ]=========', fg='green'))
# Creating Desktop Entry
click.echo(click.style('Installing Icons', fg='blue'))
os.system('mkdir ~/.local/share/icons')
os.system('cp ~/.themesaver/GUI/Icons/OG/ThemeSaver.png ~/.local/share/icons')
click.echo(click.style('Creating Desktop Entry', fg='blue'))
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

print()
click.echo(click.style('Creating Default Configs', fg='blue'))
os.system('mkdir ~/.config/ThemeSaver')
os.system('cp ~/.themesaver/config.env ~/.config/ThemeSaver/')

click.echo(click.style('\n=========[ Installing Python Package ]=========', fg='green'))


# Installing themesaver bin file
click.echo(click.style('Installing package with pip', fg='blue'))
os.system('cd ~/.themesaver && pip install --editable .')

noBin = False
for path in os.environ['PATH'].split(':'):
    if path.endswith('/.local/bin'):
        noBin = True
        break

os.system(f'sudo cp ~/.local/bin/themesaver /usr/bin')

shell = os.environ['SHELL'].strip().replace('/', '').replace('usr', '').replace('bin', '')
if noBin == False:
    click.echo(click.style('Adding local bin to path', fg='blue'))
    if shell == 'bash':
        os.system("echo 'export PATH=~/.local/bin/:$PATH' >> ~/.bashrc")
    elif shell == 'zsh':
        os.system("echo 'export PATH=~/.local/bin/:$PATH' >> ~/.zshrc")
    

click.echo(click.style('\nFinished Installing Themesaver', fg='green'))
