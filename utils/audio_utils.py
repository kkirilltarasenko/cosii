"""
Утилиты для работы с аудиофайлами.
Обеспечивает сохранение всех аудиофайлов в папку static/audio.
"""
from scipy.io.wavfile import write
import numpy as np
from .file_manager import file_manager

def save_signal_to_wav(signal, filename, sample_rate=44100):
    """
    Сохраняет сигнал в WAV файл в папку static/audio
    
    Args:
        signal: массив сигнала
        filename: имя файла (без расширения)
        sample_rate: частота дискретизации
    """
    signal = np.array(signal, dtype=float)
    
    # Нормализуем значения для 16-битного WAV формата
    if np.max(np.abs(signal)) > 0:
        signal = signal / np.max(np.abs(signal))
    
    audio = (signal * 32767).astype(np.int16)
    
    # Получаем путь через file_manager
    filepath = file_manager.get_audio_path(filename)
    write(filepath, sample_rate, audio)
    
    print(f"Аудиофайл сохранен: {filepath}")
    return filepath