#!/usr/bin/env python

import os, sys, time, subprocess, tarfile, click, json, pathlib, requests
from dotenv import load_dotenv, dotenv_values
from tqdm import tqdm
from pathlib import Path

AppConfig = dotenv_values(f"{os.environ['HOME']}/.config/ThemeSaver/config.env")

# Arrays cannot be stored in .env files so converting the string into an array
def convertArray(key):
    return AppConfig[key].replace('\'', '').replace(' ', '').replace('[', '').replace(']', '').split(',')

# Config Variables
RequiredChannelsXfce = convertArray('Xfce')
RequiredFoldersLXDE = convertArray('LXDE')
RequiredKDEConfig = convertArray('KDEConf')
RequiredKDELocal = convertArray('KDELocal')
PlankProperties = convertArray('Plank')
Configs = convertArray('Configs')

NumberOfMonitors = int(os.popen('xrandr --listactivemonitors').read().split('\n')[0].strip().replace('Monitors: ', ''))

if 'XDG_CURRENT_DESKTOP' in os.environ.keys():
    DE = os.environ['XDG_CURRENT_DESKTOP'].lower().strip()
    if len(DE.split(':')) != 1:
        DE = DE.split(':')[1]
elif 'DESKTOP_SESSION' in os.environ.keys():
    DE = os.environ['DESKTOP_SESSION'].lower().strip()
WM = os.popen("wmctrl -m").read().split('\n')[0].replace('Name: ', '').lower()
if DE.strip() == '':
    DE = WM
HomePath = os.environ['HOME']

# Folder Paths
FolderPath = Path(AppConfig['FolderPath']).expanduser()
SlotsFolder = Path(FolderPath / 'Slots').expanduser()
ConfigFolder = Path('~/.config').expanduser()

if not SlotsFolder.exists():
    os.system(f'mkdir {SlotsFolder}')


@click.group()
def group():
    pass

