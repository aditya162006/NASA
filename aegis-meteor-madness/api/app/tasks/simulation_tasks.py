from __future__ import annotations

from celery import shared_task
from typing import Dict, Any

from app.core.impact_calculator import calculate_impact_effects, ImpactParameters


@shared_task(bind=True)
def run_full_simulation_task(self, params: Dict[str, Any]):
    distances = [1, 5, 10, 20, 50, 100, 200]
    impact_params = ImpactParameters(
        impactor_diameter_m=float(params["impactorDiameter"]),
        impactor_density_kg_m3=float(params["impactorDensity"]),
        impact_velocity_km_s=float(params["impactVelocity"]),
        impact_angle_deg=float(params["impactAngle"]),
        target_type=str(params["targetType"]),
    )

    # Placeholder; later incorporate orbital propagation and geospatial tasks
    effects = calculate_impact_effects(impact_params, distances)
    return {
        "inputs": params,
        "effects": effects,
        "metadata": {
            "version": 1,
        },
    }
