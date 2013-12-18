# pybit
#
# Copyright (c) 2013, Iain R. Learmonth <irl@sdf.org>
# All rights reserved.
#
# For redistribution and use terms, see the LICENSE file.
#

import matplotlib.pyplot as plt
import fitbit
import datetime
from getpass import getpass
from subprocess import call

username = input("Username: ")
password = getpass("Password: ")

# Get data from Fitbit
f = fitbit.Fitbit(username, password)
d = datetime.date.today()

def steps(pa):
    if pa[1] == "plot":
        plotSteps()
        return
    if pa[1] == "save":
        writeSteps(pa[2])
        return
    if pa[1] == "view":
        viewSteps()
        return

    print("Missing operation. Hint: plot, save or view.")

def writeSteps(filename):
    global d
    steps = f.getStepsForDay(d)
    with open(filename, 'w') as out:
        out.write("Start,End,Count\n")
        for ivl in steps:
            out.write(ivl['start'] + "," + ivl['end'] + "," + ivl['steps']
                + "\n")

def viewSteps():
    writeSteps("/tmp/pybit.csv")
    call(["less", "/tmp/pybit.csv"])

def plotSteps():
    global d
    steps = f.getStepsForDay(d)
    stepsCount = [int(x['steps'].split('.')[0]) for x in steps]
    width = 0.1      # the width of the bars
    fig, ax = plt.subplots()
    ax.bar(range(0, len(stepsCount)), stepsCount, width)
    plt.show()

def setDate(pa):
    global d
    try:
        d = datetime.datetime.strptime(pa[1], '%Y-%m-%d').date()
    except ValueError:
        print("Incorrect date format.")

def today(pa):
    global d
    d = datetime.date.today()

def yesterday(pa):
    global d
    d = datetime.date.today() - datetime.timedelta(1)

def empty(pa):
    pass

cmds = {
        'steps': steps,
        'date': setDate,
        'today': today,
        'yesterday': yesterday,
        '': empty,
    }

while True:
    try:
        cmd = input(d.strftime('%Y-%m-%d> '))
    except EOFError:
        print()
        break

    pa = cmd.split(' ')

    try:
        cmds[pa[0]](pa)
    except KeyError:
        print("Command not recognised.")

