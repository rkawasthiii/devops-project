export default function Topbar({ onBook }) {
  const today = new Date().toLocaleDateString('en-IN', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  })
  return (
    <header className="topbar">
      <div>
        <h1>Clinic Operations</h1>
        <p className="muted">{today} · Sunrise Multi-Speciality Clinic</p>
      </div>
      <button className="btn btn-primary" onClick={onBook}>
        + Book appointment
      </button>
    </header>
  )
}
