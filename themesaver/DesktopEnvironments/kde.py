import os, subprocess, click, time
from pathlib import Path

def save(SlotsFolder, slotname, RequiredKDEConfig, RequiredKDELocal):
    os.system(f'mkdir -p /opt/themesaver/{slotname}/share')
    for config in RequiredKDEConfig:
        os.system(f'cp -rf ~/.config/{config} {SlotsFolder}/"{slotname}"/configs &>/dev/null')

    for file in RequiredKDELocal:
        os.system(f'cp -rf ~/.local/share/{file} {SlotsFolder}/"{slotname}"/share &>/dev/null')

    WallpaperPath = os.popen(f"sed -n '/Image=/p' ~/.config/plasma-org.kde.plasma.desktop-appletsrc").read().strip()
    WallpaperPath = WallpaperPath.replace('Image=', '').replace('file://', '').strip()
    if os.path.isdir(WallpaperPath):
        WallpaperPath = f"{WallpaperPath}contents/images/{os.listdir(f'{WallpaperPath}contents/images/')[0]}"

    os.system(f'sed -i "s#{WallpaperPath.strip()}#Image=file:///opt/themesaver/Slots/{slotname}/Wallpaper.png#g" {SlotsFolder}/"{slotname}"/configs/plasma-org.kde.plasma.desktop-appletsrc')


    os.system(f'cp {WallpaperPath} /opt/themesaver/Slots/{slotname}/Wallpaper.png')

def load(SlotsFolder, slotname, backupFolder, RequiredKDEConfig, RequiredKDELocal, info):
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
     
