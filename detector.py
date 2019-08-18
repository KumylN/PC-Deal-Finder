import copy
import re
import datetime
import uuid


TEN_DIGITS = '0123456789'

def detect_part(deal):
    if 'prebuilt' in deal:
        return 'PREBUILT'
    elif 'gpu' in deal:
        return 'GPU'
    elif 'cpu' in deal:
        return 'CPU'
    elif 'psu' in deal:
        return 'PSU'
    elif 'hdd' in deal:
        return 'HDD'
    elif 'ssd' in deal:
        return 'SSD'
    elif 'ram' in deal:
        return 'RAM',
    elif 'mobo' in deal:
        return 'MOBO'
    elif 'nvme' in deal:
        return 'NVMe'
    elif 'case' in deal:
        return 'Case'
    elif 'monitor' in deal:
        return 'Monitor'
    elif 'audio' in deal:
        return 'Audio'
    elif 'coupons' in deal:
        return 'Coupons'
    elif 'keyboard' in deal:
        return 'Keyboard'
    elif 'mouse' in deal:
        return 'Mouse'
    else:
        return False

def detect_seller(deal):
    if 'newegg' in deal:
        return 'NewEgg'
    elif 'cc' in deal:
        return 'CC'
    elif 'amazon' in deal:
        return 'Amazon'
    elif 'banggood' in deal:
        return 'Banggood'
    elif 'staples' in deal:
        return 'Staples'
    elif 'canada computers' in deal:
        return 'CC'
    elif 'memory express' in deal:
        return 'Memory Express'
    elif 'bestbuy' in deal:
        return 'Bestbuy'
    elif 'primecables' in deal:
        return 'PrimeCables'
    elif 'source' in deal:
        return 'Source'
    elif 'pccanada' in deal or 'pc-canada' in deal:
        return 'PC-Canada'
    elif 'dell' in deal:
        return 'Dell'
    elif 'microsoft' in deal:
        return 'Microsoft'
    elif 'razer' in deal:
        return 'Razer'
    elif 'mike' in deal:
        return 'mike'
    else:
        False

def detect_price(deal):

    def reverse_catch_price(cur_deal):
        reverse_factor = 1
        price = ''
        while (cur_deal[len(cur_deal) - reverse_factor] in (TEN_DIGITS + ',.')):
            price = cur_deal[len(cur_deal) - reverse_factor] + price
            reverse_factor += 1
        return price

    def parse_price(latest_price, price):
        decimal = False
        for i in range(0, len(latest_price)) :
            val = latest_price[i]
            if val in TEN_DIGITS:
                price += val
            elif val == ',':
                continue
            elif val == '.':
                if (i + 1 <= len(latest_price)) and latest_price[i+1] in TEN_DIGITS:
                    decimal = True
                    price += val
                else:
                    break
            else:
                break
        if not price:
            price = '0'
        if not decimal:
            price += '.00'
        return price

    if '$' not in deal:
        modified_title = copy.deepcopy(deal)
        while (modified_title[-1] not in TEN_DIGITS):
            modified_title = modified_title[:-1]
            if len(modified_title) == 0:
                return 0
        latest_price = reverse_catch_price(modified_title)
        price = ''
        return parse_price(latest_price, price)


    split_deal = deal.split('$')
    last_val = -1
    latest_price = split_deal[last_val]
    price = ''
    list_of_digits = list(TEN_DIGITS)
    while not [i for i in list_of_digits if i in split_deal[last_val]]:
        last_val -= 1
        if last_val + len(split_deal) < 0:
            return 0
        if not [i for i in list_of_digits if i in split_deal[last_val]]:
            continue
        latest_price = reverse_catch_price(split_deal[last_val])
        price = ''
        break
    
    return parse_price(latest_price, price)

def get_date(submission):
    time = submission.created
    return datetime.datetime.fromtimestamp(time)

def jsonify_title(title):
    title_list = list(title)
    lenght_of_list = len(title_list)
    for i in range(0, lenght_of_list):
        if title_list[i] == '[':
            title_list[i] = '('
        elif title_list[i] == ']':
            title_list[i] = ')'
        elif title_list[i] == '$':
            title_list[i] = ''
        elif title_list[i] == '.':
            title_list[i] = ''
        elif title_list[i] == "%":
            title_list[i] = ''
    return ''.join(title_list)

def fix_text(title):
    if not title:
        return ""
    wip_title = title.replace("/", "")
    wip_title = wip_title.replace("\\", "")
    wip_title = wip_title.replace("\"", "")
    return wip_title

def detect_deal(deal_obj, alert_factor=75, key_word=''):   
    deal = fix_text(deal_obj.title)
    deal_lower = deal.lower()

    part = detect_part(deal_lower)
    seller = detect_seller(deal_lower)
    alert = "false"
    if 'price error' in deal or 'priceerror' in deal:
        alert = "true"
    elif deal_obj.ups > alert_factor:
        alert = "true"
    elif key_word and key_word in deal_obj.title:
        alert = "true"
    price = detect_price(deal_lower)
    date = get_date(deal_obj)
    return {
        'name': deal,
        'part': part,
        'seller': seller,
        'alert': alert,
        'price': price,
        'url': deal_obj.url,
        'date': str(date),
        'flair': fix_text(deal_obj.link_flair_text),
        'upvotes': deal_obj.ups,
        'uuid': str(uuid.uuid4()),
        }
    
    
    
