import threading
from pedalboard import (
    Pedalboard,
    Gain,
    Limiter,
    Compressor,
)
import librosa
import pyaudio
import pyAudioDspTools
import time
import numpy
from threading import Thread
from scipy.signal import butter, lfilter

pyAudioDspTools.sampling_rate = 44100
pyAudioDspTools.chunk_size = 4096


class PyAudioThreading(Thread):
    def __init__(self):
        Thread.__init__(self)
        self._stop = threading.Event()
        self._play = threading.Event()
        self.input = None
        self.output = None
        self.stream = None
        self.muted = False
        self.thd = 0
        self.rto = 1
        self.att = 1.0
        self.rel = 100
        self.rs = 0.5
        self.dp = 0.5
        self.dly = False
        self.gain1 = 0
        self.gain2 = 0
        self.gain3 = 0
        self.gain4 = 0
        self.gain5 = 0
        self.filter = pyAudioDspTools.CreateDelay(time_in_ms=1000, feedback_loops=5)
        self.pitch = 0
        self.fl = 2
        self.li = 10
        self.board_gain = Pedalboard([], sample_rate=pyAudioDspTools.sampling_rate)
        self.board_compressor = Pedalboard([], sample_rate=pyAudioDspTools.sampling_rate)
        self.board_limiter = Pedalboard([], sample_rate=pyAudioDspTools.sampling_rate)
        self.pyaudio_instance = pyaudio.PyAudio()

    def run(self):
        self.stream_init()

    def pitch_shifting(self, in_data, pitch):
        self.pitch = pitch
        data = librosa.effects.pitch_shift(in_data, pyAudioDspTools.sampling_rate, n_steps=self.pitch)
        data = pyAudioDspTools.VolumeChange(data, -8)
        return data

    def stream_init(self):
        info = self.pyaudio_instance.get_host_api_info_by_index(0)
        num_devices = info.get('deviceCount')
        if self.output is None:
            for i in range(0, num_devices):
                if self.pyaudio_instance.get_device_info_by_host_api_device_index(0, i).get('maxOutputChannels') > 0:
                    if self.pyaudio_instance.get_device_info_by_host_api_device_index(0, i).\
                            get('name') == 'CABLE Input (VB-Audio Virtual C':
                        self.output = i


        self.board_gain.append(Gain(gain_db=0))

        def callback(in_data, frame_count, time_info, status):
            try:
                in_data = numpy.frombuffer(in_data, dtype=numpy.float32)
                in_data = self.board_gain(in_data)
                in_data = self.equalizer_5band(in_data, int(pyAudioDspTools.sampling_rate))
                in_data = self.pitch_shifting(in_data, self.pitch)
                in_data = self.board_limiter(in_data)
                in_data = self.board_compressor(in_data)
                if self.dly:
                    in_data = self.filter.apply(in_data)
                return in_data, pyaudio.paContinue
            except Exception as e:
                print(e)

        self.stream = self.pyaudio_instance.open(format=pyaudio.paFloat32,
                                                 channels=1,
                                                 rate=pyAudioDspTools.sampling_rate,
                                                 input=True,
                                                 output=True,
                                                 frames_per_buffer=pyAudioDspTools.chunk_size,
                                                 stream_callback=callback,
                                                 input_device_index=self.input,
                                                 output_device_index=self.output,
                                                 start=False)

        # print(self.stream)
        while self.played():
            time.sleep(0.1)
            while self.stream.is_active():
                if self._stop.is_set():
                    print("stop")
                    break
                time.sleep(0.1)
            break

    def set_compressor(self, thd, rto, att, rel):
        self.thd = thd
        self.rto = rto
        self.att = att
        self.rel = rel
        self.board_compressor[0] = Compressor(threshold_db=thd, ratio=rto, attack_ms=att, release_ms=rel)

    def compressor(self, value):
        if value == 1:
            self.board_compressor.append(Compressor(threshold_db=self.thd, ratio=self.rto, attack_ms=self.att, release_ms=self.rel))
            print(self.board_compressor)
        elif value == 0:
            self.board_compressor.pop(0)
            print(self.board_compressor)

    def delay(self, value):
        if value == 1:
            self.dly = True
        elif value == 0:
            self.dly = False

    def set_delay(self, tim, fl):
        self.filter.set_param(time_in_ms=tim, feedback_loops=fl)

    def set_limiter(self, value):
        self.li = value
        self.board_limiter[0] = Limiter(threshold_db=value)

    def limiter(self, value):
        if value == 1:
            self.board_limiter.append(Limiter(threshold_db=self.li))
        elif value == 0:
            self.board_limiter.pop(0)

    def mute(self):
        return self.muted

    def set_mute(self, value):
        if value == 1:
            self.muted = True
            self.stop()
        elif value == 0:
            self.muted = False
            self.play()

    def stop(self):
        self.stream.stop_stream()
        self._stop.set()

    def stopped(self):
        return self._stop.is_set()

    def play(self):
        if not self.muted:
            print("asd")
            self.stream.start_stream()
            self._stop.clear()
            self._play.set()

    def played(self):
        return self._play.is_set()

    def close(self):
        self._stop.set()
        time.sleep(0.2)
        self._play.set()
        time.sleep(0.2)
        self.stream.close()

    def available_channel_outputs(self):
        info = self.pyaudio_instance.get_host_api_info_by_index(0)
        num_devices = info.get('deviceCount')
        # for each audio device, determine if its an output
        for i in range(0, num_devices):
            if self.pyaudio_instance.get_device_info_by_host_api_device_index(0, i).get('maxOutputChannels') > 0:
                print("Output Device id ", i, " - ",
                      self.pyaudio_instance.get_device_info_by_host_api_device_index(0, i).get('name'))

    def input_changer(self, input_name):
        info = self.pyaudio_instance.get_host_api_info_by_index(0)
        num_devices = info.get('deviceCount')
        inputs = []
        # for each audio device, determine if its an input
        for i in range(0, num_devices):
            if self.pyaudio_instance.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels') > 0:
                inputs += [[self.pyaudio_instance.get_device_info_by_host_api_device_index(0, i).get('name'), int(i)]]
        for i in inputs:
            if i[0] == input_name:
                self.input = i[1]

    def output_changer(self, output_name):
        info = self.pyaudio_instance.get_host_api_info_by_index(0)
        num_devices = info.get('deviceCount')
        outputs = []
        # for each audio device, determine if its an output
        for i in range(0, num_devices):
            if self.pyaudio_instance.get_device_info_by_host_api_device_index(0, i).get('maxOutputChannels') > 0:
                outputs += [[self.pyaudio_instance.get_device_info_by_host_api_device_index(0, i).get('name'), int(i)]]
        for i in outputs:
            if i[0] == output_name:
                self.output = i[1]

    def equalizer_5band(self, data, fs):
        band1 = bandpass_filter(data, 33, 119, fs, order=0) * 10 ** (self.gain1 / 20)
        band2 = bandpass_filter(data, 120, 474, fs, order=0) * 10 ** (self.gain2 / 20)
        band3 = bandpass_filter(data, 475, 1897, fs, order=0) * 10 ** (self.gain3 / 20)
        band4 = bandpass_filter(data, 1898, 6588, fs, order=0) * 10 ** (self.gain4 / 20)
        band5 = bandpass_filter(data, 6589, 20000, fs, order=0) * 10 ** (self.gain5 / 20)
        filtered = band1 + band2 + band3 + band4 + band5
        return filtered

    def set_gain(self, value):
        self.board_gain[0] = Gain(gain_db=value)

    def set_pitch(self, value):
        self.pitch = value

    def set_gain1(self, value):
        self.gain1 = value

    def set_gain2(self, value):
        self.gain2 = value

    def set_gain3(self, value):
        self.gain3 = value

    def set_gain4(self, value):
        self.gain4 = value

    def set_gain5(self, value):
        self.gain5 = value


def bandpass_filter(data, lowcut, highcut, fs, order=0):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='bandpass')
    filtered = lfilter(b, a, data)
    return filtered
