import requests
import base64
from bs4 import BeautifulSoup
from urllib.request import urlopen
from PIL import Image
from io import BytesIO
import urllib.parse as urlparse
import re
suffs = [".com", ".net", ".org", ".gov", ".info", ".io"]
chars = [c for c in "abcdefghijklmnopqrstuvwxyz0123456789"]
types = ["jpeg", "png", "tiff", "gif", "svg", "bmp"]

headers_mobile = { 'User-Agent' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1'}


def is_url(string): 
    # findall() has been used  
    # with valid conditions for urls in string 
    if "http" in string: return True
    for i in suffs:
        if i in string:
            return True

    return False

def getHTML(url):
    return (requests.get(url,headers=headers_mobile).text)


def parse_hrefs(source,url):
    soup = BeautifulSoup(source,'html.parser') 
    # find the tag : <img ... >

    for tag in soup.find_all():
        if "href" in tag.attrs: ## all tags with href
            href = tag.attrs['href']
            #print(href,"HREF")
            if is_url(href) or href == "#": continue
            
            else:  
                ##print("HIT", href)
                hostname = urlparse.urlparse(url).hostname
                #print(hostname,"HOSTNAME",href,"HREF")
                href = "http://" + hostname + href
            tag.attrs['href'] = href
    return str(soup)





url = "https://www.espn.com"
html = getHTML(url)
##print(html)
with open('test.html',"w") as outfile:
    outfile.write(html)
print(parse_hrefs(html,url))
##print(is_url("https://stackoverflow.com/questions/4989182/converting-java-bitmap-to-byte-array"))
##print(is_url("/feeds/question/4989182"))