@click.command(help='Save a new slot')
@click.argument('slotname' )
def save(slotname):
    # Overwrite Check
    Overwrite = False
    if Path(SlotsFolder / slotname).exists():
        Overwrite = click.prompt(click.style(
            'A slot with that name already exists. Do you want to overwrite it ? [Y/n]', fg='red'), type=str)
        if Overwrite.lower() == 'y':
            click.echo(click.style('Okay overwriting', fg='green'))
            # os.system(f'rm -rf {SlotsFolder}/"{slotname}"')
        else:
            print(click.style('Not overwriting', fg='green'))
            quit()

    click.echo(click.style('======= Saving Slot =======', fg='green'))

    # Creating Slot
    if not Overwrite:
        os.system(f'mkdir {Path(SlotsFolder / slotname)}')

    # Taking a Screenshot  
    os.system(f'{FolderPath}/TakeScreenshot.sh &')
    time.sleep(0.5)
    os.system(f'rm {SlotsFolder}/"{slotname}"/Screenshot.png')
    os.system(f'scrot {SlotsFolder}/"{slotname}"/Screenshot.png')
    os.system(f'convert {SlotsFolder}/"{slotname}"/Screenshot.png -resize 470x275 {SlotsFolder}/"{slotname}"/Screenshot.png')

    # Saving Plank Configs If Running
    PlankRunning = os.popen('pgrep plank').read()
    if PlankRunning != '':
        # Storing Plank Configuration
        os.mkdir(Path(SlotsFolder / slotname / 'plank'))
        for PlankProperty in PlankProperties:
            os.system(
                f'gsettings get net.launchpad.plank.dock.settings:/net/launchpad/plank/docks/dock1/ {PlankProperty} > {SlotsFolder}/"{slotname}"/plank/{PlankProperty}')

    if not Overwrite:
        os.system(f"mkdir {SlotsFolder}/{slotname}/'configs'")

    # Saving Polybar Configs If Running
    PolybarRunning = os.popen('pgrep polybar').read()
    if PolybarRunning != '':
        os.system(f"cp -r {Path(ConfigFolder / 'polybar')} {Path(SlotsFolder / slotname / 'configs')}")

    # Saving Conky Configs If Running
    ConkyRunning = os.popen('pgrep conky').read()
    if ConkyRunning != '':
        os.system(f"cp -r {Path(ConfigFolder / 'conky')} {Path(SlotsFolder / slotname / 'configs')}")

    # Saving LatteDock Configs If Running
    LatteRunning = os.popen('pgrep latte-dock').read()
    if LatteRunning != '':
        os.system(f"cp -r {Path(ConfigFolder / 'latte')} {Path(SlotsFolder / slotname / 'configs')}")

    # Storing Fish and OMF Fish configs
    shell = os.environ['SHELL'].strip().replace('/', '').replace('usr', '').replace('bin', '')
    shells = {
        'fish': ['~/.config/fish', '~/.config/omf'],
        'bash': ['~/.bash_profile', '~/.bashrc', '~/.bash_logout'],
        'zsh': []
    }

    if shell in shells.keys():
        if not Overwrite:        
            os.system(f'mkdir {Path(SlotsFolder / slotname / shell)}')
        for file in shells[shell]:
            os.system(
                f'cp -rf {file} {SlotsFolder}/"{slotname}"/{shell}')

    for config in Configs:
        click.echo(click.style(f'Saving config: ', fg='green') + click.style(f'{config}', fg='blue'))
        os.system(f'cp -rf ~/.config/{config} {SlotsFolder}/"{slotname}"/configs &>/dev/null')


    if DE == 'plasma' and WM == 'kwin':
        if not Overwrite:
            os.system(f'mkdir {Path(SlotsFolder / slotname / share)}')
        for config in RequiredKDEConfig:
            os.system(f'cp -rf ~/.config/{config} {SlotsFolder}/"{slotname}"/configs &>/dev/null')

        for file in RequiredKDELocal:
            os.system(f'cp -rf ~/.local/share/{file} {SlotsFolder}/"{slotname}"/share &>/dev/null')

        WallpaperPath = os.popen(f"sed -n '/Image=/p' ~/.config/plasma-org.kde.plasma.desktop-appletsrc").read().strip()
        os.system(f'sed -i "s#{WallpaperPath.strip()}#Image=#g" {SlotsFolder}/"{slotname}"/configs/plasma-org.kde.plasma.desktop-appletsrc')

        WallpaperPath = WallpaperPath.replace('Image=', '').replace('file://', '').strip()
        if os.path.isdir(WallpaperPath):
            WallpaperPath = f"{WallpaperPath}contents/images/{os.listdir(f'{WallpaperPath}contents/images/')[0]}"


    if DE == 'xfce' and WM == 'xfwm4':
        for channel in RequiredChannelsXfce:
            os.system(f'xfconf-query -c {channel.strip()} -l > {SlotsFolder}/{channel.strip()}')
            PropertiesFile = open(f'{SlotsFolder}/{channel.strip()}', 'r')
            Properties = PropertiesFile.readlines()
            os.mkdir(SlotsFolder / slotname / channel.strip())
            os.system(f'mkdir {Path(SlotsFolder / slotname / channel.strip())}')
            for Property in Properties:
                os.system(f'xfconf-query -c {channel.strip()} -p {Property.strip()} > {SlotsFolder}/"{slotname}"/{channel.strip()}/{Property.replace("/","+")}')

            os.system(f'rm {SlotsFolder}/{channel.strip()}')
        os.system(f'xfce4-panel-profiles save {SlotsFolder}/"{slotname}"/"{slotname}"')

        WallpaperPath = os.popen('''xfconf-query -c xfce4-desktop -p /backdrop/screen0/$(xrandr|awk '/\<connected/{print "monitor"$1}')/workspace0/last-image''').read().strip()


    if  DE == 'lxde-pi':
        for folder in RequiredFoldersLXDE:
            os.system(f'cp -rf ~/.config/{folder} {SlotsFolder}/"{slotname}"/configs &>/dev/null')

        if os.path.isfile(Path(f'~/.config/pcmanfm/LXDE-pi/desktop-items-0.conf').expanduser()):
            WallpaperPath = os.popen(f"sed -n '/wallpaper=/p' ~/.config/pcmanfm/LXDE-pi/desktop-items-0.conf").read().split('\n')[0].replace('wallpaper=', '')    
        else:
            WallpaperPath = os.popen(f"sed -n '/wallpaper=/p' /etc/xdg/pcmanfm/LXDE-pi/desktop-items-0.conf").read().split('\n')[0].replace('wallpaper=', '')     
                    

    if WM == 'awesome':
        os.system(f'cp -rf ~/.config/awesome {SlotsFolder}/"{slotname}"/configs &>/dev/null')
        WallpaperPath = os.popen(f"sed -n '/file/p' ~/.config/nitrogen/bg-saved.cfg").read().split('\n')[0].replace('file=', '') 

    if WM == 'qtile' or WM == 'lg3d':
        os.system(f'cp -rf ~/.config/qtile {SlotsFolder}/"{slotname}"/configs &>/dev/null')
        os.system(f'cp -r ~/.config/nitrogen {SlotsFolder}/"{slotname}"/configs')
        WallpaperPath = os.popen(f"sed -n '/file/p' ~/.config/nitrogen/bg-saved.cfg").read().strip().split('\n')

        for n in range(len(WallpaperPath)):
            if n == 0:
                os.system(f'cp \'{WallpaperPath[n].replace("file=", "").strip()}\' \'{AppConfig["FolderPath"]}/Slots/{slotname}/Wallpaper.png\'')
                os.system(f'sed -i "s#{WallpaperPath[n].strip()}#file={AppConfig["FolderPath"]}/Slots/{slotname}/Wallpaper.png#g" /opt/themesaver/Slots/{slotname}/configs/nitrogen/bg-saved.cfg')
            else:
                os.system(f'cp \'{WallpaperPath[n].replace("file=", "").strip()}\' \'{AppConfig["FolderPath"]}/Slots/{slotname}/Wallpaper-Monitor{n+1}.png\'')
                os.system(f'sed -i "s#{WallpaperPath[n].strip()}#file={AppConfig["FolderPath"]}/Slots/{slotname}/Wallpaper-Monitor{n}#g" /opt/themesaver/Slots/{slotname}/configs/nitrogen/bg-saved.cfg')

    if DE == 'gnome' and WM == 'gnome shell':
        os.system(f'dconf dump / > {SlotsFolder}/"{slotname}"/{slotname}')
        WallpaperPath = os.popen('gsettings get org.gnome.desktop.background picture-uri').read().strip().replace('file://', '').replace('\'', '')

    
    if not os.path.isfile(f'{AppConfig["FolderPath"]}/Slots/{slotname}/Wallpaper.png'):
        os.system(f'cp \'{WallpaperPath}\' \'{SlotsFolder}/{slotname}/Wallpaper.png\'')

    Theme = os.popen('gsettings get org.gnome.desktop.interface gtk-theme').read().strip().strip("'")
    IconTheme = os.popen('gsettings get org.gnome.desktop.interface icon-theme').read().strip().strip("'")
    CursorTheme  = os.popen('gsettings get org.gnome.desktop.interface cursor-theme').read().strip().strip("'")

    info = {
        "name": slotname,
        "gtkTheme": Theme,
        "iconTheme": IconTheme,
        "cursorTheme": CursorTheme,
        "shell": os.environ['SHELL'].replace('/', '').replace('bin', '').replace('usr', ''),
        "desktopEnvironment": DE.strip(),
        "windowManager": WM.strip(),
    }

    if DE == 'gnome' and WM == 'gnome shell':
        gnomeExtensions = os.popen('gsettings get org.gnome.shell enabled-extensions').read().replace(' ', '').replace('\'', '').replace('[', '').replace(']', '').split(',')
        for ext in gnomeExtensions:
            gnomeExtensions[gnomeExtensions.index(ext)] = ext.strip()
        info['gnomeExtensions'] = gnomeExtensions
  
    # Serializing json 
    jsonPath = Path(SlotsFolder / slotname / 'info.json')
    jsonPath.write_text(json.dumps(info , indent = 4))

    print()

    os.system(f'touch {SlotsFolder}/"{slotname}"/import.sh')

    click.echo(click.style('======= Slot Info =======', fg='green'))

    for info,value in info.items():
        click.echo(click.style(f'{info}: ', fg='green') + click.style(f'{value}', fg='blue'))


