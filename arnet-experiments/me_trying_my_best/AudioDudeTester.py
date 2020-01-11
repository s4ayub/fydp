import AudioDude
import signal
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading
import datetime as dt
import sys
import time
import scipy.signal
import scipy.io.wavfile as wavfile
import argparse
from filtersuite import bpf

def print_data(in_data):
    data = np.frombuffer(in_data, dtype=np.int16)
    print(data)

class AudioDudeTester:
    def __init__(self):
        self.ad = AudioDude.AudioDude()
        self.data_lock = threading.Lock()
        self.sampling_frequency = 44100
        self.frames_per_buffer = 1024

        # Graphing
        self.ys = []
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)

        # Recording
        self.filepath = None
        self.timeout = 10
        self.recorded_data = []

        # Filtering
        self.enable_filtering = False
        self.lowf = None
        self.highf = None
        self.f_order = None

    def print_mic_byte_stream(self):
        self.ad.start_mic_input_stream(num_channels=1, sampling_rate=self.sampling_frequency, num_frames_per_buffer=self.frames_per_buffer, callback=print_data)
        signal.pause()

    def graph_mic_byte_stream_animate(self, i, xs, ys):
        if self.ad.stream and len(self.ys):
            self.data_lock.acquire()
            data = self.ys
            self.data_lock.release()
            if self.enable_filtering:
                data = bpf(data, fs=self.sampling_frequency, lowf=self.lowf, highf=self.highf, order=self.f_order)
            self.ax.clear()
            self.ax.plot(data)
            self.ax.set_yticks(range(-255, 255, 500))

    def graph_mic_byte_stream_callback(self, in_data):
        self.data_lock.acquire()
        self.ys = np.frombuffer(in_data, dtype=np.int16).tolist()
        self.data_lock.release()

    def graph_mic_byte_stream(self):
        ani = animation.FuncAnimation(self.fig, self.graph_mic_byte_stream_animate, fargs=(None, self.ys), interval=1)
        self.ad.start_mic_input_stream(num_channels=1, sampling_rate=self.sampling_frequency, num_frames_per_buffer=self.frames_per_buffer, callback=self.graph_mic_byte_stream_callback)
        plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
        plt.show()

    def record_mic_byte_stream_callback(self, in_data):
        data = np.frombuffer(in_data, dtype=np.int16).tolist()
        if self.enable_filtering:
            data = bpf(data, fs=self.sampling_frequency, lowf=self.lowf, highf=self.highf, order=self.f_order).tolist()
        self.recorded_data += data

    def record_mic_byte_stream(self):
        timeout = 10
        print("Entered recording mode with filepath='{0}' and timeout={1}s".format(self.filepath, timeout))
        self.ad.start_mic_input_stream(num_channels=1, sampling_rate=self.sampling_frequency, num_frames_per_buffer=self.frames_per_buffer, callback=self.record_mic_byte_stream_callback)
        signal.alarm(timeout)
        input("Press enter to stop recording.\n")
        signal.alarm(0)
        self.ad.stop_mic_input_stream()
        data = np.array(self.recorded_data)
        data = data.astype(np.int16)
        wavfile.write(self.filepath, self.sampling_frequency, data)

    def play_wav_file(self, filepath):
        print("Entered playback mode with filepath='{0}'\n".format(self.filepath))
        self.ad.play_wav_file(filepath)

    def loopback(self):
        filepath = '_loopback.wav'
        print("Entered loopback mode\n")
        while True:
            timeout = 10
            self.ad.start_mic_input_stream(num_channels=1, sampling_rate=self.sampling_frequency, num_frames_per_buffer=self.frames_per_buffer, callback=self.record_mic_byte_stream_callback)
            signal.alarm(timeout)
            input("Recording mode... Press enter for playback mode.")
            signal.alarm(0)
            self.ad.stop_mic_input_stream()
            data = np.array(self.recorded_data)
            data = data.astype(np.int16)
            wavfile.write(filepath, self.sampling_frequency, data)
            self.recorded_data = []

            print("Playback mode...", end='')
            self.ad.play_wav_file(filepath)
            input("Press enter for recording mode")

def main():
    mode_choices = ['print','graph','record','play', 'loopback']
    default_filter_specs = '2000,12000,3'

    custom_formatter = lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position=100)
    p = argparse.ArgumentParser(formatter_class=custom_formatter)

    p.add_argument('-m', '--mode', type=str, required=True, choices=mode_choices, metavar='print/graph/record/play', help="specify mode: " + str(mode_choices))
    p.add_argument('-f', '--filter', type=str, nargs='?', const=default_filter_specs, metavar='LOW,HIGH,ORDER', help="enable bandpass filtering")
    p.add_argument('-p', '--path', type=str, help="specify path for recording output / file playback")

    args = p.parse_args()
    tester = AudioDudeTester()

    if args.filter:
        filter_specs = list(map(int, args.filter.split(',')))
        if len(filter_specs) is not 3:
            print("Must specify filter specs with LOW,HIGH,ORDER -- e.g. -f 20,20000,3")
            return
        tester.lowf = filter_specs[0]
        tester.highf = filter_specs[1]
        tester.f_order = filter_specs[2]
        tester.enable_filtering = True
        print("\nEnabled bandpass filtering: {0}hz-{1}hz, filter order {2}".format(tester.lowf, tester.highf, tester.f_order))

    if args.path:
       tester.filepath = args.path

    print("")

    if args.mode == 'print':
        tester.print_mic_byte_stream() 
    elif args.mode == 'graph':
        tester.graph_mic_byte_stream()
    elif args.mode == 'record':
        if not args.path:
            print("For recording mode, must specify output filepath -- e.g. -m record -p recording.wav")
            return
        tester.record_mic_byte_stream()
    elif args.mode == 'play':
        if not args.path:
            print("For playback mode, must specify input filepath -- e.g. -m play -p recording.wav")
            return
        tester.play_wav_file(tester.filepath) # Implement bandpass filtering for this mode
    elif args.mode == 'loopback':
        tester.loopback()

if __name__ == "__main__":
    main()
