import os
from pydub import AudioSegment

def ampfunc(filepath, newfilename, ampval):
    
    try:
        #filepath is used to find and import the file as AudioSegment object
        audio=AudioSegment.from_file(filepath, "mp3")
        #ampval is relative amplitude by which audio should be louder
        audio+=int(ampval)
        #newfilename is the name of the file to be saved
        audio.export("res/{f}.mp3".format(f=newfilename), format="mp3")
        return True
    except:
        return False
    
def redfunc(filepath, newfilename, redval):
    try:
        #filepath is used to find and import the file as AudioSegment object
        audio=AudioSegment.from_file(filepath, "mp3")
        #redval is relative amplitude by which audio should be quieter
        audio-=int(redval)
        #newfilename is the name of the file to be saved
        audio.export("res/{f}.mp3".format(f=newfilename), format="mp3")
        return True
    except:
        return False
    
def merfunc(fileonepath, filetwopath, newfilename):
    try:
        #fileonepath is used to find and import the first file as AudioSegment object
        audio1=AudioSegment.from_file(fileonepath, "mp3")
        #filetwopath is used to find and import the second file as AudioSegment object
        audio2=AudioSegment.from_file(filetwopath, "mp3")
        #both audio files are merged together
        audio1+=audio2
        #newfilename is the name of the file to be saved
        audio1.export("res/{f}.mp3".format(f=newfilename), format="mp3")
        return True
    except:
        return False

def splitfunc(filepath, newfilename, splitstart, splitend):
    try:
        #filepath is used to find and import the file as AudioSegment object
        audio=AudioSegment.from_file(filepath, "mp3")
        if(splitstart==None):   
            #if user doesn't provide splitstart this statement is executed
            audsplit=audio[:(int(splitend)*1000)]
        elif(splitend==None):
            #if user doesn't provide splitend this statement is executed
            audsplit=audio[(int(splitstart)*1000):]
        else:
            audsplit=audio[(int(splitstart)*1000):(int(splitend)*1000)]
        #newfilename is the name of the file to be saved
        audsplit.export("res/{f}.mp3".format(f=newfilename), format="mp3")
        return True
    except:
        return False
    
def insfunc(filepath, newfilename, gapval, gapat):
    try:
        #filepath is used to find and import the file as AudioSegment object
        audio=AudioSegment.from_file(filepath, "mp3")
        #Here gapat represents the second as index till where silence is inserted
        audstart=audio[:gapat]
        #Here gapat represents the second as index from where silence is inserted
        audend=audio[gapat+1:]
        #adds silence for gapval seconds
        audgap=audstart+AudioSegment.silent(duration = gapval*1000)+audend
        #newfilename is the name of the file to be saved
        audgap.export("res/{f}.mp3".format(f=newfilename), format="mp3")
        return True
    except:
        return False

def revfunc(filepath, newfilename):
    try:
        #filepath is used to find and import the file as AudioSegment object
        audio=AudioSegment.from_file(filepath, "mp3")
        #reverses the audio
        audio.reverse()
        filename="res/{f}.mp3".format(f=newfilename)
        #newfilename is the name of the file to be saved
        audio.export(filename, format="mp3")
        return True
    except:
        return False
    
def fadeInfunc(filepath, newfilename, fadeInval):
    try:
        #filepath is used to find and import the file as AudioSegment object
        audio=AudioSegment.from_file(filepath, "mp3")
        #fadeInval specifies how long the fade-in effect will last
        audio=audio.fade_in(int(fadeInval)*1000)
        #newfilename is the name of the file to be saved
        audio.export("res/{f}.mp3".format(f=newfilename), format="mp3")
        return True
    except:
        return False

def fadeOutfunc(filepath, newfilename, fadeOutval):
    try:
        #filepath is used to find and import the file as AudioSegment object
        audio=AudioSegment.from_file(filepath, "mp3")
        #fadeOutval specifies from when audio starts fading out
        audio=audio.fade_out(int(fadeOutval)*1000)
        #newfilename is the name of the file to be saved
        audio.export("res/{f}.mp3".format(f=newfilename), format="mp3")
        return True
    except:
        return False

def convertfunc(filepath, extension):
    try:
        #splittext() method splits the filename and its directory from its extension
        filename, file_extension = os.path.splitext(filepath)
        file_extension=file_extension[1:]
        #filepath is used to find and import the file as AudioSegment object
        audio=AudioSegment.from_file(filepath, file_extension)
        #Returns the name of the file from the provided directory
        filename=os.path.basename(filepath)
        filename=filename.split(".")[0]
        #newfilename is the name of the file to be saved 
        #extension specifies in which format to save
        audio.export("res/{f}.{e}".format(f=filename,e=extension),format=extension)
        return True
    except:
        return False

def seclen(filepath):
    #filepath is used to find and import the file as AudioSegment object
    audio=AudioSegment.from_file(filepath, "mp3")
    #returns length of the audio file in seconds
    return audio.duration_seconds
    