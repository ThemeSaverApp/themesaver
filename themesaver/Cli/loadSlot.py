import os, sys, click, time, json
from themesaver.WindowManagers import qtile, awesome, i3
from themesaver.DesktopEnvironments import kde, gnome, xfce, lxde
from dotenv import load_dotenv, dotenv_values

AppConfig = dotenv_values(f"{os.environ['HOME']}/.config/themesaver/config.env")


# Arrays cannot be stored in .env files so converting the string into an array
def convertArray(key):
    return AppConfig[key].replace('\'', '').replace(' ', '').replace('[', '').replace(']', '').split(',')

RequiredChannelsXfce = convertArray('Xfce')
RequiredFoldersLXDE = convertArray('LXDE')
RequiredKDEConfig = convertArray('KDEConf')
RequiredKDELocal = convertArray('KDELocal')

def loadSlot(SlotsFolder, slotname, DE, WM):
    if os.path.isdir(f'{SlotsFolder}/{slotname}') == False:
        click.echo(click.style('No slot like that exists. Use command `themesaver ls` to print the list of slots', fg='red'))
        quit()

    info = json.load(open(f'{SlotsFolder}/{slotname}/info.json'))
    if info['desktopEnvironment'] != DE and info['windowManager'] != WM:
        click.echo(click.style(f'This slot was made for the {info["desktopEnvironment"]} Desktop Environment and the {info["windowManager"]} window manager', fg='red'))
        quit()


    if not os.path.isdir(os.path.expanduser('~/.config_backups')):
        os.system(f'mkdir ~/.config_backups')
    backupFolder = f'Backup - {str(time.strftime("%a, %H:%M:%S", time.localtime()))}'
    os.system(f'mkdir ~/.config_backups/"{backupFolder}"')

    # Restoring Config Files
    click.echo(click.style(f'=========[ RESTORING CONFIG FILES ]=========', fg='green'))
    for config in os.listdir(f'{SlotsFolder}/{slotname}/configs'):
        click.echo(click.style(f'Restoring Config: ', fg='green') + click.style(f'{config}', fg='blue'))
        os.system(f'mv ~/.config/{config} ~/.config_backups/"{backupFolder}" &>/dev/null')
        os.system(f'cp -rf {SlotsFolder}/"{slotname}"/configs/{config} ~/.config/')

    if WM == 'qtile':
        qtile.load()        

    if DE == 'kde' and WM == 'kwin':
        kde.load(SlotsFolder, slotname, backupFolder, RequiredKDEConfig, RequiredKDELocal, info)

    if DE == 'gnome' or DE == 'pop:gnome' and WM == 'gnome shell':
        gnome.load(SlotsFolder, slotname, info)

    if DE == 'xfce' and WM == 'xfwm4':
        xfce.load(SlotsFolder, slotname, RequiredChannelsXfce)

    if DE == 'lxde':
        lxde.load(SlotsFolder, slotname, RequiredFoldersLXDE, backupFolder)