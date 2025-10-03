from __future__ import annotations

from typing import Any, Dict, Tuple

import rasterio


class UsgsService:
    def __init__(self, dem_path: str = "/data/usgs/dem.tif") -> None:
        self.dem_path = dem_path

    def get_elevation_for_bbox(self, bounding_box: Tuple[float, float, float, float]) -> Dict[str, Any]:
        # min_lon, min_lat, max_lon, max_lat
        with rasterio.open(self.dem_path) as src:
            # This is a stub for now; real implementation will window by bbox
            data = src.read(1, out_shape=(256, 256))
            return {"width": data.shape[1], "height": data.shape[0], "stats": {
                "min": float(data.min()),
                "max": float(data.max()),
                "mean": float(data.mean()),
            }}

    def get_historical_seismicity(self, bounding_box: Tuple[float, float, float, float]):
        # Stub: would call USGS NEIC API
        return {"events": []}
