# importing the eel library  
from yt_dlp import YoutubeDL
import eel  
import validators
from os import chdir , getlogin , name
import socket


names = []
errors = 0
info = {}
wifi = {}
errors_list = []

# initializing the application  
eel.init("web")  
          
        
def check_data(url , path):
    global errors , errors_list       
    try:
        chdir(path)
    except:
        errors = errors + 1
        errors_list.append("You have entered an invalid directory for the path!")
    if validators.url(url) ==  True:
        pass
    else:
        errors = errors + 1
        errors_list.append("You have entered an invalid URL for the youtube video.")                           
        
def download_video(url , path):
    ydl = YoutubeDL()
    cd = chdir(path)
    r = ydl.extract_info(url, download=True)
      
# using the eel.expose command  
@eel.expose
def send_data(url , path):
 
    url = url
    path = path
    check_data(url , path)
    if errors == 0:
        download_video(url , path)
        eel.start("success.html" , port = 8002)
    if errors > 0:
        file = open('errors.txt' , 'w')
        data = "No. Of Errors: " + str(len(errors_list)) + "\n"                    
        file.write(data)
        for a in errors_list:
            data = a + "\n"
            file.write(data)
        file.close()            
        eel.start("error.html" , mode = 'chrome' , port = 8001)           

 

            


        
# starting the application  
eel.start("yt.html" ,size = (800,800) , port = 8000 , mode = 'chrome')  