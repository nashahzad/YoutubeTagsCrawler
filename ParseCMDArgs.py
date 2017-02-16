import argparse
import urllib.request as req
from Stats import YOUTUBE
from sys import exit


def parse():
    parser = argparse.ArgumentParser(description="Grab command line arguments for time and optional starting youtube url")
    parser.add_argument('--time', type=int, help="Time in seconds for crawler to run, default to 1 minute.")
    parser.add_argument('--url', help="Optional staring url argument, default to " + YOUTUBE + " if not specified.")
    args = parser.parse_args()

    if args.time == None:
        args.time = 60
    if args.url == None:
        args.url = YOUTUBE

    if args.url != YOUTUBE:
        try:
            check = req.Request(args.url)
            temp = req.urlopen(check)
        except:
            print("Invalid url was given, " + args.url)
            exit()


    return args.time, args.url

