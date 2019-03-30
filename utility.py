import os
import os as os1
from shutil import copyfile
import paths 
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

proxy = 'http://172.31.2.4:8080'

os.environ['http_proxy'] = proxy 
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy


DOWNLOAD_PATH = paths.DOWNLOAD_PATH # '/home/shreyasus/Downloads/'
SAVING_PATH = paths.SAVING_PATH # '/home/shreyasus/Desktop/HINT4/'
START_PATH = paths.START_PATH 
HINT_PATH = paths.HINT_PATH
PASSWORD = paths.PASSWORD

activePath = START_PATH
os1.chdir(activePath)

def createYoutubeLink(query):
    query=query.replace(' ','+')
    link = 'https://youtube.com/results?search_query='+query
    return link

def checkAlreadyExistingFile(fileName):
    os.chdir(DOWNLOAD_PATH)
    return (fileName in os.listdir('.'))

def organizePDF(fileName):
    folder = fileName[0:fileName.find(' -')]
    os.chdir(SAVING_PATH)
    if ((folder in os.listdir('.'))==False):
        os.mkdir(folder)
    copyfile(DOWNLOAD_PATH+fileName,SAVING_PATH+'/'+folder+'/'+fileName)

def checkAlreadyExistingFile2(path, fileName):
    os.chdir(path)
    return (fileName in os.listdir('.'))

def uploadDrive(path):
    os.system('gdrive upload ' + path)

def executeTerminalCommands(command):

   

    

    global activePath
    os1.chdir(activePath)

    response = ''

    if ('upload ' in command)==False:
        status = os1.system(command)
        
        if (status == 0):
            response = 'Successful'
        else:
            response = 'Failed'

    # cd .. cd Desktop
    if ('cd ' in command ):
        command = command[3:]
        if (command.strip()=='..'):
            tmp = activePath
            tmp = tmp[ 0 : tmp[0:len(tmp)-1].rfind('/') ] + '/'
        else:
            tmp = activePath + command + '/'
        activePath = tmp
        os1.chdir(activePath)
    
    # ls
    elif ('ls'==command):
        response = str(os1.listdir('.'))
    
    # find /home/shreyasus/ -name file.ext
    elif ('find ' in command):
        #tmp = os1.popen('echo %s|sudo -S %s' % (PASSWORD, command)).read().split('\n')
        tmp = os1.popen(command).read().split('\n')
        response = tmp[0]
    
    # upload /home/shreyasus/Desktop/...
    elif ('upload ' in command):
        tmp = command[7:]
        if (os.path.isfile(tmp)):
            uploadDrive(tmp)
            response = 'Successful'
        elif (os.path.isdir(tmp)):
            # Creating a zipped folder
            status = os.system('zip -r '+tmp+'.zip '+tmp)
            if (status == 0):
                uploadDrive(tmp+'.zip')
                response = 'Successful'
            else:
                response = 'Failed'
        else:
            response = 'File not found'
    elif "kill" in command.lower():
        command = "ps -A | grep " + command[5:len(command)]
        tmp = os1.popen(command).read().split('\n')
        tmp = str(tmp[0])
        print (tmp[0: tmp.find(' ')])
        os1.popen('kill -9 ' + tmp).read().split('\n')
        response = "Successful"

            

    return response

def savePollResults(results, title) :
    objectss = []
    performance = []
    for key, value in results.items() :
        objectss.append(key) 
        performance.append(value)
    objects = tuple(objectss)

    plt.pie(performance, labels=objects, startangle=90, autopct='%.1f%%')
    plt.title(title)
    plt.savefig(HINT_PATH+'foo.png')

'''
while False:
    command = input('>> ')
    responses = executeTerminalCommands(command)
    for response in responses:
        if (response.strip()!=''):
            print ('>'+response+'<<')
'''


#organizePDF('Android - Problem-statements.pdf')

'''
from pathlib import Path

MY_DOCS_LIST_PATH = '/home/shreyasus/Desktop/HINT4/MyDocs/myDocsList.txt'
MY_DOCS_PATH = '/home/shreyasus/Desktop/HINT4/MyDocs/'

myDocsList = Path(MY_DOCS_LIST_PATH).read_text().split('\n')

myDocsMap = {}
for element in myDocsList:
    key,value = element.split(' - ')
    myDocsMap[key] = value
print("My Docs")
print(myDocsMap)
'''