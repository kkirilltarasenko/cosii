"""
Запускатель для лабораторной работы 2.
Адаптированная версия с использованием централизованного управления файлами.
"""

import sys
from pathlib import Path
import numpy as np

# Добавляем пути к модулям
sys.path.append(str(Path(__file__).parent / "laba2"))
sys.path.append(str(Path(__file__).parent / "utils"))

# Импорты из laba2
from generate_audio import create_wav_file
from filters import HomogeneousFilter, FIRHighPassFilter, IIRLowPassFilter
from signal_processing import add_noise_and_distortion, plot_filter_response, analyze_filter_performance

# Импорты утилит
from utils.audio_utils import save_signal_to_wav
from utils.plot_utils import plot_time_signal, plot_spectrum
from utils.file_manager import file_manager

from scipy.io.wavfile import read

def run_laba2():
    """Выполняет лабораторную работу 2"""
    
    # Параметры
    sample_rate = 44100
    duration = 2
    
    print("📊 Загрузка сигналов из лабораторной работы 1...")
    
    # Загрузка сигналов из laba1 (из папки audio)
    filename1 = file_manager.get_audio_path("periodic_signal_1")
    filename2 = file_manager.get_audio_path("periodic_signal_2")
    
    file1_path = Path(filename1)
    file2_path = Path(filename2)
    
    if not (file1_path.exists() and file2_path.exists()):
        print("⚠️ Сигналы из лабораторной работы 1 не найдены. Создаем новые...")
        # Создаем файлы во временной папке, затем перемещаем
        temp_files = create_wav_file(2, sample_rate, duration)
        
        # Перемещаем файлы в правильную папку
        import shutil
        shutil.move(temp_files[0], filename1)
        shutil.move(temp_files[1], filename2)
    
    # Чтение сигналов
    _, signal_x = read(filename1)
    _, signal_y = read(filename2)
    
    # Преобразование в float для обработки
    x = signal_x.astype(np.float32) / 32767.0
    y = signal_y.astype(np.float32) / 32767.0
    
    print("🔊 Добавление шума и искажений к сигналу...")
    # Создание искаженного сигнала для демонстрации работы фильтров
    x_distorted = add_noise_and_distortion(x, sample_rate)
    
    # Сохранение искаженного сигнала
    save_signal_to_wav((x_distorted * 32767).astype(np.int16), "laba2_distorted_signal", sample_rate)
    
    print("🔧 Создание фильтров...")
    # Создание фильтров
    
    # 1. Однородный фильтр (простое усиление/ослабление)
    homogeneous_filter = HomogeneousFilter(gain=0.5)
    
    # 2. ВЧ-фильтр с окном Блэкмана (FIR)
    cutoff_freq = 1000  # Частота среза 1 кГц
    filter_order = 51   # Порядок фильтра (нечетный для симметрии)
    fir_filter = FIRHighPassFilter(cutoff_freq, sample_rate, filter_order)
    
    # 3. Однополюсный НЧ-фильтр (IIR)
    cutoff_freq_lp = 2000  # Частота среза 2 кГц
    iir_filter = IIRLowPassFilter(cutoff_freq_lp, sample_rate)
    
    print("⚡ Применение фильтров...")
    # Применение фильтров
    x_homogeneous = homogeneous_filter.filter(x_distorted)
    x_fir_filtered = fir_filter.filter(x_distorted)
    x_iir_filtered = iir_filter.filter(x_distorted)
    
    # Сохранение отфильтрованных сигналов
    save_signal_to_wav((x_homogeneous * 32767).astype(np.int16), "laba2_homogeneous_filtered", sample_rate)
    save_signal_to_wav((x_fir_filtered * 32767).astype(np.int16), "laba2_fir_filtered", sample_rate)
    save_signal_to_wav((x_iir_filtered * 32767).astype(np.int16), "laba2_iir_filtered", sample_rate)
    
    print("📈 Построение графиков временных сигналов...")
    # Графики временных сигналов
    plot_time_signal(x, sample_rate, "laba2_original_signal", "Original Signal")
    plot_time_signal(x_distorted, sample_rate, "laba2_distorted_signal", "Distorted Signal")
    plot_time_signal(x_homogeneous, sample_rate, "laba2_homogeneous_filtered", "Homogeneous Filtered")
    plot_time_signal(x_fir_filtered, sample_rate, "laba2_fir_filtered", "FIR High-Pass Filtered")
    plot_time_signal(x_iir_filtered, sample_rate, "laba2_iir_filtered", "IIR Low-Pass Filtered")
    
    print("📊 Построение АЧХ фильтров...")
    # АЧХ фильтров
    plot_filter_response(fir_filter, sample_rate, "laba2_fir_frequency_response", "FIR High-Pass Filter")
    plot_filter_response(iir_filter, sample_rate, "laba2_iir_frequency_response", "IIR Low-Pass Filter")
    
    print("🔬 Построение спектров сигналов...")
    # Спектры сигналов
    # Для спектрального анализа нужно преобразовать в комплексные числа
    x_complex = [complex(val, 0) for val in x]
    x_distorted_complex = [complex(val, 0) for val in x_distorted]
    x_fir_complex = [complex(val, 0) for val in x_fir_filtered]
    x_iir_complex = [complex(val, 0) for val in x_iir_filtered]
    
    plot_spectrum(x_complex, sample_rate, "laba2_original_spectrum", "Original Signal")
    plot_spectrum(x_distorted_complex, sample_rate, "laba2_distorted_spectrum", "Distorted Signal")
    plot_spectrum(x_fir_complex, sample_rate, "laba2_fir_filtered_spectrum", "FIR Filtered Signal")
    plot_spectrum(x_iir_complex, sample_rate, "laba2_iir_filtered_spectrum", "IIR Filtered Signal")
    
    print("📋 Детальный анализ эффективности фильтров...")
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
    
    # Выводим результаты
    print("\n" + "="*60)
    print("РЕЗУЛЬТАТЫ ЛАБОРАТОРНОЙ РАБОТЫ 2")
    print("="*60)
    print(f"📊 Создано графиков: {len([p for p in file_manager.list_plots() if 'laba2' in p.name])}")
    print(f"🔊 Создано аудиофайлов: {len([a for a in file_manager.list_audio() if 'laba2' in a.name])}")
    
    print("\n📁 Созданные файлы:")
    print("Аудиофайлы:")
    for audio_file in sorted(file_manager.list_audio()):
        if "laba2" in audio_file.name:
            print(f"  - {audio_file.name}")
    
    print("Графики:")
    for plot_file in sorted(file_manager.list_plots()):
        if "laba2" in plot_file.name:
            print(f"  - {plot_file.name}")

if __name__ == "__main__":
    run_laba2()