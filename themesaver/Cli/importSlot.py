from pathlib import Path
import os, tarfile, click
from tqdm import tqdm

def importSlot(filepath, shop, FolderPath, SlotsFolder, DE, WM):

    ImportDir = f"{FolderPath}/import"

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
    if os.path.isdir(f"{SlotsFolder}/{slotname}"):
        Overwrite = click.prompt(click.style('A slot with that name already exists. Do you want to overwrite it ? [Y/n]', fg='red'), type=str)
        if Overwrite.lower() == 'y':
            click.echo(click.style('Okay overwriting', fg='green'))
            os.system(f'rm -rf {SlotsFolder}/"{tarFile.getnames()[0]}"')
            print()
        else:
            print(click.style('Not overwriting', fg='green'))
            quit()

    ImportSlotDir = f"{ImportDir}/'{slotname}'"

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

    if os.path.isdir(f"{ImportSlotDir}/'plank'"):
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
