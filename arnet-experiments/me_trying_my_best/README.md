### Record

python AudioDudeTester.py -m record -o filename.wav

### Play

python AudioDudeTester.py -m play -i filename.wav

### Spectrogram

python AudioDudeTester.py -m spec -i filename.wav

### NN prep

python AudioDudeTester.py -m spec -i recording.wav --nn-prep --chunk-size 4 --window-size 200 --window-step 100 -o test_output_folder
