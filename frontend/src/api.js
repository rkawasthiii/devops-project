// Thin fetch wrapper around the MediDesk REST API.
// The browser only ever talks to same-origin paths; Nginx (local) and the
// Kubernetes Ingress (cluster) forward /api/* to the backend service.

async function request(path, options = {}) {
  const resp = await fetch(path, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!resp.ok) {
    let detail = `${resp.status} ${resp.statusText}`
    try {
      const body = await resp.json()
      if (body?.detail) detail = Array.isArray(body.detail)
        ? body.detail.map((d) => d.msg).join(', ')
        : body.detail
    } catch { /* keep status text */ }
    throw new Error(detail)
  }
  return resp.status === 204 ? null : resp.json()
}

export const api = {
  health: () => request('/health'),
  listAppointments: (filters = {}) => {
    const params = new URLSearchParams()
    Object.entries(filters).forEach(([key, value]) => {
      if (value) params.set(key, value)
    })
    const qs = params.toString()
    return request(`/api/appointments${qs ? `?${qs}` : ''}`)
  },
  stats: () => request('/api/appointments/stats'),
  createAppointment: (payload) =>
    request('/api/appointments', { method: 'POST', body: JSON.stringify(payload) }),
  updateAppointment: (id, payload) =>
    request(`/api/appointments/${id}`, { method: 'PUT', body: JSON.stringify(payload) }),
  deleteAppointment: (id) => request(`/api/appointments/${id}`, { method: 'DELETE' }),
}
