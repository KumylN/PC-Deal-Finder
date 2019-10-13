import datetime
import praw
import json
import sys
import time

from detector import detect_deal, jsonify_title
from newegg import getNewEggList
from firebaseDB.app import DATABASE

file_p = open("pwd.txt")

# reddit login

reddit = praw.Reddit(
    client_id='GVnA-Hvi9sw4Ig',
    client_secret='EN-ai10yYkEncqY3D9fCbVawVv0',
    username='bapcbotdeals',
    password=open("pwd.txt").read().splitlines()[0],
    user_agent='bapc_bot')


def determine_to_include(deal):
    text = deal.link_flair_text
    if text:
        if text.lower() == 'expired':
            return False
        elif text.lower() == 'oos':
            return False
        elif text.lower() == 'out of stock':
            return False
        elif text.lower() == 'outofstock':
            return False
    name = deal.title.lower()
    if 'daily thread' in name:
        return False
    return True

def find_deals(alert_price=75, key_word=''):
    subreddit = reddit.subreddit('bapcsalescanada')
    submissions = list(subreddit.new())
    deals_list = []
    for i in range(len(submissions)):
        include_deal = determine_to_include(submissions[i]) 
        if not include_deal:
            continue
        deals_list.append(detect_deal(submissions[i], alert_price, key_word))
    return deals_list

def buffer(buffer_time, alert):
    time.sleep(600)
    if (buffer_time == 15):
        DATABASE.child("Deals").remove()
        buffer_time = 0
    else:
        run()
    buffer(buffer_time + 1, alert)

def run(alert_price=75):
    # REDDIT
    deals_list = find_deals(alert_price=75)
    deal_keys = deals_list[0].keys()

    for deal in deals_list:
        try:
            for key in deal_keys:
                DATABASE.child("Deals").child(jsonify_title(deal['name'])).update({key: deal[key]})
        except:
            pass
    
    # NEWEGG
    newEgg_list = getNewEggList(DEBUG=True)
    newEgg_keys = newEgg_list[0].keys()
    for part in newEgg_list:
        try:
            for key in newEgg_keys:
                DATABASE.child("NewEggDeals").child((part['uuid'])).update({key: part[key]})
            print ("ADDED PART")
        except:
            pass
    

if __name__ == "__main__":
    alert = 75
    if len(sys.argv) == 1:
        run()
    else:
        for i in range(len(sys.argv)):
            if sys.argv[i] == "--alert":
                if (i + 1 == len(sys.argv)):
                    print("ERROR: Expected alert votes after --alert option")
                    exit()
                alert = sys.argv[i + 1]
            elif sys.argv[i] == "--destroy":
                DATABASE.child("Deals").remove()
                DATABASE.child("NewEggDeals").remove()
    if "--buffer" in sys.argv:
        buffer(0, alert)
    else:
        run(alert)

