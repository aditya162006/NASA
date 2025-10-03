import React from 'react'
import { useSimulationStore } from '@/store/simulationStore'
import { startSimulation, getSimulationStatus } from '@/api/simulationApi'

export function ControlPanel() {
  const { state, update, setTaskId } = useSimulationStore()

  async function run() {
    const { task_id } = await startSimulation({
      impactorDiameter: state.impactorDiameter,
      impactorDensity: state.impactorDensity,
      impactVelocity: state.impactVelocity,
      impactAngle: state.impactAngle,
      targetType: state.targetType,
      targetLat: state.targetLat,
      targetLon: state.targetLon,
    })
    setTaskId(task_id)
    // Optionally start polling here
    const first = await getSimulationStatus(task_id)
    console.log(first)
  }

  return (
    <div>
      <h2>Controls</h2>
      <label>
        Diameter (m)
        <input type="number" value={state.impactorDiameter} onChange={e => update({ impactorDiameter: Number(e.target.value) })} />
      </label>
      <label>
        Density (kg/m³)
        <input type="number" value={state.impactorDensity} onChange={e => update({ impactorDensity: Number(e.target.value) })} />
      </label>
      <label>
        Velocity (km/s)
        <input type="number" value={state.impactVelocity} onChange={e => update({ impactVelocity: Number(e.target.value) })} />
      </label>
      <label>
        Angle (deg)
        <input type="number" value={state.impactAngle} onChange={e => update({ impactAngle: Number(e.target.value) })} />
      </label>
      <label>
        Target Lat
        <input type="number" value={state.targetLat} onChange={e => update({ targetLat: Number(e.target.value) })} />
      </label>
      <label>
        Target Lon
        <input type="number" value={state.targetLon} onChange={e => update({ targetLon: Number(e.target.value) })} />
      </label>
      <button onClick={run}>Run Simulation</button>
    </div>
  )
}
