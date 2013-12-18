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
 * today - Sets the current date to today
 * yesterday - Sets the current date to yesterday
 * date *YYYY-MM-DD* - Sets the current date to an arbitrary date

Use Ctrl-D to exit.

