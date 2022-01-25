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

DE = os.environ['DESKTOP_SESSION'].lower()
WM = os.popen("wmctrl -m").read().split('\n')[0].replace('Name: ', '').lower()
HomePath = os.environ['HOME']

# Folder Paths
FolderPath = Path(AppConfig['FolderPath']).expanduser()
SlotsFolder = Path(FolderPath / 'Slots').expanduser()
ConfigFolder = Path('~/.config').expanduser()



@click.group()
def group():
    pass

@click.command(help='Save a new slot')
@click.argument('slotname' )
def save(slotname):
    if not SlotsFolder.exists():
        os.system(f'mkdir {SlotsFolder}')

    # Overwrite Check
    if Path(SlotsFolder / slotname).exists():
        Overwrite = click.prompt(click.style(
            'A slot with that name already exists. Do you want to overwrite it ? [Y/n]', fg='red'), type=str)
        if Overwrite.lower() == 'y':
            click.echo(click.style('Okay overwriting', fg='green'))
            os.system(f'rm -rf {SlotsFolder}/"{slotname}"')
        else:
            print(click.style('Not overwriting', fg='green'))
            quit()



    # Creating Slot
    os.mkdir(Path(SlotsFolder / slotname))

    # Taking a Screenshot  
    os.system(f'{FolderPath}/TakeScreenshot.sh &')
    time.sleep(0.5)
    os.system(f'scrot {SlotsFolder}/"{slotname}"/Screenshot.png')
    os.system(f'convert {SlotsFolder}/"{slotname}"/Screenshot.png -resize 470x275 {SlotsFolder}/"{slotname}"/Screenshot.png')

    # Saving Plank Configs If Running
    PlankRunning = os.popen('pgrep plank').read()
    if PlankRunning != '':
        # Storing Plank Configuration
        os.mkdir(Path(SlotsFolder / slotname / 'plank'))(f'mkdir {SlotsFolder}/"{slotname}"/plank')
        for PlankProperty in PlankProperties:
            os.system(
                f'gsettings get net.launchpad.plank.dock.settings:/net/launchpad/plank/docks/dock1/ {PlankProperty} > {SlotsFolder}/"{slotname}"/plank/{PlankProperty}')

    os.mkdir(SlotsFolder / slotname / 'configs')

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
        os.mkdir(SlotsFolder / slotname / shell)
        for file in shells[shell]:
            os.system(
                f'cp -rf {file} {SlotsFolder}/"{slotname}"/{shell}')

    for config in Configs:
        os.system(f'cp -rf ~/.config/{config} {SlotsFolder}/"{slotname}"/configs &>/dev/null')


    if DE == 'plasma' and WM == 'kwin':
        os.mkdir(SlotsFolder / slotname / 'share')
        for config in RequiredKDEConfig:
            os.system(f'cp -rf ~/.config/{config} {SlotsFolder}/"{slotname}"/configs &>/dev/null')

        for file in RequiredKDELocal:
            os.system(f'cp -rf ~/.local/share/{file} {SlotsFolder}/"{slotname}"/share &>/dev/null')


    if DE == 'xfce' and WM == 'xfwm4':
        for channel in RequiredChannelsXfce:
            os.system(f'xfconf-query -c {channel.strip()} -l > {SlotsFolder}/{channel.strip()}')
            PropertiesFile = open(f'{SlotsFolder}/{channel.strip()}', 'r')
            Properties = PropertiesFile.readlines()
            os.mkdir(SlotsFolder / slotname / channel.strip())
            for Property in Properties:
                os.system(f'xfconf-query -c {channel.strip()} -p {Property.strip()} > {SlotsFolder}/"{slotname}"/{channel.strip()}/{Property.replace("/","+")}')

            os.system(f'rm {SlotsFolder}/{channel.strip()}')
        os.system(f'xfce4-panel-profiles save {SlotsFolder}/"{slotname}"/"{slotname}"')

    if DE == 'lxde' or DE == 'lxde-pi':
        for folder in RequiredFoldersLXDE:
            os.system(
                f'cp -rf ~/.config/{folder} {SlotsFolder}/"{slotname}"/configs &>/dev/null')

    if WM == 'awesome':
        os.system(f'cp -rf ~/.config/awesome {SlotsFolder}/"{slotname}"/configs &>/dev/null')

    if WM == 'qtile':
        os.system(f'cp -rf ~/.config/qtile {SlotsFolder}/"{slotname}"/configs &>/dev/null')


    
    if os.path.isdir(Path(f'~/.config/nitrogen').expanduser()):
        WallpaperPath = os.popen(f"sed -n '/file/p' ~/.config/nitrogen/bg-saved.cfg").read().split('\n')[0].replace('file=', '')
        print(WallpaperPath)

    if DE == 'lxde-pi':
        if os.path.isfile(Path(f'~/.config/pcmanfm/LXDE-pi/desktop-items-0.conf').expanduser()):
            WallpaperPath = os.popen(f"sed -n '/wallpaper=/p' ~/.config/pcmanfm/LXDE-pi/desktop-items-0.conf").read().split('\n')[0].replace('wallpaper=', '')    
        else:
            WallpaperPath = os.popen(f"sed -n '/wallpaper=/p' /etc/xdg/pcmanfm/LXDE-pi/desktop-items-0.conf").read().split('\n')[0].replace('wallpaper=', '')     
        
    if DE == 'plasma' and WM == 'kwin':
        WallpaperPath = os.popen(f"sed -n '/Image=file:/p' ~/.config/plasma-org.kde.plasma.desktop-appletsrc")

    if DE == 'xfce' and WM == 'xfwm4':
        for path in os.listdir(f'{SlotsFolder}/{slotname}/xfce4-desktop'):
            if path.endswith('last-image'):
                WallpaperPath = open(f'{SlotsFolder}/{slotname}/xfce4-desktop/{path}').read().strip()
                break

    if WallpaperPath.startswith(os.environ['HOME']):
        WallpaperPath = WallpaperPath.replace(os.environ['HOME'], '~')
        
    os.system(f'cp {WallpaperPath} {SlotsFolder}/"{slotname}"/Wallpaper')        

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
        "windowManager": WM.strip()
    }
  
    # Serializing json 
    jsonPath = Path(SlotsFolder / slotname / 'info.json')
    jsonPath.write_text(json.dumps(info , indent = 4))


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
        subprocess.Popen(['nohup', 'plank'],
                         stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        for PlankConfig in os.listdir(f'{SlotsFolder}/{slotname}/plank'):
            PlankConfigFile = open(
                f'{SlotsFolder}/{slotname}/plank/{PlankConfig}')
            PlankConfigData = PlankConfigFile.read()
            os.system(
                f'gsettings set net.launchpad.plank.dock.settings:/net/launchpad/plank/docks/dock1/ {PlankConfig} {PlankConfigData}')
    # Killing Plank If Configs dont exist
    else:
        subprocess.Popen(['killall', 'plank'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


    if not Path('~/.config_backups').expanduser().exists():
        os.system(f'mkdir ~/.config_backups')
    backupFolder = f'Backup - {str(time.strftime("%a, %H:%M:%S", time.localtime()))}'
    os.system(f'mkdir ~/.config_backups/"{backupFolder}"')


    if DE == 'plasma' and WM =='kwin':
        for config in RequiredKDEConfig:
            os.system(f'mv ~/.config/{config} ~/.config_backups/"{backupFolder}"')
            # os.system(f'cp -rf {SlotsFolder}/"{slotname}"/configs/{config} ~/.config')

        os.system(f'mkdir ~/.config_backups/"{backupFolder}"/share')
        for file in RequiredKDELocal:
            os.system(f'mv ~/.local/share/{file} ~/.config_backups/"{backupFolder}"/share')
            # os.system(f'cp -rf {SlotsFolder}/"{slotname}"/share/{file} ~/.local/share/')

    for config in os.listdir(f'{SlotsFolder}/{slotname}/configs/'):
        os.system(f'mv ~/.config/{config} ~/.config_backups/"{backupFolder}"')
        os.system(f'cp -rf {SlotsFolder}/"{slotname}"/configs/{config} ~/.config')
    
    os.system(f'cp -rf {SlotsFolder}/"{slotname}"/share/* ~/.local/share/ &>/dev/null')

    # Using subprocesss to run apps as os.system is not working properly with &>/dev/null

    def runApp(app, config):
        if Path(f'{SlotsFolder}/{slotname}/configs/{config}').exists():
            print(app)
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

    if os.path.isdir(f'{SlotsFolder}/{slotname}/configs/qtile'):
        os.system('qtile cmd-obj -o cmd -f restart')

    if os.path.isdir(f'{SlotsFolder}/{slotname}/configs/nitrogen'):
        os.system(f'nitrogen --save {AppConfig["NitrogenStyle"]} {SlotsFolder}/"{slotname}"/Wallpaper &>/dev/null')

    if DE == 'xfce':
        for PropertyFolders in RequiredChannelsXfce:
            for PropertyFiles in os.listdir(f'{SlotsFolder}/{slotname}/{PropertyFolders}'):
                PropertyFile = open(
                    f'{SlotsFolder}/{slotname}/{PropertyFolders}/{PropertyFiles}')
                PropertyFileValue = PropertyFile.read()
                PropertyFilePath = PropertyFiles.replace('+', '/').strip()
                os.popen(
                    f'xfconf-query -c "{PropertyFolders.strip()}" -p "{PropertyFilePath}" -s "{PropertyFileValue.strip()}" ')

        os.system(
            f'xfce4-panel-profiles load {SlotsFolder}/"{slotname}"/"{slotname}"')
        subprocess.Popen(['setsid', 'xfce4-panel', '&>/dev/null'],
                         stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        os.system('clear')

    if DE == 'lxde' or DE == 'lxde-pi':
        for config in RequiredFoldersLXDE:
            os.system(f'mv ~/.config/{config} ~/.config_backups/"{backupFolder}"')
            os.system(f'cp -rf {SlotsFolder}/"{slotname}"/configs/{config} ~/.config')

        # Refreshing Desktop
        subprocess.Popen(['killall', 'openbox-lxde-pi', 'openbox', 'pcmanfm',
                         'lxpanel'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        time.sleep(2)
        subprocess.Popen(['setsid', 'openbox-lxde-pi'],
                         stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        time.sleep(2)
        subprocess.Popen(['nohup', 'lxpanel', '--profile', 'LXDE-pi'],
                         stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        time.sleep(2)
        subprocess.Popen(['nohup', 'pcmanfm', '--desktop', '--profile',
                         'LXDE-pi'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    
    if DE == 'plasma' and WM =='kwin':
        # Kde cursors not setting automatically so setting manually
        if os.path.isfile(f'{SlotsFolder}/{slotname}/cursorTheme'):
            CursorThemeFile = open(f'{SlotsFolder}/{slotname}/cursorTheme')
            CursorTheme = CursorThemeFile.read()
            CursorTheme = CursorTheme.strip("'")
            print(f'gsettings set org.gnome.desktop.interface cursor-theme {CursorTheme}')
            os.system(f'gsettings set org.gnome.desktop.interface cursor-theme {CursorTheme}')

        os.system('setsid qdbus org.kde.KWin /KWin reconfigure &>/dev/null')
        os.system('setsid konsole -e kquitapp5 plasmashell && kstart5 plasmashell --windowclass plasmashell --window Desktop &>/dev/null')


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

    if Path(filepath/slotname).exists():
        os.system(f'rm -rf {Path(filepath/slotname)}')
    os.mkdir(Path(filepath/slotname))        

    # A Function to find where the icon theme or cursor is stored
    def checkUsrLocal(path, name, Filepath):
        paths = [f'/usr/share/{path}' + name.strip("'"), f'{HomePath}/.local/share/{path}' + name.strip("'"), f'{HomePath}/.{path}' + name.strip("'")]
        for p in paths:
            if os.path.isdir(p):
                os.system(f'cp -rf {p} {Filepath}')

    info = json.load(open(f'{SlotsFolder}/{slotname}/info.json'))

    os.mkdir(Path(filepath / slotname / 'theme'))
    checkUsrLocal(f'themes/', info['gtkTheme'], f'{filepath}/{slotname}/theme/' )

    os.mkdir(Path(filepath / slotname / 'icons'))
    checkUsrLocal(f'icons/', info['iconTheme'] , f'{filepath}/"{slotname}"/icons/')

    os.mkdir(Path(filepath / slotname / 'cursors'))
    checkUsrLocal(f'icons/', info['cursorTheme'], f'{filepath}/"{slotname}"/cursors/')

    # Exporting Wallpaper
    if os.path.isfile(f'{SlotsFolder}/{slotname}/wallpaperPath'):
        Wallpaper = Path(SlotsFolder / slotname / 'wallpaperPath').read_text().replace('\'', '').strip()
        os.mkdir(Path(filepath / slotname / 'wallpaper'))
        os.system(f"cp -r {Wallpaper} {Path(filepath / slotname / 'wallpaper')}")

    # Exporting Plank Theme
    if os.path.isdir(f'{SlotsFolder}/{slotname}/plank'):
        PlankTheme = open(f'{SlotsFolder}/{slotname}/plank/theme').read_text().strip().replace("'", '')
        os.system(f'mkdir {filepath}/"{slotname}"/plank')
        if os.path.isdir(f'{HomePath}/.local/share/plank/themes/{PlankTheme}'):
            os.system(f'cp -rf {HomePath}/.local/share/plank/themes/{PlankTheme} {filepath}/"{slotname}"/plank')
        elif os.path.isdir(f'/usr/share/plank/themes/{PlankTheme}'):
            os.system(f'cp -rf /usr/share/plank/themes/{PlankTheme} {filepath}/"{slotname}"/plank')

    # Exporting Slot
    os.system(f'mkdir {filepath}/"{slotname}"/slot/')
    os.system(f'cp -rf {SlotsFolder}/"{slotname}" {filepath}/"{slotname}"/slot/')

    # Compressing files
    tar = tarfile.open(f'{filepath}/{slotname}.tar.gz', 'w:gz')
    tar.add(f'{filepath}/{slotname}', arcname=f'{slotname}')
    tar.close()

    # Cleaning Up
    os.system(f'rm -rf {filepath}/"{slotname}"')

    click.echo(click.style('Finished exporting slot ', fg='green'))


@click.command(help='Import Slot')
@click.argument('filepath')
@click.option('--shop/--no-shop', default=False)
def Import(filepath, shop):

    ImportDir = Path(FolderPath / 'import')

    if not shop:
        if not Path(filepath).exists() or not filepath.endswith('.tar.gz'):
            print(f'{filepath} is not a valid filepath')
            exit()

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

    # print(filepath)
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

    print()


    #Importing themes and other stuff
    click.echo(click.style('Importing Slot', fg='green'))
    os.system(f'cp -rf {Path(ImportSlotDir)}/slot/* {SlotsFolder}/ &> /dev/null')

    click.echo(click.style('Importing Themes', fg='green'))
    if not os.path.isdir(Path('~/.local/share/themes').expanduser()):
        os.mkdir(Path('~/.local/share/themes').expanduser())
    os.system(f'cp -rf {Path(ImportSlotDir)}/theme/* ~/.local/share/themes &> /dev/null')

    click.echo(click.style('Importing Icons', fg='green'))
    if not os.path.isdir(Path('~/.local/share/icons').expanduser()):
        os.mkdir(Path('~/.local/share/icons').expanduser())    
    os.system(f'cp -rf {Path(ImportSlotDir)}/icons/* ~/.local/share/icons &> /dev/null')

    click.echo(click.style('Importing Cursors', fg='green'))
    os.system(f'cp -rf {Path(ImportSlotDir)}/cursors/* /usr/share/icons/ &> /dev/null')

    if Path(ImportSlotDir / 'plank').exists():
        click.echo(click.style('Importing Plank Theme', fg='green'))
        os.system(f'cp -rf {Path(ImportSlotDir)}/plank/* /usr/share/plank/themes/ &> /dev/null')


    click.echo(click.style('Importing Wallpaper', fg='green'))
    WallpaperPath = open(f"{Path(ImportSlotDir)}/slot/{os.listdir(f'{FolderPath}/import')[0]}/wallpaperPath").read()
    WallpaperFolder = '/'.join(WallpaperPath.split('/')[:-1])
    
    os.system(f'rm {WallpaperPath}')
    if not os.path.isdir(WallpaperFolder):
        os.makedirs(WallpaperFolder)
    os.system(f'cp {Path(ImportSlotDir)}/wallpaper/* {WallpaperPath}')

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


