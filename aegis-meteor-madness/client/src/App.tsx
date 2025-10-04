import React from 'react'
import { CelestialView } from './components/views/CelestialView'
import { GeospatialView } from './components/views/GeospatialView'
import { ControlPanel } from './components/views/ControlPanel'

export default function App() {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: '320px 1fr', height: '100vh' }}>
      <div style={{ borderRight: '1px solid #e5e7eb', padding: 16, overflowY: 'auto' }}>
        <ControlPanel />
      </div>
      <div style={{ display: 'grid', gridTemplateRows: '1fr 1fr' }}>
        <div style={{ borderBottom: '1px solid #e5e7eb' }}>
          <CelestialView />
        </div>
        <div>
          <GeospatialView />
        </div>
      </div>
    </div>
  )
}
