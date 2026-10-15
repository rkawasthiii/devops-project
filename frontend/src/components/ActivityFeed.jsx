const VERB = {
  scheduled: 'Booked',
  completed: 'Completed',
  cancelled: 'Cancelled',
}

export default function ActivityFeed({ items }) {
  return (
    <section className="panel rail-panel">
      <h3 className="panel-title">Recent activity</h3>
      <ul className="feed">
        {items.length === 0 && <li className="muted">No activity yet.</li>}
        {items.map((a) => (
          <li key={a.id} className="feed-item">
            <span className={`feed-dot feed-${a.status}`} />
            <div>
              <p className="feed-text">
                <strong>{VERB[a.status] || 'Updated'}</strong> — {a.patient_name} with {a.doctor_name}
              </p>
              <p className="feed-time">
                {new Date(a.updated_at).toLocaleString('en-IN', {
                  day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit',
                })}
              </p>
            </div>
          </li>
        ))}
      </ul>
    </section>
  )
}
