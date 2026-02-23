import sys
import re
import requests
from bs4 import BeautifulSoup


def get_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        r = requests.get(url, headers=headers)
    except:
        print("url not opening")
        sys.exit(1)

    soup = BeautifulSoup(r.text, "html.parser")

    # extracting the title of the web page
    title = ""
    if soup.title:
        title = soup.title.string

    
    for item in soup(["script", "style"]):
        item.extract()

    #extracting the body text of web page 
    text = soup.get_text()
    

    # storing all the linkes present in the web page
    links = []
    for a in soup.find_all("a"):
        link = a.get("href")
        if link:
            links.append(link)
    return title, text, links




if len(sys.argv) < 2:
    print("URL not provided")
    sys.exit(1)

url = sys.argv[1]

title, text, links = get_data(url)

print("\nTITLE OF THE PAGE ------->")
print( title)
print("\nBODY OF THE PAGE----->   ")
print(text)

print("\nLINKS PRESENT IN THE PAGE----->  ")
for l in links:
    print(l)


