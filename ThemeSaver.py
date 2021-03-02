import os 
import sys
import time
import subprocess
import tarfile
from colorama import Fore, Back, Style

#Initialing List and Variables
RequiredChannelsXfce = [ "xfce4-desktop", "xfwm4","xsettings" ]
RequiredFoldersLXDE = ['lxsession', 'lxterminal', 'lxpanel', 'pcmanfm', 'openbox']

#SaveSlotXfce Functions
def SaveSlotXfce(SlotName):
    #Checking if data directory is there
    if not os.path.isdir(f"/home/pi/ThemeSaver/data"):
        #Creating data directory if not there
        os.system('mkdir /home/pi/ThemeSaver/data')
    #Checking if there is a slot with the given name
    if os.path.isdir(f"/home/pi/ThemeSaver/data/{SlotName}"):
        #Aksing user if they want to overwrite existing slot
        Overwrite = input(Fore.RED + "A slot with that name already exists. Do you want to overwrite it ? [Y/n]")
        if Overwrite.lower() == 'y':
            print(Fore.GREEN + 'Okay overwriting')
            #Removing old slot
            os.system(f'rm -r ~/ThemeSaver/data/{SlotName}')
        else:
            print(Fore.GREEN + 'Not overwriting')
            #Stopping the program if user does not want to overwrite
            quit()
    
    #Creating a directory for slot in ~/ThemeSaver/data/
    os.system(f'mkdir ~/ThemeSaver/data/{SlotName}')
    #Taking Screenshot
    os.system('xdotool key ctrl+alt+d') #Hiding all windows on desktop
    time.sleep(2) #Waiting for two seconds
    os.system(f'scrot ~/ThemeSaver/data/{SlotName}/Screenshot.png') #Taking a Screenshot
    os.system('xdotool key ctrl+alt+d') #Unhiding all windows on desktop

    for channel in RequiredChannelsXfce:
        #Creating list of properties 
        os.system(f"xfconf-query -c {channel.strip()} -l > ~/ThemeSaver/data/{channel.strip()}")
        #Opening list of properties
        PropertiesFile = open(f'/home/pi/ThemeSaver/data/{channel.strip()}', 'r')
        #Reading list of proerties file
        Properties = PropertiesFile.readlines()
        #Creating a folder for slot
        os.system(f'mkdir ~/ThemeSaver/data/{SlotName}/{channel.strip()}')
        #Looping through properties in properties file
        for Property in Properties:
            #Storing the output of the xconf-query channels to file
            os.system(f'xfconf-query -c {channel.strip()} -p {Property.strip()} > ~/ThemeSaver/data/{SlotName}/{channel.strip()}/{Property.replace("/","+")}')
        
        #Delting List of properties file
        os.system(f"rm ~/ThemeSaver/data/{channel.strip()}")
    
    #Saving xfce4-panel configuration
    os.system(f"xfce4-panel-profiles save ~/ThemeSaver/data/{SlotName}/{SlotName}")
        
    #Checking if plank is running
    PlankRunning = os.popen('pgrep plank').read()
    if PlankRunning != "":
        #Storing Plank Configuration
        os.system(f"mkdir ~/ThemeSaver/data/{SlotName}/plank")
        #Plank Themes
        os.system(f'gsettings get net.launchpad.plank.dock.settings:/net/launchpad/plank/docks/dock1/ theme > ~/ThemeSaver/data/{SlotName}/plank/theme')
        #Plank Position
        os.system(f'gsettings get net.launchpad.plank.dock.settings:/net/launchpad/plank/docks/dock1/ position > ~/ThemeSaver/data/{SlotName}/plank/position')
        #Plank Alignment
        os.system(f'gsettings get net.launchpad.plank.dock.settings:/net/launchpad/plank/docks/dock1/ alignment > ~/ThemeSaver/data/{SlotName}/plank/alignment')

    print(Fore.GREEN + 'Finished Saving')

