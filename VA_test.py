import os
import threading
import time
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
from tkinter import ttk

from mutagen.mp3 import MP3
from pygame import mixer
from ttkthemes import themed_tk as tk

from functions import ampfunc, redfunc, merfunc, splitfunc, insfunc, revfunc, fadeInfunc, fadeOutfunc, convertfunc

root = tk.ThemedTk()
root.get_themes()  # Returns a list of all themes that can be set
root.set_theme("radiance")  # Sets an available theme

# Fonts - Arial (corresponds to Helvetica), Courier New (Courier), Comic Sans MS, Fixedsys,
# MS Sans Serif, MS Serif, Symbol, System, Times New Roman (Times), and Verdana
#
# Styles - normal, bold, roman, italic, underline, and overstrike.

statusbar = ttk.Label(root, text="Welcome to Voice Archive", relief=SUNKEN, anchor=W, font='Times 10 italic')
statusbar.pack(side=BOTTOM, fill=X)

# Create the menubar
menubar = Menu(root)

root.config(menu=menubar)

# Create the fileMenu, helpMenu

fileMenu = Menu(menubar, tearoff=0)
viewMenu = Menu(menubar, tearoff=0)
helpMenu = Menu(menubar, tearoff=0)
playlist = []


# playlist - contains the full path + filename
# playlistbox - contains just the filename
# Fullpath + filename is required to play the music inside play_music load function

def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    if (filename_path == ""):
        tkinter.messagebox.showinfo("Not selected", "No file was selected, please select a file!")
    else:
        add_to_playlist(filename_path)

        mixer.music.queue(filename_path)


def browse_files():
    global filenames_paths
    filenames_paths = filedialog.askopenfilenames()
    for file in filenames_paths:
        if (file == ""):
            tkinter.messagebox.showinfo("Not selected", "No file was selected, please select a file!")
        else:
            add_to_playlist(file)

            mixer.music.queue(file)


def add_to_playlist(filename_path):
    filename = os.path.basename(filename_path)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1


def help_manual():
    helpManual = tk.ThemedTk()
    helpManual.set_theme("radiance")
    helpManual.title("Help")
    file = open("readme.txt", "r")
    ttk.Label(helpManual, text=file.read()).pack()
    ttk.Button(helpManual, text="Close", command=helpManual.destroy).pack()


def close(window):
    window.destroy()


themelist = ['smog', 'alt', 'plastik', 'vista', 'blue', 'default', 'scidmint', 'scidpink', 'winnative', 'scidgreen',
             'xpnative', 'scidpurple', 'equilux', 'radiance', 'scidsand', 'black', 'scidblue', 'itft1', 'arc',
             'aquativo', 'kroc', 'keramik', 'classic', 'scidgrey', 'winxpblue', 'clearlooks', 'elegance', 'clam',
             'ubuntu']


def change(index, window):
    root.set_theme(themelist[index])
    close(window)


def themeChange():
    theme = tk.ThemedTk()
    listbox = tkinter.Listbox(theme)
    for x in range(0, len(themelist)):
        listbox.insert(x, themelist[x])
    listbox.pack()
    ttk.Button(theme, text="Apply", command=lambda: change(int(listbox.curselection()[0]), window=theme)).pack()


def open_playlist(name, window):
    file = open("data/{f}.csv".format(f=name), "r")
    for path in file:
        lyst = path.split(",")
    for l in lyst:
        if l == "":
            continue
        else:
            add_to_playlist(l)
    close(window)


def opConfirm(name, window):
    if (os.path.isfile("data/{f}.csv".format(f=name))):
        open_playlist(name, window)
    else:
        tkinter.messagebox.showerror("Not found", "The playlist doesn't exist!")


def openPlaylistUI():
    op = tk.ThemedTk()
    op.set_theme("radiance")
    op.title("Open Playlist")
    ttk.Label(op, text="Playlist name:").grid(row=0, column=0)
    opName = ttk.Entry(op)
    opName.grid(row=0, column=1)
    opBtn = ttk.Button(op, text="Open", command=lambda: opConfirm(opName.get(), window=op))
    opBtn.grid(row=2, column=3)


def removeConfirm(name, window):
    if (os.path.isfile("data/{f}.csv".format(f=name))):
        ans = tkinter.messagebox.askyesno("Remove", name + ".csv will be removed permanently, Do you want to continue?")
        if (ans):
            os.remove("data/{f}.csv".format(f=name))
            tkinter.messagebox.showinfo('Removed', name + '.csv has been removed!')
            close(window)
        else:
            close(window)
    else:
        tkinter.messagebox.showerror("Not found", "The playlist doesn't exist!")


