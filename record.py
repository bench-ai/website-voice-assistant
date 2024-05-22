import wave
import sys
import pyaudio
from functools import partial

from pynput import keyboard

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1 if sys.platform == 'darwin' else 2
RATE = 44100
RECORD_SECONDS = 5

cont = True


def on_press(key, signal_dict):
    try:
        signal_dict["signal"] = False
    except AttributeError:
        print('special key {0} pressed'.format(key))


def start_recording_session(signal_dict: dict):
    with wave.open('output.wav', 'wb') as wf:
        p = pyaudio.PyAudio()
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)

        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)

        print('Recording...')
        # for _ in range(0, RATE // CHUNK * RECORD_SECONDS):

        while signal_dict["signal"]:
            wf.writeframes(stream.read(CHUNK))

        stream.close()
        p.terminate()


def record_audio():
    signal_dict = {"signal": True}
    press_func = partial(on_press, signal_dict=signal_dict)

    listener = keyboard.Listener(
        on_press=press_func)

    listener.start()
    start_recording_session(signal_dict)


if __name__ == '__main__':
    record_audio()
