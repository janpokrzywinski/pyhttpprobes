#!/usr/bin/env python
# Filename: reuse.py
# Create HTTP session that will reuse KA connection to send multiple requests

import argparse
import signal
import sys
import requests
import time


def signal_handler(signal, frame):
    """ Signal hander used to capture Ctrl+C """
    print 'User Interrupted'
    sys.exit(0)


class probe():
    """ Class used for sending KA probes """
    s = requests.Session()

    def __init__(self):
        return

    def infinite(self, dest, delay):
        counter = 0
        while True:
            r = self.s.head(dest)
            print "Response Code: {} Request ID {}".format(
                                            str(r.status_code), str(counter))
            counter += 1
            time.sleep(delay)
        return

    def counted(self, dest, delay, end):
        for i in range(0, end):
            r = self.s.head(dest)
            print "Response Code: {} Request ID: {}".format(
                                            str(r.status_code), str(i))
            time.sleep(delay)
        return


def main():
    """ Main function of the script """
    signal.signal(signal.SIGINT, signal_handler)
    prob = probe()
    delay = 0
    par = argparse.ArgumentParser(
        description='Reuse single KA connection for multiple HTTP requests')
    par.add_argument(
        '-c',
        '--count',
        metavar='N',
        type=int,
        help='amount of the requests to send')
    par.add_argument(
        '-d',
        '--delay',
        metavar='N',
        type=int,
        help='delay in millisecond between the requests')
    par.add_argument('URL')
    args = par.parse_args()
    if "http://" or "https://" not in args.URL:
        args.URL = "http://" + args.URL
    print "Probing URL: {}".format(args.URL)
    if args.delay:
        delay = args.delay / 1000
    if args.count:
        prob.counted(args.URL, delay, args.count)
    else:
        prob.infinite(args.URL, delay)


if __name__ == '__main__':
    main()
