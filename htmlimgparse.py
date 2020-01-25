import bs4 as bs
import urllib.request
def parse(source):
    soup = bs.BeautifulSoup(source,'html')
    print(soup.title)

html = ""
with open('inputcnn.txt', encoding = "utf-8") as infile:
    html = infile.read()
parse(html)
