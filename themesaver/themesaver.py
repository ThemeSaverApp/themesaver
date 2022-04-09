#!/usr/bin/env python

import os, sys,  click
from dotenv import load_dotenv, dotenv_values
from tqdm import tqdm
from pathlib import Path

from themesaver.Misc.getInfo import getDE, getWM
from themesaver.Cli.listSlots import listSlots
from themesaver.Cli.saveSlot import saveSlot
from themesaver.Cli.loadSlot import loadSlot
from themesaver.Cli.deleteSlot import deleteSlot
from themesaver.Cli.exportSlot import exportSlot
from themesaver.Cli.importSlot import importSlot

AppConfig = dotenv_values(f"{os.environ['HOME']}/.config/themesaver/config.env")

# Arrays cannot be stored in .env files so converting the string into an array
def convertArray(key):
    return AppConfig[key].replace('\'', '').replace(' ', '').replace('[', '').replace(']', '').split(',')

# Config Variables
RequiredChannelsXfce = convertArray('Xfce')
RequiredFoldersLXDE = convertArray('LXDE')
RequiredKDEConfig = convertArray('KDEConf')
RequiredKDELocal = convertArray('KDELocal')
PlankProperties = convertArray('Plank')
Configs = convertArray('Configs')
HomePath = os.environ['HOME']

# Folder Paths
FolderPath = os.path.expanduser(AppConfig['FolderPath'])
SlotsFolder = os.path.expanduser(f'{FolderPath}/Slots')
ConfigFolder = os.path.expanduser('~/.config')

DE = getDE()
WM = getWM()

@click.group()
def group():
    pass

@click.command(help='Save a new slot')
@click.argument('slotname' )
def save(slotname):
    saveSlot(SlotsFolder, slotname, DE, WM, Configs)

@click.command(help='Load existing slot')
@click.argument('slotname')
def load(slotname):
    loadSlot(SlotsFolder, slotname, DE, WM)

@click.command( help='List all saved slots')
@click.option('--all/--no-all', default=False)
def list(all):
    listSlots(SlotsFolder, all, DE, WM)

@click.command(help='Delete existing slot')
@click.argument('slotname')
def delete(slotname):
    deleteSlot(SlotsFolder, slotname)

@click.command(help='Export Slot To Upload To Shop')
@click.argument('slotname')
@click.argument('filepath',  type=click.Path(exists=True))
def export(slotname, filepath):
    exportSlot(SlotsFolder, slotname, filepath, DE, WM)

@click.command(help='Import Slot')
@click.argument('filepath')
@click.option('--shop/--no-shop', default=False)
def Import(filepath, shop):
    importSlot(filepath, shop, FolderPath, SlotsFolder, DE, WM)

@click.command(help='Launch the gui app for themesaver')
def gui():
    path = os.path.realpath(__file__).replace('/themesaver.py', '')
    os.system(f'python3 {path}/GUI/MainWindow.py')

group.add_command(save)
group.add_command(load)
group.add_command(list)
group.add_command(delete)
group.add_command(export)
group.add_command(Import)
group.add_command(gui)

if __name__ == '__main__':
    group()


