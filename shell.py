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
import math
from getpass import getpass
from subprocess import call
import argparse
import sys

parser = argparse.ArgumentParser(description='Scrape the FitBit website.')
parser.add_argument('-b', action='store_true', help='Batch mode')
parser.add_argument('--email', help='Your registered FitBit email address (required for batch mode)')
parser.add_argument('--passwd', help='Your registered FitBit password (required for batch mode)')
args = parser.parse_args()

try:
    if not args.b:
        import readline
except ImportError:
    print("readline not available. Line editing functions will not be available.")

if args.email != None or args.passwd != None:
    username = args.email
    password = args.passwd
else:
    if args.b:
        print("Nope. Email address and password required.")
        sys.exit(1)
    username = input("E-Mail Address: ")
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
            rowParts = [
                ivl['start'].strftime('%Y-%m-%dT%H:%M'),
                ivl['end'].strftime('%Y-%m-%dT%H:%M'),
                ivl['steps']
            ]
            out.write(','.join(rowParts) + "\n")

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

def sleep(pa):
    if pa[1] == "plot":
        plotSleep()
        return
    if pa[1] == "save":
        writeSleep(pa[2])
        return
    if pa[1] == "view":
        viewSleep()
        return

def writeSleep(filename):
    global d
    sleep = f.getSleepForDay(d)
    with open(filename, 'w') as out:
        out.write("Start,End,State\n")
        for ivl in sleep:
            rowParts = [
                ivl['start'].strftime('%Y-%m-%dT%H:%M'),
                ivl['end'].strftime('%Y-%m-%dT%H:%M'),
                ivl['state']
            ]
            out.write(','.join(rowParts) + "\n")

def viewSleep():
    writeSleep("/tmp/pybit.csv")
    call(["less", "/tmp/pybit.csv"])

def plotSleep():
    global d
    sleep = f.getSleepForDay(d)
    sleepState = [int(x['state'].split('.')[0]) for x in sleep]
    width = 0.1      # the width of the bars
    fig, ax = plt.subplots()
    ax.bar(range(0, len(sleepState)), sleepState, width)
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

def bedtime(pa):
    global d
    print(f.getTimeToBed(d))

def timeInBed(pa):
    global d
    timeInBed = f.getTimeInBed(d)
    print("PT" + str(math.floor(timeInBed.total_seconds() / 3600)) + "H" + str(math.floor(timeInBed.total_seconds() / 60) % 60) + "M")

def empty(pa):
    pass

cmds = {
        'steps': steps,
        'sleep': sleep,
        'date': setDate,
        'today': today,
        'yesterday': yesterday,
        'bedtime': bedtime,
        'timeinbed': timeInBed,
        '': empty,
    }

while True:
    try:
        if not args.b:
            cmd = input(d.strftime('%Y-%m-%d> '))
        else:
            cmd = sys.stdin.readline().strip()
            if not cmd:
                break
    except EOFError:
        print()
        break

    pa = cmd.split(' ')

    try:
        cmds[pa[0]](pa)
    except KeyError:
        print("Command not recognised.")

