import { api } from './client'

export async function fetchNeos(start?: string, end?: string) {
  const params: Record<string, string> = {}
  if (start) params.start_date = start
  if (end) params.end_date = end
  const { data } = await api.get('/neos', { params })
  return data
}

export async function fetchNeoById(id: string) {
  const { data } = await api.get(`/neos/${id}`)
  return data
}
