from collections import OrderedDict
import json
from firebaseDB.app import DATABASE
from flask import *
from pcDealBot import run

app = Flask(__name__)

def filter_db(name, alert=True, part=True):
    deals = DATABASE.child("Deals").get()
    deals_dict = deals.val()
    filtered_dict = {}
    for key, value in deals_dict.items():
        query = False
        try:
            if name in value['part'].lower():
                query = True
            elif name in value['seller'].lower():
                query = True
            elif name == 'all':
                query = True
            elif name == 'alert' and value['alert']:
                query = True
            elif name in value['name']:
                query = True
        except:
            pass
        if query:
            filtered_dict[key] = value
    sorted_db = OrderedDict(sorted(
        filtered_dict.items(), 
        key=lambda x: x[1]['date'],
        reverse=True,
        ))
    return sorted_db

@app.route('/', methods=['GET', 'POST'])
def basic():
    if request.method == 'POST':
        if 'alert' in request.form:
            db = filter_db('all')
            sorted_db = OrderedDict(sorted(
                db.items(), 
                key=lambda x: x[1]['alert'],
                reverse=True,
                )
            )
            return render_template(
                'index.html', 
                t=sorted_db.values()
                )
        elif 'date' in request.form:
            db = filter_db('all')
            sorted_db = OrderedDict(sorted(
                db.items(), 
                key=lambda x: x[1]['date'],
                reverse=True,
                )
            )
            return render_template(
                'index.html', 
                t=sorted_db.values()
                )
        elif 'part' in request.form:
            db = filter_db('all')
            sorted_db = OrderedDict(sorted(
                db.items(), 
                key=lambda x: (x[1]['date'], x[1]['part']),
                reverse=True,
                )
            )
            return render_template(
                'index.html', 
                t=sorted_db.values()
                )
        else:
            name = request.form['name']
            return render_template(
                'index.html', 
                t=filter_db(name).values())

    return render_template(
        'index.html', 
        t = filter_db('all').values()
        )

if __name__ == '__main__':
    app.run(debug=True)