import { create } from 'zustand'
import type { SimulationParams } from '@/api/simulationApi'

export type SimulationState = SimulationParams & {
  taskId?: string
}

const defaultState: SimulationState = {
  impactorDiameter: 100,
  impactorDensity: 3000,
  impactVelocity: 20,
  impactAngle: 45,
  targetType: 'Sedimentary Rock',
  targetLat: 34.0522,
  targetLon: -118.2437,
}

export const useSimulationStore = create<{
  state: SimulationState
  update: (partial: Partial<SimulationState>) => void
  setTaskId: (id?: string) => void
}>(set => ({
  state: defaultState,
  update: partial => set(s => ({ state: { ...s.state, ...partial } })),
  setTaskId: id => set(s => ({ state: { ...s.state, taskId: id } })),
}))
