import math

# Прямое преобразование
def fft_dif(a, direction=1):
    # Если длина вектора равна 1, вернуть a.
    n = len(a)

    if n == 1:
        return a

    # Присвоить ωN значение главного комплексного корня N-й степени из единицы:
    # ωN = cos(2π/N) + dir ⋅ isin(2π/N)
    angle = 2 * math.pi / n
    omega_n = complex(math.cos(angle), direction * math.sin(angle))

    # Присвоить ω = 1, 0j - чтоб избежать конфликта для комплексных чисел
    omega = 1 + 0j

    half = n // 2

    for j in range(half):
        temp1 = a[j]
        temp2 = a[j + half]

        a[j] = temp1 + temp2
        a[j + half] = (temp1 - temp2) * omega

        omega *= omega_n

    # Рекурсивно вызвать БПФ на каждой из частей
    first_half = fft_dif(a[:half], direction)
    second_half = fft_dif(a[half:], direction)


    return first_half + second_half

# Обратное преобразование
def ifft_dif(x):
    n = len(x)
    x_conj = [_x.conjugate() for _x in x]
    X = fft_dif(x_conj)
    x_restored = [X[i].conjugate() / n for i in range(n)]
    return x_restored

def pad_to_power_of_2(signal):
    n = len(signal)
    size = 1 << (n - 1).bit_length()
    return signal + [0] * (size - n)