def LoadSlotXfce(SlotName):
    if not os.path.isdir(f'/home/pi/ThemeSaver/data/{SlotName}'):
        print(Fore.RED + 'No slot like that exists. Use command "themesave list" to print the list of slots')
        quit()
    for PropertyFolders in RequiredChannelsXfce:
        for PropertyFiles in os.listdir(f"/home/pi/ThemeSaver/data/{SlotName}/{PropertyFolders}"):
            PropertyFile = open(f"/home/pi/ThemeSaver/data/{SlotName}/{PropertyFolders}/{PropertyFiles}")
            PropertyFileValue = PropertyFile.read()
            PropertyFilePath = PropertyFiles.replace("+","/").strip()
            os.popen(f"xfconf-query -c {PropertyFolders.strip()} -p {PropertyFilePath} -s '{PropertyFileValue.strip()}' ") 

    #Loading Plank configs if they exist
    if os.path.isdir(f"/home/pi/ThemeSaver/data/{SlotName}/plank") == True:
        subprocess.Popen(["nohup", "plank"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        for PlankConfig in os.listdir(f"/home/pi/ThemeSaver/data/{SlotName}/plank"):
            PlankConfigFile = open(f"/home/pi/ThemeSaver/data/{SlotName}/plank/{PlankConfig}")
            PlankConfigData = PlankConfigFile.read()
            os.system(f"gsettings set net.launchpad.plank.dock.settings:/net/launchpad/plank/docks/dock1/ {PlankConfig} {PlankConfigData}")
    else:
        subprocess.Popen(["killall", "plank"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    os.system(f"xfce4-panel-profiles load ~/ThemeSaver/data/{SlotName}/{SlotName}")
    subprocess.Popen(["setsid", "xfce4-panel", "&>/dev/null"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    os.system('clear')

def RefreshDesktopLXDE():
    subprocess.Popen(["killall", "openbox-lxde-pi", "openbox", "pcmanfm", "lxpanel"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    time.sleep(2) #Waiting for two seconds
    subprocess.Popen(["setsid", "openbox-lxde-pi"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    time.sleep(2) #Waiting for two seconds
    subprocess.Popen(["nohup", "lxpanel", "--profile", "LXDE-pi"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    time.sleep(2) #Waiting for two seconds
    subprocess.Popen(["nohup", "pcmanfm", "--desktop", "--profile", "LXDE-pi"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    

def SaveSlotLXDE(SlotName):
    #Checking if data directory is there
    if not os.path.isdir(f"/home/pi/ThemeSaver/data"):
        #Creating data directory if not there
        os.system('mkdir /home/pi/ThemeSaver/data')
    #Checking if there is a slot with the given name
    if os.path.isdir(f"/home/pi/ThemeSaver/data/{SlotName}"):
        #Aksing user if they want to overwrite existing slot
        Overwrite = input(Fore.RED + "A slot with that name already exists. Do you want to overwrite it ? [Y/n]")
        if Overwrite.lower() == 'y':
            print(Fore.GREEN + 'Okay overwriting')
            #Removing old slot
            os.system(f'rm -r ~/ThemeSaver/data/{SlotName}')
        else:
            print(Fore.GREEN + 'Not overwriting')
            #Stopping the program if user does not want to overwrite
            quit()
    
    os.system(f'mkdir ~/ThemeSaver/data/{SlotName}')
    
    #Taking Screenshot
    os.system('xdotool key ctrl+alt+d') #Hiding all windows on desktop
    time.sleep(2) #Waiting for two seconds
    os.system(f'scrot ~/ThemeSaver/data/{SlotName}/Screenshot.png') #Taking a Screenshot
    os.system('xdotool key ctrl+alt+d') #Unhiding all windows on desktop
    
    for folder in RequiredFoldersLXDE:
        os.system(f'cp -r ~/.config/{folder} ~/ThemeSaver/data/{SlotName}')

def LoadSlotLXDE(SlotName):
    if not os.path.isdir(f'/home/pi/ThemeSaver/data/{SlotName}'):
        print(Fore.RED + 'No slot like that exists. Use command "themesave list" to print the list of slots')
        quit()
    for folder in RequiredFoldersLXDE:
        os.system(f'cp -r ~/ThemeSaver/data/{SlotName}/{folder} ~/.config')
    RefreshDesktopLXDE()

def List():
    SlotNumber = 0
    print(Fore.GREEN + 'Slots:')
    for SlotNames in os.listdir('/home/pi/ThemeSaver/data/'):
        SlotNumber += 1
        print(Fore.CYAN + f'{SlotNumber}) ' + SlotNames)

def Del(SlotName):
    if os.path.isdir(f'/home/pi/ThemeSaver/data/{SlotName}'):
        os.system(f'rm -r /home/pi/ThemeSaver/data/{SlotName}')
    else:
        print(Fore.RED + 'No Slot like that. Use command "themesaver list" to print the list of slots')

def Export(SlotName):
    if not os.path.isdir(f'/home/pi/ThemeSaver/data/{SlotName}'):
        print(Fore.RED + 'No slot like that. Use command "themesaver ls" to print the list of saved slots')
        quit()

    if not os.path.isdir('/home/pi/ThemeSaver/export/'):
        os.system(f'mkdir ~/ThemeSaver/export/')

    os.system(f'mkdir ~/ThemeSaver/export/{SlotName}')

    ThemeFile = open(f'/home/pi/ThemeSaver/data/{SlotName}/xsettings/+Net+ThemeName')
    Theme = ThemeFile.read()
    Theme = Theme.strip()
    os.system(f'mkdir ~/ThemeSaver/export/{SlotName}/theme')
    if os.path.isdir(f'/home/pi/.themes/{Theme}'):
        os.system(f'cp -r ~/.themes/{Theme} ~/ThemeSaver/export/{SlotName}/theme/')
    elif os.path.isdir(f'/usr/share/themes/{Theme}'):
        os.system(f'cp -r /usr/share/themes/{Theme} ~/ThemeSaver/export/{SlotName}/theme/')

    IconThemeFile = open(f'/home/pi/ThemeSaver/data/{SlotName}/xsettings/+Net+IconThemeName')
    IconTheme = IconThemeFile.read()
    IconTheme = IconTheme.strip()
    os.system(f'mkdir ~/ThemeSaver/export/{SlotName}/icons')
    if os.path.isdir(f'/home/pi/.icons/{IconTheme}'):
        os.system(f'cp -r ~/.icons/{IconTheme} ~/ThemeSaver/export/{SlotName}/icons/')
    elif os.path.isdir(f'/usr/share/icons/{IconTheme}'):
        os.system(f'cp -r /usr/share/icons/{IconTheme} ~/ThemeSaver/export/{SlotName}/icons/')

    CursorThemeFile = open(f'/home/pi/ThemeSaver/data/{SlotName}/xsettings/+Gtk+CursorThemeName')
    CursorTheme = CursorThemeFile.read()
    CursorTheme = CursorTheme.strip()
    os.system(f'mkdir ~/ThemeSaver/export/{SlotName}/cursors')
    if os.path.isdir(f'/home/pi/.icons/{CursorTheme}'):
        os.system(f'cp -r ~/.icons/{CursorTheme} ~/ThemeSaver/export/{SlotName}/cursors/')
    elif os.path.isdir(f'/usr/share/icons/{CursorTheme}'):
        os.system(f'cp -r /usr/share/icons/{CursorTheme} ~/ThemeSaver/export/{SlotName}/cursors/')


    if os.path.isdir(f'/home/pi/ThemeSaver/data/{SlotName}/plank'):
        PlankThemeFile = open(f'/home/pi/ThemeSaver/data/{SlotName}/plank/theme')
        PlankTheme = PlankThemeFile.read()
        PlankTheme = PlankTheme.strip().replace("'", "")
        os.system(f'mkdir ~/ThemeSaver/export/{SlotName}/plank')
        if os.path.isdir(f'/home/pi/.local/share/plank/themes/{PlankTheme}'):
            os.system(f'cp -r /home/pi/.local/share/plank/themes/{PlankTheme} ~/ThemeSaver/export/{SlotName}/plank')
        elif os.path.isdir(f'/usr/share/plank/themes/{PlankTheme}'):
            os.system(f'cp -r /usr/share/plank/themes/{PlankTheme} ~/ThemeSaver/export/{SlotName}/plank')


    WallpaperFile = open(f'/home/pi/ThemeSaver/data/{SlotName}/xfce4-desktop/+backdrop+screen0+monitor0+workspace0+last-image')
    Wallpaper = WallpaperFile.read()
    Wallpaper = Wallpaper.strip()
    os.system(f'mkdir ~/ThemeSaver/export/{SlotName}/wallpaper/')
    os.system(f'cp {Wallpaper} ~/ThemeSaver/export/{SlotName}/wallpaper/')

    os.system(f'mkdir ~/ThemeSaver/export/{SlotName}/slot/')
    os.system(f'cp -r ~/ThemeSaver/data/{SlotName} ~/ThemeSaver/export/{SlotName}/slot/')
    tar = tarfile.open(f"/home/pi/ThemeSaver/export/{SlotName}.tar.gz", "w:gz")
    tar.add(f"/home/pi/ThemeSaver/export/{SlotName}", arcname=f"{SlotName}")
    tar.close()
    os.system(f'rm -r ~/ThemeSaver/export/{SlotName}')
    print(Fore.GREEN + 'Finished exporting slot ')

def Import(FilePath):
    if not os.path.isfile(FilePath):
        print(Fore.RED + 'No File Like That')
        quit()
    #Removing and creating import directory
    os.system('rm -r ~/ThemeSaver/import/')
    os.system('mkdir ~/ThemeSaver/import/')

    #Extracting archive
    file = tarfile.open(FilePath)
    file.extractall('/home/pi/ThemeSaver/import/') 
    file.close() 

    #Copying themes and other stuff
    print(Fore.GREEN + 'Copying slot')
    os.system('cp -r /home/pi/ThemeSaver/import/*/slot/* ~/ThemeSaver/data/')

    print(Fore.GREEN + 'Copying themes')
    os.system('sudo cp -r /home/pi/ThemeSaver/import/*/theme/* /usr/share/themes/')

    print(Fore.GREEN + 'Copying icons')
    os.system('sudo cp -r /home/pi/ThemeSaver/import/*/icons/* /usr/share/icons/')

    print(Fore.GREEN + 'Copying cursors')
    os.system('sudo cp -r /home/pi/ThemeSaver/import/*/cursors/* /usr/share/icons/')

    print(Fore.GREEN + 'Copying plank theme')
    os.system('sudo cp -r /home/pi/ThemeSaver/import/*/plank/* /usr/share/plank/themes/')

    print(Fore.GREEN + 'Copying wallpaper')
    os.system('echo $(cat /home/pi/ThemeSaver/import/*/slot/*/xfce4-desktop/+backdrop+screen0+monitor0+workspace0+last-image) > ~/ThemeSaver/import/wallpaperpath')
    WallpaperPathFile = open('/home/pi/ThemeSaver/import/wallpaperpath')
    WallpaperPath = WallpaperPathFile.read()
    os.system(f'sudo cp ~/ThemeSaver/import/*/wallpaper/* {WallpaperPath}')

    #Removing import directory after copying files
    os.system('rm -r ~/ThemeSaver/import')

    print(Fore.GREEN + 'Finished importing slot')

#Terminal Usage
if len(sys.argv) > 1:
    if sys.argv[1].lower() == 'load':
        if len(sys.argv) > 2:
            DesktopEntryFile = open('/home/pi/ThemeSaver/DesktopEnvironment')
            DesktopEntry = DesktopEntryFile.read()
            if DesktopEntry.strip() == 'xfce':
                LoadSlotXfce(sys.argv[2])
            elif DesktopEntry.strip() == 'lxde' or DesktopEntry.strip() == 'LXDE-pi':
                LoadSlotLXDE(sys.argv[2])
                
        else:
            print(Fore.RED + "Enter Valid Slot Name")
    elif sys.argv[1].lower() == 'save':
        if len(sys.argv) > 2:
            os.system('echo $DESKTOP_SESSION > ~/ThemeSaver/DesktopEnvironment')
            DesktopEntryFile = open('/home/pi/ThemeSaver/DesktopEnvironment')
            DesktopEntry = DesktopEntryFile.read()
            if DesktopEntry.strip() == 'xfce':
                SaveSlotXfce(sys.argv[2])
            elif DesktopEntry.strip() == 'lxde' or DesktopEntry.strip() == 'LXDE-pi':
                SaveSlotLXDE(sys.argv[2])
        else:
            print(Fore.RED + "Enter Valid Slot Name")
    elif sys.argv[1].lower() == 'delete' or sys.argv[1].lower() == 'del' :
        if len(sys.argv) > 2:
            Del(sys.argv[2])
        else:
            print(Fore.RED + "Enter Valid Slot Name")
    elif sys.argv[1].lower() == 'export':
        os.system('echo $DESKTOP_SESSION > ~/ThemeSaver/DesktopEnvironment')
        DesktopEntryFile = open('/home/pi/ThemeSaver/DesktopEnvironment')
        DesktopEntry = DesktopEntryFile.read()
        if len(sys.argv) > 2:
            if DesktopEntry.strip() == 'xfce':
                Export(sys.argv[2])
            elif DesktopEntry.strip() == 'lxde' or DesktopEntry.strip() == 'LXDE-pi':
                print(Fore.RED + 'Export Slot is not ready for LXDE yet :(')
        else:
            print(Fore.RED + "Enter Valid Slot Name")
    elif sys.argv[1].lower() == 'import':
        os.system('echo $DESKTOP_SESSION > ~/ThemeSaver/DesktopEnvironment')
        DesktopEntryFile = open('/home/pi/ThemeSaver/DesktopEnvironment')
        DesktopEntry = DesktopEntryFile.read()
        if len(sys.argv) > 2:
            if DesktopEntry.strip() == 'xfce':
                Import(sys.argv[2])
            elif DesktopEntry.strip() == 'lxde' or DesktopEntry.strip() == 'LXDE-pi':
                print(Fore.RED + 'Import Slot is not ready for LXDE yet :(')         
        else:
            print(Fore.RED + "Enter Valid File Path")
    elif sys.argv[1].lower() == 'list' or sys.argv[1].lower() == 'ls':
        List()
    elif sys.argv[1].lower() == 'gui':
        os.system('python3 ~/ThemeSaver/gui.py')
    elif sys.argv[1] == 'help':
        print(Fore.GREEN + 'Available arguments:')
        print(Fore.GREEN + '1) ' + Fore.CYAN + '"save [slotname]"' + Fore.GREEN + ' Save a new slot')
        print(Fore.GREEN + '2) ' + Fore.CYAN + '"load [slotname]"' + Fore.GREEN + ' Load existing slot')
        print(Fore.GREEN + '3) ' + Fore.CYAN + '"del [slotname]"' + Fore.GREEN + ' Delete a slot')
        print(Fore.GREEN + '4) ' + Fore.CYAN + '"ls"' + Fore.GREEN + ' List all saved slots')
        print(Fore.GREEN + '5) ' + Fore.CYAN + '"gui"' + Fore.GREEN + ' Launches GUI for themesaver')
        print(Fore.GREEN + '6) ' + Fore.CYAN + '"help"' + Fore.GREEN + ' Get a list of available argument')
        
    else:
        print(Fore.RED + 'Please Enter Valid Argument, Use command "themesaver help" to get a list of available arguments')
else:
    print(Fore.RED + 'Please Enter Valid Argument, Use command "themesaver help" to get a list of available arguments')

