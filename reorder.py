import csv
import os
import glob 

labeledDataFilePath = '/home/harminder/fydp/labelled_csv_files'
filePath = '/home/harminder/fydp/labelled_csv_files_reorder/'
extension = 'csv'
os.chdir(labeledDataFilePath)
csvFiles = glob.glob('*.{}'.format(extension))


startTime = 0
endTime = 0
label = ''

for csvFile in csvFiles:
	writeFile = open(filePath + os.path.splitext(csvFile)[0] + ".txt",'w')
	with open(csvFile, 'r') as file:
		fileData = csv.reader(file)
		for i, row in enumerate(fileData):
			print(row)
			if i != 0:
				if i == 1:
					label = row[5] 
				if label != row[5]:
					if (label == " "):
						label = "E"
					if (label == "p, w"):
						label =  "pw"	
					print("Writing: " + label + " " + str(startTime) + " " + str(endTime))
					writeFile.write (str(label) + " " + str(startTime) + " " + str(endTime) +  "\n")
					startTime = row[2]
					endTime = row[3]
					label = row[5]
				else:
					endTime = row[3]
	print("Writing: " + label + " " + str(startTime) + " " + str(endTime))
	if (label == " "):
		label = "E"
	if (label == "p, w"):
		label =  "pw"
	writeFile.write(str(label) + " " + str(startTime) + " " + str(endTime) + "\n")
	writeFile.close()
	startTime = 0
	endTime = 0


# Creating script to tranform the transcripts to appropriate form for other paper 
# TODO:
# 1. Query all files with .csv endings 
# 2. Read the files line by line, lump preceeding stutters into one, ignore stutters with label 'i' [removing interjection]
# 3. Write to a .txt file in the format 'label start_time end_time', 
#    name of text file should be the same as the cvs maybe relocate it  



