



from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
import time 
from time import sleep
import random
from pathlib import Path
import chatbot
import utility
from threading import Thread
import os
import paths
import reminder
import getEvent

# Old pages //*[@id="main"]/div[3]/div/div/div[3]/div[19]/div/div
# New pages //*[@id="main"]/div[3]/div/div/div[2]/div[3]/div/div/div[1]/div


DRIVER_PATH = paths.DRIVER_PATH # '/home/shreyasus/Downloads/chromedriver'
REPLY_ONLY_LIST_PATH = paths.REPLY_ONLY_LIST_PATH # '/home/shreyasus/Desktop/HINT4/replyOnlyList.txt'
SLANG_WORDS_PATH = paths.SLANG_WORDS_PATH # '/home/shreyasus/Desktop/HINT4/slangWords.txt'
SLANG_WORDS_RESPONSE_PATH = paths.SLANG_WORDS_RESPONSE_PATH # '/home/shreyasus/Desktop/HINT4/slangWordsResponse.txt'
MY_DOCS_LIST_PATH = paths.MY_DOCS_LIST_PATH # '/home/shreyasus/Desktop/HINT4/MyDocs/myDocsList.txt'
MY_DOCS_PATH = paths.MY_DOCS_PATH # '/home/shreyasus/Desktop/HINT4/MyDocs/'
HINT_PATH = paths.HINT_PATH # '/home/shreyasus/Desktop/HINT4/'
URL = 'https://web.whatsapp.com/'
BOT_NAME = 'Bot'
COMMAND_LINK_FOR_VIDEO = 'Link for '
CHAT_COUNT = 25
MESSAGE_COUNT = 50
EMAIL = paths.EMAIL

driver = webdriver.Chrome(DRIVER_PATH) 
driver.get(URL)                              

wait = WebDriverWait(driver, 600) 

replyOnlyList = Path(REPLY_ONLY_LIST_PATH).read_text().split('\n')
slangWords = Path(SLANG_WORDS_PATH).read_text().split('\n')
slangWordsResponse = Path(SLANG_WORDS_RESPONSE_PATH).read_text().split('\n')
myDocsList = Path(MY_DOCS_LIST_PATH).read_text().split('\n')
isBotActive = True
isCommandMode = False
loadPercent = 0.50

myDocsMap = {}
for element in myDocsList:
    key,value = element.split(' - ')
    myDocsMap[key] = value
print("My Docs")
print(myDocsMap)

lastCommand = ''
inBotPage = False

activePolls = {}
startTimes = {}
currGroupName = ""
currPurpose = ""
currOptions = {}

lastReadMessages = {}
def initialize():
    global lastReadMessages
    invalids=0
    # Checking every chats
    for i in range(1,CHAT_COUNT):
        try:
            print (i)
            tmpHead = driver.find_element_by_xpath('//*[@id="pane-side"]/div/div/div/div['+str(i)+']')
            block = tmpHead.text.split('\n')
            print (block)
            tmpHead.click()
            sleep(0.5)
            print (block[0]+' is clicked')
            # Checking every messages
            messages = []
            for i in range(1,MESSAGE_COUNT):
                try :
                    # for normal ones
                    temp = driver.find_element_by_xpath('//*[@id="main"]/div[3]/div/div/div[3]/div['+str(i)+']/div/div/div[1]/div/span').text
                    print (temp)
                    if (temp != ''):
                        messages.append(temp)
                except:
                    try :
                        # for empty ones
                        temp = driver.find_element_by_xpath('//*[@id="main"]/div[3]/div/div/div[2]/div['+str(i)+']/div/div/div[1]/div/span').text
                        print (temp)
                        if (temp != ''):
                            messages.append(temp)
                    except:
                        # ignore
                        ...
            print (messages)
            lastReadMessages[block[0]]=messages

        except:
            #ignore
            invalids = invalids+1
            ...
    if (invalids > CHAT_COUNT*(1 - loadPercent)):
        initialize()
    else:
        print('\033c')
        
        for key,value in lastReadMessages.items():
            print (key,' -> ',value) 

        startAssistant()

