"""
Модуль для управления файлами и папками проекта.
Обеспечивает централизованное сохранение всех результатов в структурированные папки.
"""
import os
from pathlib import Path

class FileManager:
    """Класс для управления файлами проекта"""
    
    def __init__(self, base_dir="."):
        self.base_dir = Path(base_dir)
        self.static_dir = self.base_dir / "static"
        self.plots_dir = self.static_dir / "plots"
        self.audio_dir = self.static_dir / "audio"
        self.data_dir = self.static_dir / "data"
        
        # Создаем папки если их нет
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Создает необходимые папки если их нет"""
        for directory in [self.static_dir, self.plots_dir, self.audio_dir, self.data_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def get_plot_path(self, filename):
        """Возвращает путь для сохранения графика"""
        if not filename.endswith('.png'):
            filename += '.png'
        return str(self.plots_dir / filename)
    
    def get_audio_path(self, filename):
        """Возвращает путь для сохранения аудиофайла"""
        if not filename.endswith('.wav'):
            filename += '.wav'
        return str(self.audio_dir / filename)
    
    def get_data_path(self, filename):
        """Возвращает путь для сохранения данных"""
        return str(self.data_dir / filename)
    
    def list_plots(self):
        """Возвращает список всех графиков"""
        return list(self.plots_dir.glob("*.png"))
    
    def list_audio(self):
        """Возвращает список всех аудиофайлов"""
        return list(self.audio_dir.glob("*.wav"))
    
    def clean_directory(self, dir_type="all"):
        """Очищает указанную папку"""
        if dir_type == "plots" or dir_type == "all":
            for file in self.plots_dir.glob("*"):
                file.unlink()
        if dir_type == "audio" or dir_type == "all":
            for file in self.audio_dir.glob("*"):
                file.unlink()
        if dir_type == "data" or dir_type == "all":
            for file in self.data_dir.glob("*"):
                file.unlink()

# Глобальный экземпляр для использования во всем проекте
file_manager = FileManager()