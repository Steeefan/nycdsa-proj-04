from flask import Flask, render_template, request
import os
import mysql.connector
from mysql.connector import errorcode
import yaml
import pickle
import pandas as pd
import json
import content_helpers as hp
import sqlite3 as lite

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, 'templates')
app = Flask(__name__, template_folder=template_path)

cfg = yaml.safe_load(open('_inc.yaml'))


def sqlCon():
    try:
        cnx = mysql.connector.connect(user=cfg['mysql']['user'], password=cfg['mysql']['pwd'],
                                      host=cfg['mysql']['server'], database=cfg['mysql']['db'])
        return cnx
    except mysql.connector.Error as e:
        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            return "Something is wrong with your user name or password"
        elif e.errno == errorcode.ER_BAD_DB_ERROR:
            return "Database does not exist"
        else:
            return e


def mcImg(url):
    defaultImg = 'http://static.metacritic.com/images/products/games/98w-game.jpg'
    return defaultImg if url is None else url if url[-12:] == '98w-game.jpg' else \
        url.replace('-98.jpg', '.jpg').replace('.jpg', '-98.jpg')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/reco/content', methods=['GET', 'POST'])
def recoContent():
    if request.method == 'POST':
        item = int(request.form.get('item'))
        amount = int(request.form.get('amount'))
    elif request.method == 'GET':
        item = int(request.args.get('item'))
        amount = int(request.args.get('amount'))
    else:
        item = -1

    # Load pickle file with trained doc2vecs
    with open('models/summary_critics_docvecs.pickle', 'rb') as f:
        summary_critics_docvecs = pickle.load(f)

    # get recommendation
    recos = hp.content_recommend(item, amount, summary_critics_docvecs)
    ids = [x[0] for x in recos]
    recos = pd.DataFrame(sorted(recos, key=lambda x: x[1], reverse=True), columns=['uniqueID', 'cossim'])

    cnx = sqlCon()
    strSQL = 'SELECT uniqueID, name, "Game" AS itemType, image, link, system FROM tblGame WHERE uniqueID IN (' + ', '.join(str(x) for x in ids) + ')' \
             'UNION ' \
             'SELECT uniqueID, name, "Movie" AS itemType, image, link, "" AS system FROM tblMovie WHERE uniqueID IN (' + ', '.join(str(x) for x in ids) + ')' \
             'UNION ' \
             'SELECT uniqueID, name, "TV" AS itemType, image, link, "" AS system FROM tblTVShow WHERE uniqueID IN (' + ', '.join(str(x) for x in ids) + ')'

    recosInfo = pd.read_sql(strSQL, cnx)
    recos = recos.merge(recosInfo, how='left', on='uniqueID')
    cnx.close()

    reco = []
    [reco.append({
        'uniqueID': row['uniqueID'],
        'name': row['name'],
        'cossim': round(row['cossim']*100, 2),
        'itemType': row['itemType'] + ' (' + row['system'] + ')' if row['itemType'] == 'Game' else row['itemType'],
        'image': mcImg(row['image']),
        'link': row['link']
        }) for index, row in recos.iterrows()
    ]
    return json.dumps(reco)


