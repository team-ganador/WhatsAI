

from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
import time 
from time import sleep
import random
from pathlib import Path
from threading import Thread
from time import sleep
import utility

DRIVER_PATH = '/home/shreyasus/Downloads/chromedriver'
URL = 'https://web.whatsapp.com/'

CHAT_COUNT = 25
MESSAGE_COUNT = 50

driver = webdriver.Chrome(DRIVER_PATH) 
driver.get(URL)                       

wait = WebDriverWait(driver, 600) 

# //*[@id="main"]/div[3]/div/div/div[3]/div[18]/div/div
# driver.find_element_by_xpath('//*[@id="pane-side"]/div/div/div/div['+str(i)+']')

voteMap = {}
startMessage = 'Oye Aayush tu Bunk likh group pe'
startFlag=False
for i in range (1,MESSAGE_COUNT):
    try :
        msg = driver.find_element_by_xpath('//*[@id="main"]/div[3]/div/div/div[3]/div['+str(i)+']/div/div').text.split('\n')
        if (msg[0]==startMessage):          #//*[@id="main"]/div[3]/div/div/div[3]/div[21]/div/div/div[1]/div
            startFlag=True
        msgLen = len(msg)
        if (msgLen>2):
            if (startFlag):
                print(msg[0],' -> ',msg[msgLen-2])
                voteMap[msg[0]]=msg[msgLen-2]
    except:
        ...
    driver.find_element_by_css_selector

voteCount = {}
for key,value in voteMap.items():
    print(key,' = > ',value)
    if (value in voteCount):
        voteCount[value]=voteCount[value]+1
    else:
        voteCount[value]=1

print (voteCount)
    
    
# //*[@id="main"]/div[3]/div/div/div[3]/div[21]/div/div/div[1]/div          gives the message     
# //*[@id="main"]/div[3]/div/div/div[3]/div[21]/div/div                     gives the list of all labels
# //*[@id="main"]/div[3]/div/div/div[3]/div[21]/div/div/div[1]/div/span     gives the message
# //*[@id="main"]/div[3]/div/div/div[3]/div[20]/div/div[1]/a/div[2]/div[3]/span download button


for i in range (1,MESSAGE_COUNT):
    try :
        # print (i)
        labels = driver.find_element_by_xpath('//*[@id="main"]/div[3]/div/div/div[3]/div['+str(i)+']/div/div').text.split('\n')
        isPDF = False
        pdfName = ''
        # print ('valid')
        for label in labels:
            isPDF = isPDF or ('pagesPDF' in label)
        if (isPDF):
            print ('PDF detected')
            print (labels)
            downloadBtn = driver.find_element_by_xpath('//*[@id="main"]/div[3]/div/div/div[3]/div['+str(i)+']/div/div[1]/a/div[2]/div[3]/span')
            # check need to download
            downloadReq = True
            for label in labels:
                chk = utility.checkAlreadyExistingFile(label+'.pdf')
                if (chk):
                    pdfName = label+'.pdf'
                    downloadReq = False
                    break

            if (downloadReq):
                downloadBtn.click()
                break
                # TODO Start a thread to check when download of PDF is completed by using labels
            else:
                print (pdfName,'Already downloaded')
            
    except:
        ...
        

for i in range (1,MESSAGE_COUNT):
     try :
             labels = driver.find_element_by_xpath('//*[@id="main"]/div[3]/div/div/div[3]/div['+str(i)+']/div/div').text.split('\n')
             isPDF = False
             pdfName = ''
             for label in labels:
                     isPDF = isPDF or ('pagesPDF' in label)
             if (isPDF):
                     print ('PDF Detected')
                     print (labels)
                     downloadBtn = driver.find_element_by_xpath('//*[@id="main"]/div[3]/div/div/div[3]/div['+str(i)+']/div/div[1]/a/div[2]/div[3]/span')
                     downloadReq = True
                     for label in labels:
                             chk = utility.checkAlreadyExistingFile(label+'.pdf')
                             if (chk):
                                     pdfName = label+'.pdf'
                                     downloadReq = False
                                     break
                     if (downloadReq):
                             downloadBtn.click()
                             break
                     else:
                             print (pdfName,'Already downloaded')
     except:
             ...

list = ['You', 'acadcal_2018_19 ', 'Dekh ispe nhi aaya', '18:25']
for i in list:
    if ('•' in i and 'pages' in i):
        print ('PDF Detected')


 driver.find_element_by_css_selector("input[type='file']").send_keys('/home/shreyasus/Downloads/icon.png')

 driver.find_element_by_css_selector("span[data-icon='send-light']").click()


driver.find_element_by_css_selector("span[data-icon='clip']").click()
driver.find_element_by_css_selector("input[type='file']").send_keys('/home/shreyasus/Downloads/icon.png')
driver.find_element_by_css_selector("span[data-icon='send-light']").click()