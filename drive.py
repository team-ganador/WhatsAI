import os
proxy = 'http://172.31.2.4:8080'

os.environ['http_proxy'] = proxy 
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy

def uploadDrive(path):
    os.system('gdrive upload ' + path)

# uploadDrive('/home/shreyasus/Desktop/Ganador')