import os 
import glob

read_dir = '/home/harminder/fydp/gcp_transcripts'
store_dir_wr = '/home/harminder/fydp/word_rep'
store_dir_pr = '/home/harminder/fydp/phrase_rep'


def find_word_repetitions(path_transcript):
	read_file_=open(path_transcript,"r")
	lines=read_file_.readlines();

	word_prev  = ""
	start_prev = 0

	# note that the first line of wr will always be trash
	# but it gets filtered when we write to files
	wr = []  
	num_rep = 0

	for i, line in enumerate(lines):
		tokens = line.split()

		if i == 0:
			word_prev = str(tokens[0])
		
		if word_prev == str(tokens[0]):
			if(num_rep == 0):
				wr.append([word_prev, start_prev, ""]) 
			num_rep = num_rep + 1 
		else:
			if num_rep != 0:
				#num_times.append(num_rep)
				wr[len(wr)-1][2] = num_rep
			num_rep=0	
			word_prev = str(tokens[0])
			start_prev = str(tokens[1])

	return wr	

def find_phrase_repetitions(path_transcript):
	read_file_=open(path_transcript,"r")
	lines=read_file_.readlines();

	phrase_words = []
	reps_found = 0
	check_next = False

	phr = []
	phr.append(["", "", ""])

	phrase_words.append(str(lines[0].split()[0]))
	phrase_words.append(str(lines[1].split()[0]))

	for i in range(2, len(lines)-1):
		tokens = lines[i].split()

		if check_next:
			if(phrase_words[1] == str(tokens[0])):
				if(reps_found == 0):
					phr.append([phrase_words[0]+" "+phrase_words[1], 10, ""]) # FIGURE OUT THE REST 
				reps_found += 1 
			else:
				tmp = phrase_words[0]
				phrase_words[0] = phrase_words[1]
				phrase_words[1] =tmp
				if(reps_found != 0):
					phr[len(phr)-1][2] = reps_found
				reps_found = 0	
			check_next = False	 
		else: # len(phrase_words) == 2:
			if(phrase_words[0] != str(tokens[0])):
				phrase_words[0]=phrase_words[1]
				phrase_words[1]=str(tokens[0])
				if(reps_found != 0):
					phr[len(phr)-1][2] = reps_found
				reps_found = 0
			else:
				check_next = True	

	return phr			


def write_to_file(data_wr, write_file_name, dir):
	writeFile = open(dir + "/" + write_file_name, 'w')

	for i, data in enumerate(data_wr):
		if i==0:
			writeFile.write("word start_time num_reps \n")
		else:
			writeFile.write(str(data[0]) + " " + str(data[1]) + " " + str(data[2]) + "\n")

	writeFile.close()	


def get_filenames(dir):
	extension = 'txt'
	os.chdir(dir)
	files = glob.glob('*.{}'.format(extension))
	return files


filenames = get_filenames(read_dir)

for filename in filenames:
	result_wr = find_word_repetitions(read_dir+"/"+filename)
	if(len(result_wr) ==  1):
		continue
	write_to_file(result_wr, filename, store_dir_wr)	

	result_pr = find_phrase_repetitions(read_dir+"/"+filename)
	if(len(result_pr) ==  1):
		continue
	write_to_file(result_pr, filename, store_dir_pr)



