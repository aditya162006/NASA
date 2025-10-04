import { api } from './client'

export type SimulationParams = {
  impactorDiameter: number
  impactorDensity: number
  impactVelocity: number
  impactAngle: number
  targetType: 'Sedimentary Rock' | 'Crystalline Rock' | 'Water'
  targetLat: number
  targetLon: number
}

export async function startSimulation(params: SimulationParams) {
  const { data } = await api.post('/simulate', params)
  return data as { task_id: string; status_url: string }
}

export async function getSimulationStatus(taskId: string) {
  const { data } = await api.get(`/simulate/status/${taskId}`)
  return data as { task_id: string; status: string; result?: unknown }
}
