#!/usr/bin/python

import sys
import re

def netstatTCPDiff(oldStatsFileName, newStatsFileName):
    f = open(oldStatsFileName, 'r');
    old = f.readlines();
    f.close()
    f = open(newStatsFileName, 'r');
    new = f.readlines();
    f.close()

    stats = dict();
    name  = '';
    for line in old:
        if line[0] != ' ' and len(line) > 0:
            name = line;
            stats[name] = dict()
        n = re.search("\d+(\s|$)", line)
        if not n:
            continue
        n = n.group()
        idx = "".join(re.sub("\d+(\s|$)", "", line).split())
        stats[name][idx] = n;

    name  = '';
    for line in new:
        if line[0] != ' ' and len(line) > 0:
            name = line;
            print name,
        n = re.search("\d+(\s|$)", line)
        if not n:
            continue
        n = n.group()
        idx = "".join(re.sub("\d+(\s|$)", "", line).split())
        if idx in stats[name]:
            if(int(n)-int(stats[name][idx])) != 0:
                print "\t%d %s" % (int(n)-int(stats[name][idx]),
                                   " ".join(re.sub("\d+", "", line).split()))
        elif n > 0:
            print "\t%d %s" % (int(n)," ".join(re.sub("\d+", "", line).split()))

                   
if __name__ == "__main__":
    if (len(sys.argv) == 3):
        netstatTCPDiff(sys.argv[1],sys.argv[2])
    else:
        print "Missing parameters"
