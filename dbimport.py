# pybit
#
# Copyright (c) 2013, Iain R. Learmonth <irl@sdf.org>
# All rights reserved.
#
# For redistribution and use terms, see the LICENSE file.
#

import fitbit
import datetime
import argparse
import sqlite3

# Initialise the database, use once just to create it

def initDb():
    try:
        with sqlite3.connect('pybit.db') as db:
            cur = db.cursor()
            cur.executescript(open('schema.sql', 'r').read())
            db.commit()
    except:
        print("Failed. Make sure you have permission to create and write files"
                + "in this directory")

# Define databas population functions

def fetchSteps(date):
    global db
    steps = f.getStepsForDay(date)
    stepone = "DELETE FROM `fitbit_steps` WHERE `start`=?"
    steptwo = "INSERT INTO `fitbit_steps` VALUES ( ?, ?, ? )"
    cur = db.cursor()
    for ivl in steps:
        cur.execute(stepone, (ivl['start'],))
        cur.execute(steptwo, (ivl['start'], ivl['end'], ivl['steps']))
    db.commit()

def fetchSleep(date):
    global db
    sleep = f.getSleepForDay(date)
    stepone = "DELETE FROM `fitbit_steps` WHERE `start`=?"
    steptwo = "INSERT INTO `fitbit_sleep` VALUES ( ?, ?, ? )"
    cur = db.cursor()
    for ivl in sleep:
        cur.execute(stepone, (ivl['start'],))
        cur.execute(steptwo, (ivl['start'], ivl['end'], ivl['state']))
    db.commit()


if __name__ == "__main__":

    # Read command line arguments

    parser = argparse.ArgumentParser()
    parser.add_argument('--email', help='Registered FitBit Email Address')
    parser.add_argument('--password', help='Registered FitBit Password')
    args = parser.parse_args()

    username = args.email
    password = args.password

    # Get data from Fitbit
    f = fitbit.Fitbit(username, password)

    with sqlite3.connect('pybit.db') as db:
        today = datetime.datetime.now().date()
        fetchSteps(today)
        fetchSleep(today)
        yesterday = (datetime.datetime.now() - datetime.timedelta(1)).date()
        fetchSteps(yesterday)
        fetchSleep(yesterday)


