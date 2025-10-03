from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Tuple

import math

MU_SUN = 1.32712440018e20  # m^3/s^2


@dataclass
class KeplerianElements:
    semi_major_axis_m: float
    eccentricity: float
    inclination_rad: float
    raan_rad: float
    arg_periapsis_rad: float
    mean_anomaly_rad: float


class KeplerianPropagator:
    def __init__(self, elements: KeplerianElements) -> None:
        self.elements = elements

    def calculate_trajectory(
        self, start_time: datetime, end_time: datetime, time_step_seconds: float
    ) -> List[Dict[str, float]]:
        if start_time.tzinfo is None:
            start_time = start_time.replace(tzinfo=timezone.utc)
        if end_time.tzinfo is None:
            end_time = end_time.replace(tzinfo=timezone.utc)

        results: List[Dict[str, float]] = []
        dt = start_time
        while dt <= end_time:
            M = self.elements.mean_anomaly_rad + self._mean_motion() * (
                (dt - start_time).total_seconds()
            )
            E = self._solve_keplers_equation(M, self.elements.eccentricity)
            x, y, z = self._state_from_elements(E)
            results.append({"t": dt.timestamp(), "x": x, "y": y, "z": z})
            dt += timedelta(seconds=time_step_seconds)
        return results

    def _mean_motion(self) -> float:
        a = self.elements.semi_major_axis_m
        return math.sqrt(MU_SUN / (a ** 3))

    def _solve_keplers_equation(self, M: float, e: float, tol: float = 1e-8) -> float:
        E = M if e < 0.8 else math.pi
        for _ in range(100):
            f = E - e * math.sin(E) - M
            fp = 1 - e * math.cos(E)
            dE = -f / fp
            E += dE
            if abs(dE) < tol:
                break
        return E

    def _state_from_elements(self, E: float) -> Tuple[float, float, float]:
        a = self.elements.semi_major_axis_m
        e = self.elements.eccentricity
        i = self.elements.inclination_rad
        Omega = self.elements.raan_rad
        omega = self.elements.arg_periapsis_rad

        x_prime = a * (math.cos(E) - e)
        y_prime = a * math.sqrt(1 - e * e) * math.sin(E)
        z_prime = 0.0

        cos_Omega = math.cos(Omega)
        sin_Omega = math.sin(Omega)
        cos_i = math.cos(i)
        sin_i = math.sin(i)
        cos_omega = math.cos(omega)
        sin_omega = math.sin(omega)

        x = (
            (cos_Omega * cos_omega - sin_Omega * sin_omega * cos_i) * x_prime
            + (-cos_Omega * sin_omega - sin_Omega * cos_omega * cos_i) * y_prime
        )
        y = (
            (sin_Omega * cos_omega + cos_Omega * sin_omega * cos_i) * x_prime
            + (-sin_Omega * sin_omega + cos_Omega * cos_omega * cos_i) * y_prime
        )
        z = (sin_omega * sin_i) * x_prime + (cos_omega * sin_i) * y_prime
        return x, y, z
