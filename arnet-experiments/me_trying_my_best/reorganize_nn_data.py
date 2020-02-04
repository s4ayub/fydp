import pandas as pd
import os
import argparse

def reorg(label_folder, spectrogram_folder, output_folder):
    label_file_map = {}

    for f in os.listdir(label_folder):
        if f.endswith('.csv'):
            temp = f.split('.')[0].split('_')[1:-1]
            audio_file = '_'.join(temp)
            label_file_map[audio_file] = f

    for per_audio_dir in os.listdir(spectrogram_folder):
        per_audio_dir_path = os.path.join(spectrogram_folder, per_audio_dir_path)

        raw_data = pd.read_csv(label_file_map[per_audio_dir], usecols=[3, 5], header=0)
        end_times = list(raw_data['end_times'])
        stutter_types = list(raw_data['stutter_types'])

        for per_chunk_dir in os.listdir(per_audio_dir_path):
            per_chunk_dir_path = os.path.join(per_audio_dir_path, per_chunk_dir)
            chunk_index = per_chunk_dir.split('_')[-1]


def main():
    custom_formatter = lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position=100)
    p = argparse.ArgumentParser(formatter_class=custom_formatter)

    p.add_argument('-l', '--labels', type=str, required=True, help='Specify the folder with the labelled .xlsx files')
    p.add_argument('-s', '--spectrograms', type=str, required=True, help='Specify the folder with the spectrograms')
    p.add_argument('-o', '--output', type=str, required=True, help='Specify the output folder')

    args = p.parse_args()

    label_folder = os.path.expanduser(p.labels)
    spectrogram_folder = os.path.expanduser(p.spectrograms)
    output_folder = os.path.expanduser(p.output)

    if not os.path.exists(label_folder):
        print('Labelled stutter folder does not exist: ' + label_folder)
        return
    if not os.path.exists(spectrogram_folder):
        print('Spectrogram folder does not exist: ' + spectrogram_folder)
        return
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    reorg(label_folder, spectrogram_folder, output_folder)

if __name__ == '__main__':
    main()