def removePlaylistUI():
    rm = tk.ThemedTk()
    rm.set_theme("radiance")
    rm.title("Remove Playlist")
    ttk.Label(rm, text="Playlist name:").grid(row=0, column=0)
    rmName = ttk.Entry(rm)
    rmName.grid(row=0, column=1)
    rmBtn = ttk.Button(rm, text="Remove", command=lambda: removeConfirm(rmName.get(), window=rm))
    rmBtn.grid(row=2, column=3)


def conConfirm(filepath, extension, window):
    print(filepath)
    if (filepath == ""):
        tkinter.messagebox.showerror("Error", "Please select a file")
    else:
        if (convertfunc(filepath, extension)):
            tkinter.messagebox.showinfo("Success", "File converted successfully")
            close(window)
        else:
            print("ERROR")


def askfile(con):
    global confile
    confile = filedialog.askopenfilename()


def convertUI():
    con = tk.ThemedTk()
    con.set_theme("radiance")
    con.title("Convert")
    ttk.Label(con, text="Select file to convert").grid(row=0, column=0)
    fileBtn = ttk.Button(con, text="Open", command=askfile(con))
    fileBtn.grid(row=0, column=1)
    ttk.Label(con, text="Enter the new file format extension:").grid(row=1, column=0)
    conName = ttk.Entry(con)
    conName.grid(row=1, column=1)
    conBtn = ttk.Button(con, text="Save",
                        command=lambda: conConfirm(filepath=confile, extension=conName.get(), window=con))
    conBtn.grid(row=2, column=3)


menubar.add_cascade(label="File", menu=fileMenu)
menubar.add_cascade(label="View", menu=viewMenu)
menubar.add_cascade(label="Help", menu=helpMenu)
fileMenu.add_command(label="Open", command=browse_file)
fileMenu.add_command(label="Convert & Save", command=convertUI)
fileMenu.add_separator()
fileMenu.add_command(label="Open playlist", command=openPlaylistUI)
fileMenu.add_command(label="Remove playlist", command=removePlaylistUI)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=root.destroy)

viewMenu.add_command(label="Change Theme", command=themeChange)

helpMenu.add_command(label="Manual", command=help_manual)

mixer.init()  # initializing the mixer

root.title("Voice Archive")
root.iconbitmap(r'images/va.ico')

# Root Window - StatusBar, LeftFrame, rightframe
# LeftFrame - The listbox (playlist)
# rightframe - TopFrame,MiddleFrame and the BottomFrame

leftframe = Frame(root)
leftframe.pack(side=LEFT, padx=30, pady=30)

playlistbox = Listbox(leftframe)
playlistbox.pack()


def save_playlist(name, window):
    file = open("data/{f}.csv".format(f=name), "a")
    for play in playlist:
        file.write(play + ",")
    tkinter.messagebox.showinfo('Success', 'Playlist saved!')
    file.close()
    close(window)


def write_playlist(name, window):
    file = open("data/{f}.csv".format(f=name), "w")
    for play in playlist:
        file.write(play + ",")
    tkinter.messagebox.showinfo('Success', 'Playlist replaced!')
    file.close()
    close(window)


def saveConfirm(name, window):
    if (os.path.isfile("data/{f}.csv".format(f=name))):
        ans = tkinter.messagebox.askyesno("Save Anyway?",
                                          name + ".csv already exists, overwrite the existing playlist?")
        if (ans):
            write_playlist(name, window)
    else:
        save_playlist(name, window)


def saveUI():
    if len(playlist) > 0:
        save = tk.ThemedTk()
        save.set_theme("radiance")
        save.title("Save Playlist")
        ttk.Label(save, text="Save playlist as:").grid(row=0, column=0)
        saveName = ttk.Entry(save)
        saveName.grid(row=0, column=1)
        saveBtn = ttk.Button(save, text="OK", command=lambda: saveConfirm(saveName.get(), window=save))
        saveBtn.grid(row=2, column=3)
    else:
        tkinter.messagebox.showerror('Error', 'No file in the playlist')


SaveBtn = ttk.Button(leftframe, text="Save", command=lambda: saveUI())
SaveBtn.pack(side=BOTTOM)

addBtn = ttk.Button(leftframe, text="+ Add", command=browse_files)
addBtn.pack(side=LEFT)


