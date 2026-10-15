export default function DepartmentBars({ stats }) {
  const entries = Object.entries(stats?.by_department || {}).sort((a, b) => b[1] - a[1])
  const max = Math.max(1, ...entries.map(([, n]) => n))
  return (
    <section className="panel rail-panel">
      <h3 className="panel-title">Load by department</h3>
      {entries.length === 0 && <p className="muted">No data.</p>}
      {entries.map(([dept, n]) => (
        <div className="bar-row" key={dept}>
          <span className="bar-label">{dept}</span>
          <div className="bar-track">
            <div className="bar-fill" style={{ width: `${(n / max) * 100}%` }} />
          </div>
          <span className="bar-value">{n}</span>
        </div>
      ))}
    </section>
  )
}
