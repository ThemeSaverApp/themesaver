import os 
import sys
import time
import subprocess
import tarfile
from colorama import Fore, Back, Style

#Initialing List and Variables
RequiredChannelsXfce = [ 'xfce4-desktop', 'xfwm4','xsettings' ]
RequiredFoldersLXDE = ['lxsession', 'lxterminal', 'lxpanel', 'pcmanfm', 'openbox']
PlankProperties = ['theme', 'position', 'alignment']
FolderPath = f"{os.environ['HOME']}/.themesaver"


if not os.path.isdir(f'{FolderPath}/Slots/'):
    #Creating data directory if not there
    os.system(f'mkdir {FolderPath}/Slots/')

def SaveSlot(SlotName, Desktop_Environment):
    #Checking if there is a slot with the given name
    if os.path.isdir(f'{FolderPath}/Slots/{SlotName}'):
        #Aksing user if they want to overwrite existing slot
        Overwrite = input(Fore.RED + 'A slot with that name already exists. Do you want to overwrite it ? [Y/n]')
        if Overwrite.lower() == 'y':
            print(Fore.GREEN + 'Okay overwriting')
            #Removing old slot
            os.system(f'sudo rm -rf ~/.themesaver/Slots/"{SlotName}"')
        else:
            print(Fore.GREEN + 'Not overwriting')
            #Stopping the program if user does not want to overwrite
            quit()
    
    # Creating Slot
    os.system(f'mkdir ~/.themesaver/Slots/"{SlotName}"')

    #Taking Screenshot
    os.system('xdotool key ctrl+alt+d') #Hiding all windows on desktop
    time.sleep(2) #Waiting for two seconds
    os.system(f'scrot {FolderPath}/Slots/"{SlotName}"/Screenshot.png') #Taking a Screenshot
    os.system('xdotool key ctrl+alt+d') #Unhiding all windows on desktop
    os.system(f'convert {FolderPath}/Slots/"{SlotName}"/Screenshot.png -resize 470x275 {FolderPath}/Slots/"{SlotName}"/Screenshot.png')

    # Saving Plank Configs If Running
    PlankRunning = os.popen('pgrep plank').read()
    if PlankRunning != '':
        #Storing Plank Configuration
        os.system(f'mkdir ~/.themesaver/Slots/"{SlotName}"/plank')
        for PlankProperty in PlankProperties:
            os.system(f'gsettings get net.launchpad.plank.dock.settings:/net/launchpad/plank/docks/dock1/ {PlankProperty} > ~/.themesaver/Slots/"{SlotName}"/plank/{PlankProperty}')    

    # Saving Polybar Configs If Running
    PolybarRunning = os.popen('pgrep plank').read()
    if PolybarRunning != '':
        os.system(f'cp -rf ~/.config/polybar ~/.themesaver/Slots/"{SlotName}/"')

    # Storing Fish and OMF Fish configs
    if os.environ['SHELL'].strip() == '/usr/bin/fish':
        os.system(f'mkdir ~/.themesaver/Slots/"{SlotName}"/fish')
        os.system(f'cp -rf ~/.config/fish ~/.themesaver/Slots/"{SlotName}"/fish')
        os.system(f'cp -rf ~/.config/omf ~/.themesaver/Slots/"{SlotName}"/fish')

    if os.path.isfile('/usr/bin/rofi'):
        os.system(f'cp -rf ~/.config/rofi ~/.themesaver/Slots/"{SlotName}"/')

    if os.path.isfile('/usr/bin/nitrogen'):
        os.system(f'cp -rf ~/.config/nitrogen ~/.themesaver/Slots/"{SlotName}"/')


    if Desktop_Environment == 'xfce':
        for channel in RequiredChannelsXfce:
            os.system(f'xfconf-query -c {channel.strip()} -l > ~/.themesaver/Slots/{channel.strip()}')
            PropertiesFile = open(f'{FolderPath}/Slots/{channel.strip()}', 'r')
            Properties = PropertiesFile.readlines()
            os.system(f'mkdir ~/.themesaver/Slots/"{SlotName}"/{channel.strip()}')
            for Property in Properties:
                os.system(f'xfconf-query -c {channel.strip()} -p {Property.strip()} > ~/.themesaver/Slots/"{SlotName}"/{channel.strip()}/{Property.replace("/","+")}')
            
            os.system(f'rm ~/.themesaver/Slots/{channel.strip()}')
        os.system(f'xfce4-panel-profiles save ~/.themesaver/Slots/"{SlotName}"/"{SlotName}"')

    if Desktop_Environment == 'lxde':
        for folder in RequiredFoldersLXDE:
            os.system(f'cp -rf ~/.config/{folder} ~/.themesaver/Slots/"{SlotName}"')
    
    if Desktop_Environment == 'awesome':
        os.system(f'cp -rf ~/.config/awesome ~/.themesaver/Slots/"{SlotName}"')

    if Desktop_Environment == 'qtile':
        os.system(f'cp -rf ~/.config/qtile ~/.themesaver/Slots/"{SlotName}"')
        
