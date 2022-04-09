import os, click, time, subprocess

def save(SlotsFolder, slotname, RequiredFoldersLXDE):
    for folder in RequiredFoldersLXDE:
        os.system(f'cp -rf ~/.config/{folder} {SlotsFolder}/"{slotname}"/configs &>/dev/null')

    if os.path.isfile(Path(f'~/.config/pcmanfm/LXDE-pi/desktop-items-0.conf').expanduser()):
        WallpaperPath = os.popen(f"sed -n '/wallpaper=/p' ~/.config/pcmanfm/LXDE-pi/desktop-items-0.conf").read().split('\n')[0].replace('wallpaper=', '')    
    else:
        WallpaperPath = os.popen(f"sed -n '/wallpaper=/p' /etc/xdg/pcmanfm/LXDE-pi/desktop-items-0.conf").read().split('\n')[0].replace('wallpaper=', '')     
    
    os.system(f'cp {WallpaperPath} /opt/themesaver/Slots/{slotname}/Wallpaper.png')

def load(SlotsFolder, slotname, RequiredFoldersLXDE, backupFolder):
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
