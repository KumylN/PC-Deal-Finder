from collections import OrderedDict
import json
from firebaseDB.app import DATABASE
from flask import *

app = Flask(__name__)

def filter_db(name, db):
    ret = {}
    for key in db:
        if name.lower() in (str(db[key]['name']).lower() + str(db[key]['part']).lower()):# + db[key]['seller'].lower()):
            ret[key] = db[key]
    return ret


@app.route('/searchResults')
def searchResults():
    part = request.args.get('part')

    deals = DATABASE.child("Deals").get()
    deals_newegg = DATABASE.child("NewEggDeals").get()

    deals_dict = deals.val()
    deals_dict.update(deals_newegg.val())

    # return render_template('index.html', t = deals_dict.values())
    return render_template('index.html', t = filter_db(part, deals_dict).values())

@app.route('/', methods=['GET', 'POST'])
def basic():
    if request.method == 'POST':
        if request.form['Part'] != '':
            return redirect(url_for('searchResults', part=request.form["Part"]))
    return render_template('frontPage.html')

if __name__ == '__main__':
    app.run(debug=True)