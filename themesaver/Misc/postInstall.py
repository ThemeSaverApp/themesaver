import os, sys
from themesaver.Misc.getInfo import getDE, getWM

def installDependencies(DE, WM):
    if os.path.isfile("/usr/bin/pacman"):
        Dependencies = ['xdotool', 'ttf-ubuntu-font-family', 'imagemagick', 'scrot', 'python-pip', 'wmctrl', 'xfce4-panel-profiles-git']
        toinstall = []

        for d in Dependencies:
            installCheck = os.popen(f'pacman -Qs --color always {d} | grep "local" | grep {d}').read()
            if installCheck.strip() == "":
                toinstall.append(d)

        if 'xfce4-panel-profiles-git' in toinstall:
            quit()
            os.system(f'sudo pacman -S --needed base-devel git wget yajl')
            os.system(f'git clone https://aur.archlinux.org/xfce4-panel-profiles-git.git')
            p = os.getcwd()
            os.chdir(f'xfce4-panel-profiles-git/')
            os.system(f'makepkg -si')
            os.chdir(p)

        if not len(toinstall) == 0:
            os.system(f'sudo pacman -S {" ".join(toinstall)} --noconfirm --noprogressbar --needed')  
        
    if os.path.isfile("/usr/bin/apt"):
        Dependencies = ['xdotool', 'fonts-ubuntu', 'imagemagick', 'scrot', 'python3-pyqt5', 'python3-pip', 'gnome-shell-extensions', 'gnome-tweaks']
        toinstall = []


def checkCompatibility(DE, WM):
    SupportedDE_WM = ['xfce', 'xfwm4', 'plasma', 'kde','kwin','qtile', 'lg3d', 'gnome', 'gnome shell', 'awesome', 'i3']
    if DE not in SupportedDE_WM and WM not in SupportedDE_WM:
        # click.echo(click.style(, fg='red')) 
        print(f'The Desktop Environment {DE} and Window Manager {WM} Is Not Supported')
        return False
    return True

def generatingRequiredFiles():
    def createDir(path):
        if not os.path.isdir(os.path.expanduser(path)):
            os.system(f'mkdir {path}')

    createDir('~/.local/share/icons')
    createDir('~/.local/share/applications')
    createDir('~/.config/themesaver')

    os.system('sudo mkdir -p /opt/themesaver')
    os.system("sudo chmod -R 777 /opt/themesaver")    
    os.system('mkdir -p /opt/themesaver/Slots')

    path = os.path.realpath(__file__).replace('/Misc/postInstall.py', '')

    if not os.path.isfile(os.path.expanduser('~/.local/share/icons/ThemeSaver.png')):
        os.system(f'cp {path}/GUI/Icons/OG/ThemeSaver.png ~/.local/share/icons')

    if not os.path.isfile(os.path.expanduser('~/.config/themesaver/config.env')):
        os.system(f'cp {path}/config.env ~/.config/themesaver')

    if not os.path.isfile(os.path.expanduser('~/.local/share/applications/ThemeSaver.desktop')):
        os.system('touch ~/.local/share/applications/ThemeSaver.desktop')
        with open(f"{os.environ['HOME']}/.local/share/applications/ThemeSaver.desktop", "w") as DesktopFile:
            DesktopFile.write('''[Desktop Entry]
            Type=Application
            Terminal=false
            Exec=themesaver gui
            Name=ThemeSaver
            Icon=ThemeSaver
            Categories=Utility;
            '''
            )

    # noBin = False
    # for path in os.environ['PATH'].split(':'):
    #     if path.endswith('/.local/bin'):
    #         noBin = True
    #         break

    os.system('sudo ln -s ~/.local/bin/themesaver /usr/bin/themesaver')

    shell = os.environ['SHELL'].strip().replace('/', '').replace('usr', '').replace('bin', '')
    if noBin == False:
        # click.echo(click.style('Adding local bin to path', fg='blue'))
        print('Adding local bin to path')
        if shell == 'bash':
            os.system("echo 'export PATH=~/.local/bin/:$PATH' >> ~/.bashrc")
        elif shell == 'zsh':
            os.system("echo 'export PATH=~/.local/bin/:$PATH' >> ~/.zshrc")

def postInstall():
    if checkCompatibility(getDE(), getWM()):
        installDependencies(getDE(), getWM())
        generatingRequiredFiles()
