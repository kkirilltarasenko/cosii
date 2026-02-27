import math
import cmath

def bit_reverse(n, bits):
    result = 0
    for _ in range(bits):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result

def bit_reverse_array(arr):
    n = len(arr)
    bits = n.bit_length() - 1
    result = [0] * n
    for i in range(n):
        j = bit_reverse(i, bits)
        result[j] = arr[i]
    return result

def _fft_dif_recursive(a, direction=1):
    n = len(a)

    if n == 1:
        return a

    half = n // 2
    
    # Улучшенное вычисление корней единицы для повышения точности
    angle = -2.0 * math.pi * direction / n
    
    # Используем более точное вычисление комплексных экспонент
    omega_n = cmath.exp(1j * angle)
    
    # Инициализация с высокой точностью
    omega = complex(1.0, 0.0)
    
    # Операция бабочки для DIF FFT с улучшенной точностью
    for j in range(half):
        temp1 = a[j]
        temp2 = a[j + half]
        
        a[j] = temp1 + temp2
        a[j + half] = (temp1 - temp2) * omega
        
        # Более точное обновление omega для предотвращения накопления ошибок
        if j < half - 1:  # Избегаем лишнего умножения на последней итерации
            omega *= omega_n
            
            # Периодическая нормализация для предотвращения дрейфа
            if j % 64 == 63:  # Каждые 64 итерации
                magnitude = abs(omega)
                if magnitude > 0:
                    omega = omega / magnitude
    
    # Рекурсивный вызов для каждой части
    first_half = _fft_dif_recursive(a[:half], direction)
    second_half = _fft_dif_recursive(a[half:], direction)
    
    # Объединение двух частей
    return first_half + second_half

def _fft_dif_iterative(a, direction=1):
    """
    Итеративная версия DIF FFT для больших сигналов.
    Более стабильна численно чем рекурсивная версия.
    """
    n = len(a)
    if n <= 1:
        return a
    
    # Проверяем, что n - степень двойки
    if n & (n - 1) != 0:
        raise ValueError("Длина массива должна быть степенью двойки")
    
    # Копируем входной массив
    result = a.copy()
    
    # Количество уровней
    levels = n.bit_length() - 1
    
    # DIF FFT - работаем от больших блоков к меньшим
    for level in range(levels):
        block_size = n >> level  # Размер блока на текущем уровне
        half_block = block_size >> 1
        
        # Угол для корней единицы
        angle = -2.0 * math.pi * direction / block_size
        omega_n = cmath.exp(1j * angle)
        
        # Обрабатываем все блоки на текущем уровне
        for block_start in range(0, n, block_size):
            omega = complex(1.0, 0.0)
            
            # Операции бабочки внутри блока
            for j in range(half_block):
                idx1 = block_start + j
                idx2 = block_start + j + half_block
                
                temp1 = result[idx1]
                temp2 = result[idx2]
                
                result[idx1] = temp1 + temp2
                result[idx2] = (temp1 - temp2) * omega
                
                # Обновляем omega
                if j < half_block - 1:
                    omega *= omega_n
                    
                    # Периодическая нормализация
                    if j % 32 == 31:
                        magnitude = abs(omega)
                        if magnitude > 0:
                            omega = omega / magnitude
    
    # Применяем bit-reversal
    return bit_reverse_array(result)

# Прямое преобразование
def fft_dif(a, direction=1):
    a_copy = a.copy()
    
    result = _fft_dif_recursive(a_copy, direction)
    
    return bit_reverse_array(result)

# Обратное преобразование
def ifft_dif(x):
    n = len(x)
    # Для обратного FFT: сопряжение -> FFT -> сопряжение -> деление на n
    x_conj = [_x.conjugate() for _x in x]
    X = fft_dif(x_conj, direction=1)
    x_restored = [X[i].conjugate() / n for i in range(n)]
    return x_restored

def pad_to_power_of_2(signal):
    n = len(signal)
    size = 1 << (n - 1).bit_length()
    return signal + [0] * (size - n)