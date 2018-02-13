#!/usr/bin/env python

import sys
import argparse
import time
import datetime
import subprocess

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('year', type=int, help="year ", choices=[
                    2016, 2017, 2018, 2019, 2020, 2021])
parser.add_argument('month', help="month", default = datetime.date.month)
parser.add_argument('day', help="day ")
parser.add_argument('hour', help="hour ")
parser.add_argument('minute', help="minute ")
parser.add_argument('second', help="second ")
parser.add_argument(
    '-pre', help="time before event,seconds", type=int, default=60)
parser.add_argument(
    '-post', help="time after event, seconds", type=int, default=200)

args = parser.parse_args()

s = args.hour + ":" + args.minute + ":" + args.second + \
    "-" + args.day + "/" + args.month + "/" + str(args.year)
unixTime = time.mktime(datetime.datetime.strptime(
    s, "%H:%M:%S-%d/%m/%Y").timetuple())

print "unixTime = ", unixTime

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
    return time.mktime(datetime.datetime.strptime('20'+stri,"%Y.%m.%d-%H.%M.%S").timetuple())

def unixToCreaTime(time):
    return datetime.datetime.fromtimestamp(time).strftime('%Y.%m.%d-%H.%M.%S')[2:]

def pickFile(requiredTime):
    retName = ''
    for filNam in getLogFiles():
        fil = open(filNam,'r')
        lines = fil.readlines()
        lower = creaToUnixTime(lines[1].split()[0])
        if lower > requiredTime:
            continue
        upper =  creaToUnixTime(lines[-2].split()[0])
        if upper < requiredTime:
            continue
        retName = filNam
        break
    if retName == '':   print "Corresponding file not found. Sad"
    return retName

def makeGnup(fil,lower,upper):
    gnup = "#!/usr/bin/gnuplot -p\n\
set xdata time\n\
set timefmt \"%y.%m.%d-%H.%M.%S\"\n\
set xrange[\"" + unixToCreaTime(fr)+ "\":\"" + unixToCreaTime(to) + "\"]\n\
plot '"+fil+"' u 1:5"
    return gnup


print "YARGS! ", args
print makeGnup(pickFile(unixTime),fr,to)
