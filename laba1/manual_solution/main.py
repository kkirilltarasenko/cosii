# Лабораторная работа 1. Вариант: БПФ_Ч. Тарасенко К.А.

import convolution as conv
import correlation as corr

from fft_dif import fft_dif, ifft_dif, pad_to_power_of_2
from save_signal_to_wav import save_signal_to_wav
from scipy.io.wavfile import read
from pathlib import Path
from generate_audio import create_wav_file

amount_of_audio = 2
sample_rate = 44100
duration = 2

filename1 = "periodic_signal_1.wav"
filename2 = "periodic_signal_2.wav"

file1_path = Path(filename1)
file2_path = Path(filename2)

if file1_path.exists() or file2_path.exists():
    file1, file2 = [filename1, filename2]
else:
    file1, file2 = create_wav_file(amount_of_audio, sample_rate, duration)

_, signal_x = read(file1)
_, signal_y = read(file2)

x = signal_x.tolist()
y = signal_y.tolist()

# 1. Свертка двух сигналов
# raw_signal_after_convolution = conv.convolution(x, y)
# save_signal_to_wav(raw_signal_after_convolution, "signals_after_convolution", sample_rate)

# 2. Корреляция двух сигналов
# raw_signal_after_correlation = corr.correlation(x, y)
# save_signal_to_wav(raw_signal_after_correlation, "signals_after_correlation", sample_rate)

# 3. БПФ с прореживанием по частоте
x_pad = pad_to_power_of_2(x)
x_complex = [complex(v) for v in x_pad]

X = fft_dif(x_complex.copy())
x_restored = ifft_dif(X.copy())

y_pad = pad_to_power_of_2(y)
y_complex = [complex(v) for v in y_pad]

Y = fft_dif(y_complex.copy())
y_restored = ifft_dif(Y.copy())
