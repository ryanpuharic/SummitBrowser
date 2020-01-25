import requests
import base64
from bs4 import BeautifulSoup
from urllib.request import urlopen
from PIL import Image
from io import BytesIO
import urllib.parse as urlparse
suffs = [".com", ".net", "org", ".gov", ".co.uk"]
chars = [c for c in "abcdefghijklmnopqrstuvwxyz0123456789"]

def getHTML(url):
    return (requests.get(url).text)

def parse(source, url):
    # get soup
    soup = BeautifulSoup(source,'html.parser') 
    # find the tag : <img ... >
    image_tags = soup.findAll('img')
    # print out image urls
    imgs = []
    for image_tag in image_tags:
        ##print((image_tag))
        tags = list(image_tag.attrs)
        srcTag = sorted([x for x in tags if "src" in x], key = len)[0]
        ##print(srcTag)
        imgFmt = image_tag.get('src') #img urls

        


url = 'http://www.frhsd.com/'
content = getHTML(url)
parse(content, url)