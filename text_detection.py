import cv2
from imageai.Detection import ObjectDetection
from moviepy.editor import VideoFileClip
import os
from PIL import Image
import pytesseract

proxy = 'http://172.31.2.4:8080'

os.environ['http_proxy'] = proxy 
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy

def image_text(path):
    text = pytesseract.image_to_string(Image.open(path), lang = "eng")
    print(text.lower())

image_text('image.jpeg')
#--proxy="https://edcguest:edcguest@172.31.100.29:3128"
