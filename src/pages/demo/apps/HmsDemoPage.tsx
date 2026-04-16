import { useMemo, useState, type FormEvent } from 'react'
import { FiActivity, FiCalendar, FiClipboard, FiCreditCard, FiUsers } from 'react-icons/fi'
import {
  DemoBadge,
  DemoDataTable,
  DemoMetricGrid,
  DemoPanel,
  DemoShell,
  DemoToastStack,
  DemoTrendChart,
} from '../../../components/demo/DemoPrimitives'
import { buildDemoRequestPath, buildDemoWhatsAppHref } from '../../../config/demo-apps'
import { createHmsState, hmsUsers } from '../../../data/demo/hms'
import { buildToast, createCsvFromRows, downloadSampleFile } from '../../../lib/demo/mock'
import { useDemoAppState } from '../../../lib/demo/useDemoAppState'
import { useDemoNetworkGuard } from '../../../lib/demo/useDemoNetworkGuard'
import type { DemoAppRouteProps, DemoMetric, DemoNavItem } from '../../../lib/demo/types'
import Seo from '../../../components/ui/Seo'

const sections: DemoNavItem[] = [
  { slug: 'dashboard', label: 'Control Desk', icon: FiActivity, description: 'Reception, occupancy, and collections overview.' },
  { slug: 'patients', label: 'Patients', icon: FiUsers, description: 'Registration records and active patient flow.' },
  { slug: 'appointments', label: 'Appointments', icon: FiCalendar, description: 'Front-desk scheduling and doctor coordination.' },
  { slug: 'billing', label: 'Billing', icon: FiCreditCard, description: 'Collections, claims, and payment completion.' },
]

