import numpy as np
from scipy.io.wavfile import write

sample_rate = 44100

def note(freq, duration):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    return np.sin(2 * np.pi * freq * t)

def save_melody(notes, filename):
    melody = np.concatenate(notes)
    audio = melody * (2**15 - 1) / np.max(np.abs(melody))
    write(filename, sample_rate, audio.astype(np.int16))

melody_1 = [
    note(440, 0.4),
    note(523, 0.4),
    note(659, 0.4),
    note(880, 0.8),
]

save_melody(melody_1, "melody_1.wav")
print("Первая мелодия создана!")

melody_2 = [
    note(330, 0.5),
    note(392, 0.5),
    note(494, 0.5),
    note(660, 1),
]

save_melody(melody_2, "melody_2.wav")
print("Вторая мелодия создана!")
