from os import listdir
from os.path import isfile, join 
import sys
import argparse

from aeneas.tools.execute_task import ExecuteTaskCLI

parser = argparse.ArgumentParser()

parser.add_argument("--audioPath", "-a", help="path to audio dir", required=True)
parser.add_argument("--transPath", "-t", help="path to transcripts dir", required=True)
parser.add_argument("--outputPath", "-o", help="path to ouput dir", required=True)

args = parser.parse_args()

audioPath = args.audioPath
transPath = args.transPath
outputPath = args.outputPath

# Assumes same filename for audio and transcript  
audioFiles = [f for f in listdir(audioPath) if isfile(join(audioPath,f))]
transFiles = [f for f in listdir(transPath) if isfile(join(transPath,f))]

print("===================== # Audio Files found:      " + str(len(audioFiles)))
print("===================== # Transcript Files found: " + str(len(transFiles)) +  "\n")

count = 0
for audioFile in audioFiles:
	transFile = name=audioFile[:-4] + ".txt" 
	if transFile in transFiles:
		print("[START] Force aligning \"" + audioFile + "\"...")
		ExecuteTaskCLI(use_sys=False).run(arguments=[
    			None, # dummy program name argument
    			unicode(audioPath+audioFile),
    			unicode(transPath+transFile),
    			u"task_language=eng|is_text_type=mplain|os_task_file_format=aud|os_task_file_levels=3",
    			unicode(outputPath + audioFile[:-4] + "_fa.aud"),
    			u"--presets-word"])
		count += 1
		print("[FINISH] Completed Files: " + str(count) + "/" + str(len(audioFiles)))

	else:
		print("ERROR: Transcript not found for audio file: " + audioFile)	





