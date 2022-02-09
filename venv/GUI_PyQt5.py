from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QPushButton, QFileDialog, QLabel
from pathlib import Path
import sys
import pyaudio
from pyAudioThread import PyAudioThreading
from pyAudioFilePlayer import PyAudioFile


def input_devices():
    py = pyaudio.PyAudio()
    info = py.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')
    inputs = []
    inputs += [""]
    # for each audio device, determine if its an input and add it to the list and dictionary
    for i in range(0, num_devices):
        if py.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels') > 0:
            inputs += [py.get_device_info_by_host_api_device_index(0, i).get('name')]
    # print(inputs)
    return inputs


def output_devices():
    py = pyaudio.PyAudio()
    info = py.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')
    outputs = []
    outputs += [""]
    # for each audio device, determine if its an input and add it to the list and dictionary
    for i in range(0, num_devices):
        if py.get_device_info_by_host_api_device_index(0, i).get('maxOutputChannels') > 0:
            outputs += [py.get_device_info_by_host_api_device_index(0, i).get('name')]
    # print(outputs)
    return outputs


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super(MainWindow, self).__init__()
        # Load the .ui file
        uic.loadUi("mainWindow.ui", self)
        width = 800
        height = 755
        # setting  the fixed size of window
        self.setFixedSize(width, height)
        # Show the GUI
        self.show()
        # Read available inputs and outputs
        inputs_name = input_devices()
        output_names = output_devices()
        # input comboBox configuration
        self.comboBox_input_1.addItems(inputs_name)
        self.comboBox_input_2.addItems(inputs_name)
        self.comboBox_input_1.activated[str].connect(lambda: self.on_input_changed("combo_in_1"))
        self.comboBox_input_2.activated[str].connect(lambda: self.on_input_changed("combo_in_2"))
        # output comboBox configuration
        self.comboBox_out_1.addItems(output_names)
        self.comboBox_out_2.addItems(output_names)
        self.comboBox_out_1.activated[str].connect(lambda: self.on_output_changed("combo_out_1"))
        self.comboBox_out_2.activated[str].connect(lambda: self.on_output_changed("combo_out_2"))
        # mute buttons configuration
        self.mute_input_1.setCheckable(True)
        self.mute_input_1.clicked.connect(lambda: self.mute('mute_1'))
        self.mute_input_2.setCheckable(True)
        self.mute_input_2.clicked.connect(lambda: self.mute('mute_2'))
        self.mute_input_2.setCheckable(True)
        self.mute_input_3.clicked.connect(lambda: self.mute('mute_3'))
        self.mute_input_3.setCheckable(True)
        # gain sliders configuration
        self.gain_slider_in_1.valueChanged.connect(lambda: self.slider("slider_1"))
        self.gain_slider_in_2.valueChanged.connect(lambda: self.slider("slider_2"))
        self.gain_slider_in_3.valueChanged.connect(lambda: self.slider("slider_3"))
        # pitch sliders configuration
        self.pitch_slider_in_1.valueChanged.connect(lambda: self.slider("pitch_1"))
        self.pitch_slider_in_2.valueChanged.connect(lambda: self.slider("pitch_2"))
        self.pitch_slider_in_3.valueChanged.connect(lambda: self.slider("pitch_3"))
        # single mode buttons configuration
        self.single_in_1.setCheckable(True)
        self.single_in_1.clicked.connect(lambda: self.single('single_1'))
        self.single_in_2.setCheckable(True)
        self.single_in_2.clicked.connect(lambda: self.single('single_2'))
        self.single_in_3.setCheckable(True)
        self.single_in_3.clicked.connect(lambda: self.single('single_3'))
        # A , B output configuration
        self.toggleButton_output_a_1.setCheckable(True)
        self.toggleButton_output_a_1.clicked.connect(lambda: self.output('out_a_1'))
        self.toggleButton_output_a_2.setCheckable(True)
        self.toggleButton_output_a_2.clicked.connect(lambda: self.output('out_a_2'))
        self.toggleButton_output_b_1.setCheckable(True)
        self.toggleButton_output_b_1.clicked.connect(lambda: self.output('out_b_1'))
        self.toggleButton_output_b_2.setCheckable(True)
        self.toggleButton_output_b_2.clicked.connect(lambda: self.output('out_b_2'))
        # compressor dial configuration
        self.compressor_threshold_db_1.valueChanged.connect(lambda: self.compressor_dial("compressor_threshold_db_1"))
        self.compressor_threshold_db_1.setEnabled(False)
        self.compressor_threshold_db_2.valueChanged.connect(lambda: self.compressor_dial("compressor_threshold_db_2"))
        self.compressor_threshold_db_2.setEnabled(False)
        # self.compressor_threshold_db_3.valueChanged.connect(lambda: self.compressor_dial("compressor_threshold_db_3"))
        # self.compressor_threshold_db_3.setEnabled(False)
        self.compressor_ratio_1.valueChanged.connect(lambda: self.compressor_dial("compressor_ratio_1"))
        self.compressor_ratio_1.setEnabled(False)
        self.compressor_ratio_2.valueChanged.connect(lambda: self.compressor_dial("compressor_ratio_2"))
        self.compressor_ratio_2.setEnabled(False)
        # self.compressor_ratio_3.valueChanged.connect(lambda: self.compressor_dial("compressor_ratio_3"))
        # self.compressor_ratio_3.setEnabled(False)
        self.compressor_attack_1.valueChanged.connect(lambda: self.compressor_dial("compressor_attack_1"))
        self.compressor_attack_1.setEnabled(False)
        self.compressor_attack_2.valueChanged.connect(lambda: self.compressor_dial("compressor_attack_2"))
        self.compressor_attack_2.setEnabled(False)
        # self.compressor_attack_3.valueChanged.connect(lambda: self.compressor_dial("compressor_attack_3"))
        # self.compressor_attack_3.setEnabled(False)
        self.compressor_release_1.valueChanged.connect(lambda: self.compressor_dial("compressor_release_1"))
        self.compressor_release_1.setEnabled(False)
        self.compressor_release_2.valueChanged.connect(lambda: self.compressor_dial("compressor_release_2"))
        self.compressor_release_2.setEnabled(False)
        # self.compressor_release_3.valueChanged.connect(lambda: self.compressor_dial("compressor_release_3"))
        # self.compressor_release_3.setEnabled(False)
        # compressor mode buttons configuration
        self.compressorButton_1.setCheckable(True)
        self.compressorButton_1.clicked.connect(lambda: self.compressor('compressorButton_1'))
        self.compressorButton_2.setCheckable(True)
        self.compressorButton_2.clicked.connect(lambda: self.compressor('compressorButton_2'))
        # self.compressorButton_3.setCheckable(True)
        # self.compressorButton_3.clicked.connect(lambda: self.compressor('compressorButton_3'))
        # Delay mode buttons configuration
        self.delayButton_1.setCheckable(True)
        self.delayButton_1.clicked.connect(lambda: self.delay('delayButton_1'))
        self.delayButton_2.setCheckable(True)
        self.delayButton_2.clicked.connect(lambda: self.delay('delayButton_2'))
        #
        self.delay_time_dial_1.valueChanged.connect(lambda: self.delay_dial("delay_time_dial_1"))
        self.delay_time_dial_1.setEnabled(False)
        self.delay_loops_dial_1.valueChanged.connect(lambda: self.delay_dial("delay_loops_dial_1"))
        self.delay_loops_dial_1.setEnabled(False)
        self.delay_time_dial_2.valueChanged.connect(lambda: self.delay_dial("delay_time_dial_2"))
        self.delay_time_dial_2.setEnabled(False)
        self.delay_loops_dial_2.valueChanged.connect(lambda: self.delay_dial("delay_loops_dial_2"))
        self.delay_loops_dial_2.setEnabled(False)
        # Limiter dial configuration
        self.limiter_dial_1.valueChanged.connect(lambda: self.limiter_dial("limiter_dial_1"))
        self.limiter_dial_1.setEnabled(False)
        self.limiter_dial_2.valueChanged.connect(lambda: self.limiter_dial("limiter_dial_2"))
        self.limiter_dial_2.setEnabled(False)
        # Limiter mode buttons configuration
        self.limiterButton_1.setCheckable(True)
        self.limiterButton_1.clicked.connect(lambda: self.limiter('limiterButton_1'))
        self.limiterButton_2.setCheckable(True)
        self.limiterButton_2.clicked.connect(lambda: self.limiter('limiterButton_2'))
        # slider_band configuration
        self.band_slider_1.valueChanged.connect(lambda: self.slider_band("band_slider_1"))
        self.band_slider_2.valueChanged.connect(lambda: self.slider_band("band_slider_2"))
        self.band_slider_3.valueChanged.connect(lambda: self.slider_band("band_slider_3"))
        self.band_slider_4.valueChanged.connect(lambda: self.slider_band("band_slider_4"))
        self.band_slider_5.valueChanged.connect(lambda: self.slider_band("band_slider_5"))
        self.band_slider_6.valueChanged.connect(lambda: self.slider_band("band_slider_6"))
        self.band_slider_7.valueChanged.connect(lambda: self.slider_band("band_slider_7"))
        self.band_slider_8.valueChanged.connect(lambda: self.slider_band("band_slider_8"))
        self.band_slider_9.valueChanged.connect(lambda: self.slider_band("band_slider_9"))
        self.band_slider_10.valueChanged.connect(lambda: self.slider_band("band_slider_10"))
        self.band_slider_11.valueChanged.connect(lambda: self.slider_band("band_slider_11"))
        self.band_slider_12.valueChanged.connect(lambda: self.slider_band("band_slider_12"))
        self.band_slider_13.valueChanged.connect(lambda: self.slider_band("band_slider_13"))
        self.band_slider_14.valueChanged.connect(lambda: self.slider_band("band_slider_14"))
        self.band_slider_15.valueChanged.connect(lambda: self.slider_band("band_slider_15"))
        # bind buttons configuration
        self.choose_button_1.clicked.connect(lambda: self.choose_file("choose_button_1"))
        self.play_button_1.clicked.connect(lambda: self.play_btn())
        self.stop_button_1.clicked.connect(lambda: self.stop_btn())

    def stop_btn(self):
        try:
            if fname:
                file_threads[0].stop()
        except Exception as e:
            print(e)

    def play_btn(self):
        try:
            if fname:
                file_threads[0].play()
        except Exception as e:
            print(e)

    def choose_file(self, name):
        try:
            # Open file dialog
            global fname
            fname = QFileDialog.getOpenFileName(self, "Open File", "C:\\Users\\Public\\Music", "wav Files (*.wav)")
            filename = Path(fname[0]).name
            if fname:
                file_threads[0].close()
                file_threads[0].set_fname(fname[0])
                file_threads[0].play_init
                self.play_button_label_1.setText(filename)
        except Exception as e:
            print(e)

    def compressor_dial(self, name):
        try:
            if name == "compressor_threshold_db_1":
                val_1 = self.compressor_threshold_db_1.value()
                val_2 = self.compressor_ratio_1.value()
                val_3 = self.compressor_attack_1.value()
                val_4 = self.compressor_release_1.value()
                stream_threads[0].set_compressor(val_1, val_2, val_3, val_4)
                stream_threads[1].set_compressor(val_1, val_2, val_3, val_4)
                self.compressor_threshold_db_label_1.setText(str(val_1))
            if name == "compressor_ratio_1":
                val_1 = self.compressor_threshold_db_1.value()
                val_2 = self.compressor_ratio_1.value()
                val_3 = self.compressor_attack_1.value()
                val_4 = self.compressor_release_1.value()
                stream_threads[0].set_compressor(val_1, val_2, val_3, val_4)
                stream_threads[1].set_compressor(val_1, val_2, val_3, val_4)
                self.compressor_ratio_label_1.setText(str(val_2))
            if name == "compressor_attack_1":
                val_1 = self.compressor_threshold_db_1.value()
                val_2 = self.compressor_ratio_1.value()
                val_3 = self.compressor_attack_1.value()
                val_4 = self.compressor_release_1.value()
                stream_threads[0].set_compressor(val_1, val_2, val_3, val_4)
                stream_threads[1].set_compressor(val_1, val_2, val_3, val_4)
                self.compressor_attack_label_1.setText(str(val_3))
            if name == "compressor_release_1":
                val_1 = self.compressor_threshold_db_1.value()
                val_2 = self.compressor_ratio_1.value()
                val_3 = self.compressor_attack_1.value()
                val_4 = self.compressor_release_1.value()
                stream_threads[0].set_compressor(val_1, val_2, val_3, val_4)
                stream_threads[1].set_compressor(val_1, val_2, val_3, val_4)
                self.compressor_release_label_1.setText(str(val_4))
            if name == "compressor_threshold_db_2":
                val_1 = self.compressor_threshold_db_2.value()
                val_2 = self.compressor_ratio_2.value()
                val_3 = self.compressor_attack_2.value()
                val_4 = self.compressor_release_2.value()
                stream_threads[2].set_compressor(val_1, val_2, val_3, val_4)
                stream_threads[3].set_compressor(val_1, val_2, val_3, val_4)
                self.compressor_threshold_db_label_2.setText(str(val_1))
            if name == "compressor_ratio_2":
                val_1 = self.compressor_threshold_db_2.value()
                val_2 = self.compressor_ratio_2.value()
                val_3 = self.compressor_attack_2.value()
                val_4 = self.compressor_release_2.value()
                stream_threads[2].set_compressor(val_1, val_2, val_3, val_4)
                stream_threads[3].set_compressor(val_1, val_2, val_3, val_4)
                self.compressor_ratio_label_2.setText(str(val_2))
            if name == "compressor_attack_2":
                val_1 = self.compressor_threshold_db_1.value()
                val_2 = self.compressor_ratio_1.value()
                val_3 = self.compressor_attack_1.value()
                val_4 = self.compressor_release_1.value()
                stream_threads[0].set_compressor(val_1, val_2, val_3, val_4)
                stream_threads[1].set_compressor(val_1, val_2, val_3, val_4)
                self.compressor_attack_label_2.setText(str(val_3))
            if name == "compressor_release_2":
                val_1 = self.compressor_threshold_db_1.value()
                val_2 = self.compressor_ratio_1.value()
                val_3 = self.compressor_attack_1.value()
                val_4 = self.compressor_release_1.value()
                stream_threads[0].set_compressor(val_1, val_2, val_3, val_4)
                stream_threads[1].set_compressor(val_1, val_2, val_3, val_4)
                self.compressor_release_label_2.setText(str(val_4))
            if name == "compressor_threshold_db_3":
                val_1 = self.compressor_threshold_db_3.value()
                val_2 = self.compressor_ratio_3.value()
                val_3 = self.compressor_attack_3.value()
                val_4 = self.compressor_release_3.value()
                print(val_1, val_2)
                file_threads[0].set_compressor(val_1, val_2, val_3, val_4)
                self.compressor_threshold_db_label_3.setText(str(val_1))
        except Exception as e:
            print(e)

    def compressor(self, name):
        try:
            if name == "compressorButton_1":
                if self.compressorButton_1.isChecked():
                    self.compressorButton_1.setStyleSheet("background-color : green")
                    self.compressor_threshold_db_1.setEnabled(True)
                    self.compressor_ratio_1.setEnabled(True)
                    self.compressor_release_1.setEnabled(True)
                    self.compressor_attack_1.setEnabled(True)
                    stream_threads[0].compressor(1)
                    stream_threads[1].compressor(1)
                else:
                    self.compressorButton_1.setStyleSheet("background-color : lightgrey")
                    self.compressor_threshold_db_1.setEnabled(False)
                    self.compressor_ratio_1.setEnabled(False)
                    self.compressor_release_1.setEnabled(False)
                    self.compressor_attack_1.setEnabled(False)
                    stream_threads[0].compressor(0)
                    stream_threads[1].compressor(0)
            if name == "compressorButton_2":
                if self.compressorButton_2.isChecked():
                    self.compressorButton_2.setStyleSheet("background-color : green")
                    self.compressor_threshold_db_2.setEnabled(True)
                    self.compressor_ratio_2.setEnabled(True)
                    self.compressor_release_2.setEnabled(True)
                    self.compressor_attack_2.setEnabled(True)
                    stream_threads[2].compressor(1)
                    stream_threads[3].compressor(1)
                else:
                    self.compressorButton_2.setStyleSheet("background-color : lightgrey")
                    self.compressor_threshold_db_2.setEnabled(False)
                    self.compressor_ratio_2.setEnabled(False)
                    self.compressor_release_2.setEnabled(False)
                    self.compressor_attack_2.setEnabled(False)
                    stream_threads[2].compressor(0)
                    stream_threads[3].compressor(0)
            if name == "compressorButton_3":
                if self.compressorButton_3.isChecked():
                    self.compressorButton_3.setStyleSheet("background-color : green")
                    self.compressor_threshold_db_3.setEnabled(True)
                    self.compressor_ratio_3.setEnabled(True)
                    self.compressor_release_3.setEnabled(True)
                    self.compressor_attack_3.setEnabled(True)
                    file_threads[0].compressor(1)
                else:
                    self.compressorButton_3.setStyleSheet("background-color : lightgrey")
                    self.compressor_threshold_db_3.setEnabled(False)
                    self.compressor_ratio_3.setEnabled(False)
                    self.compressor_release_3.setEnabled(False)
                    self.compressor_attack_3.setEnabled(False)
                    file_threads[0].compressor(0)
        except Exception as e:
            print(e)

    def delay(self, name):
        try:
            if name == "delayButton_1":
                if self.delayButton_1.isChecked():
                    self.delayButton_1.setStyleSheet("background-color : green")
                    self.delay_time_dial_1.setEnabled(True)
                    self.delay_loops_dial_1.setEnabled(True)
                    stream_threads[0].delay(1)
                    stream_threads[1].delay(1)
                else:
                    self.delayButton_1.setStyleSheet("background-color : lightgrey")
                    self.delay_time_dial_1.setEnabled(False)
                    self.delay_loops_dial_1.setEnabled(False)
                    stream_threads[0].delay(0)
                    stream_threads[1].delay(0)
            if name == "delayButton_2":
                if self.delayButton_2.isChecked():
                    self.delayButton_2.setStyleSheet("background-color : green")
                    self.delay_time_dial_2.setEnabled(True)
                    self.delay_loops_dial_2.setEnabled(True)
                    stream_threads[2].delay(1)
                    stream_threads[3].delay(1)
                else:
                    self.delayButton_2.setStyleSheet("background-color : lightgrey")
                    self.delay_time_dial_2.setEnabled(False)
                    self.delay_loops_dial_2.setEnabled(False)
                    stream_threads[2].delay(0)
                    stream_threads[3].delay(0)
        except Exception as e:
            print(e)

    def delay_dial(self, name):
        try:
            if name == "delay_time_dial_1":
                val_1 = self.delay_time_dial_1.value()
                val_2 = self.delay_loops_dial_1.value()
                stream_threads[0].set_delay(val_1, val_2)
                stream_threads[1].set_delay(val_1, val_2)
                self.delay_time_label_1.setText(str(val_1))
            if name == "delay_loops_dial_1":
                val_1 = self.delay_time_dial_1.value()
                val_2 = self.delay_loops_dial_1.value()
                stream_threads[0].set_delay(val_1, val_2)
                stream_threads[1].set_delay(val_1, val_2)
                self.delay_loops_label_1.setText(str(val_2))
            if name == "delay_time_dial_2":
                val_1 = self.delay_time_dial_2.value()
                val_2 = self.delay_loops_dial_2.value()
                stream_threads[0].set_delay(val_1, val_2)
                stream_threads[1].set_delay(val_1, val_2)
                self.delay_time_dial_2.setText(str(val_1))
            if name == "delay_loops_dial_2":
                val_1 = self.delay_time_dial_2.value()
                val_2 = self.delay_loops_dial_2.value()
                stream_threads[0].set_delay(val_1, val_2)
                stream_threads[1].set_delay(val_1, val_2)
                self.delay_loops_dial_2.setText(str(val_2))
        except Exception as e:
            print(e)

    def limiter_dial(self, name):
        try:
            if name == "limiter_dial_1":
                val = self.limiter_dial_1.value()
                stream_threads[0].set_limiter(val)
                stream_threads[1].set_limiter(val)
                self.limiter_value_label_1.setText(str(val))
            if name == "limiter_dial_2":
                val = self.limiter_dial_2.value()
                stream_threads[2].set_limiter(val)
                stream_threads[3].set_limiter(val)
                self.limiter_value_label_2.setText(str(val))
        except Exception as e:
            print(e)

    def limiter(self, name):
        try:
            if name == "limiterButton_1":
                if self.limiterButton_1.isChecked():
                    self.limiterButton_1.setStyleSheet("background-color : green")
                    self.limiter_dial_1.setEnabled(True)
                    stream_threads[0].limiter(1)
                    stream_threads[1].limiter(1)
                else:
                    self.limiterButton_1.setStyleSheet("background-color : lightgrey")
                    self.limiter_dial_1.setEnabled(False)
                    stream_threads[0].limiter(0)
                    stream_threads[1].limiter(0)
            if name == "limiterButton_2":
                if self.limiterButton_2.isChecked():
                    self.limiterButton_2.setStyleSheet("background-color : green")
                    self.limiter_dial_2.setEnabled(True)
                    stream_threads[2].limiter(1)
                    stream_threads[3].limiter(1)
                else:
                    self.limiterButton_2.setStyleSheet("background-color : lightgrey")
                    self.limiter_dial_2.setEnabled(False)
                    stream_threads[2].limiter(0)
                    stream_threads[3].limiter(0)
        except Exception as e:
            print(e)

    def slider_band(self, name):
        try:
            if name == "band_slider_1":
                val = self.band_slider_1.value()
                file_threads[0].set_gain1(val)
                self.label_band_1.setText(str(val))
            if name == "band_slider_2":
                val = self.band_slider_2.value()
                file_threads[0].set_gain2(val)
                self.label_band_2.setText(str(val))
            if name == "band_slider_3":
                val = self.band_slider_3.value()
                file_threads[0].set_gain3(val)
                self.label_band_3.setText(str(val))
            if name == "band_slider_4":
                val = self.band_slider_4.value()
                file_threads[0].set_gain4(val)
                self.label_band_4.setText(str(val))
            if name == "band_slider_5":
                val = self.band_slider_5.value()
                file_threads[0].set_gain5(val)
                self.label_band_5.setText(str(val))
            if name == "band_slider_6":
                val = self.band_slider_6.value()
                stream_threads[0].set_gain1(val)
                stream_threads[1].set_gain1(val)
                self.label_band_6.setText(str(val))
            if name == "band_slider_7":
                val = self.band_slider_7.value()
                stream_threads[0].set_gain2(val)
                stream_threads[1].set_gain2(val)
                self.label_band_7.setText(str(val))
            if name == "band_slider_8":
                val = self.band_slider_8.value()
                stream_threads[0].set_gain3(val)
                stream_threads[1].set_gain3(val)
                self.label_band_8.setText(str(val))
            if name == "band_slider_9":
                val = self.band_slider_9.value()
                stream_threads[0].set_gain4(val)
                stream_threads[1].set_gain4(val)
                self.label_band_9.setText(str(val))
            if name == "band_slider_10":
                val = self.band_slider_10.value()
                stream_threads[0].set_gain5(val)
                stream_threads[1].set_gain5(val)
                self.label_band_10.setText(str(val))
            if name == "band_slider_11":
                val = self.band_slider_11.value()
                stream_threads[2].set_gain1(val)
                stream_threads[3].set_gain1(val)
                self.label_band_11.setText(str(val))
            if name == "band_slider_12":
                val = self.band_slider_12.value()
                stream_threads[2].set_gain2(val)
                stream_threads[3].set_gain2(val)
                self.label_band_12.setText(str(val))
            if name == "band_slider_13":
                val = self.band_slider_13.value()
                stream_threads[2].set_gain3(val)
                stream_threads[3].set_gain3(val)
                self.label_band_13.setText(str(val))
            if name == "band_slider_14":
                val = self.band_slider_14.value()
                stream_threads[2].set_gain4(val)
                stream_threads[3].set_gain4(val)
                self.label_band_14.setText(str(val))
            if name == "band_slider_15":
                val = self.band_slider_15.value()
                stream_threads[2].set_gain5(val)
                stream_threads[3].set_gain5(val)
                self.label_band_15.setText(str(val))
        except Exception as e:
            print(e)

    def single(self, name):
        try:
            if name == "single_1":
                if self.single_in_1.isChecked():
                    self.single_in_2.setEnabled(False)
                    self.single_in_3.setEnabled(False)
                    self.mute_input_2.setEnabled(False)
                    self.mute_input_3.setEnabled(False)
                    self.toggleButton_output_a_2.setEnabled(False)
                    self.toggleButton_output_b_2.setEnabled(False)
                    stream_threads[2].stop()
                    stream_threads[3].stop()
                    file_threads[0].stop()
                    self.single_in_1.setStyleSheet("background-color : lightblue")
                else:
                    self.single_in_2.setEnabled(True)
                    self.single_in_3.setEnabled(True)
                    self.mute_input_2.setEnabled(True)
                    self.mute_input_3.setEnabled(True)
                    self.toggleButton_output_a_2.setEnabled(True)
                    self.toggleButton_output_b_2.setEnabled(True)
                    stream_threads[2].play()
                    stream_threads[3].play()
                    file_threads[0].play()
                    self.single_in_1.setStyleSheet("background-color : lightgrey")
            elif name == "single_2":
                if self.single_in_2.isChecked():
                    self.single_in_1.setEnabled(False)
                    self.single_in_3.setEnabled(False)
                    self.mute_input_1.setEnabled(False)
                    self.mute_input_3.setEnabled(False)
                    self.toggleButton_output_a_1.setEnabled(False)
                    self.toggleButton_output_b_1.setEnabled(False)
                    stream_threads[0].stop()
                    stream_threads[1].stop()
                    file_threads[0].stop()
                    self.single_in_2.setStyleSheet("background-color : lightblue")
                else:
                    self.single_in_1.setEnabled(True)
                    self.single_in_3.setEnabled(True)
                    self.mute_input_1.setEnabled(True)
                    self.mute_input_3.setEnabled(True)
                    self.toggleButton_output_a_1.setEnabled(True)
                    self.toggleButton_output_b_1.setEnabled(True)
                    stream_threads[0].play()
                    stream_threads[1].play()
                    file_threads[0].play()
                    self.single_in_2.setStyleSheet("background-color : lightgrey")
            elif name == "single_3":
                if self.single_in_3.isChecked():
                    self.single_in_1.setEnabled(False)
                    self.single_in_2.setEnabled(False)
                    self.mute_input_1.setEnabled(False)
                    self.mute_input_2.setEnabled(False)
                    self.toggleButton_output_a_1.setEnabled(False)
                    self.toggleButton_output_a_2.setEnabled(False)
                    self.toggleButton_output_b_1.setEnabled(False)
                    self.toggleButton_output_b_2.setEnabled(False)
                    stream_threads[0].stop()
                    stream_threads[1].stop()
                    stream_threads[2].stop()
                    stream_threads[3].stop()
                    self.single_in_3.setStyleSheet("background-color : lightblue")
                else:
                    self.single_in_1.setEnabled(True)
                    self.single_in_2.setEnabled(True)
                    self.mute_input_1.setEnabled(True)
                    self.mute_input_2.setEnabled(True)
                    self.toggleButton_output_a_1.setEnabled(True)
                    self.toggleButton_output_a_2.setEnabled(True)
                    self.toggleButton_output_b_1.setEnabled(True)
                    self.toggleButton_output_b_2.setEnabled(True)
                    stream_threads[0].play()
                    stream_threads[1].play()
                    stream_threads[2].play()
                    stream_threads[3].play()
                    self.single_in_3.setStyleSheet("background-color : lightgrey")
        except Exception as e:
            print(e)

    def output(self, name):
        try:
            if name == "out_a_1":
                if not self.mute_input_1.isChecked():
                    if self.toggleButton_output_a_1.isChecked():
                        stream_threads[0].set_mute(1)
                        self.toggleButton_output_a_1.setStyleSheet("background-color : lightblue")
                    else:
                        stream_threads[0].set_mute(0)
                        self.toggleButton_output_a_1.setStyleSheet("background-color : lightgrey")
            if name == "out_a_2":
                if not self.mute_input_2.isChecked():
                    if self.toggleButton_output_a_2.isChecked():
                        stream_threads[2].set_mute(1)
                        self.toggleButton_output_a_2.setStyleSheet("background-color : lightblue")
                    else:
                        stream_threads[2].set_mute(0)
                        self.toggleButton_output_a_2.setStyleSheet("background-color : lightgrey")
            if name == "out_b_1":
                if not self.mute_input_1.isChecked():
                    if self.toggleButton_output_b_1.isChecked():
                        stream_threads[1].set_mute(1)
                        self.toggleButton_output_b_1.setStyleSheet("background-color : lightblue")
                    else:
                        stream_threads[1].set_mute(0)
                        self.toggleButton_output_b_1.setStyleSheet("background-color : lightgrey")
            if name == "out_b_2":
                if not self.mute_input_2.isChecked():
                    if self.toggleButton_output_b_2.isChecked():
                        stream_threads[3].set_mute(1)
                        self.toggleButton_output_b_2.setStyleSheet("background-color : lightblue")
                    else:
                        stream_threads[3].set_mute(0)
                        self.toggleButton_output_b_2.setStyleSheet("background-color : lightgrey")
        except Exception as e:
            print(e)

    def slider(self, name):
        try:
            if name == "slider_1":
                val = self.gain_slider_in_1.value()
                stream_threads[0].set_gain(val)
                stream_threads[1].set_gain(val)
                self.gain_value_label_1.setText(str(val)+" dB")
            if name == "slider_2":
                val = self.gain_slider_in_2.value()
                stream_threads[2].set_gain(val)
                stream_threads[3].set_gain(val)
                self.gain_value_label_2.setText(str(val)+" dB")
            if name == "slider_3":
                val = self.gain_slider_in_3.value()
                file_threads[0].set_gain(val)
                self.gain_value_label_3.setText(str(val)+" dB")
            if name == "pitch_1":
                val = self.pitch_slider_in_1.value()
                stream_threads[0].set_pitch(val)
                stream_threads[1].set_pitch(val)
                self.pitch_value_label_1.setText(str(val))
            if name == "pitch_2":
                val = self.pitch_slider_in_2.value()
                stream_threads[2].set_pitch(val)
                stream_threads[3].set_pitch(val)
                self.pitch_value_label_2.setText(str(val))
            if name == "pitch_3":
                val = self.pitch_slider_in_3.value()
                file_threads[0].set_pitch(val)
                self.pitch_value_label_3.setText(str(val))
        except Exception as e:
            print(e)

    def mute(self, name):
        try:
            if name == "mute_1":
                if self.mute_input_1.isChecked():
                    self.mute_input_1.setStyleSheet("background-color : lightblue")
                    self.toggleButton_output_a_1.setEnabled(False)
                    self.toggleButton_output_b_1.setEnabled(False)
                    if not self.toggleButton_output_a_1.isChecked():
                        stream_threads[0].stop()
                    if not self.toggleButton_output_b_1.isChecked():
                        stream_threads[1].stop()
                else:
                    self.mute_input_1.setStyleSheet("background-color : lightgrey")
                    self.toggleButton_output_a_1.setEnabled(True)
                    self.toggleButton_output_b_1.setEnabled(True)
                    if not self.toggleButton_output_a_1.isChecked():
                        stream_threads[0].play()
                    if not self.toggleButton_output_b_1.isChecked():
                        stream_threads[1].play()
            elif name == "mute_2":
                if self.mute_input_2.isChecked():
                    self.mute_input_2.setStyleSheet("background-color : lightblue")
                    self.toggleButton_output_a_2.setEnabled(False)
                    self.toggleButton_output_b_2.setEnabled(False)
                    if not self.toggleButton_output_a_2.isChecked():
                        stream_threads[2].stop()
                    if not self.toggleButton_output_b_2.isChecked():
                        stream_threads[3].stop()
                else:
                    self.mute_input_2.setStyleSheet("background-color : lightgrey")
                    self.toggleButton_output_a_2.setEnabled(True)
                    self.toggleButton_output_b_2.setEnabled(True)
                    if not self.toggleButton_output_a_2.isChecked():
                        stream_threads[2].play()
                    if not self.toggleButton_output_b_2.isChecked():
                        stream_threads[3].play()
            elif name == "mute_3":
                if self.mute_input_3.isChecked():
                    self.mute_input_3.setStyleSheet("background-color : lightblue")
                    file_threads[0].set_mute(1)
                    file_threads[0].stop()
                else:
                    self.mute_input_3.setStyleSheet("background-color : lightgrey")
                    file_threads[0].set_mute(0)
                    stream_threads[0].play()
        except Exception as e:
            print(e)

    def on_input_changed(self, name):
        try:
            if name == "combo_in_1":
                stream_threads[0].close()
                stream_threads[0].input_changer(str(self.comboBox_input_1.currentText()))
                stream_threads[0].stream_init()
                stream_threads[1].close()
                stream_threads[1].input_changer(str(self.comboBox_input_1.currentText()))
                stream_threads[1].stream_init()
                if not stream_threads[0].mute():
                    stream_threads[0].play()
                    stream_threads[1].play()
                if not file_threads[0].mute():
                    file_threads[0].play()
            elif name == "combo_in_2":
                stream_threads[2].close()
                stream_threads[2].input_changer(str(self.comboBox_input_2.currentText()))
                stream_threads[2].stream_init()
                stream_threads[3].close()
                stream_threads[3].input_changer(str(self.comboBox_input_2.currentText()))
                stream_threads[3].stream_init()
                if not stream_threads[2].mute():
                    stream_threads[2].play()
                    stream_threads[3].play()
        except Exception as e:
            print(e)

    def on_output_changed(self, name):
        try:
            if name == "combo_out_1":
                if stream_threads[0].played():
                    stream_threads[0].close()
                    stream_threads[0].output_changer(str(self.comboBox_out_1.currentText()))
                    stream_threads[0].stream_init()
                    stream_threads[0].play()
                if stream_threads[2].played():
                    stream_threads[2].close()
                    stream_threads[2].output_changer(str(self.comboBox_out_1.currentText()))
                    stream_threads[2].stream_init()
                    stream_threads[2].play()
                # ///////////////////
                file_threads[0].close()
                file_threads[0].output_changer(str(self.comboBox_out_1.currentText()))
                file_threads[0].play_init
            elif name == "combo_out_2":
                if stream_threads[1].played():
                    stream_threads[1].close()
                    stream_threads[1].output_changer(str(self.comboBox_out_2.currentText()))
                    stream_threads[1].stream_init()
                    stream_threads[1].play()
                if stream_threads[3].played():
                    stream_threads[3].close()
                    stream_threads[3].output_changer(str(self.comboBox_out_2.currentText()))
                    stream_threads[3].stream_init()
                    stream_threads[3].play()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    # create threads for class pyAudioThreading
    stream_threads = []
    for p in range(4):
        thread = PyAudioThreading()
        stream_threads.append(thread)
        thread.daemon = True
        thread.start()
    # create threads for class pyAudioThreading
    file_threads = []
    for p in range(1):
        thread = PyAudioFile()
        file_threads.append(thread)
        thread.daemon = True
    # Create an instance of QtWidgets.QApplication
    app = QtWidgets.QApplication(sys.argv)
    # Create an instance of our class
    window = MainWindow()
    # Setting name of application
    window.setWindowTitle("Mixer")
    # Start the application
    app.exec_()
