import datetime
import praw
import json
import sys

from detector import detect_deal, jsonify_title
from firebaseDB.app import DATABASE

file_p = open("pwd.txt")

# reddit login

reddit = praw.Reddit(
    client_id='GVnA-Hvi9sw4Ig',
    client_secret='EN-ai10yYkEncqY3D9fCbVawVv0',
    username='bapcbotdeals',
    password=open("pwd.txt").read(),
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

def run(alert_price=75):
    deals_list = find_deals(alert_price=75)
    deal_keys = deals_list[0].keys()

    for deal in deals_list:
        try:
            for key in deal_keys:
                DATABASE.child("Deals").child(jsonify_title(deal['name'])).update({key: deal[key]})
        except:
            pass

if __name__ == "__main__":
    run()