def del_song():
    try:
        selected_song = playlistbox.curselection()
        selected_song = int(selected_song[0])
        playlistbox.delete(selected_song)
        playlist.pop(selected_song)
    except IndexError:
        tkinter.messagebox.showerror('Error', 'No file selected from the playlist!')


delBtn = ttk.Button(leftframe, text="- Remove", command=del_song)
delBtn.pack(side=RIGHT)

rightframe = Frame(root)
rightframe.pack(side=RIGHT, pady=30)

topframe = Frame(rightframe)
topframe.pack()

lengthlabel = ttk.Label(topframe, text='Total Length : --:--')
lengthlabel.pack(pady=5)

currenttimelabel = ttk.Label(topframe, text='Current Time : --:--', relief=GROOVE)
currenttimelabel.pack()


def show_details(play_song):
    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    # div - total_length/60, mod - total_length % 60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "Total Length" + ' - ' + timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global paused
    # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
    # Continue - Ignores all of the statements below it. We check if music is paused or not.
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = "Current Time" + ' - ' + timeformat
            time.sleep(1)
            current_time += 1


def play_music():
    global paused

    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = False
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File not found',
                                         'VA could not play the file. Please select one from the playlist.')


def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"


paused = False


def pause_music():
    global paused
    paused = True
    mixer.music.pause()
    statusbar['text'] = "Music Paused"


def rewind_music():
    play_music()
    statusbar['text'] = "Music Rewinded"


def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)
    # set_volume of mixer takes value only from 0 to 1. Example - 0, 0.1,0.55,0.54.0.99,1


muted = FALSE


def mute_music():
    global muted
    if muted:  # Unmute the music
        mixer.music.set_volume(0.7)
        volumeBtn.configure(image=volumePhoto)
        scale.set(70)
        muted = FALSE
    else:  # mute the music
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE


middleframe = Frame(rightframe)
middleframe.pack(side=TOP, pady=30, padx=30)

playPhoto = PhotoImage(file='images/play.png')
playBtn = ttk.Button(middleframe, image=playPhoto, command=play_music)
playBtn.grid(row=0, column=0, padx=10)

stopPhoto = PhotoImage(file='images/stop.png')
stopBtn = ttk.Button(middleframe, image=stopPhoto, command=stop_music)
stopBtn.grid(row=0, column=1, padx=10)

pausePhoto = PhotoImage(file='images/pause.png')
pauseBtn = ttk.Button(middleframe, image=pausePhoto, command=pause_music)
pauseBtn.grid(row=0, column=2, padx=10)

# Bottom Frame for volume, rewind, mute etc.

# def forward_music(value):
#    selected_song = playlistbox.curselection()
#    selected_song = int(selected_song[0])
#    play_it = playlist[selected_song]
#    global curval
#    curval+=mixer.music.get_pos()+value
#    mixer.music.load(play_it)
#    mixer.music.play(start=curval)
#    statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
#    show_details(play_it)

bottomframe = Frame(rightframe)
bottomframe.pack()

ttk.Label(bottomframe, text="Replay").grid(row=1, column=0)
rewindPhoto = PhotoImage(file='images/rewind.png')
rewindBtn = ttk.Button(bottomframe, image=rewindPhoto, command=rewind_music)
rewindBtn.grid(row=2, column=0)

ttk.Label(bottomframe, text="Mute").grid(row=1, column=1)
mutePhoto = PhotoImage(file='images/mute.png')
volumePhoto = PhotoImage(file='images/volume.png')
volumeBtn = ttk.Button(bottomframe, image=volumePhoto, command=mute_music)
volumeBtn.grid(row=2, column=1)

ttk.Label(bottomframe, text="Volume").grid(row=1, column=2)
scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)  # implement the default value of scale when music player starts
mixer.music.set_volume(0.7)
scale.grid(row=2, column=2, pady=15, padx=30)


def ampAdd(file, newfile, val, window):
    result = ampfunc(filepath=file, newfilename=newfile, ampval=val)
    if (result):
        add_to_playlist("./res/{f}.mp3".format(f=newfile))
        mess = (os.path.basename(file) + " is amplified by " + val)
        tkinter.messagebox.showinfo('Success', mess + '\nfile is addded to playlist as {f}.mp3'.format(f=newfile))
        close(window)
    else:
        tkinter.messagebox.showerror('Operation Error', 'Couldn\'nt reduce the file')


