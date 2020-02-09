### Record

python AudioDudeTester.py -m record -o filename.wav

### Play

python AudioDudeTester.py -m play -i filename.wav

### Spectrogram

python AudioDudeTester.py -m spec -i filename.wav

### NN prep

python AudioDudeTester.py -m spec -i input --nn-prep --chunk-size 4000 --window-size 200 --window-step 100 -o output
