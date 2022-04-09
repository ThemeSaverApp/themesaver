import os, click

def deleteSlot(SlotsFolder ,slotname):
    slotname = slotname
    if os.path.isdir(f'{SlotsFolder}/{slotname}'):
        Confirmation = click.prompt(click.style(
            f'Are you sure you want to delete "{slotname}" [Y/n] ', fg='red'))
        if Confirmation.lower().strip() == 'y':
            os.system(f'rm -rf {SlotsFolder}/"{slotname}"')
            click.echo(click.style('Successfully Deleted Slot', fg='green'))
        elif Confirmation.lower().strip() == 'n':
            click.echo(click.style('Ok not deleting', fg='green'))
        else:
            click.echo(click.style('invalid input', fg='red'))
    else:
        click.echo(click.style(
            'No Slot like that. Use command "themesaver ls" to print the list of slots', fg='red'))
