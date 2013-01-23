#!/usr/bin/env python
 
"""
SYNOPSIS
 
    Usage: ./tracer.py <cmd> [options]
 
DESCRIPTION
 
    Given a command, an awk filter and a time interval, this script will run
    the command periodically according to the time interval and extract the
    data returned as output of the command based on the given filter.
    The output of this is script is then a dictionary that has timestamps
    as keys and command filtered output as values
 
"""

import subprocess
import optparse
import traceback
import sys
import time
from datetime import datetime as dt

def abort(msg):
    print msg;
    sys.exit(1)

def warn(msg):
    print "WARNING:", msg

def run(cmd):
    global options, args
    
    if options.verbose:
        print "cmd:", cmd
    
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE, shell=True,
                             executable='/bin/bash')
        output,stderr = p.communicate()
        if p.returncode:
            abort('unexpected return code %d for "%s".\n%s\n%s' % 
                  (p.returncode, cmd, output, stderr))
        
        return output.strip()
    except Exception, e:
        None

def main():
    global options

    interval = float(options.interval)
    sfilter  = str(options.filter)
    cmd      = str(options.cmd)
    if (options.aggregate):
        measurements = dict()

    run(cmd)

    if options.delta:
        start = dt.now()
    try: 
        while True:
            runTime = dt.now()
            out = run("%s | awk '%s'" % (cmd, sfilter));
            
            if not options.aggregate:
                if options.delta:
                    d = runTime-start
                    t = '%d.%0.6d' % (d.seconds, d.microseconds)
                else:
                    t = runTime.strftime(options.timefmt)
                print '%s: %s' % (t,out)
            else:
                measurements[runTime] = out
            
            elapsed = dt.now() - runTime
            wait4   = interval - elapsed.seconds - (elapsed.microseconds*1e-6)
            if wait4 < 0:
                warn("Command is taking more than %f to execute!" % interval)
                wait4 = 0
            time.sleep(wait4)
    except KeyboardInterrupt, e: # Ctrl-C
        if options.aggregate:
            print measurements
    
    return 0;

if __name__ == '__main__':
    try:
        
        parser = optparse.OptionParser(
            formatter=optparse.TitledHelpFormatter(),
            usage=globals()['__doc__'],
            version='')
        
        parser.add_option('-v', '--verbose', action='store_true',
                          default=False, help='verbose output')

        parser.add_option('-a', '--aggregate', action='store_true',
                          default=False, 
                          help='print all measurements when SIGINT')
        
        parser.add_option('-t', '--timefmt', action='store',
                          default='%I:%M:%S.%f', help='')
        
        parser.add_option('-d', '--delta', action='store_false',
                          default=True,
                          help='When present, print timestamps according '
                          'to format given in --timefmt option')
        
        parser.add_option('-f', '--filter', action='store',
                          default='{print $0}', help='')
        
        parser.add_option('-i', '--interval', action='store',
                          default='1', help='Interval to run cmd')
        
        
        if len(sys.argv) > 1:
            (options, args) = parser.parse_args(args=sys.argv[1:])
            options.cmd = sys.argv[1]
            sys.exit(main())
        else:
            parser.print_usage()

    except SystemExit, e: # sys.exit()
        raise e
    except Exception, e:
        print 'Unexpected exception "%s"' % str(e)
        traceback.print_exc()
        sys.exit(1)
