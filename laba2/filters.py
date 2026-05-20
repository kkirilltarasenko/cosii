import numpy as np
import math


class HomogeneousFilter:
    """Однородный фильтр - скользящее среднее"""

    def __init__(self, window_size=9):
        self.window_size = window_size

        # коэффициенты фильтра
        self.coefficients = np.ones(window_size) / window_size

    def filter(self, signal):
        """Фильтрация методом свертки"""
        return np.convolve(
            signal,
            self.coefficients,
            mode='same'
        )

    def get_frequency_response(self, frequencies):
        """Частотная характеристика"""

        response = np.zeros(
            len(frequencies),
            dtype=complex
        )

        for k, freq in enumerate(frequencies):

            omega = (
                2 * math.pi
                * freq
            )

            H = 0

            for n, coeff in enumerate(
                self.coefficients
            ):

                H += coeff * np.exp(
                    -1j * omega * n
                )

            response[k] = H

        return response


class FIRHighPassFilter:
    """ВЧ КИХ-фильтр с окном Блэкмана"""

    def __init__(
        self,
        cutoff_freq,
        sample_rate,
        filter_order=51
    ):

        self.cutoff_freq = cutoff_freq
        self.sample_rate = sample_rate
        self.filter_order = filter_order

        self.coefficients = (
            self._calculate_coefficients()
        )

    def _blackman_window(
        self,
        n,
        N
    ):

        return (
            0.42
            - 0.5 * math.cos(
                2 * math.pi * n / (N - 1)
            )
            + 0.08 * math.cos(
                4 * math.pi * n / (N - 1)
            )
        )

    def _calculate_coefficients(self):

        N = self.filter_order
        M = (N - 1) // 2

        wc = (
            2
            * math.pi
            * self.cutoff_freq
            / self.sample_rate
        )

        coeffs = []

        for n in range(N):

            if n == M:

                h = 1 - wc / math.pi

            else:

                h = (
                    -math.sin(
                        wc * (n - M)
                    )
                    /
                    (
                        math.pi
                        * (n - M)
                    )
                )

            h *= self._blackman_window(
                n,
                N
            )

            coeffs.append(h)

        return np.array(coeffs)

    def filter(self, signal):

        return np.convolve(
            signal,
            self.coefficients,
            mode='same'
        )

    def get_frequency_response(
        self,
        frequencies
    ):

        response = np.zeros(
            len(frequencies),
            dtype=complex
        )

        for k, freq in enumerate(
            frequencies
        ):

            omega = (
                2
                * math.pi
                * freq
                / self.sample_rate
            )

            H = 0

            for n, coeff in enumerate(
                self.coefficients
            ):

                H += coeff * np.exp(
                    -1j * omega * n
                )

            response[k] = H

        return response


class IIRLowPassFilter:
    """БИХ однополюсный НЧ-фильтр"""

    def __init__(
        self,
        cutoff_freq,
        sample_rate
    ):

        self.cutoff_freq = cutoff_freq
        self.sample_rate = sample_rate

        self.alpha = math.exp(
            -2
            * math.pi
            * cutoff_freq
            / sample_rate
        )

    def filter(
        self,
        signal
    ):

        filtered = np.zeros_like(
            signal
        )

        filtered[0] = signal[0]

        for n in range(
            1,
            len(signal)
        ):

            filtered[n] = (
                (1 - self.alpha)
                * signal[n]
                +
                self.alpha
                * filtered[n - 1]
            )

        return filtered

    def get_frequency_response(
        self,
        frequencies
    ):

        response = np.zeros(
            len(frequencies),
            dtype=complex
        )

        for i, freq in enumerate(
            frequencies
        ):

            omega = (
                2
                * math.pi
                * freq
                / self.sample_rate
            )

            z = np.exp(
                -1j * omega
            )

            response[i] = (
                (1 - self.alpha)
                /
                (
                    1
                    -
                    self.alpha * z
                )
            )

        return response
