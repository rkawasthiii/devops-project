import { useCallback, useEffect, useMemo, useState } from 'react'
import { api } from './api'
import Sidebar from './components/Sidebar'
import Topbar from './components/Topbar'
import KpiCards from './components/KpiCards'
import Filters from './components/Filters'
import AppointmentTable from './components/AppointmentTable'
import ActivityFeed from './components/ActivityFeed'
import DepartmentBars from './components/DepartmentBars'
import BookingModal from './components/BookingModal'

export default function App() {
  const [appointments, setAppointments] = useState([])
  const [stats, setStats] = useState(null)
  const [filters, setFilters] = useState({ status: '', department: '', search: '' })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [modalOpen, setModalOpen] = useState(false)
  const [backendLive, setBackendLive] = useState(null)
  const [busyId, setBusyId] = useState(null)

  const load = useCallback(async () => {
    setError(null)
    try {
      const [rows, s] = await Promise.all([
        api.listAppointments(filters),
        api.stats(),
      ])
      setAppointments(rows)
      setStats(s)
      setBackendLive(true)
    } catch (err) {
      setError(err.message || 'backend unreachable')
      setBackendLive(false)
    } finally {
      setLoading(false)
    }
  }, [filters])

  useEffect(() => {
    setLoading(true)
    const t = setTimeout(load, 150) // small debounce for search typing
    return () => clearTimeout(t)
  }, [load])

  useEffect(() => {
    const tick = () => api.health().then(() => setBackendLive(true)).catch(() => setBackendLive(false))
    tick()
    const id = setInterval(tick, 15000)
    return () => clearInterval(id)
  }, [])

  const act = async (id, action) => {
    setBusyId(id)
    try {
      await action()
      await load()
    } catch (err) {
      setError(err.message)
    } finally {
      setBusyId(null)
    }
  }

  const complete = (id) => act(id, () => api.updateAppointment(id, { status: 'completed' }))
  const cancel = (id) => act(id, () => api.updateAppointment(id, { status: 'cancelled' }))
  const remove = (id) => {
    if (!window.confirm('Delete this appointment permanently?')) return
    act(id, () => api.deleteAppointment(id))
  }
  const book = async (payload) => {
    await api.createAppointment(payload)
    setModalOpen(false)
    await load()
  }

  const departments = useMemo(
    () => (stats ? Object.keys(stats.by_department).sort() : []),
    [stats],
  )
  const activity = useMemo(
    () =>
      [...appointments]
        .sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at))
        .slice(0, 6),
    [appointments],
  )

  return (
    <div className="shell">
      <Sidebar backendLive={backendLive} />
      <main className="main">
        <Topbar onBook={() => setModalOpen(true)} />
        {error && (
          <div className="banner banner-error" role="alert">
            <span>Could not reach the backend API — {error}</span>
            <button onClick={load}>Retry</button>
          </div>
        )}
        <KpiCards stats={stats} loading={loading && !stats} />
        <div className="content-grid">
          <section className="panel">
            <Filters filters={filters} onChange={setFilters} departments={departments} />
            <AppointmentTable
              appointments={appointments}
              loading={loading}
              busyId={busyId}
              onComplete={complete}
              onCancel={cancel}
              onDelete={remove}
            />
          </section>
          <aside className="rail">
            <DepartmentBars stats={stats} />
            <ActivityFeed items={activity} />
          </aside>
        </div>
      </main>
      {modalOpen && <BookingModal onClose={() => setModalOpen(false)} onSubmit={book} />}
    </div>
  )
}
