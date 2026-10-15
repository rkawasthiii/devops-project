const TYPE_LABELS = {
  consultation: 'Consult',
  follow_up: 'Follow-up',
  emergency: 'Emergency',
  checkup: 'Check-up',
}

export function StatusBadge({ status }) {
  return <span className={`badge badge-${status}`}>{status}</span>
}

export function TypeBadge({ type }) {
  return <span className={`tag tag-${type}`}>{TYPE_LABELS[type] || type}</span>
}