def LoadSlot(SlotName, Desktop_Environment):
    if not os.path.isdir(f'{FolderPath}/Slots/{SlotName}'):
        print(Fore.RED + 'No slot like that exists. Use command `themesave list` to print the list of slots')
        quit()

    #Loading Plank configs if they exist
    if os.path.isdir(f'{FolderPath}/Slots/{SlotName}/plank') == True:
        subprocess.Popen(['nohup', 'plank'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        for PlankConfig in os.listdir(f'{FolderPath}/Slots/{SlotName}/plank'):
            PlankConfigFile = open(f'{FolderPath}/Slots/{SlotName}/plank/{PlankConfig}')
            PlankConfigData = PlankConfigFile.read()
            os.system(f'gsettings set net.launchpad.plank.dock.settings:/net/launchpad/plank/docks/dock1/ {PlankConfig} {PlankConfigData}')
    else:
        subprocess.Popen(['killall', 'plank'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    if os.path.isdir(f'{FolderPath}/Slots/{SlotName}/fish'):
        os.system(f'cp -rf ~/.themesaver/Slots/"{SlotName}"/fish/fish ~/.config/')
        os.system(f'cp -rf ~/.themesaver/Slots/"{SlotName}"/fish/omf ~/.config/')

    if os.path.isdir(f'{FolderPath}/Slots/{SlotName}/rofi'):
        os.system(f'cp -rf ~/.themesaver/Slots/"{SlotName}"/rofi ~/.config/')

    if os.path.isdir(f'{FolderPath}/Slots/{SlotName}/nitrogen'):
        os.system(f'cp -rf ~/.themesaver/Slots/"{SlotName}"/nitrogen ~/.config/')

    if os.path.isdir(f'{FolderPath}/Slots/{SlotName}/polybar'):
        os.system('cp -rf ~/.themesaver/polybar ~/.config')
        os.system('polybar --reload &')
    else:
        subprocess.Popen(['killall', 'polybar'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    if Desktop_Environment == 'xfce':
        for PropertyFolders in RequiredChannelsXfce:
            for PropertyFiles in os.listdir(f'{FolderPath}/Slots/{SlotName}/{PropertyFolders}'):
                PropertyFile = open(f'{FolderPath}/Slots/{SlotName}/{PropertyFolders}/{PropertyFiles}')
                PropertyFileValue = PropertyFile.read()
                PropertyFilePath = PropertyFiles.replace('+','/').strip()
                os.popen(f'xfconf-query -c {PropertyFolders.strip()} -p {PropertyFilePath} -s "{PropertyFileValue.strip()}" ') 

        os.system(f'xfce4-panel-profiles load ~/.themesaver/Slots/"{SlotName}"/"{SlotName}"')
        subprocess.Popen(['setsid', 'xfce4-panel', '&>/dev/null'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        os.system('clear')
   
    if Desktop_Environment == 'lxde':
        for folder in RequiredFoldersLXDE:
            os.system(f'sudo rm -rf ~/.config/{folder}')
            os.system(f'cp -rf ~/.themesaver/Slots/"{SlotName}"/{folder} ~/.config')

        # Refreshing Desktop
        subprocess.Popen(['killall', 'openbox-lxde-pi', 'openbox', 'pcmanfm', 'lxpanel'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        time.sleep(2) #Waiting for two seconds
        subprocess.Popen(['setsid', 'openbox-lxde-pi'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        time.sleep(2) #Waiting for two seconds
        subprocess.Popen(['nohup', 'lxpanel', '--profile', 'LXDE-pi'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        time.sleep(2) #Waiting for two seconds
        subprocess.Popen(['nohup', 'pcmanfm', '--desktop', '--profile', 'LXDE-pi'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    if Desktop_Environment == 'awesome':
        os.system(f'cp -rf ~/.themesaver/Slots/"{SlotName}"/awesome ~/.config')
        os.system('xdotool key ctrl+Super+r')
        os.system('nitrogen --restore')

    if Desktop_Environment == 'qtile':
        os.system(f'cp -rf ~/.themesaver/Slots/"{SlotName}"/qtile ~/.config')
        os.system('qtile cmd-obj -o cmd -f restart')
        os.system('nitrogen --restore')

def List():
    SlotNumber = 0
    print(Fore.GREEN + 'Slots:')
    for SlotNames in os.listdir(f'{FolderPath}/Slots/'):
        SlotNumber += 1
        print(Fore.CYAN + f'{SlotNumber}) ' + SlotNames)

def Del(SlotName):
    if os.path.isdir(f'{FolderPath}/Slots/{SlotName}'):
        Confirmation = input(Fore.RED + f'Are you sure you want to delete "{SlotName}" [Y/n] ')
        if Confirmation.lower().strip() == 'y':
            print(Fore.GREEN + 'Ok deleting')
            os.system(f'rm -rf {FolderPath}/Slots/"{SlotName}"')
        elif Confirmation.lower().strip() == 'n':
            print(Fore.RED + 'Ok not deleting')
        else:
            print(Fore.RED + 'Invalid input')
    else:
        print(Fore.RED + 'No Slot like that. Use command "themesaver ls" to print the list of slots')

def Export(SlotName, ExportPath):
    if "DESKTOP_SESSION" in os.environ:
            Desktop_Environment = os.environ["DESKTOP_SESSION"]
    else:    
            Desktop_Environment = os.popen("wmctrl -m").read().split('\n')[0].replace('Name: ', '')    
    SupportedDesktopWindowEnvironments = ['xfce']
    if not Desktop_Environment.lower() in SupportedDesktopWindowEnvironments:
        print(Fore.RED + 'Your Desktop Environment is not supported')
        quit()

    if not os.path.isdir(f'{FolderPath}/Slots/{SlotName}'):
        print(Fore.RED + 'No slot like that. Use command "themesaver ls" to print the list of saved slots')
        quit()

    os.system(f'mkdir {ExportPath}/"{SlotName}"')

    ThemeFile = open(f'{FolderPath}/Slots/{SlotName}/xsettings/+Net+ThemeName')
    Theme = ThemeFile.read()
    Theme = Theme.strip()
    os.system(f'mkdir {ExportPath}/"{SlotName}"/theme')
    if os.path.isdir(f'{HomePath}/.themes/{Theme}'):
        os.system(f'cp -rf ~/.themes/{Theme} {ExportPath}/"{SlotName}"/theme/')
    elif os.path.isdir(f'/usr/share/themes/{Theme}'):
        os.system(f'cp -rf /usr/share/themes/{Theme} {ExportPath}/"{SlotName}"/theme/')

    IconThemeFile = open(f'{FolderPath}/Slots/{SlotName}/xsettings/+Net+IconThemeName')
    IconTheme = IconThemeFile.read()
    IconTheme = IconTheme.strip()
    os.system(f'mkdir {ExportPath}/"{SlotName}"/icons')
    if os.path.isdir(f'{HomePath}/.icons/{IconTheme}'):
        os.system(f'cp -rf ~/.icons/{IconTheme} {ExportPath}/"{SlotName}"/icons/')
    elif os.path.isdir(f'/usr/share/icons/{IconTheme}'):
        os.system(f'cp -rf /usr/share/icons/{IconTheme} {ExportPath}/"{SlotName}"/icons/')

    CursorThemeFile = open(f'{FolderPath}/Slots/{SlotName}/xsettings/+Gtk+CursorThemeName')
    CursorTheme = CursorThemeFile.read()
    CursorTheme = CursorTheme.strip()
    os.system(f'mkdir {ExportPath}/"{SlotName}"/cursors')
    if os.path.isdir(f'{HomePath}/.icons/{CursorTheme}'):
        os.system(f'cp -rf ~/.icons/{CursorTheme} {ExportPath}/"{SlotName}"/cursors/')
    elif os.path.isdir(f'/usr/share/icons/{CursorTheme}'):
        os.system(f'cp -rf /usr/share/icons/{CursorTheme} {ExportPath}/"{SlotName}"/cursors/')


    if os.path.isdir(f'{FolderPath}/Slots/{SlotName}/plank'):
        PlankThemeFile = open(f'{FolderPath}/Slots/{SlotName}/plank/theme')
        PlankTheme = PlankThemeFile.read()
        PlankTheme = PlankTheme.strip().replace("'", '')
        os.system(f'mkdir {ExportPath}/"{SlotName}"/plank')
        if os.path.isdir(f'{HomePath}/.local/share/plank/themes/{PlankTheme}'):
            os.system(f'cp -rf {HomePath}/.local/share/plank/themes/{PlankTheme} {ExportPath}/"{SlotName}"/plank')
        elif os.path.isdir(f'/usr/share/plank/themes/{PlankTheme}'):
            os.system(f'cp -rf /usr/share/plank/themes/{PlankTheme} {ExportPath}/"{SlotName}"/plank')


    WallpaperFile = open(f'{FolderPath}/Slots/{SlotName}/xfce4-desktop/+backdrop+screen0+monitor0+workspace0+last-image')
    Wallpaper = WallpaperFile.read()
    Wallpaper = Wallpaper.strip()
    os.system(f'mkdir {ExportPath}/"{SlotName}"/wallpaper/')
    os.system(f'cp {Wallpaper} {ExportPath}/"{SlotName}"/wallpaper/')

    os.system(f'mkdir {ExportPath}/"{SlotName}"/slot/')
    os.system(f'cp -rf ~/.themesaver/Slots/"{SlotName}" {ExportPath}/"{SlotName}"/slot/')
    tar = tarfile.open(f'{ExportPath}/{SlotName}.tar.gz', 'w:gz')
    tar.add(f'{ExportPath}/{SlotName}', arcname=f'{SlotName}')
    tar.close()
    os.system(f'rm -rf {ExportPath}/"{SlotName}"')
    print(Fore.GREEN + 'Finished exporting slot ')

def Import(FilePath):
    if "DESKTOP_SESSION" in os.environ:
            Desktop_Environment = os.environ["DESKTOP_SESSION"]
    else:    
            Desktop_Environment = os.popen("wmctrl -m").read().split('\n')[0].replace('Name: ', '')    
    SupportedDesktopWindowEnvironments = ['xfce']
    if not Desktop_Environment.lower() in SupportedDesktopWindowEnvironments:
        print(Fore.RED + 'Your Desktop Environment is not supported')
        quit()

    if not os.path.isfile(FilePath):
        print(Fore.RED + 'No File Like That')
        quit()
    #Removing and creating import directory
    os.system('rm -rf ~/.themesaver/import/')
    os.system('mkdir ~/.themesaver/import/')

    #Extracting archive
    file = tarfile.open(FilePath)
    file.extractall(f'{FolderPath}/import/') 
    file.close() 

    #Copying themes and other stuff
    print(Fore.GREEN + 'Copying slot')
    os.system(f'cp -rf {FolderPath}/import/*/slot/* ~/.themesaver/Slots/')

    print(Fore.GREEN + 'Copying themes')
    os.system(f'sudo cp -rf {FolderPath}/import/*/theme/* /usr/share/themes/')

    print(Fore.GREEN + 'Copying icons')
    os.system(f'sudo cp -rf {FolderPath}/import/*/icons/* /usr/share/icons/')

    print(Fore.GREEN + 'Copying cursors')
    os.system(f'sudo cp -rf {FolderPath}/import/*/cursors/* /usr/share/icons/')

    print(Fore.GREEN + 'Copying plank theme')
    os.system(f'sudo cp -rf {FolderPath}/import/*/plank/* /usr/share/plank/themes/')

    print(Fore.GREEN + 'Copying wallpaper')
    os.system(f'echo $(cat {FolderPath}/import/*/slot/*/xfce4-desktop/+backdrop+screen0+monitor0+workspace0+last-image) > ~/.themesaver/import/wallpaperpath')
    WallpaperPathFile = open(f'{FolderPath}/import/wallpaperpath')
    WallpaperPath = WallpaperPathFile.read()
    os.system(f'sudo cp ~/.themesaver/import/*/wallpaper/* {WallpaperPath}')

    #Removing import directory after copying files
    os.system('rm -rf ~/.themesaver/import')

    print(Fore.GREEN + 'Finished importing slot :)')

def uninstall():
    Confirmation = input(Fore.CYAN + 'Are you sure you want to uninstall themesaver ? [Y/n] ')
    if Confirmation.lower().strip() == 'y':
        print(Fore.GREEN + 'Ok uninstalling')
        os.system(f'python3 {FolderPath}/uninstall.py')
    elif Confirmation.lower().strip() == 'n':
        print(Fore.RED + 'Ok not uninstalling')
        quit()
    else:
        print(Fore.RED + 'Invalid input')

def help():
    print(Fore.GREEN + 'Available arguments:')
    print(Fore.GREEN + '1) ' + Fore.CYAN + '`save [slotname]`' + Fore.GREEN + ' Save a new slot')
    print(Fore.GREEN + '2) ' + Fore.CYAN + '`load [slotname]`' + Fore.GREEN + ' Load existing slot')
    print(Fore.GREEN + '3) ' + Fore.CYAN + '`del [slotname]`' + Fore.GREEN + ' Delete a slot')
    print(Fore.GREEN + '4) ' + Fore.CYAN + '`ls`' + Fore.GREEN + ' List all saved slots')
    print(Fore.GREEN + '5) ' + Fore.CYAN + '`gui`' + Fore.GREEN + ' Launches GUI for themesaver')
    print(Fore.GREEN + '6) ' + Fore.CYAN + '`uninstall`' + Fore.GREEN + ' Uninstalls themesaver :(')
    print(Fore.GREEN + '7) ' + Fore.CYAN + '`help`' + Fore.GREEN + ' Get a list of available argument')

#Terminal Usage

if "DESKTOP_SESSION" in os.environ:
    Desktop_Environment = os.environ["DESKTOP_SESSION"].strip().lower()
else:    
    if not os.path.isfile("/usr/bin/wmctrl"):
        os.system('sudo pacman -S wmctrl')
    Desktop_Environment = os.popen("wmctrl -m").read().split('\n')[0].replace('Name: ', '').strip().lower()
 
SupportedDesktopWindowEnvironments = ['xfce', 'lxde-pi', 'lxde', 'awesome', 'qtile']

if len(sys.argv) > 1:
    if sys.argv[1].lower() == 'load':
        if len(sys.argv) > 2:
            SlotName = sys.argv[2]
            if Desktop_Environment in SupportedDesktopWindowEnvironments:
                LoadSlot(SlotName, Desktop_Environment)
        else:
            print(Fore.RED + 'Enter Valid Slot Name')


    elif sys.argv[1].lower() == 'save':
        if len(sys.argv) > 2:
            SlotName = sys.argv[2]
            if Desktop_Environment in SupportedDesktopWindowEnvironments:
                SaveSlot(SlotName, Desktop_Environment)
        else:
            print(Fore.RED + 'Enter Valid Slot Name')


    elif sys.argv[1].lower() == 'delete' or sys.argv[1].lower() == 'del' :
        if len(sys.argv) > 2:
            Slot = sys.argv[2]
            Del(Slot)
        else:
            print(Fore.RED + 'Enter Valid Slot Name')


    elif sys.argv[1].lower() == 'export':
        if len(sys.argv) > 3:
            if len(sys.argv) > 2:
                SlotName = sys.argv[2]
                FilePath = sys.argv[3]
                Export(SlotName, FilePath)
            else:
                print(Fore.RED + 'Enter Valid Slot Name')
        else:
            print(Fore.RED + 'Enter Valid File Path')


    elif sys.argv[1].lower() == 'import':
        if len(sys.argv) > 2:
            FilePath = sys.argv[2]
            if Desktop_Environment == 'xfce':
                Import(FilePath)      
        else:
            print(Fore.RED + 'Enter Valid File Path')


    elif sys.argv[1].lower() == 'list' or sys.argv[1].lower() == 'ls':
        List()


    elif sys.argv[1].lower() == 'gui':
        os.system('python3 ~/.themesaver/GUI/MainWindow.py')


    elif sys.argv[1].lower() == 'uninstall':
        uninstall()


    elif sys.argv[1] == 'help':
        help()

    else:
        print(Fore.RED + 'Please Enter Valid Argument, Use command `themesaver help` to get a list of available arguments')
else:
    print(Fore.RED + 'Please Enter Valid Argument, Use command `themesaver help` to get a list of available arguments')
