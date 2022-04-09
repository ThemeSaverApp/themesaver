import os, sys, click, time
from themesaver.WindowManagers import qtile, awesome, i3
from themesaver.DesktopEnvironments import kde, gnome, xfce, lxde
from themesaver.Misc.slotInfo import slotInfo
from themesaver.Misc.getInfo import getGtkTheme, getIconTheme, getCursorTheme, getShell
from dotenv import load_dotenv, dotenv_values

AppConfig = dotenv_values(f"{os.environ['HOME']}/.config/themesaver/config.env")

# Arrays cannot be stored in .env files so converting the string into an array
def convertArray(key):
    return AppConfig[key].replace('\'', '').replace(' ', '').replace('[', '').replace(']', '').split(',')

RequiredChannelsXfce = convertArray('Xfce')
RequiredFoldersLXDE = convertArray('LXDE')
RequiredKDEConfig = convertArray('KDEConf')
RequiredKDELocal = convertArray('KDELocal')

def saveSlot(SlotsFolder, slotname, DE, WM, Configs):
    print(DE, WM)
    # Overwrite Check
    Overwrite = False
    if os.path.isdir(f'{SlotsFolder}/{slotname}'):
        Overwrite = click.prompt(click.style('A slot with that name already exists. Do you want to overwrite it ? [Y/n]', fg='red'), type=str)
        if Overwrite.lower() == 'y':
            click.echo(click.style('Okay overwriting', fg='green'))
            # os.system(f'rm -rf {SlotsFolder}/"{slotname}"')
        else:
            print(click.style('Not overwriting', fg='green'))
            quit()

    click.echo(click.style('======= Saving Slot =======', fg='green'))

    # Creating Slot
    if not Overwrite:
        os.system(f'mkdir -p "{SlotsFolder}/{slotname}"')

    # Taking a Screenshot  
    path = os.path.dirname(__file__).replace('/Cli', '')
    os.system(f'{path}/TakeScreenshot.sh &')
    time.sleep(0.5)
    os.system(f'rm {SlotsFolder}/"{slotname}"/Screenshot.png')
    os.system(f'scrot {SlotsFolder}/"{slotname}"/Screenshot.png')
    os.system(f'convert {SlotsFolder}/"{slotname}"/Screenshot.png -resize 470x275 {SlotsFolder}/"{slotname}"/Screenshot.png')

    # Saving All Configs
    for config in Configs:
        click.echo(click.style(f'Saving config: ', fg='green') + click.style(f'{config}', fg='blue'))
        os.system(f'cp -rf ~/.config/{config} {SlotsFolder}/"{slotname}"/configs &>/dev/null')

    slotInfo(SlotsFolder, slotname, DE, WM, getGtkTheme(), getIconTheme(), getCursorTheme(), getShell())

    if WM == 'qtile':
        qtile.save(SlotsFolder, slotname)
    if WM == 'awesome':
        awesome.save(SlotsFolder, slotname)
    if WM == 'i3':
        i3.save(SlotsFolder, slotname)
    if DE == 'kde' and WM == 'kwin':
        kde.save(SlotsFolder, slotname, RequiredKDEConfig, RequiredKDELocal)
    if DE == 'gnome' or DE == 'pop:gnome' and WM == 'gnome shell':
        gnome.save(SlotsFolder, slotname)
    if DE == 'xfce' and WM == 'xfwm4':
        xfce.save(SlotsFolder, slotname, RequiredChannelsXfce)
    if DE == 'lxde':
        lxde.save(SlotsFolder, slotname, RequiredFoldersLXDE)