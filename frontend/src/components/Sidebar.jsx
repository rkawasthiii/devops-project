const NAV = [
  { label: 'Dashboard', icon: '▦', active: true },
  { label: 'Appointments', icon: '🗓' },
  { label: 'Patients', icon: '⚕' },
  { label: 'Doctors', icon: '✚' },
  { label: 'Departments', icon: '⌂' },
  { label: 'Reports', icon: '📈' },
  { label: 'Settings', icon: '⚙' },
]

export default function Sidebar({ backendLive }) {
  return (
    <aside className="sidebar">
      <div className="brand">
        <span className="brand-mark">+</span>
        <div>
          <strong>MediDesk</strong>
          <small>Clinic OS</small>
        </div>
      </div>
      <nav className="nav">
        {NAV.map((item) => (
          <a
            key={item.label}
            href="#"
            onClick={(e) => e.preventDefault()}
            className={item.active ? 'nav-item active' : 'nav-item'}
          >
            <span className="nav-icon">{item.icon}</span>
            {item.label}
          </a>
        ))}
      </nav>
      <div className="sidebar-foot">
        <span className={`dot ${backendLive === null ? '' : backendLive ? 'dot-live' : 'dot-down'}`} />
        API {backendLive === null ? 'checking…' : backendLive ? 'live' : 'offline'}
      </div>
    </aside>
  )
}
