# joks-log-plotter

This is a tool created to visualise certain log files with gnuplot.

## Help

usage: plottr.py [-h] [-pre PRE] [-post POST] [-col COL [COL ...]] [-lc]  {2016,2017,2018,2019,2020,2021} month day hour minute second

Plot log files

*positional arguments:*

  {2016,2017,2018,2019,2020,2021}	year

  month                 month

  day                   day

  hour                  hour

  minute                minute

  second                second

*optional arguments:*

  -h, --help            show this help message and exit

  -pre PRE              time before event,seconds

  -post POST            time after event, seconds

  -col COL [COL ...]    Column numbers in log file

  -lc                   List columns in file


## Description

This program is divided into launch script and plotter script.

### Launch script

Launch script 'laun.sh' is the supposed callable executable. It calls plottr.py that checks available log files in the folder. Then generates gnuplot executable iplot.plt. Then the execcutable generates the output file plot.png that is showed by feh command (which is unlikely to be installed on majority of general-purpose OS'es like Ubuntu.

### Main executable

The main command is plottr.py that takes the date of the required event as input (see help) and searches for the files in the folder for the one containing the required date-time.

After the file is found it may either list columns name and exit (that will stop the abovementioned tool-chain) or proceed to generating and plotting.

### Options

* The -pre and -post flags are available to adjust timespan that is being plotted before and after the requested event. In seconds

* The -col flag allows picking several columns to be plotted

## What to do with this

You are probably interested in adjusting your image viewer. You may use 'xdg-open' command to use your default viewer. Don't forget to remove flag.

### Chart column names into legend

If you want to use column names as legend in the chart then uncomment lines 110 and 103 and 104 in the plottr.py and comment out line 111. Should do the trick

### fixdots.sh

This script is to be used if your logfile contains commas instead of dots for decimal delimiters. It replaces all commas to dots in all txt files in the folder. Probably could be better had it replaced in all files in the arguments but not now. 

*WARNING:* does not make backups. The changes are irreversible. Make sure you are working with copies.

## Requirements

* python 2.7 or more. Tested with 2.7.12. Probably could work with 2.4 and 3+

* gnuplot with png support

* feh installed. Or just change laun.sh to your taste

## Testing

Sample command is in the sample.command file. You may use 'bash sample.command' for the purpose

## Licence 

All executables are spread under MIT licence.

Copyright (c) 2018 Mark Bochkov

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

### Plus

If you are using it then praise opensource community and be nice

