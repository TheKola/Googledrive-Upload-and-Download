from __future__ import print_function
import httplib2
import os,io
import webbrowser
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
import auth
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
creds = r'C:\Users\Vivek\Desktop\ppp\signups\tempfile.temp'

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
credentials = authInst.getCredentials()

http = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive', 'v3', http=http)

def Signup(): # This is the signup definition,
    global pwordE # These globals just make the variables global to the entire script, meaning any definition can use them
    global nameE
    global roots
    roots = Tk()
    #rootA.destroy() # This creates the window, just a blank one.
    roots.title('Signup') # This renames the title of said window to 'signup'
    intruction = Label(roots, text='Sign Up here :-\n') # This puts a label, so just a piece of text saying 'please enter blah'
    intruction.grid(row=0, column=0, sticky=W) # This just puts it in the window, on row 0, col 0. If you want to learn more look up a tkinter tutorial :)

    nameL = Label(roots, text='New Username :- ') # This just does the same as above, instead with the text new username.

    nameL.grid(row=1, column=0, sticky=W) # Same thing as the instruction var just on different rows. :) Tkinter is like that.
     # ^^

    nameE = Entry(roots) # This now puts a text box waiting for input.
     # Same as above, yet 'show="*"' What this does is replace the text with *, like a password box :D
    nameE.grid(row=1, column=1)
    nameL = Label(roots, text='-----------') # This just does the same as above, instead with the text new username.

    nameL.grid(row=2, columnspan=5) # You know what this does now :D
     # ^^

    signupButton = Button(roots, text='Signup', command=FSSignup) # This creates the button with the text 'signup', when you click it, the command 'fssignup' will run. which is the def
    signupButton.grid(columnspan=2,row=3)
    roots.mainloop() # This just makes the window keep open, we will destroy it soon

def FSSignup():
    scan=0
    with open(creds,'r') as f:
        for lines in f:
            data = f.readlines()
            for i in range(len(data)):# This takes the entire document we put the info into and puts it into the data variable
                uname1 = data[i].rstrip()
                if uname1==nameE.get():
                    scan=1
                    break
                else:
                    scan=0
    if scan==0:
        with open(creds, 'a') as f: # Creates a document using the variable we made at the top.
            f.write(nameE.get()) # nameE is the variable we were storing the input to. Tkinter makes us use .get() to get the actual string.
            f.close()# Closes the file
            folder_name=nameE.get()
            #print(folder_name)
            roots.destroy()# This will destroy the signup window. :)
            file_metadata = {'name': folder_name,'mimeType':'application/vnd.google-apps.folder'}
            file = drive_service.files().create(body=file_metadata,fields='id').execute()
            #print ('Folder ID: %s' % file.get('id'))
            Login() # This will move us onto the login definition :D
    else:
        labelz=Label(roots,text="\nUsername already taken :(\n")
        labelz.grid(columnspan=2,row=4)

def Login():
    global nameEL
    global rootA
    rootA = Tk() # This now makes a new window.
    rootA.title('Login') # This makes the window title 'login'

    intruction = Label(rootA, text='Please Login :- \n') # More labels to tell us what they do
    intruction.grid(sticky=W) # Blahdy Blah

    nameL = Label(rootA, text='Username :- ') # More labels # ^
    nameL.grid(row=1, sticky=W)

    nameEL = Entry(rootA) # The entry input
    nameEL.grid(row=1, column=1)
    nameL = Label(rootA, text='---------')
    nameL.grid(columnspan=2,row=2)
    loginB = Button(rootA, text='Login',command=CheckLogin) # This makes the login button, which will go to the CheckLogin def.
    loginB.grid(row=3, column=1)

    rmuser = Button(rootA, text='Sign Up', command=Signup) # This makes the deluser button. blah go to the deluser def.
    rmuser.grid(row=3, column=0)
    rootA.mainloop()

def listFiles(size):
    results = drive_service.files().list(pageSize=size,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))

def uploadFile(filename,filepath):
    file_metadata = {'name': filename}
    media = MediaFileUpload(filepath)
    file = drive_service.files().create(body=file_metadata,media_body=media,fields='id').execute()
    print('File ID: %s' % file.get('id'))

def downloadFile(name,foldername):
    #print(name,filepath,foldername)
    results = drive_service.files().list(pageSize=1000,fields="nextPageToken, files(id, name,mimeType)").execute()
    items = results.get('files', [])
    #print(items)
    for sd in items:
        if sd['mimeType']=="application/vnd.google-apps.folder" and sd['name']==foldername:
                folderw=sd['id']

    page_token=None
    while True:
        response = drive_service.files().list(q="'"+folderw+"' in parents",
                                          spaces='drive',
                                          fields='nextPageToken, files(id, name)',
                                          pageToken=page_token).execute()
        for file in response.get('files', []):
            fname=file.get('name')
            fname=fname.split(".")[0]
        # Process change
            if fname== name:
                s=file.get('id')
                filepath=file.get('name')
                #print ('Found file: %s (%s)' % (file.get('name'), file.get('id')))
                page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    try:
        request = drive_service.files().get_media(fileId=s)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            label=Label(roott,text=" Download %d%%." % int(status.progress() * 100))
            label.grid(column=4,row=3)
            #print("Download %d%%." % int(status.progress() * 100))
            with io.open(filepath,'wb') as f:
                fh.seek(0)
                f.write(fh.read())
        st1=r'"C:\Users\Vivek\Desktop\ppp\\'
        st2=filepath
        st3= st1.__add__(st2)
        st4='"'
        st5=st3.__add__(st4)
        st5=st5.replace("\\\\", "\&");
        st5=st5.replace("&", ""); #r"C:\Users\lenovo\Desktop\pr.pdf"
        #print(st5)
        webbrowser.open(st5)
    except:
        label=Label(roott,text=" --No file found--")
        label.grid(column=4,row=3)

