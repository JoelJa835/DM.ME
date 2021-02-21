#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup



try:
    html_text = requests.get('https://www.skroutz.gr/c/55/kartes-grafikwn-vga.html?o=gpu').text
except requests.exceptions.HTTPError as errh:
    print ("Http Error:",errh)
except requests.exceptions.ConnectionError as errc:
    print ("Error Connecting:",errc)
except requests.exceptions.Timeout as errt:
    print ("Timeout Error:",errt)
except requests.exceptions.RequestException as err:
    print ("OOps: Something Else",err)
else:
    soup = BeautifulSoup(html_text, 'lxml')
    gpus = soup.findAll('li', class_ = 'cf card')
    for gpu in gpus:
        gpu_content = gpu.find('div', class_ = 'card-content')
        gpu_title = gpu_content.find('a', class_ = 'js-sku-link').get('title')
        gpu_price = gpu_content.find('a',class_ = 'js-sku-link sku-link').text.replace('από','')
        print(f'{gpu_title} costs {gpu_price}')

