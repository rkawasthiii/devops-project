const STATUS_CHIPS = ['', 'scheduled', 'completed', 'cancelled']

export default function Filters({ filters, onChange, departments }) {
  const set = (patch) => onChange({ ...filters, ...patch })
  return (
    <div className="filters">
      <div className="chips">
        {STATUS_CHIPS.map((s) => (
          <button
            key={s || 'all'}
            className={filters.status === s ? 'chip chip-active' : 'chip'}
            onClick={() => set({ status: s })}
          >
            {s === '' ? 'All' : s}
          </button>
        ))}
      </div>
      <select
        className="select"
        value={filters.department}
        onChange={(e) => set({ department: e.target.value })}
      >
        <option value="">All departments</option>
        {departments.map((d) => (
          <option key={d} value={d}>{d}</option>
        ))}
      </select>
      <input
        className="input"
        type="search"
        placeholder="Search patient, doctor, reason…"
        value={filters.search}
        onChange={(e) => set({ search: e.target.value })}
      />
    </div>
  )
}
