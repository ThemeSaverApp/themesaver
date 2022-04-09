import os, json, click
from pathlib import Path

def slotInfo(SlotsFolder, slotname, DE, WM, gtkTheme, iconTheme, cursorTheme, shell):

    info = {
        "name": slotname,
        "gtkTheme": gtkTheme,
        "iconTheme": iconTheme,
        "cursorTheme": cursorTheme,
        "shell": shell,
        "desktopEnvironment": DE.strip(),
        "windowManager": WM.strip(),
    }

    if DE == 'gnome' or DE == 'pop:gnome' and WM == 'gnome shell':
        gnomeExtensions = os.popen('gsettings get org.gnome.shell enabled-extensions').read().replace(' ', '').replace('\'', '').replace('[', '').replace(']', '').split(',')
        for ext in gnomeExtensions:
            gnomeExtensions[gnomeExtensions.index(ext)] = ext.strip()
        info['gnomeExtensions'] = gnomeExtensions    
  
    # Serializing json 
    jsonPath = Path(f'{SlotsFolder}/{slotname}/info.json')
    jsonPath.write_text(json.dumps(info , indent = 4))

    print()

    os.system(f'touch {SlotsFolder}/"{slotname}"/import.sh')

    click.echo(click.style('======= Slot Info =======', fg='green'))

    for info,value in info.items():
        click.echo(click.style(f'{info}: ', fg='green') + click.style(f'{value}', fg='blue'))
