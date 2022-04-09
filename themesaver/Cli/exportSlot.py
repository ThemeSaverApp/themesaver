import os, tarfile, click, json, pathlib
from pathlib import Path

HomePath = os.environ['HOME']

def exportSlot(SlotsFolder, slotname, filepath, DE, WM):
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