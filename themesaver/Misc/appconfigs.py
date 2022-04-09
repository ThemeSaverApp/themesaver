def SavePlank():
    # Saving Plank Configs If Running
    PlankRunning = os.popen('pgrep plank').read()
    if PlankRunning != '':
        # Storing Plank Configuration
        os.mkdir(Path(SlotsFolder / slotname / 'plank'))
        for PlankProperty in PlankProperties:
            os.system(
                f'gsettings get net.launchpad.plank.dock.settings:/net/launchpad/plank/docks/dock1/ {PlankProperty} > {SlotsFolder}/"{slotname}"/plank/{PlankProperty}')

    if not Overwrite:
        os.system(f"mkdir {SlotsFolder}/{slotname}/'configs'")

def SavePolybar():
    # Saving Polybar Configs If Running
    PolybarRunning = os.popen('pgrep polybar').read()
    if PolybarRunning != '':
        os.system(f"cp -r {Path(ConfigFolder / 'polybar')} {Path(SlotsFolder / slotname / 'configs')}")

def SaveConky():
    # Saving Conky Configs If Running
    ConkyRunning = os.popen('pgrep conky').read()
    if ConkyRunning != '':
        os.system(f"cp -r {Path(ConfigFolder / 'conky')} {Path(SlotsFolder / slotname / 'configs')}")

def SaveLatte():
    # Saving LatteDock Configs If Running
    LatteRunning = os.popen('pgrep latte-dock').read()
    if LatteRunning != '':
        os.system(f"cp -r {Path(ConfigFolder / 'latte')} {Path(SlotsFolder / slotname / 'configs')}")

def SaveShell():
    # Storing Fish and OMF Fish configs
    shell = os.environ['SHELL'].strip().replace('/', '').replace('usr', '').replace('bin', '')
    shells = {
        'fish': ['~/.config/fish', '~/.config/omf'],
        'bash': ['~/.bash_profile', '~/.bashrc', '~/.bash_logout'],
        'zsh': []
    }

    if shell in shells.keys():
        if not Overwrite:        
            os.system(f'mkdir {Path(SlotsFolder / slotname / shell)}')
        for file in shells[shell]:
            os.system(
                f'cp -rf {file} {SlotsFolder}/"{slotname}"/{shell}')

def LoadAppConfigs():

    # Loading Plank configs if they exist
    if Path(SlotsFolder / slotname / 'plank').exists():
        subprocess.Popen(['setsid', 'plank'],
                         stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        for PlankConfig in os.listdir(f'{SlotsFolder}/{slotname}/plank'):
            PlankConfigData = open(f'{SlotsFolder}/{slotname}/plank/{PlankConfig}').read()
            os.system(
                f'gsettings set net.launchpad.plank.dock.settings:/net/launchpad/plank/docks/dock1/ {PlankConfig} {PlankConfigData}')
    # Killing Plank If Configs dont exist
    else:
        subprocess.Popen(['killall', 'plank'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


    # Using subprocesss to run apps as os.system is not working properly with &>/dev/null
    def runApp(app, config):
        if Path(f'{SlotsFolder}/{slotname}/configs/{config}').exists():
            subprocess.Popen(['killall', app], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            time.sleep(2)
            subprocess.Popen(['setsid', app], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        else:
            subprocess.Popen(['killall', app], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            
    runApp('polybar', 'polybar')
    runApp('conky', 'conky')
    runApp('latte-dock', 'latte')    