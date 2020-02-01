from os import listdir
from os.path import isfile, join
import sys
import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--rawCSVPath", "-c", help="path to csvs", required=True)
parser.add_argument("--outputCSVPath", "-o", help="path to annotated csvs", required=True)

args = parser.parse_args()
rawCSVPath = args.rawCSVPath
outputCSVPath = args.outputCSVPath

# Assumes same filename for csv
csvFiles = [f for f in listdir(rawCSVPath) if isfile(join(rawCSVPath,f))]
print("===================== # CSV Files found:      " + str(len(csvFiles)))

count = 0
for csvFile in csvFiles:
  count += 1
  df = pd.read_csv(rawCSVPath + csvFile, names=["title", "start_time", "end_time", "word", "stutter_type"])
  df['stutter_type'] = df['stutter_type'].apply(str)
  print(csvFile)

  for i, row in df.iterrows():
    if (row.word.isupper() and not (row.word == 'I')):
      df.at[i, 'stutter_type'] = "s"
    elif (row.word[0:2].lower() == "um") or (row.word[0:2].lower() == "uh"):
      df.at[i, 'stutter_type'] = "i"
    elif ("{" in row.word):
      df.at[i, 'stutter_type'] = "p"
    else:
      df.at[i, 'stutter_type'] = "n"

  df.to_csv(outputCSVPath + "labelled_" + csvFile)

print("===================== # CSV Files annotated:      " + str(count))
