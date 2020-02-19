from google.cloud import speech_v1
import pdb
import os
import glob 

read_dir = '/home/harminder/fydp/audio_files'
store_dir = '/home/harminder/fydp/gcp_transcripts'
baseline_uri = 'gs://audio-test-lall/'

def sample_long_running_recognize(storage_uri):

	audio = {"uri": storage_uri}

	operation = client.long_running_recognize(config, audio)

	print(u"Waiting for operation to complete...")
	response = operation.result()
	return response

def get_audio_filenames(dir):
	extension = 'wav'
	os.chdir(dir)
	wavFiles = glob.glob('*.{}'.format(extension))
	return wavFiles

def speech_to_text(uri_complete, write_file_name):
	final_response = sample_long_running_recognize(uri_complete)
	writeFile = open(store_dir + "/" + write_file_name + ".txt",'w')

	for result in final_response.results:
		alternative = result.alternatives[0]
		for word in alternative.words:
			writeFile.write(word.word + " " + str(word.start_time.seconds) + " " + str(word.end_time.seconds) +  "\n")

	writeFile.close()		




# =========== INIT GCP 
client = speech_v1.SpeechClient()

enable_word_time_offsets = True
sample_rate_hertz = 44100
language_code = "en-GB"

config = {
    "enable_word_time_offsets": enable_word_time_offsets,
    "language_code": language_code,
    "sample_rate_hertz": sample_rate_hertz
}


audio_files = get_audio_filenames(read_dir)

for filename in audio_files:
	print("File: " + filename)
	if os.path.exists(store_dir+"/"+os.path.splitext(filename)[0]+".txt"):
		continue
	print("File: " + filename)
	uri = baseline_uri + filename
	speech_to_text(uri, os.path.splitext(filename)[0])


# gcloud ml speech recognize-long-running "gs://audio-test-lall/M_0061_14y8m_1.wav" 
# --language-code=en-GB --sample-rate=44100 --include-word-time-offsets


