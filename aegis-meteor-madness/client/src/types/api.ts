export type NeoSummary = {
  id: string
  name: string
  estimated_diameter_m: { min: number; max: number }
  close_approach_date: string
}