@click.command(help='Load existing slot')
@click.argument('slotname')
@click.option('--gui/--no-gui', default=False)
def load(slotname, gui):

    if Path(SlotsFolder / slotname).exists() == False:
        click.echo(click.style('No slot like that exists. Use command `themesaver ls` to print the list of slots', fg='red'))
        quit()

    info = json.load(open(f'{SlotsFolder}/{slotname}/info.json'))
    if info['desktopEnvironment'] != DE and info['windowManager'] != WM:
        click.echo(click.style(f'The is slot was made for the {desktopEnvironment} Desktop Environment and the {windowManager} window manager', fg='red'))
        quit()

    # Loading Plank configs if they exist
    if Path(SlotsFolder / slotname / 'plank').exists():
        subprocess.Popen(['setsid', 'plank'],
                         stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        for PlankConfig in os.listdir(f'{SlotsFolder}/{slotname}/plank'):
            PlankConfigData = open(f'{SlotsFolder}/{slotname}/plank/{PlankConfig}').read()
            os.system(
                f'gsettings set net.launchpad.plank.dock.settings:/net/launchpad/plank/docks/dock1/ {PlankConfig} {PlankConfigData}')
    # Killing Plank If Configs dont exist
    else:
        subprocess.Popen(['killall', 'plank'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    if not Path('~/.config_backups').expanduser().exists():
        os.system(f'mkdir ~/.config_backups')
    backupFolder = f'Backup - {str(time.strftime("%a, %H:%M:%S", time.localtime()))}'
    os.system(f'mkdir ~/.config_backups/"{backupFolder}"')

    # Restoring Config Files
    click.echo(click.style(f'=========[ RESTORING CONFIG FILES ]=========', fg='green'))
    for config in os.listdir(f'{SlotsFolder}/{slotname}/configs'):
        click.echo(click.style(f'Restoring Config: ', fg='green') + click.style(f'{config}', fg='blue'))
        os.system(f'mv ~/.config/{config} ~/.config_backups/"{backupFolder}" &>/dev/null')
        os.system(f'cp -rf {SlotsFolder}/"{slotname}"/configs/{config} ~/.config/')


    # Using subprocesss to run apps as os.system is not working properly with &>/dev/null
    def runApp(app, config):
        if Path(f'{SlotsFolder}/{slotname}/configs/{config}').exists():
            subprocess.Popen(['killall', app], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            time.sleep(2)
            subprocess.Popen(['setsid', app], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        else:
            subprocess.Popen(['killall', app], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            
    runApp('polybar', 'polybar')
    runApp('conky', 'conky')
    runApp('latte-dock', 'latte')

    if os.path.isdir(f'{SlotsFolder}/{slotname}/configs/awesome'):
        os.system('echo "awesome.restart()" | awesome-client')
        os.system(f'nitrogen --save {AppConfig["NitrogenStyle"]} {SlotsFolder}/"{slotname}"/Wallpaper.png &>/dev/null')

    if os.path.isdir(f'{SlotsFolder}/{slotname}/configs/qtile'):
        os.system('qtile cmd-obj -o cmd -f restart')
        os.system(f'nitrogen --restore')


    if DE == 'xfce':
        for PropertyFolders in RequiredChannelsXfce:
            for PropertyFiles in os.listdir(f'{SlotsFolder}/{slotname}/{PropertyFolders}'):
                PropertyFile = open(
                    f'{SlotsFolder}/{slotname}/{PropertyFolders}/{PropertyFiles}')
                PropertyFileValue = PropertyFile.read()
                PropertyFilePath = PropertyFiles.replace('+', '/').strip()
                os.popen(
                    f'xfconf-query -c "{PropertyFolders.strip()}" -p "{PropertyFilePath}" -s "{PropertyFileValue.strip()}" ')

        os.system(f'xfce4-panel-profiles load {SlotsFolder}/"{slotname}"/"{slotname}"')
        subprocess.Popen(['setsid', 'xfce4-panel', '&>/dev/null'],stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        # Setting Wallpaper
        os.system('''xfconf-query -c xfce4-desktop -p /backdrop/screen0/$(xrandr|awk '/\<connected/{print "monitor"$1}')/workspace0/last-image -s ''' + f'"{SlotsFolder}/{slotname}/Wallpaper.png"')

    if DE == 'lxde-pi':
        click.echo(click.style('=========[ RESTORING LXDE CONFIGS ]=========', fg='green'))
        os.system(f'mkdir ~/.config_backups/"{backupFolder}"/share')        
        for config in RequiredFoldersLXDE:
            if not Path(f'~/.config_backups/{backupFolder}/{config}').expanduser().exists():
                os.system(f'mv ~/.config/{config} ~/.config_backups/"{backupFolder}"')
            os.system(f'cp -rf {SlotsFolder}/"{slotname}"/configs/{config} ~/.config')


        # Refreshing Desktop
        print()
        click.echo(click.style('=========[ REFRESHING DESKTOP ]=========', fg='green'))        
        subprocess.Popen(['killall', 'pcmanfm', 'lxpanel'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        time.sleep(2)
        click.echo(click.style(f'Refreshing Lxsession', fg='green'))
        subprocess.Popen(['setsid', 'lxsession', '--session=LXDE-pi','--reload'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        time.sleep(2)                
        click.echo(click.style(f'Refreshing Lxpanel', fg='green'))
        subprocess.Popen(['setsid', 'lxpanel', '--profile', 'LXDE-pi'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        time.sleep(2)
        click.echo(click.style(f'Refreshing Desktop', fg='green'))
        subprocess.Popen(['setsid', 'pcmanfm', '--desktop', '--profile', 'LXDE-pi'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        time.sleep(2)
        click.echo(click.style(f'Refreshing Mutter', fg='green'))
        subprocess.Popen(['setsid', 'mutter', '--replace'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


    if DE == 'plasma' and WM =='kwin':
        click.echo(click.style('=========[ RESTORING PLASMA CONFIGS ]=========', fg='green'))
        os.system(f'mkdir ~/.config_backups/"{backupFolder}"/share')

        for file in RequiredKDELocal:
            os.system(f'mv ~/.local/share/{file} ~/.config_backups/"{backupFolder}"/share &>/dev/null')
            os.system(f'cp -rf {SlotsFolder}/"{slotname}"/share/{file} ~/.local/share/ &>/dev/null')

        for config in os.listdir(f'{SlotsFolder}/{slotname}/configs/'):
            click.echo(click.style(f'Restoring Config: ', fg='green') + click.style(f'{config}', fg='blue'))
            os.system(f'mv ~/.config/{config} ~/.config_backups/"{backupFolder}" &>/dev/null')
            os.system(f'cp -rf {SlotsFolder}/"{slotname}"/configs/{config} ~/.config &>/dev/null')

        WallpaperPath = os.popen(f"sed -n '/Image=/p' ~/.config/plasma-org.kde.plasma.desktop-appletsrc").read().strip()
        theme = os.popen('sed -n "/LookAndFeelPackage=/p" ~/.config/kdeglobals').read().replace('LookAndFeelPackage=', '')

        # Refreshing KDE Desktop
        print()
        click.echo(click.style('=========[ REFRESHING DESKTOP ]=========', fg='green'))
        # os.system('setsid qdbus org.kde.KWin /KWin reconfigure &>/dev/null')
        
        click.echo(click.style(f'Loading Plasma Theme: ', fg='green') + click.style(f'{theme.strip()}', fg='blue'))
        subprocess.Popen(f'lookandfeeltool -a {theme.strip()}'.split(' '), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        time.sleep(2)
        click.echo(click.style(f'Using Wallpaper: ', fg='green')  + click.style(f'{SlotsFolder}/{slotname}/Wallpaper.png', fg='blue'))
        os.system(f'sed -i "s#{WallpaperPath.strip()}#Image=file://{SlotsFolder}/{slotname}/Wallpaper.png#g" ~/.config/plasma-org.kde.plasma.desktop-appletsrc')
        time.sleep(2)
        click.echo(click.style(f'Applying Icon Theme: ', fg='green') + click.style(f'{info["iconTheme"]}', fg='blue'))
        subprocess.Popen(f'/usr/lib/plasma-changeicons {info["iconTheme"]}'.split(' '), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        click.echo(click.style('Refreshing ', fg='green')  + click.style(f'Kwin', fg='blue'))
        subprocess.Popen('setsid qdbus org.kde.KWin /KWin reconfigure'.split(' '), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        time.sleep(2)
        click.echo(click.style('Refreshing ', fg='green') + click.style(f'Plasmashell', fg='blue'))
        os.system('/bin/bash -c "setsid kquitapp5 plasmashell > /dev/null  2>&1"')
        os.system('/bin/bash -c "setsid kstart5 plasmashell > /dev/null 2>&1"')
        
    if DE == 'gnome' and WM == 'gnome shell':
        click.echo(click.style('Restoring Config: ', fg='green') + click.style('dconf', fg='blue'))
        os.system(f'dconf load / < {SlotsFolder}/"{slotname}"/{slotname}')
        click.echo(click.style('\n=========[ REFRESHING GNOME EXTENSIONS ]=========', fg='green'))
        allExtenstions = os.listdir(f'{HomePath}/.local/share/gnome-shell/extensions') + os.listdir(f'/usr/share/gnome-shell/extensions/')

        # Checking ubuntu dock seperately cause if it loads after something like dash to dock it overwrites it
        if 'ubuntu-dock@ubuntu.com' in info['gnomeExtensions']:
            click.echo(click.style(f'Refreshing Extension: ', fg='green') + click.style(f'ubuntu-dock@ubuntu.com', fg='blue'))
            os.system(f'gnome-extensions disable ubuntu-dock@ubuntu.com')
            os.system(f'gnome-extensions enable ubuntu-dock@ubuntu.com')

        for extension in allExtenstions:
            if extension in info['gnomeExtensions']:
                if extension != 'ubuntu-dock@ubuntu.com':
                    click.echo(click.style(f'Refreshing Extension: ', fg='green') + click.style(f'{extension}', fg='blue'))
                    os.system(f'gnome-extensions disable {extension}')
                    os.system(f'gnome-extensions enable {extension}')
            else:
                os.system(f'gnome-extensions disable {extension}')


@click.command( help='List all saved slots')
@click.option('--all/--no-all', default=False)
def list(all):
    Slots = []
    if not all:
        for slotname in os.listdir(f"{SlotsFolder}/"):
            if json.load(open(f'{FolderPath}/Slots/{slotname}/info.json'))['desktopEnvironment'] == DE and json.load(open(f'{FolderPath}/Slots/{slotname}/info.json'))['windowManager'] == WM:
                Slots.append(slotname)
    else:
        Slots = os.listdir(f"{SlotsFolder}/")
    SlotNumber = 0
    click.echo(click.style('Slots:', fg='green'))
    for slotname in Slots:
        SlotNumber += 1
        click.echo(click.style(f'{SlotNumber}) {slotname}', fg='blue'))

@click.command(help='Delete existing slot')
@click.argument('slotname')
def delete(slotname):
    slotname = slotname
    if os.path.isdir(f'{SlotsFolder}/{slotname}'):
        Confirmation = click.prompt(click.style(
            f'Are you sure you want to delete "{slotname}" [Y/n] ', fg='red'))
        if Confirmation.lower().strip() == 'y':
            os.system(f'rm -rf {SlotsFolder}/"{slotname}"')
            click.echo(click.style('Successfully Deleted Slot', fg='green'))
        elif Confirmation.lower().strip() == 'n':
            click.echo(click.style('Ok not deleting', fg='green'))
        else:
            click.echo(click.style('invalid input', fg='red'))
    else:
        click.echo(click.style(
            'No Slot like that. Use command "themesaver ls" to print the list of slots', fg='red'))

@click.command(help='Export Slot To Upload To Shop')
@click.argument('slotname')
@click.argument('filepath',  type=click.Path(exists=True))
def export(slotname, filepath):
    filepath = Path(filepath)
    slotname = Path(slotname)
    if not os.path.isdir(f'{SlotsFolder}/{slotname}'):
        click.echo(click.style('No slot like that. Use command "themesaver ls" to print the list of saved slots', fg='red'))
        quit()

    if DE == 'gnome' and WM == 'gnome shell':
        click.echo(click.style('Gnome Export Is Still a work in progress :(', fg='red'))
        quit()


    if Path(filepath/slotname).exists():
        os.system(f'rm -rf {Path(filepath/slotname)}')
    os.mkdir(Path(filepath/slotname))        

    # A Function to find where the icon theme or cursor is stored
    def checkUsrLocal(path, name, Filepath, message):
        paths = [f'/usr/share/{path}' + name.strip("'"), f'{HomePath}/.local/share/{path}' + name.strip("'"), f'{HomePath}/.{path}' + name.strip("'")]
        for p in paths:
            if os.path.isdir(p):
                os.system(f'cp -rf {p} {Filepath}')
                click.echo(click.style(f'Exporting {message}: ', fg='green') + click.style(f'{p}', fg='blue'))
                break

    info = json.load(open(f'{SlotsFolder}/{slotname}/info.json'))

    click.echo(click.style(f'=========[ EXPORTING SLOT: {slotname} ]=========', fg='green'))
    print()

    os.mkdir(Path(filepath / slotname / 'theme'))
    checkUsrLocal(f'themes/', info['gtkTheme'], f'{filepath}/{slotname}/theme/', 'GtkTheme' )

    os.mkdir(Path(filepath / slotname / 'icons'))
    checkUsrLocal(f'icons/', info['iconTheme'] , f'{filepath}/"{slotname}"/icons/', 'IconTheme')

    os.mkdir(Path(filepath / slotname / 'cursors'))
    checkUsrLocal(f'icons/', info['cursorTheme'], f'{filepath}/"{slotname}"/cursors/', 'Cursors')

    # if DE == 'gnome' and WM == 'gnome shell':
    #     os.mkdir(Path(filepath / slotname / 'gnomeExtensions'))
    #     for extension in info['gnomeExtensions']:
    #         if os.path.isdir(f'{HomePath}/.local/share/gnome-shell/extensions/{extension}'):
    #             os.system(f'cp -r "{HomePath}/.local/share/gnome-shell/extensions/{extension}" "{filepath}/{slotname}/gnomeExtensions"')
    #         elif os.path.isdir(f'/usr/share/gnome-shell/extensions/{extension}'):
    #             os.system(f'cp -r "/usr/share/gnome-shell/extensions/{extension}" "{filepath}/{slotname}/gnomeExtensions"')


    # Exporting Plank Theme
    if os.path.isdir(f'{SlotsFolder}/{slotname}/plank'):
        PlankTheme = open(f'{SlotsFolder}/{slotname}/plank/theme').read().strip().replace("'", '')
        os.system(f'mkdir {filepath}/"{slotname}"/plank')
        if os.path.isdir(f'{HomePath}/.local/share/plank/themes/{PlankTheme}'):
            os.system(f'cp -rf {HomePath}/.local/share/plank/themes/{PlankTheme} {filepath}/"{slotname}"/plank')
        elif os.path.isdir(f'/usr/share/plank/themes/{PlankTheme}'):
            os.system(f'cp -rf /usr/share/plank/themes/{PlankTheme} {filepath}/"{slotname}"/plank')

    # Exporting Slot
    os.system(f'mkdir {filepath}/"{slotname}"/slot/')
    os.system(f'cp -rf {SlotsFolder}/"{slotname}" {filepath}/"{slotname}"/slot/')
    click.echo(click.style(f'Exporting ', fg='green') + click.style(f'Slot Folder', fg='blue'))

    # Compressing files
    print()
    click.echo(click.style(f'Compressing Archive', fg='green'))
    tar = tarfile.open(f'{filepath}/{slotname}.tar.gz', 'w:gz')
    tar.add(f'{filepath}/{slotname}', arcname=f'{slotname}')
    tar.close()

    os.system(f'cp {SlotsFolder}/"{slotname}"/info.json {filepath}/info.json')

    # Cleaning Up
    os.system(f'rm -rf {filepath}/"{slotname}"')

    click.echo(click.style('Slot Exported To: ', fg='green') + click.style(f'{filepath}/{slotname}.tar.gz', fg='blue'))


@click.command(help='Import Slot')
@click.argument('filepath')
@click.option('--shop/--no-shop', default=False)
def Import(filepath, shop):

    ImportDir = Path(FolderPath / 'import')

    if not shop:
        if not Path(filepath).exists() or not filepath.endswith('.tar.gz'):
            print(f'{filepath} is not a valid filepath')
            exit()

    if DE == 'gnome' and WM == 'gnome shell':
        click.echo(click.style('Gnome Import Is Still a work in progress :(', fg='red'))
        quit()


    # Removing and creating import directory
    os.system(f'rm -rf {ImportDir}')
    os.mkdir(ImportDir)

    def getShop():
        url = filepath.split(':')
        r = requests.get(f'https://api.github.com/repos/{url[0]}/git/trees/{url[1]}?recursive=1')
        for i in r.json()['tree']:
            if i['path'].endswith('.tar.gz'):
                print(f'https://github.com/{url[0]}/blob/{url[1]}/{i["path"]}?raw=true')
                archive = requests.get(f'https://github.com/{url[0]}/blob/{url[1]}/{i["path"]}?raw=true', allow_redirects=True)
                open(Path(f'{FolderPath}/{i["path"]}'), 'wb').write(archive.content)
                print(Path(f'{FolderPath}/{i["path"]}'))
                return Path(f'{FolderPath}/{i["path"]}')
        else:
            return gui
                

    if shop == True:
        filepath = getShop()

    tarFile = tarfile.open(filepath)
    slotname = tarFile.getnames()[0]

    # Checking if a folder with that name exists when importing slot
    if Path( SlotsFolder / slotname).exists():
        Overwrite = click.prompt(click.style('A slot with that name already exists. Do you want to overwrite it ? [Y/n]', fg='red'), type=str)
        if Overwrite.lower() == 'y':
            click.echo(click.style('Okay overwriting', fg='green'))
            os.system(f'rm -rf {Path(SlotsFolder / tarFile.getnames()[0])}')
            print()
        else:
            print(click.style('Not overwriting', fg='green'))
            quit()

    ImportSlotDir = Path(ImportDir / slotname)

    click.echo(click.style('=========[ IMPORTING ARCHIVE ]=========', fg='blue'))
    # Extracting Archive
    with tarFile as tar:
        # Go over each member
        for member in tqdm(iterable=tar.getmembers(), total=len(tar.getmembers())):
            # Extract member
            tar.extract(member, f'{FolderPath}/import/')
        tar.close()

    #Importing themes and other stuff
    click.echo(click.style('\nImporting Slot', fg='green'))
    os.system(f'cp -rf {Path(ImportSlotDir)}/slot/* {SlotsFolder} &> /dev/null')

    click.echo(click.style('Importing Themes', fg='green'))
    if not os.path.isdir(Path('~/.local/share/themes').expanduser()):
        os.mkdir(Path('~/.local/share/themes').expanduser())
    os.system(f'cp -rf {Path(ImportSlotDir)}/theme/* ~/.local/share/themes &> /dev/null')

    click.echo(click.style('Importing Icons', fg='green'))
    if not os.path.isdir(Path('~/.local/share/icons').expanduser()):
        os.mkdir(Path('~/.local/share/icons').expanduser()) 
    os.system(f'cp -rf {Path(ImportSlotDir)}/icons/* ~/.local/share/icons &> /dev/null')

    click.echo(click.style('Importing Cursors', fg='green'))
    os.system(f'cp -rf {Path(ImportSlotDir)}/cursors/* ~/.local/share/icons &> /dev/null')

    # if os.path.isdir(f'{Path(ImportSlotDir)}/gnomeExtensions'):
    #     click.echo(click.style('Importing Gnome Extensions', fg='green'))
    #     os.system(f'mkdir ~/.local/share/gnome-shell/extensions')
    #     os.system(f'cp -rf {Path(ImportSlotDir)}/gnomeExtensions/* {HomePath}/.local/share/gnome-shell/extensions/ &> /dev/null')
    #     # Refreshing gnome shell so that the extenstions are registered by the gnome shell
    #     os.system(f''' busctl --user call org.gnome.Shell /org/gnome/Shell org.gnome.Shell Eval s 'Meta.restart("Restarting…")' ''')

    if Path(ImportSlotDir / 'plank').exists():
        click.echo(click.style('Importing Plank Theme', fg='green'))
        os.system('mkdir ~/.local/share/plank')
        os.system('mkdir ~/.local/share/plank/themes')
        os.system(f'cp -rf {Path(ImportSlotDir)}/plank/* ~/.local/share/plank/themes &> /dev/null')

    click.echo(click.style('Running import script', fg='green'))
    os.system(f'chmod +x {Path(ImportSlotDir)}/slot/*/import.sh')
    os.system(f'{Path(ImportSlotDir)}/slot/*/import.sh')

    #Removing import directory after Importing files
    os.system(f'rm -rf {ImportDir}')

    if shop:
        os.system(f'rm {filepath}')

    click.echo(click.style('Finished importing slot :)', fg='green'))
    quit()


@click.command(help='Launch the gui app for themesaver')
def gui():
    os.system(f'python3 {FolderPath}/GUI/MainWindow.py')

group.add_command(save)
group.add_command(load)
group.add_command(list)
group.add_command(delete)
group.add_command(export)
group.add_command(Import)
group.add_command(gui)

if __name__ == '__main__':
    group()