def ampUI():
    try:
        selected_song = playlistbox.curselection()
        selected_song = int(selected_song[0])
        play_it = playlist[selected_song]
        amp = tk.ThemedTk()
        amp.set_theme("radiance")
        amp.title("Amplify")
        ttk.Label(amp, text=os.path.basename(play_it)).grid(row=0, column=0)
        ttk.Label(amp, text="Value:").grid(row=1, column=0)
        ampVal = ttk.Entry(amp)
        ampVal.grid(row=1, column=1)
        ttk.Label(amp, text="New filename:").grid(row=2, column=0)
        ampname = ttk.Entry(amp)
        ampname.grid(row=2, column=1)
        saveBtn = ttk.Button(amp, text="Save As",
                             command=lambda: ampAdd(file=play_it, newfile=ampname.get(), val=ampVal.get(), window=amp))
        saveBtn.grid(row=2, column=3)
    except IndexError:
        tkinter.messagebox.showerror('Error', 'Please select a file from the playlist!')


def redAdd(file, newfile, val, window):
    result = redfunc(filepath=file, newfilename=newfile, redval=val)
    if (result):
        add_to_playlist("./res/{f}.mp3".format(f=newfile))
        mess = (os.path.basename(file) + " is reduced by " + val)
        tkinter.messagebox.showinfo('Success', mess + '\nfile is addded to playlist as {f}.mp3'.format(f=newfile))
        close(window)
    else:
        tkinter.messagebox.showerror('Operation Error', 'Couldn\'nt reduce the file')


def redUI():
    try:
        selected_song = playlistbox.curselection()
        selected_song = int(selected_song[0])
        play_it = playlist[selected_song]
        red = tk.ThemedTk()
        red.set_theme("radiance")
        red.title("Reduce")
        red.focus()
        ttk.Label(red, text=os.path.basename(play_it)).grid(row=0, column=0)
        ttk.Label(red, text="Value:").grid(row=1, column=0)
        redVal = ttk.Entry(red)
        redVal.grid(row=1, column=1)
        ttk.Label(red, text="New filename:").grid(row=2, column=0)
        redname = ttk.Entry(red)
        redname.grid(row=2, column=1)
        saveBtn = ttk.Button(red, text="Save As",
                             command=lambda: redAdd(file=play_it, newfile=redname.get(), val=redVal.get(), window=red))
        saveBtn.grid(row=2, column=3)
    except IndexError:
        tkinter.messagebox.showerror('Error', 'Please select a file from the playlist!')


def browse():
    global file
    file = filedialog.askopenfilename()


def merAdd(fileone, filetwo, newfile, window):
    result = merfunc(fileonepath=fileone, filetwopath=filetwo, newfilename=newfile)
    if (result):
        add_to_playlist("./res/{f}.mp3".format(f=newfile))
        mess = os.path.basename(fileone), " and ", os.path.basename(filetwo), " have been merged as ", os.path.basename(
            newfile)
        tkinter.messagebox.showinfo('Success', mess)
        close(window)
    else:
        tkinter.messagebox.showerror('Operation Error', 'Couldn\'nt merge the file')


def merUI():
    try:
        selected_song = playlistbox.curselection()
        selected_song = int(selected_song[0])
        play_it = playlist[selected_song]
        mer = tk.ThemedTk()
        mer.set_theme("radiance")
        mer.title("Merge")
        ttk.Label(mer, text=os.path.basename(play_it)).grid(row=0, column=0)
        ttk.Label(mer, text="Open file to be merged").grid(row=1, column=0)
        openBtn = ttk.Button(mer, text="Open", command=browse)
        openBtn.grid(row=1, column=1)
        ttk.Label(mer, text="New filename:").grid(row=2, column=0)
        mername = ttk.Entry(mer)
        mername.grid(row=2, column=1)
        saveBtn = ttk.Button(mer, text="Save As",
                             command=lambda: merAdd(fileone=play_it, filetwo=file, newfile=mername.get(), window=mer))
        saveBtn.grid(row=2, column=3)
    except IndexError:
        tkinter.messagebox.showerror('Error', 'Please select a file from the playlist!')


def splitcheck(file, newfile, start, end, window):
    if (start == ""):
        start = None
    elif (end == ""):
        end = None
    result = splitfunc(filepath=file, newfilename=newfile, splitstart=start, splitend=end)
    if (result):
        add_to_playlist("./res/{f}.mp3".format(f=newfile))
        tkinter.messagebox.showinfo('Success', "File has been split and saved as " + newfile)
        close(window)
    else:
        tkinter.messagebox.showerror('Operation Error', 'Couldn\'nt split the file')


