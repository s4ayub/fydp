from pydub import AudioSegment
import os 

audioFilePrefix = '/home/harminder/fydp/audio_files/'			# Audio File location
labeledFilePrefix = '/home/harminder/fydp/labelled_csv_files_reorder/'			# full files
storeDirectory = '/home/harminder/fydp/audio_files_1s/'     # SplitAudio full files

#labeledFilePrefix = 'LabeledText4s/'		# 4 s files
#storeDirectory = './SplitAudio_1s/'     # SplitAudio full files


names = [(f.split("labelled_")[1]).split("_fa.txt")[0] for f in os.listdir(labeledFilePrefix)]

for name in names:
	print ("**** NEW FILE *****")
	print (name)
	audioName = audioFilePrefix + name + ".wav"
	textName = labeledFilePrefix + "labelled_" + name + "_fa.txt"
	song = AudioSegment.from_wav(audioName)
	open_=open(textName,"r")
	lines=open_.readlines();
	for i in range(0, len(lines)):
		print (lines[i])
		tokens = lines[i].split()
		if len(tokens) == 0: continue
		label = tokens[0]
		t1 = (float(tokens[1])) * 1000
		t2 = (float(tokens[2])) * 1000

		if t2 - t1 <= 1.0:
			newAudio = song[t1:t2]
			newName = str(label) + '-' + name + '_' + str(int(round(float(tokens[1])))) + '_' + str(int(round(float(tokens[2])))) + ".wav"
			newAudio.export(storeDirectory + newName, format='wav')
		else:
			# print tokens[1] * 60
			# print tokens[2] * 60
			numIters = ((float(tokens[2])) - (float(tokens[1])))/1
			print (str(int(numIters)))
			prevNum = float(tokens[1]) * 1000
			for j in range(int(numIters)):
				curr = prevNum + 1000
				newAudio = song[prevNum:curr]
				newName = str(label) + '-' + name + '_' + str(int(round(float(prevNum)/1000))) + '_' + str(int(round(float(curr)/1000))) + ".wav"
				newAudio.export(storeDirectory + newName, format='wav')
				prevNum = curr

			newAudio = song[prevNum:t2]
			newName = str(label) + '-' + name + '_' + str(int(round(float(prevNum)/1000))) + '_' + str(int(round(float(tokens[2])))) + ".wav"
			newAudio.export(storeDirectory + newName, format='wav')