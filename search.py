from collections import OrderedDict
import json
from firebaseDB.app import DATABASE
from flask import *

app = Flask(__name__)

# def filter_db(name, alert=True, part=True):
#     deals = DATABASE.child("Deals").get()
#     deals_newegg = DATABASE.child("NewEggDeals").get()
#     deals_dict = deals.val()
#     deals_dict.update(deals_newegg.val())
#     filtered_dict = {}
#     i = 0
#     for key, value in deals_dict.items():
#         query = False
#         # import pdb; pdb.set_trace()
#         try:
#             if name in value['part'].lower():
#                 query = True
#             elif name in value['seller'].lower():
#                 query = True
#             elif name == 'all':
#                 query = True
#             elif name == 'alert' and value['alert']:
#                 query = True
#             elif name in key.lower():
#                 query = True
#             elif name in value['name'].lower():
#                 query = True
#         except:
#             pass
#         if query:
#             filtered_dict[key] = value
#         i+= 1
#         if i == 50:
#             break
#     sorted_db = OrderedDict(sorted(
#         filtered_dict.items(), 
#         key=lambda x: x[1]['date'],
#         reverse=True,
#         ))
#     return sorted_db

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


# @app.route('/', methods=['GET', 'POST'])
# def basic():
#     if request.method == 'POST':
#         if 'alert' in request.form:
#             db = filter_db('all')
#             sorted_db = OrderedDict(sorted(
#                 db.items(), 
#                 key=lambda x: x[1]['alert'],
#                 reverse=True,
#                 )
#             )
#             return render_template(
#                 'index.html', 
#                 t=sorted_db.values()
#                 )
#         elif 'date' in request.form:
#             db = filter_db('all')
#             sorted_db = OrderedDict(sorted(
#                 db.items(), 
#                 key=lambda x: x[1]['date'],
#                 reverse=True,
#                 )
#             )
#             return render_template(
#                 'index.html', 
#                 t=sorted_db.values()
#                 )
#         elif 'part' in request.form:
#             db = filter_db('all')
#             sorted_db = OrderedDict(sorted(
#                 db.items(), 
#                 key=lambda x: (x[1]['part'], x[1]['date']),
#                 reverse=True,
#                 )
#             )
#             return render_template(
#                 'index.html', 
#                 t=sorted_db.values()
#                 )
#         else:
#             name = request.form['name']
#             return render_template(
#                 'index.html', 
#                 t=filter_db(name).values())

#     return render_template(
#         'index.html', 
#         t = filter_db('all').values()
#         )

if __name__ == '__main__':
    app.run(debug=True)