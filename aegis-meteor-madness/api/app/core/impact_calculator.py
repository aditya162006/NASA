from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ImpactParameters:
    impactor_diameter_m: float
    impactor_density_kg_m3: float
    impact_velocity_km_s: float
    impact_angle_deg: float
    target_type: str


def calculate_impact_effects(impact_params: ImpactParameters, distances_km: List[float]) -> Dict:
    # Placeholder simplified outputs; to be replaced with Collins et al. model
    results = {
        "atmospheric_entry": {
            "fate": "intact",
            "airburst_altitude_km": 0.0,
            "kinetic_energy_j": 1.0e15,
            "kinetic_energy_kt": 238.85,
        },
        "crater": {
            "transient_diameter_km": 5.0,
            "transient_depth_km": 1.2,
            "final_diameter_km": 7.5,
            "final_depth_km": 1.0,
        },
        "ejecta": [],
        "thermal": {
            "fireball_radius_km": 3.0,
            "duration_s": 5.0,
            "by_distance": [],
        },
        "seismic": {
            "richter_magnitude": 6.0,
            "by_distance": [],
        },
        "air_blast": {
            "by_distance": [],
        },
    }

    for d in distances_km:
        results["ejecta"].append({"distance_km": d, "thickness_m": max(0.0, 0.5 / (d + 1e-3))})
        results["thermal"]["by_distance"].append(
            {"distance_km": d, "arrival_s": d / 0.3, "total_energy_j_m2": max(0.0, 1e6 / (d + 1))}
        )
        results["seismic"]["by_distance"].append(
            {"distance_km": d, "arrival_s": d / 5.0, "pgv_m_s": max(0.0, 1.0 / (d + 1))}
        )
        results["air_blast"]["by_distance"].append(
            {"distance_km": d, "arrival_s": d / 0.34, "overpressure_pa": max(0.0, 2e5 / (d + 1)), "wind_m_s": max(0.0, 100 / (d + 1))}
        )

    return results
