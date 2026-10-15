export default function KpiCards({ stats, loading }) {
  const cards = [
    { label: "Today's appointments", value: stats?.today, accent: 'teal' },
    { label: 'Scheduled (7 days)', value: stats?.upcoming_week, accent: 'blue' },
    { label: 'Completed visits', value: stats?.completed, accent: 'green' },
    { label: 'Cancelled', value: stats?.cancelled, accent: 'red' },
    { label: 'Doctors on roster', value: stats?.doctors, accent: 'violet' },
  ]
  return (
    <section className="kpis">
      {cards.map((c) => (
        <div className={`kpi kpi-${c.accent}`} key={c.label}>
          <span className="kpi-value">{loading ? '—' : c.value ?? '—'}</span>
          <span className="kpi-label">{c.label}</span>
        </div>
      ))}
    </section>
  )
}
