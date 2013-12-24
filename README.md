pybit
=====

(C) Iain R. Learmonth. All rights reserved.

See LICENSE for terms of usage and redistribution.

Introduction
------------

*pybit* is a Python interface to the data collected by FitBit trackers. It uses
the FitBit website to download steps and sleep data with 5 minutes and 1 minute
intervals respectively. This software is still under development, and be aware
that if the FitBit website changes, this software will break. This software is
not using the documented API as it does not provide the intraday data, only
daily totals.

Pre-requisites
--------------

 * Python 3.2+
 * matplotlib

Usage
-----

 * fitbit.py contains the functions you may like to use in your application.
   They're quite self-explanatory.
 * shell.py contains an interactive shell that allows you to save the intraday
   data to CSV files with no programming knowledge.

Using the shell
---------------

The shell is launched by running:

    python shell.py

in the directory containing pybit.

You will be asked to log in with your registered email address and password.
You will then be presented with a prompt displaying todays date. The following
commands are available:

 * steps plot - Uses matplotlib to draw a plot of the current date's steps
 * steps view - Displays the raw data in CSV format using the `less` pager
 * steps write *filename* - Writes the CSV data to the file of your choice
 * bedtime - Display the time at which you went to bed the night prior to the
   current date.
 * sleep plot - Uses matplotlib to draw a plot of sleep data for the night prior
   to the current date.
 * sleep view - Displays the raw data in CSV format using the `less` pager
 * sleep write *filename* - Writes the CSV data to the file of your choice
 * today - Sets the current date to today
 * yesterday - Sets the current date to yesterday
 * date *YYYY-MM-DD* - Sets the current date to an arbitrary date

Use Ctrl-D to exit.

Importing to sqlite3
--------------------

The dbimport.py script contains functions for importing your fitbit data into an
sqlite3 database with the schema described in schema.sql. To get started:

    $ python
    >>> import dbimport
    >>> dbimport.initDb()

This will create the sqlite3 database. To import your data, run:

    $ python dbimport.py --email <email> --password <password>

and todays and yesterdays data will be populated in the database. You can run
the import command multiple times a day and the old data will be overwritten.

Using the web interface
-----------------------

The web interface depends on Flask[1]. You must ensure that it is installed
before attempting to run the web interface.

You must also create the sqlite3 database and populate it as that is where the
web interface takes its data from.

In the `web` subdirectory, run:

    $ python pybit-web.py

and then browse to http://localhost:5000/ in your web browser.

