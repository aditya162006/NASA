import React, { useEffect, useRef } from 'react'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

export function GeospatialView() {
  const mapRef = useRef<HTMLDivElement>(null)
  const leafletRef = useRef<L.Map>()

  useEffect(() => {
    const container = mapRef.current!
    const map = L.map(container).setView([34.0522, -118.2437], 4)
    leafletRef.current = map

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map)

    return () => {
      map.remove()
    }
  }, [])

  return <div ref={mapRef} style={{ width: '100%', height: '100%' }} />
}
