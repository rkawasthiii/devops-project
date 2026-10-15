import { StatusBadge, TypeBadge } from './StatusBadge'

function fmtDateTime(iso) {
  const d = new Date(iso)
  return {
    date: d.toLocaleDateString('en-IN', { day: 'numeric', month: 'short' }),
    time: d.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' }),
  }
}

export default function AppointmentTable({
  appointments, loading, busyId, onComplete, onCancel, onDelete,
}) {
  return (
    <div className="table-wrap">
      <table className="table">
        <thead>
          <tr>
            <th>Patient</th>
            <th>Doctor</th>
            <th>Department</th>
            <th>Schedule</th>
            <th>Type</th>
            <th>Status</th>
            <th className="col-actions">Actions</th>
          </tr>
        </thead>
        <tbody>
          {loading &&
            Array.from({ length: 5 }).map((_, i) => (
              <tr key={`skel-${i}`} className="skel-row">
                <td colSpan={7}><div className="skel" /></td>
              </tr>
            ))}
          {!loading && appointments.length === 0 && (
            <tr>
              <td colSpan={7} className="empty">
                No appointments match these filters.
              </td>
            </tr>
          )}
          {!loading &&
            appointments.map((a) => {
              const { date, time } = fmtDateTime(a.scheduled_at)
              const busy = busyId === a.id
              return (
                <tr key={a.id}>
                  <td>
                    <div className="cell-strong">{a.patient_name}</div>
                    <div className="cell-sub">{a.reason || '—'}</div>
                  </td>
                  <td>{a.doctor_name}</td>
                  <td>{a.department}</td>
                  <td>
                    <div className="cell-strong">{date}</div>
                    <div className="cell-sub">{time} · {a.duration_minutes}m</div>
                  </td>
                  <td><TypeBadge type={a.visit_type} /></td>
                  <td><StatusBadge status={a.status} /></td>
                  <td className="col-actions">
                    {a.status === 'scheduled' && (
                      <>
                        <button
                          className="btn-xs btn-ok"
                          disabled={busy}
                          onClick={() => onComplete(a.id)}
                        >Done</button>
                        <button
                          className="btn-xs btn-warn"
                          disabled={busy}
                          onClick={() => onCancel(a.id)}
                        >Cancel</button>
                      </>
                    )}
                    <button
                      className="btn-xs btn-danger"
                      disabled={busy}
                      onClick={() => onDelete(a.id)}
                    >Delete</button>
                  </td>
                </tr>
              )
            })}
        </tbody>
      </table>
    </div>
  )
}
