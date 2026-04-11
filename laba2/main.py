# Лабораторная работа 2. Фильтры: ВЧ с окном Блэкмана, Однополюсный НЧ-фильтр. Тарасенко К.А.
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write
from pathlib import Path

# Импорт локальных модулей
from generate_audio import create_wav_file
from save_signal_to_wav import save_signal_to_wav
from signal_plot import plot_time_signal
from signal_spectrum import plot_spectrum

# Импорт модулей фильтров
from filters import HomogeneousFilter, FIRHighPassFilter, IIRLowPassFilter
from signal_processing import add_noise_and_distortion, plot_filter_response, analyze_filter_performance

def main():
    # Параметры
    sample_rate = 44100
    duration = 2
    
    # Загрузка или создание сигналов из laba1
    filename1 = "../laba1/periodic_signal_1.wav"
    filename2 = "../laba1/periodic_signal_2.wav"
    
    file1_path = Path(filename1)
    file2_path = Path(filename2)
    
    if not (file1_path.exists() and file2_path.exists()):
        print("Создание тестовых сигналов...")
        create_wav_file(2, sample_rate, duration)
        filename1 = "periodic_signal_1.wav"
        filename2 = "periodic_signal_2.wav"
    
    # Чтение сигналов
    _, signal_x = read(filename1)
    _, signal_y = read(filename2)
    
    # Преобразование в float для обработки
    x = signal_x.astype(np.float32) / 32767.0
    y = signal_y.astype(np.float32) / 32767.0
    
    # Создание искаженного сигнала для демонстрации работы фильтров
    print("Добавление шума и искажений к сигналу...")
    x_distorted = add_noise_and_distortion(x, sample_rate)
    
    # Сохранение искаженного сигнала
    save_signal_to_wav((x_distorted * 32767).astype(np.int16), "distorted_signal", sample_rate)
    
    # Создание фильтров
    print("Создание фильтров...")
    
    # 1. Однородный фильтр (простое усиление/ослабление)
    homogeneous_filter = HomogeneousFilter(gain=0.5)
    
    # 2. ВЧ-фильтр с окном Блэкмана (FIR)
    cutoff_freq = 1000  # Частота среза 1 кГц
    filter_order = 51   # Порядок фильтра (нечетный для симметрии)
    fir_filter = FIRHighPassFilter(cutoff_freq, sample_rate, filter_order)
    
    # 3. Однополюсный НЧ-фильтр (IIR)
    cutoff_freq_lp = 2000  # Частота среза 2 кГц
    iir_filter = IIRLowPassFilter(cutoff_freq_lp, sample_rate)
    
    # Применение фильтров
    print("Применение фильтров...")
    
    x_homogeneous = homogeneous_filter.filter(x_distorted)
    x_fir_filtered = fir_filter.filter(x_distorted)
    x_iir_filtered = iir_filter.filter(x_distorted)
    
    # Сохранение отфильтрованных сигналов
    save_signal_to_wav((x_homogeneous * 32767).astype(np.int16), "homogeneous_filtered", sample_rate)
    save_signal_to_wav((x_fir_filtered * 32767).astype(np.int16), "fir_filtered", sample_rate)
    save_signal_to_wav((x_iir_filtered * 32767).astype(np.int16), "iir_filtered", sample_rate)
    
    # Построение графиков
    print("Построение графиков...")
    
    # Графики временных сигналов
    plot_time_signal(x, sample_rate, "original_signal.png", "Original Signal")
    plot_time_signal(x_distorted, sample_rate, "distorted_signal.png", "Distorted Signal")
    plot_time_signal(x_homogeneous, sample_rate, "homogeneous_filtered.png", "Homogeneous Filtered")
    plot_time_signal(x_fir_filtered, sample_rate, "fir_filtered.png", "FIR High-Pass Filtered")
    plot_time_signal(x_iir_filtered, sample_rate, "iir_filtered.png", "IIR Low-Pass Filtered")
    
    # АЧХ фильтров
    plot_filter_response(fir_filter, sample_rate, "fir_frequency_response.png", "FIR High-Pass Filter")
    plot_filter_response(iir_filter, sample_rate, "iir_frequency_response.png", "IIR Low-Pass Filter")
    
    # Спектры сигналов
    # Для спектрального анализа нужно преобразовать в комплексные числа
    x_complex = [complex(val, 0) for val in x]
    x_distorted_complex = [complex(val, 0) for val in x_distorted]
    x_fir_complex = [complex(val, 0) for val in x_fir_filtered]
    x_iir_complex = [complex(val, 0) for val in x_iir_filtered]
    
    plot_spectrum(x_complex, sample_rate, "original_spectrum.png", "Original Signal")
    plot_spectrum(x_distorted_complex, sample_rate, "distorted_spectrum.png", "Distorted Signal")
    plot_spectrum(x_fir_complex, sample_rate, "fir_filtered_spectrum.png", "FIR Filtered Signal")
    plot_spectrum(x_iir_complex, sample_rate, "iir_filtered_spectrum.png", "IIR Filtered Signal")
    
    # Детальный анализ эффективности фильтров
    print("\n" + "="*60)
    print("АНАЛИЗ ЭФФЕКТИВНОСТИ ФИЛЬТРОВ")
    print("="*60)
    
    # Анализ каждого фильтра
    homogeneous_stats = analyze_filter_performance(x, x_distorted, x_homogeneous, "Однородного фильтра")
    fir_stats = analyze_filter_performance(x, x_distorted, x_fir_filtered, "FIR ВЧ-фильтра")
    iir_stats = analyze_filter_performance(x, x_distorted, x_iir_filtered, "IIR НЧ-фильтра")
    
    # Сводная таблица результатов
    print(f"\n{'='*90}")
    print("СВОДНАЯ ТАБЛИЦА РЕЗУЛЬТАТОВ")
    print(f"{'='*90}")
    print(f"{'Фильтр':<12} {'SNR до':<8} {'SNR после':<10} {'Улучшение':<10} {'Подавление':<12} {'Сохранение':<12} {'Корреляция':<10}")
    print(f"{'':12} {'(дБ)':<8} {'(дБ)':<10} {'SNR (дБ)':<10} {'шума (%)':<12} {'сигнала (%)':<12} {'с ориг.':<10}")
    print("-" * 90)
    print(f"{'Однородный':<12} {homogeneous_stats['snr_before']:<8.2f} {homogeneous_stats['snr_after']:<10.2f} {homogeneous_stats['snr_improvement']:<10.2f} {homogeneous_stats['noise_suppression_percent']:<12.1f} {homogeneous_stats['signal_preservation']:<12.1f} {homogeneous_stats['correlation_after']:<10.3f}")
    print(f"{'FIR ВЧ':<12} {fir_stats['snr_before']:<8.2f} {fir_stats['snr_after']:<10.2f} {fir_stats['snr_improvement']:<10.2f} {fir_stats['noise_suppression_percent']:<12.1f} {fir_stats['signal_preservation']:<12.1f} {fir_stats['correlation_after']:<10.3f}")
    print(f"{'IIR НЧ':<12} {iir_stats['snr_before']:<8.2f} {iir_stats['snr_after']:<10.2f} {iir_stats['snr_improvement']:<10.2f} {iir_stats['noise_suppression_percent']:<12.1f} {iir_stats['signal_preservation']:<12.1f} {iir_stats['correlation_after']:<10.3f}")
    
    # Информация о параметрах фильтров
    print(f"\n{'='*60}")
    print("ПАРАМЕТРЫ ФИЛЬТРОВ")
    print(f"{'='*60}")
    print(f"Однородный фильтр: коэффициент усиления = {homogeneous_filter.gain}")
    print(f"FIR ВЧ-фильтр: частота среза = {fir_filter.cutoff_freq} Гц, порядок = {fir_filter.filter_order}")
    print(f"IIR НЧ-фильтр: частота среза = {iir_filter.cutoff_freq} Гц")
    
    print(f"\n{'='*60}")
    print("СОЗДАННЫЕ ФАЙЛЫ")
    print(f"{'='*60}")
    print("Аудиофайлы:")
    print("  - distorted_signal.wav")
    print("  - homogeneous_filtered.wav")
    print("  - fir_filtered.wav")
    print("  - iir_filtered.wav")
    print("\nГрафики временных сигналов:")
    print("  - original_signal.png")
    print("  - distorted_signal.png")
    print("  - homogeneous_filtered.png")
    print("  - fir_filtered.png")
    print("  - iir_filtered.png")
    print("\nЧастотные характеристики фильтров:")
    print("  - fir_frequency_response.png")
    print("  - iir_frequency_response.png")
    print("\nСпектры сигналов:")
    print("  - original_spectrum.png")
    print("  - distorted_spectrum.png")
    print("  - fir_filtered_spectrum.png")
    print("  - iir_filtered_spectrum.png")
    
    print(f"\n{'='*60}")
    print("ЛАБОРАТОРНАЯ РАБОТА 2 ВЫПОЛНЕНА УСПЕШНО!")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()