export default function HmsDemoPage({ app, section }: DemoAppRouteProps) {
  useDemoNetworkGuard()

  const { state, patchState, currentUser, users, switchUser, resetDemo, refreshDemo, isRefreshing, toasts, addToast } = useDemoAppState({
    storageKey: 'qode27-demo-hms',
    createInitialState: createHmsState,
    users: hmsUsers,
  })

  const activeSection = sections.some((item) => item.slug === section) ? section ?? 'dashboard' : 'dashboard'
  const [appointmentForm, setAppointmentForm] = useState({ patient: '', doctor: state.doctors[0]?.name ?? '', time: '03:15 PM', type: 'Follow-up' })

  const patientRows = useMemo(() => state.patients.map((patient) => ({ ...patient, id: patient.id })), [state.patients])
  const metrics: DemoMetric[] = [
    { label: 'Appointments Today', value: '126', change: '14 walk-ins included', tone: 'neutral' },
    { label: 'Collections', value: 'Rs 4.8L', change: 'Billing desk running ahead', tone: 'positive' },
    { label: 'Pending Claims', value: '11', change: '3 need escalation', tone: 'warning' },
    { label: 'Ward Utilisation', value: '82%', change: '12 beds available', tone: 'warning' },
  ]

  const handleUserSwitch = (email: string) => {
    switchUser(email)
    addToast(buildToast('Persona switched', 'Hospital workflow view updated for the selected role.', 'info'))
  }

  const handleReset = () => {
    resetDemo()
    addToast(buildToast('Demo reset', 'Hospital sample data has been restored.', 'success'))
  }

  const handleRefresh = () => {
    refreshDemo()
    addToast(buildToast('Desk refreshed', 'Clinical workflow view refreshed locally.', 'info'))
  }

  const handleAppointmentSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!appointmentForm.patient.trim()) {
      addToast(buildToast('Patient name required', 'Add a patient name to create a mock appointment.', 'warning'))
      return
    }

    patchState((current) => ({
      ...current,
      appointments: [
        {
          id: `APT-${Date.now()}`,
          patient: appointmentForm.patient,
          doctor: appointmentForm.doctor,
          time: appointmentForm.time,
          type: appointmentForm.type,
          status: 'Confirmed',
        },
        ...current.appointments,
      ],
    }))
    setAppointmentForm({ patient: '', doctor: state.doctors[0]?.name ?? '', time: '03:15 PM', type: 'Follow-up' })
    addToast(buildToast('Appointment created', 'Registration stayed inside local demo state.', 'success'))
  }

  const settleBilling = (billingId: string) => {
    patchState((current) => ({
      ...current,
      billings: current.billings.map((billing) => (billing.id === billingId ? { ...billing, status: 'Settled' } : billing)),
    }))
    addToast(buildToast('Billing updated', 'Collection status changed in the local sandbox.', 'success'))
  }

  const exportBilling = () => {
    downloadSampleFile(
      'qode27-hms-billing.csv',
      createCsvFromRows(
        state.billings.map((billing) => ({
          id: billing.id,
          department: billing.department,
          amount: billing.amount,
          paymentMode: billing.paymentMode,
          status: billing.status,
        })),
      ),
      'text/csv;charset=utf-8',
    )
    addToast(buildToast('Billing report ready', 'Sample collections report generated in-browser.', 'success'))
  }

  return (
    <>
      <Seo title="Hospital Management Interactive Demo | Qode27" description="Interactive frontend-only hospital management demo with patient flow, appointments, and billing." canonicalPath={activeSection === 'dashboard' ? '/demo/hms' : `/demo/hms/${activeSection}`} />

      <DemoShell
        app={app}
        sections={sections}
        activeSection={activeSection}
        title="A clinical operations interface built for speed, trust, and patient movement."
        subtitle="Unlike the HRMS demo, this product behaves more like a workflow desk. It emphasizes reception throughput, doctor coordination, patient status, and payment urgency with a denser but still premium medical UI."
        currentUser={currentUser}
        onSwitchUser={handleUserSwitch}
        users={users}
        onReset={handleReset}
        onRefresh={handleRefresh}
        isRefreshing={isRefreshing}
        actions={[
          { label: 'Request hospital rollout demo', href: buildDemoRequestPath('Hospital Management Demo') },
          { label: 'WhatsApp Qode27', href: buildDemoWhatsAppHref('Hospital Management Demo'), variant: 'secondary' },
        ]}
      >
        <DemoMetricGrid app={app} items={metrics} isRefreshing={isRefreshing} columnsClass="md:grid-cols-2 xl:grid-cols-4" />

        {activeSection === 'dashboard' ? (
          <>
            <div className="mt-4 grid gap-4 xl:grid-cols-[1.15fr_0.85fr]">
              <DemoPanel app={app} title="Care throughput" subtitle="Daily collection and patient movement shown like a clinical control surface.">
                <DemoTrendChart app={app} title="Daily collections (lakhs)" data={state.collectionsTrend} mode="lineish" />
              </DemoPanel>
              <DemoPanel app={app} title="Urgency board" subtitle="Compact medical priority view with a workflow tone.">
                <div className="space-y-3">
                  {[
                    ['Reception queue', '7 patients waiting check-in', 'warning'],
                    ['Lab billing', '2 claims missing insurer code', 'warning'],
                    ['Doctor availability', 'Cardiology and medicine running on schedule', 'positive'],
                  ].map(([title, note, tone]) => (
                    <div key={title} className="rounded-[1.15rem] border border-teal-100 bg-teal-50/50 p-4">
                      <div className="flex items-center justify-between gap-3">
                        <p className="text-sm font-semibold text-slate-950">{title}</p>
                        <DemoBadge app={app} value={tone === 'positive' ? 'Stable' : 'Attention'} tone={tone === 'positive' ? 'positive' : 'warning'} />
                      </div>
                      <p className="mt-2 text-sm leading-6 text-slate-600">{note}</p>
                    </div>
                  ))}
                </div>
              </DemoPanel>
            </div>

            <div className="mt-4 grid gap-4 xl:grid-cols-[1.1fr_0.9fr]">
              <DemoPanel app={app} title="Live patient board" subtitle="A slightly denser workflow list than the HRMS demo.">
                <DemoDataTable
                  app={app}
                  columns={[
                    { key: 'patient', header: 'Patient', render: (row) => <div><p className="font-semibold text-slate-950">{row.name}</p><p className="text-xs text-slate-500">{row.id}</p></div> },
                    { key: 'unit', header: 'Unit', render: (row) => row.unit },
                    { key: 'doctor', header: 'Doctor', render: (row) => row.doctor },
                    { key: 'bill', header: 'Billing', render: (row) => row.bill },
                    { key: 'status', header: 'Status', render: (row) => <DemoBadge app={app} value={row.status} tone={row.status === 'Admitted' ? 'positive' : row.status === 'Waiting' ? 'warning' : 'neutral'} /> },
                  ]}
                  rows={patientRows}
                />
              </DemoPanel>
              <DemoPanel app={app} title="Doctor availability" subtitle="Schedule density and room assignment are emphasized more than decoration.">
                <div className="space-y-3">
                  {state.doctors.map((doctor) => (
                    <div key={doctor.id} className="rounded-[1.15rem] border border-teal-100 bg-white p-4">
                      <div className="flex items-center justify-between gap-3">
                        <div>
                          <p className="text-sm font-semibold text-slate-950">{doctor.name}</p>
                          <p className="mt-1 text-sm text-slate-600">{doctor.specialty}</p>
                        </div>
                        <DemoBadge app={app} value={doctor.room} />
                      </div>
                      <p className="mt-3 text-xs text-slate-500">{doctor.opdLoad}</p>
                    </div>
                  ))}
                </div>
              </DemoPanel>
            </div>
          </>
        ) : null}

        {activeSection === 'patients' ? (
          <div className="mt-4">
            <DemoPanel app={app} title="Patient registration records" subtitle="Patient handling stays compact and operational.">
              <DemoDataTable
                app={app}
                columns={[
                  { key: 'name', header: 'Patient', render: (row) => <div><p className="font-semibold text-slate-950">{row.name}</p><p className="text-xs text-slate-500">{row.id}</p></div> },
                  { key: 'unit', header: 'Unit', render: (row) => row.unit },
                  { key: 'doctor', header: 'Doctor', render: (row) => row.doctor },
                  { key: 'status', header: 'Priority', render: (row) => <DemoBadge app={app} value={row.status} tone={row.status === 'Admitted' ? 'positive' : row.status === 'Waiting' ? 'warning' : 'neutral'} /> },
                  { key: 'bill', header: 'Bill', render: (row) => row.bill },
                ]}
                rows={patientRows}
              />
            </DemoPanel>
          </div>
        ) : null}

        {activeSection === 'appointments' ? (
          <div className="mt-4 grid gap-4 xl:grid-cols-[1.1fr_0.9fr]">
            <DemoPanel app={app} title="Front-desk appointment flow" subtitle="Reception-first scheduling surface with confirmation states.">
              <DemoDataTable
                app={app}
                columns={[
                  { key: 'patient', header: 'Patient', render: (row) => row.patient },
                  { key: 'doctor', header: 'Doctor', render: (row) => row.doctor },
                  { key: 'time', header: 'Time', render: (row) => row.time },
                  { key: 'type', header: 'Visit Type', render: (row) => row.type },
                  { key: 'status', header: 'Status', render: (row) => <DemoBadge app={app} value={row.status} tone={row.status === 'Delayed' ? 'warning' : row.status === 'Checked In' ? 'positive' : 'neutral'} /> },
                ]}
                rows={state.appointments.map((appointment) => ({ ...appointment, id: appointment.id }))}
              />
            </DemoPanel>
            <DemoPanel app={app} title="Register appointment" subtitle="A mock front-desk form that updates instantly.">
              <form className="grid gap-4" onSubmit={handleAppointmentSubmit}>
                <label className="space-y-2">
                  <span className="text-sm font-medium text-slate-700">Patient name</span>
                  <input value={appointmentForm.patient} onChange={(event) => setAppointmentForm((current) => ({ ...current, patient: event.target.value }))} className="w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none focus:border-[var(--demo-primary)]" />
                </label>
                <label className="space-y-2">
                  <span className="text-sm font-medium text-slate-700">Doctor</span>
                  <select value={appointmentForm.doctor} onChange={(event) => setAppointmentForm((current) => ({ ...current, doctor: event.target.value }))} className="w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none focus:border-[var(--demo-primary)]">
                    {state.doctors.map((doctor) => (
                      <option key={doctor.id} value={doctor.name}>
                        {doctor.name}
                      </option>
                    ))}
                  </select>
                </label>
                <div className="grid gap-4 sm:grid-cols-2">
                  <label className="space-y-2">
                    <span className="text-sm font-medium text-slate-700">Time</span>
                    <input value={appointmentForm.time} onChange={(event) => setAppointmentForm((current) => ({ ...current, time: event.target.value }))} className="w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none focus:border-[var(--demo-primary)]" />
                  </label>
                  <label className="space-y-2">
                    <span className="text-sm font-medium text-slate-700">Visit type</span>
                    <input value={appointmentForm.type} onChange={(event) => setAppointmentForm((current) => ({ ...current, type: event.target.value }))} className="w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none focus:border-[var(--demo-primary)]" />
                  </label>
                </div>
                <button type="submit" className="inline-flex min-h-12 items-center justify-center rounded-xl bg-[var(--demo-primary)] px-5 text-sm font-semibold text-white">
                  Add to schedule
                </button>
              </form>
            </DemoPanel>
          </div>
        ) : null}

        {activeSection === 'billing' ? (
          <div className="mt-4 grid gap-4 xl:grid-cols-[1.15fr_0.85fr]">
            <DemoPanel
              app={app}
              title="Billing and claims"
              subtitle="Collections and claim follow-up with a compact healthcare workflow tone."
              action={
                <button type="button" onClick={exportBilling} className="inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-900 hover:border-[var(--demo-primary)] hover:text-[var(--demo-primary)]">
                  <FiClipboard />
                  Export sample report
                </button>
              }
            >
              <div className="space-y-3">
                {state.billings.map((billing) => (
                  <div key={billing.id} className="rounded-[1.15rem] border border-teal-100 bg-white p-4">
                    <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                      <div>
                        <p className="text-sm font-semibold text-slate-950">{billing.department}</p>
                        <p className="mt-1 text-sm text-slate-600">{billing.paymentMode} · {billing.amount}</p>
                      </div>
                      <div className="flex items-center gap-3">
                        <DemoBadge app={app} value={billing.status} tone={billing.status === 'Settled' ? 'positive' : 'warning'} />
                        {billing.status === 'Pending' ? (
                          <button type="button" onClick={() => settleBilling(billing.id)} className="rounded-xl bg-[var(--demo-primary)] px-4 py-2 text-sm font-semibold text-white">
                            Mark settled
                          </button>
                        ) : null}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </DemoPanel>
            <DemoPanel app={app} title="Revenue notes" subtitle="Fast scanning panels built for admin workflow, not decorative dashboards.">
              <div className="space-y-3">
                {[
                  'Cashless claims stay separate from front-desk walk-in billing.',
                  'Sample exports are generated in-browser and never sent to a backend.',
                  'Urgent queues use chips and compact cards instead of big generic tiles.',
                ].map((item) => (
                  <div key={item} className="rounded-[1.15rem] border border-teal-100 bg-teal-50/50 p-4 text-sm leading-6 text-slate-600">
                    {item}
                  </div>
                ))}
              </div>
            </DemoPanel>
          </div>
        ) : null}
      </DemoShell>

      <DemoToastStack toasts={toasts} />
    </>
  )
}