def getUnreadMessages(chatName):
    global lastReadMessages
    
    print ('In ',chatName)

    # Detecting PDFs
    for i in range (1,MESSAGE_COUNT):
        try:
            # detecting PDFs
            print ('Detecting PDF')
            labels = driver.find_element_by_xpath('//*[@id="main"]/div[3]/div/div/div[3]/div['+str(i)+']/div/div').text.split('\n')
            print (labels)
            isPDF = False
            pdfName = ''
            for label in labels:
                isPDF = isPDF or ('pagesPDF' in label)
            
            for label in labels:
                isPDF = isPDF or ('•' in i and 'pages' in i)
            
            if (isPDF):
                print ('PDF Detected')
                print (labels)
                downloadBtn = driver.find_element_by_xpath('//*[@id="main"]/div[3]/div/div/div[3]/div['+str(i)+']/div/div[1]/a/div[2]/div[3]/span')
                downloadReq = True
                for label in labels:
                    chk = utility.checkAlreadyExistingFile(label+'.pdf')
                    chk = chk or utility.checkAlreadyExistingFile(label)
                    if (chk):
                        pdfName = label+'.pdf'
                        downloadReq = False
                        break
                if (downloadReq):
                    downloadBtn.click()
                    print ('downloading ....')
                    # TODO Start a thread to check when download of PDF is completed by using labels
                    print(labels[max(0,len(labels)-3)])
                    thread1 = Thread(target = downloadPDF, args = (labels[max(0,len(labels)-3)],))
                    thread1.start()
                    #break
                else:
                    print (pdfName,'Already downloaded')
            
        except:
            ...
    
    old = []
    if (chatName in lastReadMessages):
        old = lastReadMessages[chatName]
    
    print ('Old message',old)

    # Detecting messages
    messages = []
    for i in range(1,MESSAGE_COUNT):
        try :
            # for normal ones
            temp = driver.find_element_by_xpath('//*[@id="main"]/div[3]/div/div/div[3]/div['+str(i)+']/div/div/div[1]/div/span').text
            #print (temp)                        
            if (temp != ''):
                messages.append(temp)
            
            

        except:
            try :
                temp = driver.find_element_by_xpath('//*[@id="main"]/div[3]/div/div/div[2]/div['+str(i)+']/div/div/div[1]/div/span').text
                
                if (temp != ''):
                    messages.append(temp)
            except:
                ...
    



    new = messages
    print ('New messages',new)
    lastReadMessages[chatName]=new


    unread = []

    for i in range(0,len(new)):
        comFlag=0
        for j in range(0,len(old)):
            #print (old[j],new[i])
            if (new[i]==old[j]):
                k=0
                while (i+k<len(new) and j+k<len(old) and new[i+k]==old[j+k]):
                    k+=1
                    if (j+k==len(old)):
                        break
                if (j+k==len(old)):
                    unread = new[i+k:]
                    comFlag=1
                    break
        if (comFlag==1):
            break

    if (comFlag==0):
        unread=new
    
    print ('Unread messages')
    print (unread)
    return unread[len(unread)-1]


