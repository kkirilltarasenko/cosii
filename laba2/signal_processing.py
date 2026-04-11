import numpy as np
import matplotlib.pyplot as plt
import math

def add_noise_and_distortion(signal, sample_rate):
    """
    Добавить шум и искажения к сигналу для демонстрации работы фильтров
    Стратегически добавляем шум в частотных диапазонах, которые фильтры должны подавлять
    """
    # Создание копии сигнала
    distorted = np.array(signal, dtype=np.float32)
    
    # Временная ось
    t = np.linspace(0, len(signal) / sample_rate, len(signal), endpoint=False)
    
    # 1. Добавление белого шума (умеренный уровень)
    noise_level = 0.05
    white_noise = np.random.normal(0, noise_level, len(signal))
    distorted += white_noise
    
    # 2. Добавление высокочастотного шума (выше частоты среза ВЧ-фильтра)
    # ВЧ-фильтр с частотой среза 1000 Гц должен пропускать частоты выше 1000 Гц
    # Добавляем НЧ-шум, который ВЧ-фильтр должен подавить
    low_freq_interference = 0.3 * np.sin(2 * np.pi * 100 * t)  # 100 Гц помеха
    low_freq_interference += 0.2 * np.sin(2 * np.pi * 300 * t)  # 300 Гц помеха
    distorted += low_freq_interference
    
    # 3. Добавление высокочастотного шума (выше частоты среза НЧ-фильтра)
    # НЧ-фильтр с частотой среза 2000 Гц должен подавлять частоты выше 2000 Гц
    high_freq_noise = 0.25 * np.sin(2 * np.pi * 4000 * t)  # 4 кГц шум
    high_freq_noise += 0.15 * np.sin(2 * np.pi * 8000 * t)  # 8 кГц шум
    distorted += high_freq_noise
    
    # 4. Добавление импульсного шума (редкие импульсы)
    impulse_probability = 0.0005  # Снижена вероятность
    impulse_positions = np.random.random(len(signal)) < impulse_probability
    impulse_amplitudes = np.random.uniform(-0.3, 0.3, len(signal))
    distorted[impulse_positions] += impulse_amplitudes[impulse_positions]
    
    # Нормализация для предотвращения клиппинга
    max_val = np.max(np.abs(distorted))
    if max_val > 1.0:
        distorted = distorted / max_val * 0.9
    
    return distorted

