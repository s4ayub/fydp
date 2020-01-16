from os import listdir
from os.path import isfile, join
import sys
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--csvPath", "-c", help="path to csvs", required=True)

args = parser.parse_args()

csvPath = args.csvPath

# Assumes same filename for csv
csvFiles = [f for f in listdir(csvPath) if isfile(join(csvPath,f))]

print("===================== # CSV Files found:      " + str(len(csvFiles)))

count = 0
for csvFile in csvFiles:
  print csvFile
