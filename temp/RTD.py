import math
import numpy as np


class RTD:

    def __init__(self, R0=1000.0, A=3.9083e-3, B=-5.775e-7, C=-4.183e-12):
        """
        Callendar–Van Dusen RTD model.

        Default coefficients correspond to IEC 60751 platinum RTDs
        (PT100/PT1000).

        Parameters
        ----------
        R0 : float
            Resistance at 0°C.
        A, B, C : float
            Callendar–Van Dusen coefficients.
        """

        self.R0 = R0

        self.A = A
        self.B = B
        self.C = C

        self.R = R0
        self.temp = 0.0

    def set_resistance(self, value):
        if value <= 0:
            raise ValueError("Resistance must be greater than zero.")

        self.R = value

        # First solve assuming T >= 0°C
        a = self.B
        b = self.A
        c = 1 - self.R / self.R0

        discriminant = b**2 - 4 * a * c

        if discriminant < 0:
            raise ValueError("No valid temperature solution.")

        T = (-b + math.sqrt(discriminant)) / (2 * a)

        # If solution is below 0°C use Newton-Raphson on full equation
        if T < 0:
            T = self.__solve_negative_temperature()

        self.temp = T

    def get_resistance(self):
        return self.R

    def set_temperature(self, value):
        self.temp = value

        if value >= 0:
            self.R = self.R0 * (
                1
                + self.A * value
                + self.B * value**2
            )
        else:
            self.R = self.R0 * (
                1
                + self.A * value
                + self.B * value**2
                + self.C * (value - 100) * value**3
            )

    def get_temperature(self):
        return self.temp

    def get_coefficients(self):
        return {
            "R0": self.R0,
            "A": self.A,
            "B": self.B,
            "C": self.C,
        }

    def __solve_negative_temperature(self):
        """
        Newton-Raphson solver for temperatures below 0°C.
        """

        T = -50.0

        for _ in range(30):

            f = self.R0 * (
                1
                + self.A * T
                + self.B * T**2
                + self.C * (T - 100) * T**3
            ) - self.R

            df = self.R0 * (
                self.A
                + 2 * self.B * T
                + self.C * (
                    4 * T**3
                    - 300 * T**2
                )
            )

            T_next = T - f / df

            if abs(T_next - T) < 1e-8:
                return T_next

            T = T_next

        return T