def respondTo(chatHead, chatName, botHead):
    global inBotPage
    global lastReadMessages
    chatHead.click()
    print('clicked')
    sleep(1)
    inBotPage = False
    message=getUnreadMessages(chatName)
    
    print ('>>> '+message)
    response=''
    hasSlang = False
    for slang in slangWords:
        if (slang in message):
            hasSlang = True
            break
    command = message
    if (hasSlang):
        response = random.choice(slangWordsResponse)
    elif (COMMAND_LINK_FOR_VIDEO in message):
        link = utility.createYoutubeLink(message[9:])
        response = "Here's your link "+link
    elif ('notes' in command):
        if 'Send' in command :
            print("jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
            chap = ""
            if "-" in command :
                ind = command.find(" - ")
                subject = command[5 : ind]
                chap = command[5 : command.find(" notes")]
                path = HINT_PATH + subject + "/" + chap + ".pdf"
                print (path)
            else :
                ind = command.find(" notes")
                subject = command[5 : ind]
                path = HINT_PATH + subject
            
            if chap == "" and utility.checkAlreadyExistingFile2(HINT_PATH, subject) == False :
                print ("in2")
                response = "Sorry, But I don't have such content as of now"
            elif chap != "" and utility.checkAlreadyExistingFile2(HINT_PATH+subject, chap+".pdf") == False :
                print ("in2")
                response = "Sorry, But I don't have such content as of now"
            else :
                print("jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
                if chap == "":
                    os.chdir(path)
                    for i in os.listdir(".") :
                        # path = path + "/" + i
                        thread = Thread(target = sendDocument, args = (path+"/"+i,))
                        thread.start()
                        thread.join()
                        # sendDocument(path+"/"+i)
                else :
                    sendDocument(path)
                response = "Sent! Enjoy"
        else :
            response = "Say that again!"
    # Set reminder on 2019-03-31 03:58 for calling 
    elif ('Set reminder on ' in command ):
        details = command[37:]
        time2 = command[16:32].replace(' ', 'T')
        time2 = time2 + ':00+05:30'
        reminder.setreminder(details, EMAIL , time2, time2)
        response = 'Successful'
    else:
        print ('Chatbot generated reply')
        response = chatbot.getResponse(message)
    
    print (response)

    if (response != ''):
    # Sending reply message
        inputBox = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        inputBox.send_keys(response)
        sendBtn = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')
        sendBtn.click()

    sleep(0.5)
    botHead.click()
    inBotPage = True


def respondToCommands(botHead,command):
    responseToGroup = ""
    global currGroupName
    global currOptions
    global currPurpose
    global activePolls
    global startTimes
    global isBotActive
    global inBotPage
    global isCommandMode

    # command = command.lower()

    flag = 0
    # Create poll in xxx regarding xxx with options xxx,yyy,zzz for xxx minutes  
    print("hi")
    
    
    response = ''
    purpose = ""

    if (isCommandMode):
        # Terminal mode
        print ('Terminal mode')
        if (command.lower() in ['stop','end','exit']):
            isCommandMode = False
            response = 'Terminal mode ended'
        else:
            response = utility.executeTerminalCommands(command)
            print (response)
            response = response.replace('\n',' ')
    else:
        print('Normal mode')
        # Normal mode
        
        st = command[7 : 11]
        if st == "poll" :
            ind = command.find(" regarding")
            ind2 = command.find("in")
            currGroupName = command[ind2+3 : ind]
            ind = command.find("regarding")
            ind2 = command.find(" with")
            purpose = command[ind+10 : ind2]
            ind = command.find("options")
            ind2 = command.find(" for")
            options = command[ind+8 : ind2]
            currOptions = options.split(',')
            ind = command.find(" regarding")
            ind2 = len(command)
            activePolls[currGroupName] = {}
            millis = int(round(time.time() * 1000))
            response = "Polling has been started at your request"
            responseToGroup = "Hello I am starting a poll" + command[ind : ind2]
            ind = command.find("for")
            ind2 = command.find(" minutes")
            tim = int(command[ind+4 : ind2])
        # Give my <PAN card number/copy>
        elif ('Give my' in command):
            command = command.lower()
            if ('number' in command):
                
                key = command[8:len(command)-7]
                if (key in myDocsMap):
                    response = myDocsMap[key]
                else:
                    response = 'Sorry '+key+' Not Found !'
            elif ('copy' in command):
                try :
                    flag = 1
                    key = command[8:len(command)-5]
                    path = key+'.jpeg'
                    thread = Thread(target = sendDocument, args = (MY_DOCS_PATH+path,))
                    thread.start()
                    # sendDocument(MY_DOCS_PATH+path)
                    # 123
                    response = lastCommand # "Here's your "+key
                except:
                    response = 'Sorry '+key+' Not Found !'
        # Add name 
        elif ('Add ' in command):
            name = command[4:]
            replyOnlyList.append(name)
            print (name+' added to the list')
            print (replyOnlyList)
            response = name + ' added successfully'
        # Remove name
        elif ('Remove ' in command):
            name = command[7:]
            if (name in replyOnlyList):
                replyOnlyList.remove(name)
                print (name+' removed from the list')
                print (replyOnlyList)
                response = name + ' removed successfully'
            else:
                print (name + ' not found')
                response = name + ' was already not in list'
        # Show reply list
        elif ('Show reply list' in command):
            response = str(replyOnlyList)
        # Stop / Pause
        elif (command == 'Stop' or command == 'Pause'):
            response = 'Bot Deactivated'
            print ('Bot Deactivated')
            isBotActive = False
        # Start / Resume
        elif (command == 'Start' or command == 'Resume'):
            response = 'Bot Activated'
            print ('Bot Activated')
            isBotActive = True
        # Set reminder on 2019-03-31 03:58 for calling 
        elif ('Set reminder on ' in command ):
            details = command[37:]
            time2 = command[16:32].replace(' ', 'T')
            time2 = time2 + ':00+05:30'
            reminder.setreminder(details, EMAIL , time2, time2)
            response = 'Successful'
        # getting list of upcoming events 
        #upcoming 02 events from 2019-03-31
        elif ('upcoming ' in command ):
            date = command[24:]
            date = date + 'T01:00:00+05:30'
            response = getEvent.upComingEvents(int(command[9:11]), date)
        # Terminal
        elif (command == 'Terminal'):
            isCommandMode = True
            response = 'Terminal mode started'
        else :
            response = chatbot.getResponse(command)
    
    response = response.replace('\n',' ')
    # Sending reply message
    if flag == 0 :
        inputBox = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        inputBox.send_keys(response)
        print ('Sending response = '+response)
        while (True):
            try:
                sleep(0.5)
                print('waiting for the button ... ')
                sendBtn = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')
                
                sendBtn.click()
                print (response + ' Sent ')
                break 
            except:
                ... 

        

    if responseToGroup != "" :
        flag = True
        while flag:
            for i in range(1,CHAT_COUNT):
                try:
                    print(i)
                    tmpHead = driver.find_element_by_xpath('//*[@id="pane-side"]/div/div/div/div['+str(i)+']')
                    block = tmpHead.text.split('\n')
                    if (block[0] == currGroupName):
                        print("inside")
                        flag = False
                        chatHead = tmpHead
                        # startTimes[currGroupName] = millis
                        chatHead.click()
                        inBotPage = False
                        # Sending reply message
                        inputBox = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
                        inputBox.send_keys(responseToGroup)
                        sendBtn = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')
                        sendBtn.click()
                        
                        thread = Thread(target = checkTimings, args = (currGroupName,responseToGroup, tim*60000, millis, botHead,purpose))
                        thread.start()
                except:
                    print("aaya")
                    #ignore
                    ...
    
    sleep(0.5)
    botHead.click()
    inBotPage = True
    
    return response


def handleUnreadMessages():
    global inBotPage
    global lastCommand
    # print ("detecting unread messages")
    botHead = ''
    chatName = ''
    hasUnreadMsg = 0

    for i in range(1,CHAT_COUNT):
        try:
            tmpHead = driver.find_element_by_xpath('//*[@id="pane-side"]/div/div/div/div['+str(i)+']')
            block = tmpHead.text.split('\n')
            if (block[0]==BOT_NAME):
                botHead=tmpHead

            # print (block)
            if (block[0] in replyOnlyList):
                (int(block[len(block)-1]))
                (driver.find_element_by_xpath('//*[@id="pane-side"]/div/div/div/div['+str(i)+']/div/div/div[2]/div[2]/div[2]/span[1]/div/span').text)
                chatHead=tmpHead
                chatName = block[0]
                hasUnreadMsg = hasUnreadMsg+1
        except:
            ...
    
    # Responding to unread messages
    if (hasUnreadMsg > 0 and isBotActive):
        respondTo(chatHead, chatName, botHead)
    
    # Detecting Commands
    if (inBotPage == False and botHead != ''):
        botHead.click()
        sleep(0.5)
        inBotPage = True
    
    if (botHead != ''):
        print('Bot available')

        messages = []
        message = ''
        for i in range(1,MESSAGE_COUNT):
            try :
                # for normal ones
                temp = driver.find_element_by_xpath('//*[@id="main"]/div[3]/div/div/div[3]/div['+str(i)+']/div/div/div[1]/div').text
                print ('Bot page - ',temp)
                if (temp != ''):
                    messages.append(temp)
            except:
                try :
                    # for empty ones
                    temp = driver.find_element_by_xpath('//*[@id="main"]/div[3]/div/div/div[2]/div['+str(i)+']/div/div/div[1]/div').text
                    print ('Bot page - ',temp)
                    if (temp != ''):
                        messages.append(temp)
                except:
                    # ignore
                    ...
        #print (messages)
        #new = messages
        if (len(messages)>0):
            message=messages[len(messages)-1]
        print ('Last Bot message')
        print ('>>> '+message)
        response=''

        if (lastCommand == ''):
            lastCommand = message
        
        if (message != '' and message != lastCommand):
            # New Command detected
            print ('message = ',message)
            print ('lastCommand = ',lastCommand)
            lastCommand = message
            print ('New Command Detected')
            response = respondToCommands(botHead,lastCommand)
            lastCommand = response
            ...
    
    # print ('done detecting')

def startAssistant():
    while True:
        handleUnreadMessages()
        sleep(1)

def checkTimings(groupName, responseToGroup, start, timeInMillis, botHead, purpose):
    global inBotPage
    flag = True
    while flag:
        currTime = int(round(time.time() * 1000))
        if currTime - start > timeInMillis :
            for i in range(1,CHAT_COUNT):
                try:
                    print(i)
                    tmpHead = driver.find_element_by_xpath('//*[@id="pane-side"]/div/div/div/div['+str(i)+']')
                    block = tmpHead.text.split('\n')
                    if (block[0] == groupName):
                        print("TIMEOVER")
                        flag = False
                        chatHead = tmpHead
                        chatHead.click()
                except:
                    print("ERROR AAYA")
                    ...

    
    chatHead.click()


    voteMap = {}
    startMessage = responseToGroup
    startFlag=False
    for i in range (1,MESSAGE_COUNT):
        try :
            msg = driver.find_element_by_xpath('//*[@id="main"]/div[3]/div/div/div[3]/div['+str(i)+']/div/div').text.split('\n')
            if (msg[0]==startMessage):
                startFlag=True
            msgLen = len(msg)
            if (msgLen>2):
                if (startFlag):
                    print(msg[0],' -> ',msg[msgLen-2])
                    voteMap[msg[0]]=msg[msgLen-2]
        except:
            ...
    
    voteCount = {}
    for key,value in voteMap.items():
        print(key,' = > ',value)
        if (value in voteCount):
            voteCount[value]=voteCount[value]+1
        else:
            voteCount[value]=1

    print (voteCount)

    response = "Hi the time for poll is over. Here are the results - "+str(voteCount)

    # Sending reply message
    inputBox = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
    inputBox.send_keys(response)
    sendBtn = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')
    sendBtn.click()
    
    utility.savePollResults(voteCount, purpose)
    # sleep(1)
    thread = Thread(target = sendDocument, args = (HINT_PATH+"foo.png",))
    thread.start()
    thread.join()
    sleep(0.5)
    botHead.click()
    inBotPage = True

def threadFun():
    thread1 = Thread(target = initialize, args = ())
    thread1.start()
    print ("thread finished...exiting")

# PDF name must be Subject - Chapter eg Android - Problem Statement
def downloadPDF(fileName):
    while (True):
        print('Waiting for download')
        chk = utility.checkAlreadyExistingFile(fileName+'.pdf')
        if (chk):
            # Download Compeleted
            print ('PDF Download Completed')
            utility.organizePDF(fileName+'.pdf')
            break
        sleep(1)

def sendDocument(path):
    driver.find_element_by_css_selector("span[data-icon='clip']").click()
    sleep(0.25)
    driver.find_element_by_css_selector("input[type='file']").send_keys(path)
    sleep(0.25)
    # waiting for the element to load
    while (True):
        try:
            sleep(0.5)
            driver.find_element_by_css_selector("span[data-icon='send-light']").click()
            break
        except:
            ...
    
    #driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/span/di/v/span/div/div/div[2]/span[2]/div/div').click()
    # //*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span[2]/div/div
    # //*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span[2]/div/div/span
    #app > div > div > div.MZIyP > div._3q4NP._1Iexl > span > div > span > div > div > div._2sNbV._3ySAH > span:nth-child(3) > div > div > span
    #app > div > div > div.MZIyP > div._3q4NP._1Iexl > span > div > span > div > div > div._2sNbV._3ySAH > span:nth-child(3) > div > div > span
    sleep(0.25)



threadFun()
print ("started")
print (replyOnlyList)
# startAssistant()