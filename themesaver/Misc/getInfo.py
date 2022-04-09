import os

def getDE():
    if 'XDG_CURRENT_DESKTOP' in os.environ.keys():
        return os.environ['XDG_CURRENT_DESKTOP'].lower().strip()
        if len(DE.split(':')) != 1:
            return DE.split(':')[1]
    elif 'DESKTOP_SESSION' in os.environ.keys():
        return os.environ['DESKTOP_SESSION'].lower().strip()
    else:
        return getWM()

def getWM():
    return os.popen("wmctrl -m").read().split('\n')[0].replace('Name: ', '').lower()

def getGtkTheme():
    return os.popen('gtk-query-settings gtk-theme-name').read().strip().replace('gtk-theme-name: "', '').replace('"', '')

def getIconTheme():
    return os.popen('gtk-query-settings gtk-icon-theme-name').read().strip().replace('gtk-icon-theme-name: "', '').replace('"', '')

def getCursorTheme():
    return os.popen('gtk-query-settings gtk-cursor-theme-name').read().strip().replace('gtk-cursor-theme-name: "', '').replace('"', '')  

def getShell():
    return os.environ['SHELL'].replace('/', '').replace('bin', '').replace('usr', '')