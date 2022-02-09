import threading
import wave
import time
import pyaudio
from threading import Thread
from pedalboard import (
    Pedalboard,
    Gain,
    Compressor,
)
import numpy
import librosa
from scipy.signal import butter, lfilter
import pyAudioDspTools

pyAudioDspTools.sampling_rate = 44100
pyAudioDspTools.chunk_size = 4096


class PyAudioFile(Thread):
    def __init__(self):
        Thread.__init__(self)
        self._play = threading.Event()
        self._stop = threading.Event()
        self.sample_width = None
        self.channels = None
        self.rate = None
        self.second = None
        self.output = None
        self.fname = None
        self.stream = None
        self.muted = False
        self.stared = False
        self.thd = 0
        self.rto = 1
        self.att = 1
        self.rel = 100
        self.pitch = 0
        self.gain1 = 0
        self.gain2 = 0
        self.gain3 = 0
        self.gain4 = 0
        self.gain5 = 0
        self.board_gain = Pedalboard([], sample_rate=pyAudioDspTools.sampling_rate)
        self.board_compressor = Pedalboard([], sample_rate=pyAudioDspTools.sampling_rate)
        self.pyaudio_instance = pyaudio.PyAudio()

    def mute(self):
        return self.muted

    def set_mute(self, value):
        if value == 1:
            self.muted = True
        elif value == 0:
            self.muted = False

    def set_pitch(self, value):
        """
        Set pitch value
        :param value: int
        :return: None
        """
        self.pitch = value

    def play(self):
        """
        Start stream, clear stop flag and set play flag
        :return: None
        """
        if not self.muted:
            self.stream.start_stream()
            self._stop.clear()
            self._play.set()

    def played(self):
        """
        Retrun play flag state
        :return: bool
        """
        return self._play.is_set()

    def stop(self):
        """
        Stop stream and set stop flag
        :return: None
        """
        self.stream.stop_stream()
        self._stop.set()

    def stopped(self):
        """
        Return stop flag state
        :return: bool
        """
        return self._stop.is_set()

    def close(self):
        if self.stream:
            self._stop.set()
            time.sleep(0.2)
            self._play.set()
            time.sleep(0.2)
            wf.close()
            self.stream.close()

    def set_fname(self, name):
        """
        Set file name
        :param name:
        :return: None
        """
        self.fname = name

    def output_changer(self, output_name):
        """
        Change current output device
        :param output_name:
        :return: None
        """
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

    def set_compressor(self, thd, rto, att, rel):
        self.thd = thd
        self.rto = rto
        self.att = att
        self.rel = rel
        self.board_compressor[0] = Compressor(threshold_db=self.thd, ratio=self.rto, attack_ms=self.att, release_ms=self.rel)

    def compressor(self, value):
        if value == 1:
            self.board_compressor.append(Compressor(threshold_db=self.thd, ratio=self.rto, attack_ms=self.att, release_ms=self.rel))
        elif value == 0:
            self.board_compressor.pop(0)

    def set_gain(self, value):
        if len(self.board_gain) > 0:
             self.board_gain[0] = Gain(gain_db=value)

    def pitch_shifting(self, in_data, pitch):
        self.pitch = pitch
        in_data = librosa.effects.pitch_shift(in_data, pyAudioDspTools.sampling_rate, n_steps=self.pitch, n_fft=2048)
        in_data = pyAudioDspTools.VolumeChange(in_data, -4)
        return in_data

    def run(self):
        self.play_init

    @property
    def play_init(self):
        self.board_gain.append(Gain(gain_db=0))

        def callback(in_data, frame_count, time_info, status):
            try:
                data = wf.readframes(frame_count)
                data = numpy.frombuffer(data, dtype=numpy.int16)
                data = self.board_gain(data)
                data = self.board_compressor(data)
                data = self.equalizer_5band(data, int(self.rate))
                data = (data.astype('float32') / 32768)
                if len(self.board_compressor) <= 1:
                    data = pyAudioDspTools.VolumeChange(data, -16)
                data = self.pitch_shifting(data, self.pitch)
                return data, pyaudio.paContinue
            except Exception as e:
                print(e)

        if self.fname:
            global wf
            wf = wave.open(self.fname, 'rb')
            self.sample_width = wf.getsampwidth()
            self.channels = wf.getnchannels()
            self.rate = wf.getframerate()
            self.second = self.sample_width * self.channels * self.rate
            self.stream = self.pyaudio_instance.open(format=pyaudio.paFloat32,
                                                     channels=self.channels,
                                                     rate=int(self.rate),
                                                     frames_per_buffer=pyAudioDspTools.chunkA_size,
                                                     output=True,
                                                     output_device_index=self.output,
                                                     stream_callback=callback,
                                                     start=False)
            print(self.stream)
            while self.played():
                time.sleep(0.1)
                while self.stream.is_active():
                    print("stream")
                    if self._stop.is_set():
                        print("stop")
                        break
                    time.sleep(0.1)
                break

    def equalizer_5band(self, data, fs):
        band1 = bandpass_filter(data, 33, 119, fs, order=0) * 10 ** (self.gain1 / 20)
        band2 = bandpass_filter(data, 120, 474, fs, order=0) * 10 ** (self.gain2 / 20)
        band3 = bandpass_filter(data, 475, 1897, fs, order=0) * 10 ** (self.gain3 / 20)
        band4 = bandpass_filter(data, 1898, 6588, fs, order=0) * 10 ** (self.gain4 / 20)
        band5 = bandpass_filter(data, 6589, 20000, fs, order=0) * 10 ** (self.gain5 / 20)
        signal = band1 + band2 + band3 + band4 + band5
        return signal

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
