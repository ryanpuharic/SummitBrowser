## SMS Web browsing
import numpy as np
import time
import math
from PIL import Image


def flatten(readin):
    new_list = []
    for i in range(len(readin)):
        new_list.append(readin[i][0])
    return new_list

def img_to_html(img_name, write = True):
    im = Image.open(img_name)
    readdata = list(im.getdata())
    readdata = flatten(readdata)

    newhtml = ""

    for char in readdata:
        if char != 0: ## 0 is unknown in ascii
            newhtml += chr(char)

    if write:
        with open("test.html","w") as infile:
            infile.write(newhtml)

    return newhtml

def html_to_img(html):
    ## converts html string into grayscale matrix then saves as image
    l,w = math.ceil(math.sqrt(len(html)))+1, math.ceil(math.sqrt(len(html)))+1
    imgdata = np.zeros([l, w], dtype = int) 
    print(l,w,len(html))
    row = 0
    for col in range(len(html)):
        if col % l-1 == 0 and col != 0:
            row += 1
        imgdata[row][col % l-1] = ord(html[col])    
        ##print(row,col,"===",html[col],ord(html[col]))
    img = Image.fromarray(imgdata).convert("RGB")
    img.save('html.png')



start = time.time()

html = ""
with open("input.txt", encoding = 'utf-8') as infile:
    html = infile.read() 

html_to_img(html)
test = img_to_html("html.png", True)


end = time.time()
print(end-start)
