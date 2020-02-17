import os 
import glob

read_dir = '/home/harminder/fydp/gcp_transcripts'
store_dir = '/home/harminder/fydp/word_rep'


def find_word_repetitions(path_transcript):
	read_file_=open(path_transcript,"r")
	lines=read_file_.readlines();

	word_prev  = ""
	start_prev = 0

	wr = []  
	num_rep = 0

	for i, line in enumerate(lines):
		tokens = line.split()

		if i == 0:
			word_prev = str(tokens[0])
		
		if word_prev == str(tokens[0]):
			if(num_rep == 0):
				wr.append([word_prev, start_prev, tokens[2], ""])
			num_rep = num_rep + 1 
		else:
			if num_rep != 0:
				#num_times.append(num_rep)
				wr[len(wr)-1][3] = num_rep
			num_rep=0	
			word_prev = str(tokens[0])
			start_prev = str(tokens[1])

	return wr	

def write_to_file(data_wr, write_file_name):
	writeFile = open(store_dir + "/" + write_file_name, 'w')

	for i, data in enumerate(data_wr):
		if i==0:
			writeFile.write("word start_time end_time num_reps \n")
		else:
			writeFile.write(str(data[0]) + " " + str(data[1]) + " " + str(data[2]) + " " + str(data[3]) + "\n")

	writeFile.close()	


def get_filenames(dir):
	extension = 'txt'
	os.chdir(dir)
	files = glob.glob('*.{}'.format(extension))
	return files


filenames = get_filenames(read_dir)

for filename in filenames:
	result = find_word_repetitions(read_dir+"/"+filename)
	write_to_file(result, filename)	


