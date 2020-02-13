# fydp

### Training data spectrograms

https://drive.google.com/drive/folders/1FaM79O5uHBGpg7LkkpVQPTEMrQKpvf_n

### Generate raw spectrograms

python arnet-experiments/me_trying_my_best/AudioDudeTester.py -m spec -i audio_files --nn-prep --chunk-size 4000 --window-size 200 --window-step 100 -o raw_spectrograms --use-logscale

### Reorganize raw spectrograms

python arnet-experiments/me_trying_my_best/reorganize_nn_data.py -l labelled_csv_files/ -s raw_spectrograms -o nn_spectrograms/ --bad-chunks bad_chunks.txt

### Resize raw spectrograms

python arnet-experiments/me_trying_my_best/resize_raw_spectrograms.py -i raw_spectrograms -o resized_raw_spectrograms -s 172,128