def splitUI():
    try:
        selected_song = playlistbox.curselection()
        selected_song = int(selected_song[0])
        play_it = playlist[selected_song]
        split = tk.ThemedTk()
        split.set_theme("radiance")
        split.title("Split By")
        split.focus()
        ttk.Label(split, text=os.path.basename(play_it)).grid(row=0, column=0)
        ttk.Label(split, text="Split From").grid(row=1, column=0)
        splitStart = ttk.Entry(split)
        splitStart.grid(row=1, column=1)
        ttk.Label(split, text="Split till").grid(row=2, column=0)
        splitTill = ttk.Entry(split)
        splitTill.grid(row=2, column=1)
        ttk.Label(split, text="New filename:").grid(row=3, column=0)
        splitname = ttk.Entry(split)
        splitname.grid(row=3, column=1)
        saveBtn = ttk.Button(split, text="Save As",
                             command=lambda: splitcheck(file=play_it, newfile=splitname.get(), start=splitStart.get(),
                                                        end=splitTill.get(), window=split))
        saveBtn.grid(row=3, column=3)
    except IndexError:
        tkinter.messagebox.showerror('Error', 'Please select a file from the playlist!')


def insAdd(file, newfile, val, at, window):
    result = insfunc(filepath=file, newfilename=newfile, gapval=val, gapat=at)
    if (result):
        add_to_playlist("./res/{f}.mp3".format(f=newfile))
        mess = "Gap of " + val + " seconds has been inserted at " + at + "\nand saved as " + newfile
        tkinter.messagebox.showinfo('Success', mess)
        close(window)
    else:
        tkinter.messagebox.showerror('Operation Error', 'Couldn\'nt insert gap to the file')


def insUI():
    try:
        selected_song = playlistbox.curselection()
        selected_song = int(selected_song[0])
        play_it = playlist[selected_song]
        ins = tk.ThemedTk()
        ins.set_theme("radiance")
        ins.title("Insert Gap")
        ins.focus()
        ttk.Label(ins, text=os.path.basename(play_it)).grid(row=0, column=0)
        ttk.Label(ins, text="Enter gap value (In seconds):").grid(row=1, column=0)
        insVal = ttk.Entry(ins)
        insVal.grid(row=1, column=1)
        ttk.Label(ins, text="Insert the gap at (enter seconds):").grid(row=2, column=0)
        insAt = ttk.Entry(ins)
        insAt.grid(row=2, column=1)
        ttk.Label(ins, text="New filename:").grid(row=3, column=0)
        insname = ttk.Entry(ins)
        insname.grid(row=3, column=1)
        saveBtn = ttk.Button(ins, text="Save As",
                             command=lambda: insAdd(file=play_it, newfile=insname.get(), val=insVal.get(),
                                                    at=insAt.get(), window=ins))
        saveBtn.grid(row=3, column=3)
    except IndexError:
        tkinter.messagebox.showerror('Error', 'Please select a file from the playlist!')


def revAdd(file, newfile, window):
    result = revfunc(filepath=file, newfilename=newfile)
    if (result):
        add_to_playlist("./res/{f}.mp3".format(f=newfile))
        tkinter.messagebox.showinfo('Success', 'file is addded to playlist as {f}.mp3'.format(f=newfile))
        close(window)
    else:
        tkinter.messagebox.showerror('Operation Error', 'Couldn\'nt reverse the file')


def revUI():
    try:
        selected_song = playlistbox.curselection()
        selected_song = int(selected_song[0])
        play_it = playlist[selected_song]
        rev = tk.ThemedTk()
        rev.set_theme("radiance")
        rev.title("Reverse")
        ttk.Label(rev, text=os.path.basename(play_it)).grid(row=0, column=0)
        ttk.Label(rev, text="New filename:").grid(row=1, column=0)
        revname = ttk.Entry(rev)
        revname.grid(row=1, column=1)
        ttk.Button(rev, text="Save As", command=lambda: revAdd(file=play_it, newfile=revname.get(), window=rev)).grid(
            row=1, column=3)
    except IndexError:
        tkinter.messagebox.showerror('Error', 'Please select a file from the playlist!')


