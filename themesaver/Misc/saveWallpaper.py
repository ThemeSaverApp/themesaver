import os

def nitrogen(SlotsFolder, slotname):
    os.system(f'cp -r ~/.config/nitrogen {SlotsFolder}/"{slotname}"/configs')
    WallpaperPath = os.popen(f"sed -n '/file/p' ~/.config/nitrogen/bg-saved.cfg").read().strip().split('\n')

    for n in range(len(WallpaperPath)):
        if n == 0:
            os.system(f'cp \'{WallpaperPath[n].replace("file=", "").strip()}\' \'{SlotsFolder}/{slotname}/Wallpaper.png\'')
            os.system(f'sed -i "s#{WallpaperPath[n].strip()}#file={SlotsFolder}/{slotname}/Wallpaper.png#g" /opt/themesaver/Slots/{slotname}/configs/nitrogen/bg-saved.cfg')
        else:
            os.system(f'cp \'{WallpaperPath[n].replace("file=", "").strip()}\' \'{SlotsFolder}/{slotname}/Wallpaper-Monitor{n+1}.png\'')
            os.system(f'sed -i "s#{WallpaperPath[n].strip()}#file={SlotsFolder}/{slotname}/Wallpaper-Monitor{n}#g" /opt/themesaver/Slots/{slotname}/configs/nitrogen/bg-saved.cfg')

    # if not os.path.isfile(f'{AppConfig["FolderPath"]}/Slots/{slotname}/Wallpaper.png'):
    #     os.system(f'cp \'{WallpaperPath}\' \'{SlotsFolder}/{slotname}/Wallpaper.png\'')