def searchFile(name,foldername):
    x=0
    global labelA
    results = drive_service.files().list(pageSize=1000,fields="nextPageToken, files(id, name,mimeType)").execute()
    items = results.get('files', [])
    #print(items)
    for sd in items:
        if sd['mimeType']=="application/vnd.google-apps.folder" and sd['name']==foldername:
                folderw=sd['id']
    page_token = None
    while True:
        response = drive_service.files().list(q="'"+folderw+"' in parents",
                                          spaces='drive',
                                          fields='nextPageToken, files(id, name)',
                                          pageToken=page_token).execute()
        for file in response.get('files', []):
        # Process change
            if file.get('name')== name:
                x=1
                break
            else:
                x=0
        if page_token is None:
            break
    if x==1:
        labelA=Label(roott,text=" Same name file exsist\nChange the name :)")
        labelA.grid(column=4,row=0)
    else:
        up1()

def uploadtofolder(filename,filepath,foldername):
    results = drive_service.files().list(pageSize=1000,fields="nextPageToken, files(id, name,mimeType)").execute()
    items = results.get('files', [])
    #print(items,"\n")
    for sd in items:
        if sd['mimeType']=="application/vnd.google-apps.folder" and sd['name']==foldername:
            file_metadata = {'name':filename,'parents': [sd['id']]}
            media = MediaFileUpload(filepath,resumable=True)
            file = drive_service.files().create(body=file_metadata,media_body=media,fields='id').execute()
            try:
                labelA.winfo_exists() == 1
                labelA.destroy()
                label=Label(roott,text="File uploded :)")
                label.grid(column=4,row=0)
            except:
                label=Label(roott,text="File uploded :)")
                label.grid(column=4,row=0)

def CheckLogin():
    global file_name_saveas
    global file_name_download
    global file_name_download_saveas
    global roott
    global username
    with open(creds,'r') as f:
        for lines in f:
            data = f.readlines()
            for i in range(len(data)):# This takes the entire document we put the info into and puts it into the data variable
                uname = data[i].rstrip()# Data[0], 0 is the first line, 1 is the second and so on.
                if nameEL.get() == uname: # Checks to see if you entered the correct data.
                    username=uname
                    def fileDialog():
                        global filename_loc
                        global filename
                        global folder_name
                        filename=filedialog.askopenfilename(initialdir="/",title="Select a file", filetype=(("All files","*.*"),("jpeg","*.jpg")))
                        #print(filename)
                        filename=filename.replace("/","\&")
                        filename_loc=filename.replace("&","")
                        filename=filename.split("\&")[-1]
                        #print(filename_loc)
                        #print(filename)
                        folder_name=uname
                        #print(folder_name)
                    rootA.destroy()
                    roott= Tk()
                    aaa=StringVar()
                    roott.title("Upload and Download file")
                    roott.geometry('500x200+400+400')
                    label=Label(roott,text="\nFile to Upload :-  \n")
                    label.grid(column=0,row=0,sticky=W)
                    button=Button(roott,text='Browse a file',command=fileDialog)
                    button.grid(column=1,row=0)
                    button4=Button(roott,text='OK',command=up)
                    button4.grid(column=2,row=0)
                    labell=Label(roott,text="--------------------------------------------")
                    labell.grid(columnspan=5,row=2)
                    label=Label(roott,text="Name of the File to download :-  ")
                    label.grid(column=0,row=3,sticky=W)
                    file_name_download=Entry(roott)
                    file_name_download.grid(column=1,row=3)
                    button4=Button(roott,text='OK',command=down)
                    button4.grid(column=2,row=3)
                    labell=Label(roott,text="--------------------------------------------")
                    labell.grid(columnspan=5,row=4)
                    button5=Button(roott,text='Logout',command=Login_in)
                    button5.grid(columnspan=2,row=5)
                else:
                    labelt=Label(rootA,text="\nInvalid Login :(\n")
                    labelt.grid(columnspan=2,row=4)

def up():
    searchFile(filename,folder_name)
def up1():    #print(file_name_saveas.get()," ",filename," ",folder_name)
    uploadtofolder(filename,filename_loc,folder_name)
def down():
    file_download=file_name_download.get()
    foldername=username
    #print(file_download,'' ,title)
    downloadFile(file_download,foldername)
def Login_in():
    roott.destroy()
    Login()
def Login_inn():
    roots.destroy()
    Login()
#path=input('Enter the path :- ')
#name=input('Enter the file name :- ')
#folder_name =input('Enter the folder name :- ')
#query=queries(folder_name)
#file=input('Enter the file to download :- ')
#file_to_download=queries(file)
#title=input('Enter the title with extension :- ')
#uploadFile(name,filepath)
#name=input('enter file name :-')
#foldername=input('enter folder name :-')
#listFiles(110)
#searchFile(name,foldername)
#downloadFile(name,title,foldername)
#createFolder('Google')
#uploadtofolder(name,path,query)
if os.path.isfile(creds):
    Login()
else: # This if else statement checks to see if the file exists. If it does it will go to Login, if not it will go to Signup :)
    Signup()
