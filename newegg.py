from bs4 import BeautifulSoup 
import requests
import uuid
from datetime import date

standard_url = 'https://www.newegg.ca/p/pl?Submit=StoreIM&Depa=1&Category={}&PageSize=96'

part_keys = {
    "cpu": "34",
    "ram": "17",
    "motherboard": "20",
    "gpu": "38",
    "case": "9",
    "psu": "32",
    "fans": "11",
    "ssd": "119",
    "hdd": "15"
}

today = date.today().strftime("%B %d, %Y")

def parse(part_type, DEBUG=False):
    page_num = 1
    items_list = []
    error = None
    while True:
        response = requests.get(standard_url.format(part_keys[part_type.lower()]) + "&page=" + str(page_num))
        soup = BeautifulSoup(response.text, 'html.parser')
        if soup.find("span", "result-message-error") is not None:
            break
        items_list += soup.find_all("div", "item-container")
        page_num += 1
        if DEBUG:
            print("SELECTING NEXT PAGE! :" + str(page_num))
    ret = []
    for item in items_list:
        unique_hash = str(uuid.uuid4())
        flair = item.find("p", "item-promo").text
        if "out of stock" in flair.lower():
            continue
        part = {}
        part['part'] = part_type
        part['price'] = (
            item.find("li", "price-current").find("strong").text + 
            item.find("li", "price-current").find("sup").text
            )
        part['name'] = item.find("a", "item-title").text
        part['url'] = item.find("a", "item-title").attrs['href']
        part['seller'] = "Newegg"
        part['flair'] = flair
        part['uuid'] = "NEWEGGPART" + str(unique_hash)
        part['alert'] = "false"
        part['date'] = today
        ret.append(part)
        if DEBUG:
            print("APPENDING PART")
    
    if DEBUG:
        print("PARSING COMPLETE RETURNING... PART:" + part_type)
    return ret

parts = part_keys.keys()

def getNewEggList(DEBUG=False):
    ret = []
    for part in parts:
        ret += parse(part, DEBUG=DEBUG)
    return ret
