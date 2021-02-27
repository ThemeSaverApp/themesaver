import os 
import sys
import time
import subprocess
from colorama import Fore, Back, Style

#Initialing List and Variables
RequiredChannels = [ "xfce4-desktop", "xfwm4","xsettings" ]
NumberOfSlots = 0

#Functions

#SaveSlot Functions
def SaveSlot(SlotName):
    if os.path.isdir(f"/home/pi/ThemeSaver/data/{SlotName}"):
        Overwrite = input(Fore.RED + "A slot with that name already exists. Do you want to overwrite it ? [Y/n]")
        if Overwrite.lower() == 'y':
            print('Okay overwriting')
        else:
            print('Not overwriting')
            quit()
    os.system(f'rm -r ~/ThemeSaver/data/{SlotName}')
    #Creating a directory for slot in ~/ThemeSaver/data/
    os.system(f'mkdir ~/ThemeSaver/data/{SlotName}')
    #Taking Screenshot
    os.system('xdotool key ctrl+alt+d') #Hiding all windows on desktop
    time.sleep(2) #Waiting for two seconds
    os.system(f'scrot ~/ThemeSaver/data/{SlotName}/Screenshot.png') #Taking a Screenshot
    os.system('xdotool key ctrl+alt+d') #Unhiding all windows on desktop

    for channel in RequiredChannels:
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
        print("Plank is running :)")
        #Storing Plank Configuration
        os.system(f"mkdir ~/ThemeSaver/data/{SlotName}/plank")
        os.system(f'gsettings get net.launchpad.plank.dock.settings:/net/launchpad/plank/docks/dock1/ theme > ~/ThemeSaver/data/{SlotName}/plank/theme')
        os.system(f'gsettings get net.launchpad.plank.dock.settings:/net/launchpad/plank/docks/dock1/ position > ~/ThemeSaver/data/{SlotName}/plank/position')
        os.system(f'gsettings get net.launchpad.plank.dock.settings:/net/launchpad/plank/docks/dock1/ alignment > ~/ThemeSaver/data/{SlotName}/plank/alignment')
        
    os.system('clear')

def LoadSlot(SlotName):
    if not os.path.isdir(f'/home/pi/ThemeSaver/data/{SlotName}'):
        print(Fore.RED + 'No slot like that exists. Use command "themesave list" to print the list of slots')
        quit()
    for PropertyFolders in RequiredChannels:
        for PropertyFiles in os.listdir(f"/home/pi/ThemeSaver/data/{SlotName}/{PropertyFolders}"):
            PropertyFile = open(f"/home/pi/ThemeSaver/data/{SlotName}/{PropertyFolders}/{PropertyFiles}")
            PropertyFileValue = PropertyFile.read()
            PropertyFilePath = PropertyFiles.replace("+","/").strip()
            os.popen(f"xfconf-query -c {PropertyFolders.strip()} -p {PropertyFilePath} -s '{PropertyFileValue.strip()}' ") 
            #subprocess.Popen(f"xfconf-query -c {PropertyFolders.strip()} -p {PropertyFilePath} -s '{PropertyFileValue.strip()}' ", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

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

#Terminal Usage
if len(sys.argv) > 1:
    if sys.argv[1] == 'load':
        if len(sys.argv) > 2:
            LoadSlot(sys.argv[2])
        else:
            print(Fore.RED + "Enter Valid Slot Name")
    elif sys.argv[1] == 'save':
        if len(sys.argv) > 2:
            SaveSlot(sys.argv[2])
        else:
            print(Fore.RED + "Enter Valid Slot Name")
    elif sys.argv[1] == 'del':
        if len(sys.argv) > 2:
            Del(sys.argv[2])
        else:
            print(Fore.RED + "Enter Valid Slot Name")
    elif sys.argv[1] == 'gui':
        pass
    elif sys.argv[1] == 'list':
        List()
    elif sys.argv[1] == 'help':
        print(Fore.GREEN + 'Available arguments:')
        print(Fore.GREEN + '1) ' + Fore.CYAN + '"save [slotname]"' + Fore.GREEN + ' Save a new slot')
        print(Fore.GREEN + '2) ' + Fore.CYAN + '"load [slotname]"' + Fore.GREEN + ' Load existing slot')
        print(Fore.GREEN + '3) ' + Fore.CYAN + '"del"' + Fore.GREEN + ' Delete a slot')
        print(Fore.GREEN + '3) ' + Fore.CYAN + '"help"' + Fore.GREEN + ' Get a list of available argument')
        
    else:
        print(Fore.RED + 'Please Enter Valid Argument, Use command "themesaver help" to get a list of available arguments')
else:
    print(Fore.RED + 'Please Enter Valid Argument, Use command "themesaver help" to get a list of available arguments')

