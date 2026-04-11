"""
Утилиты для лабораторных работ по цифровой обработке сигналов.

Модули:
- file_manager: управление файлами и папками
- audio_utils: работа с аудиофайлами
- plot_utils: создание и сохранение графиков
"""

from .file_manager import file_manager, FileManager
from .audio_utils import save_signal_to_wav
from .plot_utils import plot_time_signal, plot_spectrum, plot_efficiency

__all__ = [
    'file_manager',
    'FileManager', 
    'save_signal_to_wav',
    'plot_time_signal',
    'plot_spectrum',
    'plot_efficiency'
]