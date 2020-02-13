import os
import argparse
from PIL import Image

def main():
    p = argparse.ArgumentParser()

    p.add_argument('-i', '--input', type=str, required=True, help='Specify the raw spectrogram input folder to resize')
    p.add_argument('-o', '--output', type=str, required=True, help='Specify the output folder')
    p.add_argument('-s', '--size', type=str, required=True, help='Specify pixel sizes as w,h')

    args = p.parse_args()

    input_folder = os.path.expanduser(args.input)
    output_folder = os.path.expanduser(args.output)

    new_size = tuple([int(n) for n in args.size.split(',')])

    if len(new_size) is not 2:
        print('Size input error, expected wxh')
        return
    if not os.path.exists(input_folder):
        print('Input folder does not exist')
        return
    if os.path.exists(output_folder):
        print('Output folder should not already exist')
        return

    os.makedirs(output_folder)

    per_audio_dirs = os.listdir(input_folder)
    per_audio_dirs = [d for d in per_audio_dirs if not d.startswith('.')]

    for per_audio_dir in per_audio_dirs:
        per_audio_dir_path = os.path.join(input_folder, per_audio_dir)
        per_audio_dir_path_output = os.path.join(output_folder, per_audio_dir)

        os.makedirs(per_audio_dir_path_output)

        chunk_dirs = os.listdir(per_audio_dir_path)
        chunk_dirs = [d for d in chunk_dirs if not d.startswith('.')]

        for per_chunk_dir in chunk_dirs:
            per_chunk_dir_path = os.path.join(per_audio_dir_path, per_chunk_dir)
            per_chunk_dir_path_output = os.path.join(per_audio_dir_path_output, per_chunk_dir)

            os.makedirs(per_chunk_dir_path_output)

            spectrograms = os.listdir(per_chunk_dir_path)
            spectrograms = [s for s in spectrograms if not s.startswith('.')]

            for spectrogram in spectrograms:
                spectrogram_path = os.path.join(per_chunk_dir_path, spectrogram)
                spectrogram_path_output = os.path.join(per_chunk_dir_path_output, spectrogram)

                spec = Image.open(spectrogram_path)
                spec = spec.resize(new_size, resample=Image.LANCZOS)
                spec.save(spectrogram_path_output)

if __name__ == '__main__':
    main()
