## SMS Web browsing
import numpy as np
import time
import math
import random
import requests
from PIL import Image
import sys
from flask import Flask, render_template, request
import base64
from bs4 import BeautifulSoup
from urllib.request import urlopen
from PIL import Image
from io import BytesIO
import urllib.parse as urlparse
import zlib

from twilio.twiml.messaging_response import MessagingResponse
import os
from twilio.rest import Client
import re
headers_mobile = { 'User-Agent' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1'}

suffs = [".com", ".net", ".org", ".gov", ".info", ".io"]
chars = [c for c in "abcdefghijklmnopqrstuvwxyz0123456789"]
types = ["jpeg", "png", "tiff", "gif", "svg", "bmp"]

app = Flask(__name__)

cwd = "/home/turnips343/server"

account_sid = 'ACe060c1c4da2bec3b9a641416e8b018ac'
auth_token = 'f4bea2596471370d71c1544c1b6351f6'
client = Client(account_sid, auth_token)

def is_url(string): 
    # findall() has been used  
    # with valid conditions for urls in string 
    if "http" in string: return True
    for i in suffs:
        if i in string:
            return True

    return False

def parse_img(source,url):
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
        imgFmt = image_tag.get(srcTag) #formatted image
        print(imgFmt + " IMGFMT")
        if len(imgFmt) == 0:
            continue
        ##print(imgFmt)
        if type(imgFmt) is str:
            if not imgFmt.find("data:image") >= 0: #if already in base 64
                flag = False
                for i in suffs:
                    if i in imgFmt:
                        flag = True
                if flag:
                    hostname = urlparse.urlparse(imgFmt).hostname
                    indexHost = imgFmt.find(hostname)
                    imgFmt = "http://" + imgFmt[indexHost:]
                else:
                    flag2 = True
                    while flag2:
                        if imgFmt[0] not in chars:
                            imgFmt= imgFmt[1:]
                        else:
                            flag2 = False

                    imgFmt = url + "/" + imgFmt
                print(imgFmt + " WIUFHEFIUHEFIUHE")
                imageType = ""
                for i in types:
                    if i in imgFmt:
                        imageType = i
                if imageType == "":
                    imageType = "jpg"

                #formatting into base64
                response = requests.get(imgFmt)
                img = BytesIO(response.content)
                
                #encode in base64
                result = str(base64.b64encode(img.getvalue()))
                #result = "yeet"
                #print(imageType)
                result = "data:image/" + imageType + ";base64," +result[2:len(result)-1]
            ##imgs.append(result)
            print(imgFmt)
            image_tag[srcTag] = result
            ##print(image_tag[srcTag])
    ##print(imgs)
    ###print(source)
    return str(soup)

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


@app.route('/')
def show_index():
    return render_template("index.html")

@app.route("/sms", methods=['GET','POST'])
def sms_reply():
    ## this is when you receive a message
    print("FORM",request.form)
    url = request.form['Body']

    if "about:blank" in url:
        print("ABOUTBLANKHIT")
        return "ABOUTBLANK"
    if not is_url(url):
        url = "https://www.google.com/search?q=" + url.replace(" ", "+")

    print(url + " URL")
    html = getHTML(url)
    #newhtml = parse_img(html, url)
    newhtml = html
    print(sys.getsizeof(newhtml), sys.getsizeof(html))
    html = parse_hrefs(newhtml,url)
    ##html = newhtml
    print("got html")
    filename = str(random.randrange(1000000, 9999999, 1))
    ## imgL,imgW = html_to_img(html, cwd + "/static/{}.png".format(filename))
    images = []
    slices = int(len(html)/(450*1350))
    print(slices,"SLICES")
    if slices == 0:
        html = "10MULT" + html
        html_to_img(html,"{}.png".format(filename))
    else:    
        for i in range(slices):
            filename = "{}.png".format(str(random.randrange(1000000, 9999999, 1)))
            ##html = "{}{}MULT".format(slices,i) + html
            cropamt = 350*1350
            if len(html) < cropamt:
                cropamt = len(html)
            print(html[0:6], "HTMLFIRRS6")

            html_to_img("{}{}MULT".format(slices,i) + html[cropamt:], filename)
            html = html[cropamt:]
            images.append(filename)


    print("SAVED IMAGE")
    if not images == []:
        for fn in images:
            message = client.messages \
                    .create(
                        from_='+12019322527',
                        media_url=['http://35.245.241.8:5000/static/{}'.format(fn)],
                        to='7329564059'
                    )
            print("sent img")
    else:
        message = client.messages \
                    .create(
                        from_='+12019322527',
                        media_url=['http://35.245.241.8:5000/static/{}.png'.format(filename)],
                        to='7329564059'
                    )
        print("sent image")

    return("test")

def getHTML(url):
    return (requests.get(url,headers=headers_mobile).text)

def img_to_html(img_name, write = True):
    im = Image.open(img_name)
    readdata = list(im.getdata())
    print ((0,0,0) in readdata)
    newhtml = ""
    for rgb in readdata:
        for char in rgb: 
            if char != 0: ## 0 is null in ascii
                newhtml += chr(char)

    if write:
        with open("test123.html","w") as infile:
            infile.write(newhtml)

    return newhtml

def html_to_img(html, path):
    ## converts html string into rgb matrix then saves as image
    size = math.ceil(math.sqrt(len(html)))+1

    l,w = size, \
        size - (size%3) ## make it a multiple of 3 for easy splitting

    imgdata = np.zeros([l*w], dtype = np.uint8) 
    print(l,w,len(html))
    print(len(imgdata.tolist()))
    for x in range(len(html)):
        imgdata[x] = ord(html[x])
    ##print(imgdata.tolist())
    print(len(imgdata) % 3)
    print(type(imgdata))
    imgdata = imgdata.reshape(-1,3)
    print(len(imgdata))
    size = math.ceil(math.sqrt(len(imgdata)))+1
    l,w = size, \
        size - (size%3) ## make it a multiple of 3 for easy splitting

    newimg = []
    print(len(imgdata))

    for y in range(l):
        temp = []
        for x in range(w):
            ##print(temp, imgdata[x].tolist())
            if x+((y*w)-1) >= len(imgdata):
                temp.append(np.array([0,0,0], dtype = np.uint8))
                continue
            ##print(x,y,l,w,x+((y*w)-1), len(imgdata))
            temp.append(imgdata[x+((y*w)-1)])
        ##print(temp,"\n\n")
        newimg.append(temp)

    print(len(newimg), len(newimg[0]))

    

    img = Image.fromarray(np.array(newimg)).convert("RGB")
    print(path + "PATHPATHPATH")
    img.save(cwd+"/static/"+path)
    return l,w

def chunks(l, n):
    temp = np.array_split(l,n)
    for i in range(n-len(temp[-1])):
        temp[-1] = np.append(temp[-1], 0.0)
    return np.array(temp, dtype=np.uint8)
"""
start = time.time()

html = ""
with open("input.txt", encoding = 'utf-8') as infile:
    html = infile.read() 

html_to_img(html, "/static/")
test = img_to_html("html.png", True)
##print(test)

end = time.time()
print(end-start)
"""

if __name__ == "__main__":
    import os
    import glob

    files = glob.glob(cwd + "/static/*")
    for f in files:
        os.remove(f)
    app.run(host='0.0.0.0')

##html = img_to_html("small.png",write=True)
