import { useState } from 'react'

const DEPARTMENTS = [
  'General Medicine', 'Cardiology', 'Orthopedics', 'Pediatrics', 'Dermatology',
]
const DOCTORS = {
  'General Medicine': ['Dr. Priya Nair'],
  Cardiology: ['Dr. Asha Verma'],
  Orthopedics: ['Dr. Vikram Rao'],
  Pediatrics: ['Dr. Naina Kapoor'],
  Dermatology: ['Dr. Imran Sheikh'],
}

const EMPTY = {
  patient_name: '',
  patient_phone: '',
  doctor_name: DOCTORS['General Medicine'][0],
  department: 'General Medicine',
  visit_type: 'consultation',
  scheduled_at: '',
  duration_minutes: 30,
  reason: '',
}

export default function BookingModal({ onClose, onSubmit }) {
  const [form, setForm] = useState(EMPTY)
  const [error, setError] = useState(null)
  const [saving, setSaving] = useState(false)

  const set = (patch) => setForm((f) => ({ ...f, ...patch }))
  const onDept = (department) =>
    set({ department, doctor_name: DOCTORS[department][0] })

  const submit = async (e) => {
    e.preventDefault()
    setError(null)
    setSaving(true)
    try {
      await onSubmit({
        ...form,
        duration_minutes: Number(form.duration_minutes),
        scheduled_at: new Date(form.scheduled_at).toISOString(),
      })
    } catch (err) {
      setError(err.message)
      setSaving(false)
    }
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()} role="dialog" aria-modal="true">
        <header className="modal-head">
          <h2>Book appointment</h2>
          <button className="modal-close" onClick={onClose} aria-label="Close">×</button>
        </header>
        <form onSubmit={submit} className="modal-body">
          {error && <div className="banner banner-error">{error}</div>}
          <label className="field">
            <span>Patient name *</span>
            <input required value={form.patient_name}
              onChange={(e) => set({ patient_name: e.target.value })} />
          </label>
          <label className="field">
            <span>Phone</span>
            <input value={form.patient_phone}
              onChange={(e) => set({ patient_phone: e.target.value })}
              placeholder="+91-…" />
          </label>
          <label className="field">
            <span>Department *</span>
            <select value={form.department} onChange={(e) => onDept(e.target.value)}>
              {DEPARTMENTS.map((d) => <option key={d}>{d}</option>)}
            </select>
          </label>
          <label className="field">
            <span>Doctor *</span>
            <select value={form.doctor_name}
              onChange={(e) => set({ doctor_name: e.target.value })}>
              {DOCTORS[form.department].map((d) => <option key={d}>{d}</option>)}
            </select>
          </label>
          <div className="field-row">
            <label className="field">
              <span>Date &amp; time *</span>
              <input required type="datetime-local" value={form.scheduled_at}
                onChange={(e) => set({ scheduled_at: e.target.value })} />
            </label>
            <label className="field">
              <span>Duration (min)</span>
              <input type="number" min="5" max="240" value={form.duration_minutes}
                onChange={(e) => set({ duration_minutes: e.target.value })} />
            </label>
          </div>
          <label className="field">
            <span>Visit type</span>
            <select value={form.visit_type}
              onChange={(e) => set({ visit_type: e.target.value })}>
              <option value="consultation">Consultation</option>
              <option value="follow_up">Follow-up</option>
              <option value="emergency">Emergency</option>
              <option value="checkup">Check-up</option>
            </select>
          </label>
          <label className="field">
            <span>Reason / notes</span>
            <textarea rows="2" value={form.reason}
              onChange={(e) => set({ reason: e.target.value })} />
          </label>
          <footer className="modal-foot">
            <button type="button" className="btn" onClick={onClose}>Cancel</button>
            <button type="submit" className="btn btn-primary" disabled={saving}>
              {saving ? 'Booking…' : 'Book appointment'}
            </button>
          </footer>
        </form>
      </div>
    </div>
  )
}
