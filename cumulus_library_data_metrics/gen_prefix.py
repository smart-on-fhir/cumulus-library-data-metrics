#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--study")
args, _rest = parser.parse_known_args()

if args.study:
    print(f"data_metrics_{args.study}")
else:
    print("data_metrics")
