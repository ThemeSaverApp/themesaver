import os, sys
from themesaver.Misc import saveWallpaper

def save(SlotsFolder, slotname):
    os.system(f'cp -rf ~/.config/i3 {SlotsFolder}/"{slotname}"/configs &>/dev/null')
    saveWallpaper.nitrogen(SlotsFolder, slotname)

def load():
        os.system('i3 reload')
        os.system(f'nitrogen --restore')
