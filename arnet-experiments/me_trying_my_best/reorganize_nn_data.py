import pandas as pd
import os
import argparse
import shutil

classifiers = {}
classifiers['n'] = 'no_stutter'
classifiers['s'] = 'sound_repetition'
classifiers['w'] = 'word_repetition'
classifiers['p'] = 'prolongation'
classifiers['r'] = 'revision'
classifiers['i'] = 'interjection'
classifiers['ph'] = 'phrase_repetition'

bad_chunks = {}

def reorg(label_folder, spectrogram_folder, output_folder, bad_chunks_path=''):
    label_file_map = {}

    for f in os.listdir(label_folder):
        if f.endswith('.csv'):
            temp = f.split('.')[0].split('_')[1:-1]
            audio_file = '_'.join(temp)
            label_file_map[audio_file] = os.path.join(label_folder, f)

    per_audio_dirs = os.listdir(spectrogram_folder)
    per_audio_dirs = [d for d in per_audio_dirs if not d.startswith('.')]

    for per_audio_dir in per_audio_dirs:
        per_audio_dir_path = os.path.join(spectrogram_folder, per_audio_dir)

        if per_audio_dir not in label_file_map:
            print('Could not find the labelled .csv file for ' + per_audio_dir)
            continue

        raw_data = pd.read_csv(label_file_map[per_audio_dir], usecols=[2,3,5], header=0)
        start_times = list(raw_data['start_time'])
        end_times = list(raw_data['end_time'])
        stutter_types = list(raw_data['stutter_type'])

        chunk_dirs = os.listdir(per_audio_dir_path)
        chunk_dirs = [d for d in chunk_dirs if not d.startswith('.')]
        chunk_dirs = sorted(chunk_dirs, key=lambda d: int(d.split('_')[-1]))

        chunk_size_ms = 1000000 # Big number
        if len(chunk_dirs) > 1:
            t0 = int(chunk_dirs[0].split('_')[-1])
            t1 = int(chunk_dirs[1].split('_')[-1])
            chunk_size_ms = t1 - t0
        elif len(chunk_dirs) == 0:
            print('Whoops')
            return

        csv_index = 0
        for per_chunk_dir in chunk_dirs:
            stutter_classifications = {}
            per_chunk_dir_path = os.path.join(per_audio_dir_path, per_chunk_dir)
            chunk_start_time_ms = int(per_chunk_dir.split('_')[-1])
            chunk_end_time_ms = chunk_start_time_ms + chunk_size_ms

            if per_chunk_dir is chunk_dirs[-1]:
                # Rewind for last chunk because it is shifted to fit
                current_start_time_ms = int(start_times[csv_index] * 1000)
                while (current_start_time_ms > chunk_start_time_ms):
                    csv_index -= 1
                    current_start_time_ms = int(start_times[csv_index] * 1000)
                csv_index += 1

            total_labels = 0
            while csv_index < len(end_times):
                end_time_ms = int(end_times[csv_index] * 1000)
                if end_time_ms > chunk_end_time_ms:
                    break

                types = stutter_types[csv_index].split(',')
                types = [t.strip() for t in types]
                for t in types:
                    if t and t != 'n':
                        if t not in stutter_classifications:
                            stutter_classifications[t] = 1
                        else:
                            stutter_classifications[t] += 1

                csv_index += 1
                total_labels += 1

            if per_chunk_dir in bad_chunks:
                print('Skipping bad chunk: %s' % per_chunk_dir)
                continue
            
            if len(stutter_classifications.keys()) == 0:
                shutil.copytree(per_chunk_dir_path, os.path.join(classifiers['n'], per_chunk_dir))
            else:
                for key in stutter_classifications:
                    if key in classifiers:
                        #shutil.copytree(per_chunk_dir_path, os.path.join(classifiers[key], '%s_%dof%d' % (per_chunk_dir, stutter_classifications[key], total_labels)))
                        shutil.copytree(per_chunk_dir_path, os.path.join(classifiers[key], per_chunk_dir))
                    else:
                        print('Yikes')
                        import pdb; pdb.set_trace()

def main():
    custom_formatter = lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position=100)
    p = argparse.ArgumentParser(formatter_class=custom_formatter)

    p.add_argument('-l', '--labels', type=str, required=True, help='Specify the folder with the labelled .xlsx files')
    p.add_argument('-s', '--spectrograms', type=str, required=True, help='Specify the folder with the spectrograms')
    p.add_argument('-o', '--output', type=str, required=True, help='Specify the output folder')
    p.add_argument('--bad-chunks', type=str, required=False, help='Specify the path to a comma-separated list of bad chunks to avoid')

    args = p.parse_args()

    label_folder = os.path.expanduser(args.labels)
    spectrogram_folder = os.path.expanduser(args.spectrograms)
    output_folder = os.path.expanduser(args.output)

    if args.bad_chunks:
        with open(args.bad_chunks, 'r') as bcf:
            bchunks = bcf.read()
            bchunks = bchunks.split('\n')
            bchunks = [c.split('/')[-1] for c in bchunks]
            for c in bchunks:
                bad_chunks[c] = True

    if not os.path.exists(label_folder):
        print('Labelled stutter folder does not exist: ' + label_folder)
        return
    if not os.path.exists(spectrogram_folder):
        print('Spectrogram folder does not exist: ' + spectrogram_folder)
        return
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for key in classifiers:
        classifiers[key] = os.path.join(output_folder, classifiers[key])
        if not os.path.exists(classifiers[key]):
            os.makedirs(classifiers[key])

    reorg(label_folder, spectrogram_folder, output_folder)

if __name__ == '__main__':
    main()
