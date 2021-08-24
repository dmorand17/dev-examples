import logging
import os
import sys
import time
import argparse

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def parse_args():
    parser = argparse.ArgumentParser(description='HL7 Explorer to display message transactions, messages, histograms.')    
    parser.add_argument('-v', '--verbose', help='Verbose logging', action="store_const", dest="loglevel", const=logging.DEBUG)
    return parser.parse_args()

def main():
    args = parse_args()

    logger.setLevel(args.loglevel if args.loglevel is not None else logging.INFO)
    print(f"Log level: [{logging.getLevelName(logger.getEffectiveLevel())}]")

if __name__ == '__main__':
    main()
