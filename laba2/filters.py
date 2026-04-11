import numpy as np
import math

class HomogeneousFilter:
    """Однородный фильтр - простое усиление/ослабление сигнала"""
    
    def __init__(self, gain=1.0):
        self.gain = gain
    
    def filter(self, signal):
        """Применить однородный фильтр к сигналу"""
        return np.array(signal) * self.gain
    
    def get_frequency_response(self, frequencies):
        """Получить частотную характеристику (постоянная для всех частот)"""
        return np.full_like(frequencies, self.gain, dtype=complex)


class FIRHighPassFilter:
    """FIR высокочастотный фильтр с окном Блэкмана"""
    
    def __init__(self, cutoff_freq, sample_rate, filter_order=51):
        self.cutoff_freq = cutoff_freq
        self.sample_rate = sample_rate
        self.filter_order = filter_order
        self.coefficients = self._calculate_coefficients()
    
    def _blackman_window(self, n, N):
        """Вычислить значение окна Блэкмана для индекса n из N точек"""
        if n < 0 or n >= N:
            return 0.0
        return 0.42 - 0.5 * math.cos(2 * math.pi * n / (N - 1)) + 0.08 * math.cos(4 * math.pi * n / (N - 1))
    
    def _calculate_coefficients(self):
        """Вычислить коэффициенты FIR высокочастотного фильтра"""
        N = self.filter_order
        M = (N - 1) // 2  # Центральный индекс
        
        # Нормированная частота среза
        wc = 2 * math.pi * self.cutoff_freq / self.sample_rate
        
        coefficients = []
        
        for n in range(N):
            # Идеальная импульсная характеристика высокочастотного фильтра
            if n == M:
                # Особый случай для центрального коэффициента
                h_ideal = 1 - wc / math.pi
            else:
                # Общий случай
                h_ideal = -math.sin(wc * (n - M)) / (math.pi * (n - M))
            
            # Применение окна Блэкмана
            window_value = self._blackman_window(n, N)
            coefficient = h_ideal * window_value
            coefficients.append(coefficient)
        
        return np.array(coefficients)
    
    def filter(self, signal):
        """Применить FIR фильтр к сигналу методом свертки"""
        # Используем numpy для эффективной свертки
        filtered = np.convolve(signal, self.coefficients, mode='same')
        return filtered
    
    def get_frequency_response(self, frequencies):
        """Получить частотную характеристику фильтра"""
        # Вычисляем частотную характеристику через ДПФ коэффициентов
        N = len(frequencies)
        response = np.zeros(N, dtype=complex)
        
        for k, freq in enumerate(frequencies):
            omega = 2 * math.pi * freq / self.sample_rate
            H = 0
            for n, coeff in enumerate(self.coefficients):
                H += coeff * np.exp(-1j * omega * n)
            response[k] = H
        
        return response


class IIRLowPassFilter:
    """IIR однополюсный низкочастотный фильтр"""
    
    def __init__(self, cutoff_freq, sample_rate):
        self.cutoff_freq = cutoff_freq
        self.sample_rate = sample_rate
        self.a, self.b = self._calculate_coefficients()
        self.prev_input = 0.0
        self.prev_output = 0.0
    
    def _calculate_coefficients(self):
        """Вычислить коэффициенты однополюсного НЧ-фильтра"""
        # Используем более стабильный подход для однополюсного RC-фильтра
        # H(s) = wc/(s + wc), где wc = 2*pi*fc
        
        # Билинейное преобразование: s = 2/T * (z-1)/(z+1)
        # где T = 1/fs - период дискретизации
        
        wc = 2 * math.pi * self.cutoff_freq  # аналоговая частота среза
        T = 1.0 / self.sample_rate
        
        # Предварительное искажение частоты для билинейного преобразования
        wc_prewarped = (2.0 / T) * math.tan(wc * T / 2.0)
        
        # Коэффициенты после билинейного преобразования
        # H(z) = (b0 + b1*z^-1) / (1 + a1*z^-1)
        
        # Нормализация
        norm = 2.0 / T + wc_prewarped
        
        b0 = wc_prewarped / norm
        b1 = wc_prewarped / norm  # Для НЧ-фильтра b1 = b0
        a1 = (2.0 / T - wc_prewarped) / norm
        
        return [1.0, -a1], [b0, b1]  # a = [a0, a1], b = [b0, b1]
    
    def filter(self, signal):
        """Применить IIR фильтр к сигналу"""
        filtered = np.zeros_like(signal)
        
        # Инициализация состояния фильтра
        prev_input = 0.0
        prev_output = 0.0
        
        for i, x in enumerate(signal):
            # Разностное уравнение: y[n] = b0*x[n] + b1*x[n-1] + a1*y[n-1]
            # Обратите внимание: a1 уже содержит правильный знак из _calculate_coefficients
            y = self.b[0] * x + self.b[1] * prev_input + self.a[1] * prev_output
            
            filtered[i] = y
            
            # Обновление предыдущих значений
            prev_input = x
            prev_output = y
        
        return filtered
    
    def get_frequency_response(self, frequencies):
        """Получить частотную характеристику фильтра"""
        response = np.zeros(len(frequencies), dtype=complex)
        
        for k, freq in enumerate(frequencies):
            omega = 2 * math.pi * freq / self.sample_rate
            z = np.exp(1j * omega)
            
            # H(z) = (b0 + b1*z^-1) / (a0 + a1*z^-1)
            numerator = self.b[0] + self.b[1] * (z ** -1)
            denominator = self.a[0] + self.a[1] * (z ** -1)
            
            response[k] = numerator / denominator
        
        return response