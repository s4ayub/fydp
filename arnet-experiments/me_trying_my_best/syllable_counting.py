# Code is from 'Introducing Parselmouth: A Python interface to Praat' by Yannick Jadoul et al.

import parselmouth
from parselmouth.praat import call, run_file

import numpy as np
import os
import sys

SYLLABLE_SCRIPT = os.path.expanduser("~/projects/fydp/experiments/Praat-Scripts/praat-script-syllable-nuclei-v2file.praat")
AUDIO_FILE_DIRECTORY = os.path.expanduser("~/projects/fydp/experiments/me_trying_my_best/samples")

def extract_syllable_intervals(directory, file_name):
    print("Extracting syllable intervals from '{}' ... ".format(file_name), end="")

    # Use Praat script to extract syllables
    objects = run_file(SYLLABLE_SCRIPT, -25, 2, 0.4, 0.1, True, AUDIO_FILE_DIRECTORY, file_name)
    textgrid = objects[0]
    n = call(textgrid, "Get number of points", 1)
    syllable_nuclei = [call(textgrid, "Get time of point", 1, i + 1) for i in range(n)]
    # Use NumPy to calculate intervals between the syllable nuclei
    syllable_intervals = np.diff(syllable_nuclei)
    return syllable_intervals

def main():
    if len(sys.argv) is 2:
        file_name = sys.argv[1]
        intervals = extract_syllable_intervals(AUDIO_FILE_DIRECTORY, file_name)
        n_syllables = len(intervals) + 1
        print("syllable count = {}".format(n_syllables))
    else:
        print("Provide path to an audio file as an argument")

if __name__ == "__main__":
    main()
