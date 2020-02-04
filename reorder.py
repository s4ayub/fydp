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
	writeFile = open(filePath + csvFile,'w')
	with open(csvFile, 'r') as file:
		fileData = csv.reader(file)
		for i, row in enumerate(fileData):
			print(row)
			if i != 0:
				if i == 1:
					label = row[5] 
				if label != row[5]:
					txt.write (label, startTime, endTime)
					startTime = row[2]
					endTime = row[3]
					label = row[6]
				else:
					endTime = row[3]
	writeFile.close()


# Creating script to tranform the transcripts to appropriate form for other paper 
# TODO:
# 1. Query all files with .csv endings 
# 2. Read the files line by line, lump preceeding stutters into one, ignore stutters with label 'i' [removing interjection]
# 3. Write to a .txt file in the format 'label start_time end_time', 
#    name of text file should be the same as the cvs maybe relocate it  



