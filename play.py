from playsound import playsound


def play_audio(wav_path: str):
    playsound(wav_path)


if __name__ == '__main__':
    play_audio("./output.wav")
