import os, json, click

def listSlots(SlotsFolder, all, DE, WM):
    Slots = []
    if not all:
        for slotname in os.listdir(f"{SlotsFolder}/"):
            if json.load(open(f'{SlotsFolder}/{slotname}/info.json'))['desktopEnvironment'] == DE and json.load(open(f'{SlotsFolder}/{slotname}/info.json'))['windowManager'] == WM:
                Slots.append(slotname)
    else:
        Slots = os.listdir(f"{SlotsFolder}/")
    SlotNumber = 0
    click.echo(click.style('Slots:', fg='green'))
    for slotname in Slots:
        SlotNumber += 1
        click.echo(click.style(f'{SlotNumber}) {slotname}', fg='blue'))