def fadeInAdd(file, newfile, val, window):
    result = fadeInfunc(filepath=file, newfilename=newfile, fadeInval=val)
    if (result):
        add_to_playlist("./res/{f}.mp3".format(f=newfile))
        tkinter.messagebox.showinfo('Success', 'Fading in effect is added to file {f}.mp3'.format(f=newfile))
        close(window)
    else:
        tkinter.messagebox.showerror('Operation Error', 'Couldn\'nt reduce the file')


def fadeInUI():
    try:
        selected_song = playlistbox.curselection()
        selected_song = int(selected_song[0])
        play_it = playlist[selected_song]
        fadeIn = tk.ThemedTk()
        fadeIn.set_theme("radiance")
        fadeIn.title("Fade In")
        ttk.Label(fadeIn, text=os.path.basename(play_it)).grid(row=0, column=0)
        ttk.Label(fadeIn, text="Fade in duration (Enter Seconds):").grid(row=1, column=0)
        fadeInVal = ttk.Entry(fadeIn)
        fadeInVal.grid(row=1, column=1)
        ttk.Label(fadeIn, text="New filename:").grid(row=2, column=0)
        fadeInname = ttk.Entry(fadeIn)
        fadeInname.grid(row=2, column=1)
        saveBtn = ttk.Button(fadeIn, text="Save As",
                             command=lambda: fadeInAdd(file=play_it, newfile=fadeInname.get(), val=fadeInVal.get(),
                                                       window=fadeIn))
        saveBtn.grid(row=2, column=3)
    except IndexError:
        tkinter.messagebox.showerror('Error', 'Please select a file from the playlist!')


def fadeOutAdd(file, newfile, val, window):
    result = fadeOutfunc(filepath=file, newfilename=newfile, fadeOutval=val)
    if (result):
        add_to_playlist("./res/{f}.mp3".format(f=newfile))
        tkinter.messagebox.showinfo('Success', 'Fading out effect is added to file {f}.mp3'.format(f=newfile))
        close(window)
    else:
        tkinter.messagebox.showerror('Operation Error', 'Couldn\'nt reduce the file')


def fadeOutUI():
    try:
        selected_song = playlistbox.curselection()
        selected_song = int(selected_song[0])
        play_it = playlist[selected_song]
        fadeOut = tk.ThemedTk()
        fadeOut.set_theme("radiance")
        fadeOut.title("Fade Out")
        ttk.Label(fadeOut, text=os.path.basename(play_it)).grid(row=0, column=0)
        ttk.Label(fadeOut, text="Fade Out duration (Enter Seconds):").grid(row=1, column=0)
        fadeOutVal = ttk.Entry(fadeOut)
        fadeOutVal.grid(row=1, column=1)
        ttk.Label(fadeOut, text="New filename:").grid(row=2, column=0)
        fadeOutname = ttk.Entry(fadeOut)
        fadeOutname.grid(row=2, column=1)
        saveBtn = ttk.Button(fadeOut, text="Save As",
                             command=lambda: fadeOutAdd(file=play_it, newfile=fadeOutname.get(), val=fadeOutVal.get(),
                                                        window=fadeOut))
        saveBtn.grid(row=2, column=3)
    except IndexError:
        tkinter.messagebox.showerror('Error', 'Please select a file from the playlist!')


amplifyBtn = ttk.Button(bottomframe, text="Amplify", command=ampUI)
amplifyBtn.grid(row=3, column=0)

reduceBtn = ttk.Button(bottomframe, text="Reduce", command=redUI)
reduceBtn.grid(row=3, column=1)

fadeOutBtn = ttk.Button(bottomframe, text="Fade In", command=fadeInUI)
fadeOutBtn.grid(row=3, column=2)

mergeAsBtn = ttk.Button(bottomframe, text="Merge As", command=merUI)
mergeAsBtn.grid(row=4, column=0)

splitBtn = ttk.Button(bottomframe, text="Split", command=splitUI)
splitBtn.grid(row=4, column=1)

insertGapBtn = ttk.Button(bottomframe, text="Insert Gap", command=insUI)
insertGapBtn.grid(row=5, column=0)

reverseBtn = ttk.Button(bottomframe, text="Reverse", command=revUI)
reverseBtn.grid(row=5, column=1)

fadeOutBtn = ttk.Button(bottomframe, text="Fade Out", command=fadeOutUI)
fadeOutBtn.grid(row=5, column=2)


def on_closing():
    if (tkinter.messagebox.askyesno(title="Closing", message="Do you really want to exit Voice Archive?")):
        stop_music()
        root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
