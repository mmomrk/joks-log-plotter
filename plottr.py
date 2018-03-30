#!/usr/bin/env python

import sys
import argparse
import time
import datetime
import subprocess

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('year', type=int, help="year ", choices=[
                    2016, 2017, 2018, 2019, 2020, 2021])
parser.add_argument('month', help="month", default=datetime.date.month)
parser.add_argument('day', help="day ")
parser.add_argument('hour', help="hour ")
parser.add_argument('minute', help="minute ")
parser.add_argument('second', help="second ")
parser.add_argument(
    '-pre', help="time before event,seconds", type=int, default=60)
parser.add_argument(
    '-post', help="time after event, seconds", type=int, default=200)
parser.add_argument(
    '-col', help="Column numbers in log file", type=int, default=[5], nargs="+")
parser.add_argument('-lc', help='List columns in file', action='store_true')

args = parser.parse_args()

s = args.hour + ":" + args.minute + ":" + args.second + \
    "-" + args.day + "/" + args.month + "/" + str(args.year)
unixTime = time.mktime(datetime.datetime.strptime(
    s, "%H:%M:%S-%d/%m/%Y").timetuple())

# print "unixTime = ", unixTime

fr = unixTime - args.pre
to = unixTime + args.post


def bash(bashCommand):
    #    bashCommand = "cwm --rdf test.rdf --ntriples > test.nt"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output


def getLogFiles():
    files = bash("ls")
    txts = [a for a in files.split() if a[-4:] == '.txt']
    return txts


def creaToUnixTime(stri):
    return time.mktime(datetime.datetime.strptime('20' + stri, "%Y.%m.%d-%H.%M.%S").timetuple())


def unixToCreaTime(time):
    return datetime.datetime.fromtimestamp(time).strftime('%Y.%m.%d-%H.%M.%S')[2:]


def pickFile(requiredTime):
    retName = ''
    for filNam in getLogFiles():
        fil = open(filNam, 'r')
        lines = fil.readlines()
        lower = creaToUnixTime(lines[1].split()[0])
        if lower > requiredTime:
            continue
        upper = creaToUnixTime(lines[-2].split()[0])
        if upper < requiredTime:
            continue
        retName = filNam
        break
    return retName


def fileIsFat(filenam):
    # my guess is that it's the older revision of logger because files without
    # double underscore have times more parameters logged
    return not "__" in filenam


def getRGBColors(numof):
    bank = ['red', 'green', 'blue', 'violet', 'orange',
            'dark-red', 'fuchsia', 'teal', 'yelow', 'purple']
    if numof < len(bank):
        return bank[:numof]
    else:
        print "WARNING: too many lines. I will drop some to black color, sorry"
        blacks = ["black"] * (numof - len(bank))
        return bank * blacks


def makeGnup(fil, lower, upper):
    ncols = len(args.col)
    paints = getRGBColors(ncols)
    gnup = "#!/usr/bin/gnuplot -p\n\
set terminal pngcairo size 1024,768\n\
set output \"plot.png\"\n\
set multiplot\n\
set lmargin screen " + str(0.01 + .03 * ncols) + "\n\
set xdata time\n\
set timefmt \"%y.%m.%d-%H.%M.%S\"\n\
set xrange[\"" + unixToCreaTime(fr) + "\":\"" + unixToCreaTime(to) + "\"]\n"
    i = 0
    for col, paint in zip(args.col, paints):
        gnup += "set ytics offset " + str(-3 * i) + ",0 \
textcolor rgb \"" + paint + "\" \n\
set key height " + str(i * 2 + 1) + "\n\
plot '" + fil + "' u 1:" + str(col) + " w l title '" + str(col) + "' linecolor rgb \"" + paint + "\" \n\
unset border\n"
        i += 1
    return gnup


def dumpToFile(nam, content):
    ofle = open(nam, 'w')
    for line in content:
        ofle.write(line)
    ofle.close()

def showHeader(fnam):
    fle = open(fnam,'r')
    header = fle.readline()
    splitHead = header.split()
    for num,colName in zip(range(len(splitHead)),splitHead):
	print num,'\t',colName

filNam = pickFile(unixTime)
if filNam == '':
    print "Corresponding enclosing file not found. Sad"
    sys.exit(1)
else:
    print "Data found in file: ", filNam


if args.lc:
    showHeader(filNam)
else:
    dumpToFile("iplot.plt", makeGnup(filNam, fr, to))

sys.exit(0)
# print "YARGS! ", args
