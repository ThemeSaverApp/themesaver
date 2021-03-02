from tkinter import *
from tkinter import messagebox
from PIL import ImageTk,Image
from tkinter import filedialog
import os

def SaveSlot():
    os.system('echo $DESKTOP_SESSION > ~/ThemeSaver/DesktopEnvironment')
    SaveNewSlotWindow = Toplevel()
    SaveNewSlotWindow.title('Save New Slot')
    SaveNewSlotWindow.configure(bg='#13E06A')
    SaveNewSlotWindow.option_add('*Font', 'Ubuntu 12')
    SaveNewSlotWindow.iconphoto(False, WindowIcon)

    Label(SaveNewSlotWindow, text='Enter Slot Name: ', bg='#13E06A').grid(row=0, column=0)
    SlotName = Entry(SaveNewSlotWindow, width=20, bg='black', fg='white') 
    SlotName.grid(row=1, column=0, padx=2, pady=2)
    def ContinueButton():
        print(SlotName.get().replace(" ", "_"))
        if not SlotName.get().replace(" ", "_").strip() == '':
            if os.path.isdir(f'/home/pi/ThemeSaver/data/{SlotName.get().replace(" ", "_")}'):
                OverwriteAsk = messagebox.askyesno(title='Do you want to overwrite?', message='A slot with that name already exists. Do you want to overwrite it ?')
                if OverwriteAsk:
                    os.system(f'python3 ~/ThemeSaver/ThemeSaver.py del {SlotName.get().replace(" ", "_")}')
                    os.system(f'python3 ~/ThemeSaver/ThemeSaver.py save {SlotName.get().replace(" ", "_")}')
                    SaveNewSlotWindow.destroy()
                    messagebox.showinfo(title='Finished Saving Theme', message='Finished Saving Theme :)')
            else:
                os.system(f'python3 ~/ThemeSaver/ThemeSaver.py save {SlotName.get().replace(" ", "_")}')
                SaveNewSlotWindow.destroy()
                messagebox.showinfo(title='Finished Saving Theme', message='Finished Saving Theme :)')
        else:
            messagebox.showerror(title='Enter Valid Slot Name', message='Enter Valid Slot Name')
    Button(SaveNewSlotWindow, text='Continue', command=lambda: ContinueButton(), fg='#13E06A', bg='black').grid(row=2, column=0)

def LoadSlot():
    global ScreenshotLabel
    global SlotName
    global DeleteButton
    global LoadButton
    global ExportButton


    SlotList = []
    SlotNumber = [0]

    #Checking if data directory is there
    if not os.path.isdir('/home/pi/ThemeSaver/data'):
        os.system('mkdir ~/ThemeSaver/data')

    for Slot in os.listdir('/home/pi/ThemeSaver/data'):
        SlotList.append(Slot)

    if len(SlotList) == 0:
        messagebox.showerror(title='No Slots', message='There are no saved slots :(')
    else:
        LoadSlotsWindow = Toplevel()
        LoadSlotsWindow.title('Load Existing Slot')
        LoadSlotsWindow.configure(bg='#13E06A')
        LoadSlotsWindow.iconphoto(False, WindowIcon)
        #SlotName Label
        global SlotName
        SlotName = Label(LoadSlotsWindow, text=SlotList[0], bg='#13E06A')
        SlotName.grid(row=0, column=1)

        #Screenshot
        ScreenshotNotResized = Image.open(f"/home/pi/ThemeSaver/data/{SlotList[SlotNumber[0]]}/Screenshot.png")
        #Resizing Screenshot
        Resize = ScreenshotNotResized.resize((341, 189), Image.ANTIALIAS)
        global Screenshot
        Screenshot = ImageTk.PhotoImage(Resize)
        #Placing screenshot in label
        global ScreenshotLabel
        ScreenshotLabel = Label(LoadSlotsWindow, image=Screenshot)
        ScreenshotLabel.grid(row=1, column=1)
        
        #Forward and Back buttons
        if not len(SlotList) == 1:
            ForwardButton = Button(LoadSlotsWindow, text='->', state=NORMAL, command=lambda: ForwardBtn(), fg='#13E06A', bg='black')
            ForwardButton.grid(row=1, column=2)
            BackButton = Button(LoadSlotsWindow, text='<-', state=DISABLED, command=lambda: BackBtn(), fg='#13E06A', bg='black')
            BackButton.grid(row=1, column=0)

        #Load, Delete, Export Button
        DeleteButton = Button(LoadSlotsWindow, text='Delete Slot',  command=lambda: DelSlot(), fg='#13E06A', bg='black')
        DeleteButton.grid(row=2, column=0, pady=2)
        LoadButton = Button(LoadSlotsWindow, text='Load Slot',  command=lambda: os.system(f'python3 ~/ThemeSaver/ThemeSaver.py load {SlotList[SlotNumber[0]]}'), fg='#13E06A', bg='black')
        LoadButton.grid(row=2, column=1, pady=2)
        ExportButton = Button(LoadSlotsWindow, text='Export Slot',  command=lambda: ExportBtn(), fg='#13E06A', bg='black')
        ExportButton.grid(row=2, column=2, pady=2)

        def ExportBtn():
            os.system('echo $DESKTOP_SESSION > ~/ThemeSaver/DesktopEnvironment')
            DesktopEntryFile = open('/home/pi/ThemeSaver/DesktopEnvironment')
            DesktopEntry = DesktopEntryFile.read()
            if DesktopEntry.strip() == 'xfce':
                os.system(f'python3 ~/ThemeSaver/ThemeSaver.py export {SlotList[SlotNumber[0]]}')
                messagebox.showinfo(title='Export Slot', message=f'Finished Exporting Slot. Slot Exported To /home/pi/ThemeSaver/export/{SlotList[SlotNumber[0]]}.tar.gz')
            elif DesktopEntry.strip() == 'lxde' or DesktopEntry.strip() == 'LXDE-pi':
                messagebox.showinfo(title='Export Slot', message='Export Slot is not ready for LXDE yet :(')
            

        def DelSlot():
            os.system(f'python3 ~/ThemeSaver/ThemeSaver.py del {SlotList[SlotNumber[0]]}')
            LoadSlotsWindow.destroy()

        def ForwardBtn():
            global ScreenshotLabel
            global SlotName
            global DeleteButton
            global LoadButton
            global ExportButton

            DeleteButton.grid_forget()
            LoadButton.grid_forget()
            ExportButton.grid_forget()


            if SlotNumber[0] < len(SlotList) - 1:
                SlotNumber[0] += 1
            print(SlotNumber[0])
            
            #Changing Screenshot
            ScreenshotLabel.grid_forget()
            ScreenshotNotResized = Image.open(f"/home/pi/ThemeSaver/data/{SlotList[SlotNumber[0]]}/Screenshot.png")
            #Resizing Screenshot
            Resize = ScreenshotNotResized.resize((341, 189), Image.ANTIALIAS)
            Screenshot2 = ImageTk.PhotoImage(Resize)
            #Placing screenshot in label
            ScreenshotLabel2 = Label(LoadSlotsWindow, image=Screenshot2)
            ScreenshotLabel2.grid(row=1, column=1)
            ScreenshotLabel.Screenshot_ref = Screenshot2

            #Changing SlotName
            SlotName.configure(text=SlotList[SlotNumber[0]])
            
            #Load, Delete, Export Button
            
            DeleteButton = Button(LoadSlotsWindow, text='Delete Slot',  command=lambda: DelSlot(), fg='#13E06A', bg='black')
            DeleteButton.grid(row=2, column=0, pady=2)
            
            LoadButton = Button(LoadSlotsWindow, text='Load Slot',  command=lambda: os.system(f'python3 ~/ThemeSaver/ThemeSaver.py load {SlotList[SlotNumber[0]]}'), fg='#13E06A', bg='black')
            LoadButton.grid(row=2, column=1, pady=2)
            
            ExportButton = Button(LoadSlotsWindow, text='Export Slot',  command=lambda: ExportBtn(), fg='#13E06A', bg='black')
            ExportButton.grid(row=2, column=2, pady=2)     

            if SlotNumber[0] == 0:
                BackButton = Button(LoadSlotsWindow, text='<-', state=DISABLED, command=lambda: BackBtn(), fg='#13E06A', bg='black')
                BackButton.grid(row=1, column=0)
            else:
                BackButton = Button(LoadSlotsWindow, text='<-', state=NORMAL, command=lambda: BackBtn(), fg='#13E06A', bg='black')
                BackButton.grid(row=1, column=0)

            if SlotNumber[0] == len(SlotList) - 1:
                ForwardButton = Button(LoadSlotsWindow, text='->', state=DISABLED, command=lambda: ForwardBtn(), fg='#13E06A', bg='black')
                ForwardButton.grid(row=1, column=2)
            else:
                ForwardButton = Button(LoadSlotsWindow, text='->', state=NORMAL, command=lambda: ForwardBtn(), fg='#13E06A', bg='black')
                ForwardButton.grid(row=1, column=2)

                
        def BackBtn():
            SlotNumber[0] -= 2
            ForwardBtn()


