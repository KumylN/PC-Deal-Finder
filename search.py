from collections import OrderedDict
import json
from firebaseDB.app import DATABASE
from flask import *
from pcDealBot import run

app = Flask(__name__)

def filter_db(name):
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
        except:
            pass
        if query:
            filtered_dict[key] = value
    return filtered_dict

@app.route('/', methods=['GET', 'POST'])
def basic():
    if request.method == 'POST':
        if "refresh" in request.form:
            run()
            return render_template(
                'index.html', 
                t=filter_db('all').values()
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
        elif 'alert' in request.form:
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
        elif 'part' in request.form:
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
        else:
            name = request.form['name']
            return render_template(
                'index.html', 
                t=filter_db(name).values())
    deals_dict = DATABASE.child("Deals").get().val()

    return render_template(
        'index.html', 
        t = filter_db('all').values()
        )

if __name__ == '__main__':
    app.run(debug=True)