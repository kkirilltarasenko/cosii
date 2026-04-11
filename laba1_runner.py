"""
Запускатель для лабораторной работы 1.
Адаптированная версия с использованием централизованного управления файлами.
"""

import sys
from pathlib import Path

# Добавляем пути к модулям
sys.path.append(str(Path(__file__).parent / "laba1"))
sys.path.append(str(Path(__file__).parent / "utils"))

# Импорты из laba1
import benchmark as bench
import compare_manual_vs_numpy as comp
import convolution as conv
import correlation as corr
import checkup as check
from fft_dif import fft_dif, ifft_dif, pad_to_power_of_2
from generate_audio import create_wav_file

# Импорты утилит
from utils.audio_utils import save_signal_to_wav
from utils.plot_utils import plot_time_signal, plot_spectrum, plot_efficiency
from utils.file_manager import file_manager

from scipy.io.wavfile import read

def run_laba1():
    """Выполняет лабораторную работу 1"""
    
    # Параметры
    amount_of_audio = 2
    sample_rate = 44100
    duration = 2
    
    print("📊 Генерация или загрузка аудиосигналов...")
    
    # Проверяем наличие файлов в папке audio
    filename1 = file_manager.get_audio_path("periodic_signal_1")
    filename2 = file_manager.get_audio_path("periodic_signal_2")
    
    file1_path = Path(filename1)
    file2_path = Path(filename2)
    
    if file1_path.exists() and file2_path.exists():
        print("✅ Используем существующие аудиофайлы")
        file1, file2 = filename1, filename2
    else:
        print("🎵 Создаем новые аудиофайлы...")
        # Создаем файлы во временной папке, затем перемещаем
        temp_files = create_wav_file(amount_of_audio, sample_rate, duration)
        
        # Перемещаем файлы в правильную папку
        import shutil
        shutil.move(temp_files[0], filename1)
        shutil.move(temp_files[1], filename2)
        file1, file2 = filename1, filename2
    
    # Читаем сигналы
    _, signal_x = read(file1)
    _, signal_y = read(file2)
    
    x = signal_x.tolist()
    y = signal_y.tolist()
    
    print("🔄 Выполнение свертки двух сигналов...")
    # 1. Свертка двух сигналов
    raw_signal_after_convolution = conv.convolution(x, y)
    save_signal_to_wav(raw_signal_after_convolution, "signals_after_convolution", sample_rate)
    
    print("📈 Выполнение корреляции двух сигналов...")
    # 2. Корреляция двух сигналов
    raw_signal_after_correlation = corr.correlation(x, y)
    save_signal_to_wav(raw_signal_after_correlation, "signals_after_correlation", sample_rate)
    
    print("⚡ Выполнение БПФ с прореживанием по частоте...")
    # 3. БПФ с прореживанием по частоте
    x_pad = pad_to_power_of_2(x)
    x_complex = [complex(v) for v in x_pad]
    
    X = fft_dif(x_complex.copy())
    x_restored = ifft_dif(X.copy())
    
    y_pad = pad_to_power_of_2(y)
    y_complex = [complex(v) for v in y_pad]
    
    Y = fft_dif(y_complex.copy())
    y_restored = ifft_dif(Y.copy())
    
    c_pad = pad_to_power_of_2(raw_signal_after_convolution)
    c_complex = [complex(v) for v in c_pad]
    
    C = fft_dif(c_complex.copy())
    c_restored = ifft_dif(C.copy())
    
    print("📊 Построение графиков спектров...")
    # 4. Построить графики амплитудного и фазового спектра сигналов X, Y, C
    plot_spectrum(x_complex, sample_rate, "laba1_signal_x_spectrum", "Signal X")
    plot_spectrum(y_complex, sample_rate, "laba1_signal_y_spectrum", "Signal Y")
    plot_spectrum(c_complex, sample_rate, "laba1_convolution_spectrum", "Convolution Result")
    
    print("📈 Построение временных графиков...")
    # 5. Построить графики сигналов во временной области
    plot_time_signal(x, sample_rate, "laba1_signal_x_time", "Signal X")
    plot_time_signal(y, sample_rate, "laba1_signal_y_time", "Signal Y")
    plot_time_signal(raw_signal_after_convolution, sample_rate, "laba1_convolution_time", "Convolution Result")
    plot_time_signal(raw_signal_after_correlation, sample_rate, "laba1_correlation_time", "Correlation Result")
    
    print("🔍 Проверка корректности вычислений через БПФ...")
    # 6. Экспериментально проверить корректность схем вычисления свертки и корреляции через Фурье преобразование
    conv_fft = check.conv_with_fft(x, y)
    corr_fft = check.corr_with_fft(x, y)
    
    conv_match = check.compare_signals(
        raw_signal_after_convolution,
        conv_fft,
        "Convolution"
    )
    
    corr_match = check.compare_signals(
        raw_signal_after_correlation,
        corr_fft,
        "Correlation"
    )
    
    print("⏱️ Анализ эффективности алгоритмов...")
    # 7. Сравнение полученных результатов при разных значениях N
    sizes, conv_times, fft_times = bench.benchmark_algorithms(
        x,
        y,
        conv.convolution,
        check.conv_with_fft
    )
    
    plot_efficiency(sizes, conv_times, fft_times, "laba1_algorithm_efficiency")
    
    print("🔬 Сравнение с библиотечными реализациями...")
    # Сравнение с numpy
    comp.compare_manual_vs_numpy(
        x,
        y,
        fft_dif,
        ifft_dif,
        conv.convolution,
        corr.correlation,
    )
    
    # Выводим результаты
    print("\n" + "="*60)
    print("РЕЗУЛЬТАТЫ ЛАБОРАТОРНОЙ РАБОТЫ 1")
    print("="*60)
    print(f"✅ Свертка: {'корректна' if conv_match else 'некорректна'}")
    print(f"✅ Корреляция: {'корректна' if corr_match else 'некорректна'}")
    print(f"📊 Создано графиков: {len(file_manager.list_plots())}")
    print(f"🔊 Создано аудиофайлов: {len(file_manager.list_audio())}")
    
    print("\n📁 Созданные файлы:")
    print("Аудиофайлы:")
    for audio_file in sorted(file_manager.list_audio()):
        if "laba1" in audio_file.name or any(name in audio_file.name for name in ["periodic_signal", "convolution", "correlation"]):
            print(f"  - {audio_file.name}")
    
    print("Графики:")
    for plot_file in sorted(file_manager.list_plots()):
        if "laba1" in plot_file.name:
            print(f"  - {plot_file.name}")

if __name__ == "__main__":
    run_laba1()