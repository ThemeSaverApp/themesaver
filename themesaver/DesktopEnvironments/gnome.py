import os, click

def save(SlotsFolder, slotname):
    os.system(f'dconf dump / > {SlotsFolder}/"{slotname}"/{slotname}')
    WallpaperPath = os.popen('gsettings get org.gnome.desktop.background picture-uri').read().strip().replace('file://', '').replace('\'', '')
    os.system(f'cp {WallpaperPath} /opt/themesaver/Slots/{slotname}/Wallpaper.png')

def load(SlotsFolder, slotname, info):
    HomePath = os.environ['HOME']
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

