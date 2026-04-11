"""
Утилиты для создания и сохранения графиков.
Обеспечивает сохранение всех графиков в папку static/plots.
"""
import matplotlib.pyplot as plt
import math
from .file_manager import file_manager

def plot_time_signal(signal, sample_rate, filename, title="Signal", max_samples=2000):
    """
    Строит график сигнала во временной области
    
    Args:
        signal: массив сигнала
        sample_rate: частота дискретизации
        filename: имя файла (без расширения)
        title: заголовок графика
        max_samples: максимальное количество отсчетов для отображения
    """
    signal = signal[:max_samples]
    
    # время в секундах
    time = [i / sample_rate for i in range(len(signal))]
    
    plt.figure(figsize=(10, 4))
    plt.plot(time, signal)
    plt.title(f"{title} — Time Domain")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    
    # Получаем путь через file_manager
    filepath = file_manager.get_plot_path(filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"График временного сигнала сохранен: {filepath}")
    return filepath

def plot_spectrum(x, sample_rate, filename, title="Spectrum"):
    """
    Строит амплитудный и фазовый спектр сигнала
    
    Args:
        x: массив комплексных значений сигнала
        sample_rate: частота дискретизации
        filename: имя файла (без расширения)
        title: заголовок графика
    """
    n = len(x)
    
    # частоты
    freqs = [i * sample_rate / n for i in range(n)]
    
    # амплитуда |X|
    amplitude = [abs(_x) for _x in x]
    
    # фаза arg(X)
    phase = [math.atan2(_x.imag, _x.real) for _x in x]
    
    # только первая половина спектра (симметрия для реальных сигналов)
    half = n // 2
    freqs = freqs[:half]
    amplitude = amplitude[:half]
    phase = phase[:half]
    
    plt.figure(figsize=(10, 6))
    
    # амплитудный спектр
    plt.subplot(2, 1, 1)
    plt.plot(freqs, amplitude)
    plt.title(f"{title} — Amplitude Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    
    # фазовый спектр
    plt.subplot(2, 1, 2)
    plt.plot(freqs, phase)
    plt.title(f"{title} — Phase Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Phase (rad)")
    plt.grid(True)
    
    plt.tight_layout()
    
    # Получаем путь через file_manager
    filepath = file_manager.get_plot_path(filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"График спектра сохранен: {filepath}")
    return filepath

def plot_efficiency(sizes, conv_times, fft_times, filename="algorithm_efficiency"):
    """
    Строит график сравнения эффективности алгоритмов
    
    Args:
        sizes: размеры массивов
        conv_times: времена выполнения свертки
        fft_times: времена выполнения FFT
        filename: имя файла (без расширения)
    """
    plt.figure(figsize=(10, 6))
    plt.loglog(sizes, conv_times, 'o-', label='Direct Convolution', linewidth=2)
    plt.loglog(sizes, fft_times, 's-', label='FFT Convolution', linewidth=2)
    plt.xlabel('Signal Length (N)')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Algorithm Efficiency Comparison')
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.3)
    
    # Получаем путь через file_manager
    filepath = file_manager.get_plot_path(filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"График эффективности алгоритмов сохранен: {filepath}")
    return filepath