def ImportSlot():
    os.system('echo $DESKTOP_SESSION > ~/ThemeSaver/DesktopEnvironment')
    DesktopEntryFile = open('/home/pi/ThemeSaver/DesktopEnvironment')
    DesktopEntry = DesktopEntryFile.read()
    if DesktopEntry.strip() == 'xfce':
        root.filename = filedialog.askopenfilename(initialdir="/home/pi", title="Select Slot File")
        os.system(f'python3 ~/ThemeSaver/ThemeSaver.py import {root.filename}')
        messagebox.showinfo(title='Finished Importing', message='Finished Importing Slot')
    elif DesktopEntry.strip() == 'lxde' or DesktopEntry.strip() == 'LXDE-pi':
        messagebox.showinfo(title='Import Slot', message='Import Slot is not ready for LXDE yet :(')

#Main Window
root = Tk()
root.title('Theme Saver')
root.configure(bg='#13E06A')
root.option_add('*Font', 'Ubuntu 12')
WindowIcon = PhotoImage(file = '/usr/share/icons/ThemeSaver.png')
root.iconphoto(False, WindowIcon)


SaveNewSlot = Button(root, text='Save New Slot', command=lambda: SaveSlot(), fg='#13E06A', bg='black', borderwidth=0, font = ('Ubuntu','13','bold'))
LoadExistingSlot = Button(root, text='Load Existing Slots', command=lambda: LoadSlot(), fg='#13E06A', bg='black', borderwidth=0, font = ('Ubuntu','13','bold'))
ImportSlot = Button(root, text='Import Slot', command=ImportSlot, fg='#13E06A', bg='black', borderwidth=0, font = ('Ubuntu','13','bold'))

BannerNotResized = Image.open('/home/pi/ThemeSaver/Banner.png')
Resize = BannerNotResized.resize((300, 110), Image.ANTIALIAS)
Banner = ImageTk.PhotoImage(Resize)
BannerLabel = Label(root, image=Banner, borderwidth=2, bg='#13E06A')

#Placing Buttons
BannerLabel.grid(row=0, column=0, rowspan=3)
SaveNewSlot.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)
LoadExistingSlot.grid(row=1, column=1, sticky="nsew", padx=2, pady=2)
ImportSlot.grid(row=2, column=1, sticky="nsew", padx=2, pady=2)


root.mainloop()