@app.route('/getItemList', methods=['GET', 'POST'])
def getItemList():
    if request.method == 'POST':
        item = request.form.get('item')
    elif request.method == 'GET':
        item = request.args.get('item')
    else:
        item = ''

    #cnx = sqlCon()
    cnx = lite.connect(r'D:\capstone-v2.db')
    cur = cnx.cursor()

    whereClause = 'WHERE name LIKE "%' + item + '%" ' if item != '' else ''

    strSQL = '' \
            'SELECT ' \
                'uniqueID, ' \
                'name, ' \
                'image, ' \
                'system, ' \
                'itemType ' \
            'FROM ' \
                '(SELECT ' \
                    'uniqueID, ' \
                    'name, ' \
                    'image, ' \
                    'system, ' \
                    '"Game" AS itemType ' \
                'FROM ' \
                    'tblGame ' \
                    + whereClause + \
                '' \
                'UNION ' \
                '' \
                'SELECT ' \
                    'uniqueID, ' \
                    'name, ' \
                    'image, ' \
                    '"" AS system, ' \
                    '"Movie" AS itemType ' \
                'FROM ' \
                    'tblMovie ' \
                    + whereClause + \
                '' \
                'UNION ' \
                '' \
                'SELECT ' \
                    'uniqueID, ' \
                    'name, ' \
                    'image, ' \
                    '"" AS system, ' \
                    '"TV" AS itemType ' \
                'FROM ' \
                    'tblTVShow ' \
                    + whereClause + \
                ')'

    cur.execute(strSQL)

    items = []
    [items.append({
        'uniqueID': row[0],
        'name': row[1],
        'image': mcImg(row[2]),
        'system': row[3],
        'itemType': row[4]
        }) for row in cur
    ]

    cnx.close()

    return json.dumps(items)


@app.route('/getStats/<which>', methods=['GET', 'POST'])
def getStats(which):
    # cnx = sqlCon()
    cnx = lite.connect(r'D:\capstone-v2.db')
    cur = cnx.cursor()

    statsList = []

    if which == 'basic':
        games = next(cur.execute('SELECT COUNT(*) AS cnt FROM tblGame'))[0]
        movies = next(cur.execute('SELECT COUNT(*) AS cnt FROM tblMovie'))[0]
        tvShows = next(cur.execute('SELECT COUNT(*) AS cnt FROM tblTVShow'))[0]
        reviews = next(cur.execute('SELECT COUNT(*) AS cnt FROM tblReview'))[0]

        statsList.append({
            'games': games,
            'movies': movies,
            'tvShows': tvShows,
            'reviews': reviews
        })

    elif which == 'gamesPerSystem':
        gamesPerSystem = cur.execute('SELECT system, COUNT(*) AS cnt FROM tblGame GROUP BY system ORDER BY COUNT(*) ASC')

        [statsList.append({
            'system': row[0],
            'count': row[1]
        }) for row in gamesPerSystem]

    elif which == 'reviews':
        gameReviews = cur.execute('SELECT reviewType, COUNT(*) AS cnt FROM tblReview WHERE gameID > 0');
        movieReviews = cur.execute('SELECT reviewType, COUNT(*) AS cnt FROM tblReview WHERE movieID > 0');
        tvShowReviews = cur.execute('SELECT reviewType, COUNT(*) AS cnt FROM tblReview WHERE tvShowID > 0');

    return json.dumps(statsList)







@app.route('/getStats/gamesPerSystem', methods=['GET', 'POST'])
def getStatsGPS():
    #cnx = sqlCon()
    cnx = lite.connect(r'D:\capstone-v2.db')
    cur = cnx.cursor()





@app.route('/getDevList', methods=['POST'])
def getDevList():
    cnx = sqlCon()
    cur = cnx.cursor()
    strSQL = 'SELECT DISTINCT developer FROM tblGame ORDER BY developer ASC;'
    cur.execute(strSQL)

    devs = []
    [devs.append({
        'dev': row[0]
    }) for row in cur
    ]

    cnx.close()

    return json.dumps(devs)


@app.route('/getSystemList', methods=['POST'])
def getSystemList():
    cnx = sqlCon()
    cur = cnx.cursor()
    strSQL = 'SELECT DISTINCT system FROM tblGame ORDER BY developer ASC;'
    cur.execute(strSQL)

    systems = []
    [systems.append({
        'system': row[0]
    }) for row in cur
    ]

    cnx.close()

    return json.dumps(systems)


@app.route('/filter', methods=['GET'])
def filter():
    what = request.args.get('what', '')
    dev = request.args.get('dev', '')
    sys = request.args.get('system', '')

    print request.args.to_dict()

    return 'what: ' + what + ', dev: ' + dev + ', sys: ' + sys

if __name__ == '__main__':
    app.run(debug=True)