def plot_filter_response(filter_obj, sample_rate, filename, title):
    """
    Построить график частотной характеристики фильтра
    """
    # Частоты для анализа (от 0 до Найквиста)
    frequencies = np.linspace(0, sample_rate // 2, 1000)
    
    # Получение частотной характеристики
    H = filter_obj.get_frequency_response(frequencies)
    
    # Амплитудная характеристика в дБ
    magnitude_db = 20 * np.log10(np.abs(H) + 1e-10)  # +1e-10 для избежания log(0)
    
    # Фазовая характеристика в радианах
    phase_rad = np.angle(H)
    
    # Построение графиков
    plt.figure(figsize=(12, 8))
    
    # Амплитудно-частотная характеристика
    plt.subplot(2, 1, 1)
    plt.plot(frequencies, magnitude_db, 'b-', linewidth=2)
    plt.title(f"{title} - Амплитудно-частотная характеристика")
    plt.xlabel("Частота (Гц)")
    plt.ylabel("Амплитуда (дБ)")
    plt.grid(True, alpha=0.3)
    plt.xlim(0, sample_rate // 2)
    
    # Добавление линии -3дБ для определения частоты среза
    plt.axhline(y=-3, color='r', linestyle='--', alpha=0.7, label='-3 дБ')
    plt.legend()
    
    # Фазо-частотная характеристика
    plt.subplot(2, 1, 2)
    plt.plot(frequencies, phase_rad, 'g-', linewidth=2)
    plt.title(f"{title} - Фазо-частотная характеристика")
    plt.xlabel("Частота (Гц)")
    plt.ylabel("Фаза (рад)")
    plt.grid(True, alpha=0.3)
    plt.xlim(0, sample_rate // 2)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"График частотной характеристики сохранен: {filename}")

def plot_comparison_signals(original, distorted, filtered, sample_rate, filename, title):
    """
    Построить сравнительный график сигналов
    """
    # Время для оси X
    t = np.linspace(0, len(original) / sample_rate, len(original))
    
    plt.figure(figsize=(15, 10))
    
    # Исходный сигнал
    plt.subplot(3, 1, 1)
    plt.plot(t[:1000], original[:1000], 'b-', linewidth=1)  # Показываем только первые 1000 отсчетов
    plt.title("Исходный сигнал")
    plt.xlabel("Время (с)")
    plt.ylabel("Амплитуда")
    plt.grid(True, alpha=0.3)
    
    # Искаженный сигнал
    plt.subplot(3, 1, 2)
    plt.plot(t[:1000], distorted[:1000], 'r-', linewidth=1)
    plt.title("Искаженный сигнал")
    plt.xlabel("Время (с)")
    plt.ylabel("Амплитуда")
    plt.grid(True, alpha=0.3)
    
    # Отфильтрованный сигнал
    plt.subplot(3, 1, 3)
    plt.plot(t[:1000], filtered[:1000], 'g-', linewidth=1)
    plt.title(f"Отфильтрованный сигнал - {title}")
    plt.xlabel("Время (с)")
    plt.ylabel("Амплитуда")
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Сравнительный график сохранен: {filename}")

def calculate_snr(signal, noise):
    """
    Вычислить отношение сигнал/шум в дБ
    """
    signal_power = np.mean(signal ** 2)
    noise_power = np.mean(noise ** 2)
    
    if noise_power == 0:
        return float('inf')
    
    snr_db = 10 * np.log10(signal_power / noise_power)
    return snr_db

def analyze_filter_performance(original, distorted, filtered, filter_name):
    """
    Анализ эффективности фильтра с улучшенной методикой
    """
    # Более точный анализ SNR
    # 1. SNR искаженного сигнала относительно исходного
    added_noise = distorted - original
    signal_power = np.mean(original ** 2)
    noise_power_before = np.mean(added_noise ** 2)
    snr_before = 10 * np.log10(signal_power / (noise_power_before + 1e-10))
    
    # 2. SNR отфильтрованного сигнала
    # Для правильной оценки используем отношение полезного сигнала к остаточному шуму
    residual_noise = filtered - original
    noise_power_after = np.mean(residual_noise ** 2)
    snr_after = 10 * np.log10(signal_power / (noise_power_after + 1e-10))
    
    # 3. Альтернативная оценка: SNR как отношение мощностей
    distorted_power = np.mean(distorted ** 2)
    filtered_power = np.mean(filtered ** 2)
    
    snr_distorted_alt = 10 * np.log10(signal_power / (distorted_power - signal_power + 1e-10))
    snr_filtered_alt = 10 * np.log10(signal_power / (abs(filtered_power - signal_power) + 1e-10))
    
    # Выбираем лучшую оценку
    if abs(snr_after) < 50:  # Разумные значения SNR
        snr_improvement = snr_after - snr_before
        final_snr_before = snr_before
        final_snr_after = snr_after
    else:
        snr_improvement = snr_filtered_alt - snr_distorted_alt
        final_snr_before = snr_distorted_alt
        final_snr_after = snr_filtered_alt
    
    # RMS значения
    rms_original = np.sqrt(np.mean(original ** 2))
    rms_distorted = np.sqrt(np.mean(distorted ** 2))
    rms_filtered = np.sqrt(np.mean(filtered ** 2))
    
    # Коэффициент подавления шума
    noise_reduction_factor = noise_power_before / (noise_power_after + 1e-10)
    noise_reduction_db = 10 * np.log10(noise_reduction_factor)
    
    # Корреляция с исходным сигналом
    correlation_before = np.corrcoef(original, distorted)[0, 1]
    correlation_after = np.corrcoef(original, filtered)[0, 1]
    
    # Эффективность фильтрации (процент подавления шума)
    noise_suppression_percent = (1 - noise_power_after / (noise_power_before + 1e-10)) * 100
    
    # Сохранение полезного сигнала (насколько хорошо сохранен исходный сигнал)
    signal_preservation = correlation_after * 100
    
    print(f"\n=== Анализ эффективности {filter_name} ===")
    print(f"SNR до фильтрации: {final_snr_before:.2f} дБ")
    print(f"SNR после фильтрации: {final_snr_after:.2f} дБ")
    print(f"Улучшение SNR: {snr_improvement:.2f} дБ")
    print(f"Подавление шума: {noise_reduction_db:.2f} дБ")
    print(f"Подавление шума: {noise_suppression_percent:.1f}%")
    print(f"Сохранение сигнала: {signal_preservation:.1f}%")
    print(f"Корреляция с оригиналом до: {correlation_before:.3f}")
    print(f"Корреляция с оригиналом после: {correlation_after:.3f}")
    print(f"RMS исходного сигнала: {rms_original:.4f}")
    print(f"RMS искаженного сигнала: {rms_distorted:.4f}")
    print(f"RMS отфильтрованного сигнала: {rms_filtered:.4f}")
    
    return {
        'snr_before': final_snr_before,
        'snr_after': final_snr_after,
        'snr_improvement': snr_improvement,
        'noise_reduction_db': noise_reduction_db,
        'noise_suppression_percent': noise_suppression_percent,
        'signal_preservation': signal_preservation,
        'correlation_before': correlation_before,
        'correlation_after': correlation_after,
        'rms_original': rms_original,
        'rms_distorted': rms_distorted,
        'rms_filtered': rms_filtered
    }