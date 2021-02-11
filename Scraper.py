#!/usr/bin/python3

from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup

try:
    html = urlopen("https://www.skroutz.gr/s/25999039/Gigabyte-RTX-3060-Ti-Gaming-OC-8GB-GV-N306TGAMING-OC-8GD.html")
except HTTPError as e:
    print(e)
except URLError as e:
    print("The server could not be found!")
else:
    bsobj = BeautifulSoup(html, 'lxml')
    gpu = bsobj.findAll()
    print(gpu)

