from os import listdir
from os.path import isfile, join
import sys
import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--csvPath", "-c", help="path to csvs", required=True)

args = parser.parse_args()
rawCSVPath = args.csvPath

# Assumes same filename for csv
csvFiles = [f for f in listdir(rawCSVPath) if isfile(join(rawCSVPath,f))]
print("===================== # CSV Files found:      " + str(len(csvFiles)))

stutter_count = 0
total_time = 0

# for csvFile in csvFiles:
#   df = pd.read_csv(rawCSVPath + csvFile, names=["title", "start_time", "end_time", "word", "stutter_type"])
#   for i, row in df.iterrows():
#     if row.stutter_type == "s":
#       stutter_count += 1
#       total_time += (float(row.end_time) - float(row.start_time))

for csvFile in csvFiles:
  df = pd.read_csv(rawCSVPath + csvFile, names=["title", "start_time", "end_time", "word", "stutter_type"])

  i = 0
  while i < (len(df)-1):
    if df.loc[i, 'stutter_type'] == "s":
      word = df.loc[i, 'word']
      stutter_count += 1
      total_time += (float(df.loc[i, 'end_time']) - float(df.loc[i, 'start_time']))

      while((i+1 < (len(df)-1)) and df.loc[i+1, 'word'] == word and df.loc[i+1, 'stutter_type'] == "s"):
        word = df.loc[i+1, 'word']
        total_time += (float(df.loc[i+1, 'end_time']) - float(df.loc[i+1, 'start_time']))
        i += 1

    i += 1


print("Average stutter length: ")
print(total_time / stutter_count)
