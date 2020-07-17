import requests
from bs4 import BeautifulSoup


def get_url_img(url):
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    print(soup)
    img_url = soup.find('span',{'class':'bg_present'})
    print(img_url)
