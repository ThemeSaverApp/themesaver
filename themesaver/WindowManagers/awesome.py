import os, sys
from themesaver.Misc import saveWallpaper

def save(SlotsFolder, slotname):
    os.system(f'cp -rf ~/.config/awesome {SlotsFolder}/"{slotname}"/configs &>/dev/null')
    saveWallpaper.nitrogen(SlotsFolder, slotname)

def load():
    os.system('echo "awesome.restart()" | awesome-client')
    os.system(f'nitrogen --restore')