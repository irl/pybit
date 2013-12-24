# pybit
#
# Copyright (c) 2013, Iain R. Learmonth <irl@sdf.org>
# All rights reserved.
#
# For redistribution and use terms, see the LICENSE file.
#

from flask import Flask, render_template
import sqlite3
import datetime

DB_PATH = '../pybit.db'

app = Flask(__name__, static_folder='static', static_url_path='')

@app.route('/')
def home():
    db = sqlite3.connect(DB_PATH)
    cur = db.cursor()
    cur.execute("SELECT * FROM `fitbit_steps` WHERE datetime(`start`) >= datetime(?)", (datetime.datetime.combine(datetime.date.today(), datetime.time(0,0)).strftime('%Y-%m-%dT%H:%M'),))
    result = cur.fetchall()
    stepsPlot = []
    for row in result:
        ts = datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
        pos = (ts.hour * 60) + ts.minute
        stepsPlot.append((pos, row[2]))
    print(stepsPlot)
    cur.execute("SELECT * FROM `fitbit_sleep` WHERE datetime(`start`) >= datetime(?)", (datetime.datetime.combine(datetime.date.today(), datetime.time(0,0)).strftime('%Y-%m-%dT%H:%M'),))
    result = cur.fetchall()
    sleepPlot = []
    for row in result:
        ts = datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
        pos = (ts.hour * 60) + ts.minute
        sleepPlot.append((pos, row[2]))
    return render_template('steps.html', sleepPlot = sleepPlot, stepsPlot = stepsPlot, date = datetime.date.today())

if __name__ == "__main__":
    app.debug = True
    app.run()

