
from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
import time 
from time import sleep
import paths

USER = paths.USER


DRIVER_PATH = '/home/'+USER+'/Downloads/chromedriver' 
URL = 'file:///home/'+USER+'/Desktop/HINT4/chatbot.html' 
COMMAND_STOP = 'stop'
driver = webdriver.Chrome(DRIVER_PATH) 
driver.get(URL)                              

wait = WebDriverWait(driver, 600) 

driver.switch_to.frame(driver.find_element_by_tag_name("iframe")) 

txtBox = driver.find_element_by_xpath('//*[@id="query"]') 

def getResponse(message): 
    waitPlaceHolder = '...'
    msgXPath = '//*[@id="result"]'
    txtBox.send_keys(message+"\n")
    num = len(driver.find_element_by_xpath(msgXPath).text.split('\n'))
    respXPath = msgXPath+'/div['+str(num)+']'
    while (driver.find_element_by_xpath(respXPath).text == waitPlaceHolder):
        sleep(0.01)
    return driver.find_element_by_xpath(respXPath).text

def startChat():
    while True:
        message = input('>> ')
        if (message == COMMAND_STOP):
            break
        response = getResponse(message)
        print (response)
    print ('Bot shutting down')

#startChat()
