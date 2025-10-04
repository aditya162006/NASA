from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

import requests
from requests import Response

from app import redis_client

NASA_BASE_URL = "https://api.nasa.gov/neo/rest/v1"


class NasaApiService:
    def __init__(self, api_key: Optional[str] = None) -> None:
        self.api_key = api_key or os.getenv("NASA_API_KEY", "DEMO_KEY")

    def _get(self, path: str, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
        url = f"{NASA_BASE_URL}{path}"
        params = params.copy() if params else {}
        params["api_key"] = self.api_key

        cache_key = f"nasa:{path}:{json.dumps(params, sort_keys=True)}"
        if redis_client is not None:
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)

        try:
            resp: Response = requests.get(url, params=params, timeout=15)
            resp.raise_for_status()
        except requests.HTTPError as e:
            status = e.response.status_code if e.response is not None else 500
            raise RuntimeError(f"NASA API HTTP error: {status}") from e
        except requests.RequestException as e:
            raise RuntimeError("NASA API request failed") from e

        data: Dict[str, Any] = resp.json()
        if redis_client is not None:
            redis_client.setex(cache_key, 900, json.dumps(data))
        return data

    def fetch_neos_by_date_range(self, start_date: str | None, end_date: str | None) -> List[Dict[str, Any]]:
        params: Dict[str, Any] = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        data = self._get("/feed", params)
        neos: List[Dict[str, Any]] = []
        for date, objects in data.get("near_earth_objects", {}).items():
            for obj in objects:
                est = obj.get("estimated_diameter", {}).get("meters", {})
                neos.append(
                    {
                        "id": obj.get("id"),
                        "name": obj.get("name"),
                        "estimated_diameter_m": {
                            "min": est.get("estimated_diameter_min"),
                            "max": est.get("estimated_diameter_max"),
                        },
                        "close_approach_date": date,
                    }
                )
        return neos

    def fetch_neo_by_id(self, asteroid_id: str) -> Optional[Dict[str, Any]]:
        data = self._get(f"/neo/{asteroid_id}")
        if not data:
            return None
        return {
            "id": data.get("id"),
            "name": data.get("name"),
            "orbital_data": data.get("orbital_data", {}),
            "physical_data": {
                "estimated_diameter": data.get("estimated_diameter", {}),
                "absolute_magnitude_h": data.get("absolute_magnitude_h"),
            },
        }
