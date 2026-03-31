import { useEffect, useState } from 'react'
import { motion as Motion } from 'framer-motion'
import { FiActivity, FiAlertCircle, FiCheckCircle, FiCreditCard, FiPlus, FiUsers } from 'react-icons/fi'
import hmsDemoData from '../../data/hmsDemo.json'
import Button from '../../components/ui/Button'
import Container from '../../components/ui/Container'
import Skeleton from '../../components/ui/Skeleton'
import useLocalStorageState from '../../hooks/useLocalStorageState'
import {
  auditBill,
  calculateBillTotals,
  formatCurrencyFromPaise,
  type PatientBill,
} from '../../utils/billing'

type DemoPatient = {
  id: string
  name: string
  age: number
  department: string
  doctor: string
  status: string
}

type DraftPatient = {
  name: string
  age: string
  department: string
  doctor: string
}

const draftDefaults: DraftPatient = {
  name: '',
  age: '',
  department: 'General Medicine',
  doctor: 'Dr. Mehta',
}

const initialPatients = hmsDemoData.patients as DemoPatient[]
const initialBills = hmsDemoData.bills as PatientBill[]

const statusToneMap: Record<string, string> = {
  Admitted: 'bg-[#e7fbf8] text-[#04555e]',
  'Under Review': 'bg-[#eef2ff] text-[#3340a6]',
  'Discharge Ready': 'bg-[#f3faf2] text-[#2d7a38]',
}

function DemoSkeleton() {
  return (
    <div className="mt-12 grid gap-6 xl:grid-cols-[0.72fr_1.28fr]">
      <Skeleton className="h-[28rem] rounded-[2rem]" />
      <div className="space-y-6">
        <div className="grid gap-4 md:grid-cols-3">
          <Skeleton className="h-32 rounded-[1.75rem]" />
          <Skeleton className="h-32 rounded-[1.75rem]" />
          <Skeleton className="h-32 rounded-[1.75rem]" />
        </div>
        <Skeleton className="h-[26rem] rounded-[2rem]" />
      </div>
    </div>
  )
}

function getFallbackBill(patientId: string, count: number): PatientBill {
  return {
    patientId,
    invoiceNumber: `HMSQ-20260330-${String(count).padStart(4, '0')}`,
    lineItems: [
      {
        id: `LI-${patientId}-001`,
        label: 'Initial Consultation',
        unitPricePaise: 80000,
        quantity: 1,
      },
    ],
    adjustments: [],
    payments: [],
  }
}

export default function HmsDemoPage() {
  const [patients, setPatients] = useLocalStorageState<DemoPatient[]>('qode27-hms-demo-patients-v2', initialPatients)
  const [bills, setBills] = useLocalStorageState<PatientBill[]>('qode27-hms-demo-bills-v2', initialBills)
  const [selectedPatientId, setSelectedPatientId] = useLocalStorageState<string>('qode27-hms-selected-patient-v2', initialPatients[0].id)
  const [draft, setDraft] = useState<DraftPatient>(draftDefaults)
  const [isBooting, setIsBooting] = useState(true)

  useEffect(() => {
    const timer = window.setTimeout(() => setIsBooting(false), 650)
    return () => window.clearTimeout(timer)
  }, [])

  useEffect(() => {
    if (!patients.some((patient) => patient.id === selectedPatientId) && patients[0]) {
      setSelectedPatientId(patients[0].id)
    }
  }, [patients, selectedPatientId, setSelectedPatientId])

  const selectedPatient = patients.find((patient) => patient.id === selectedPatientId) ?? patients[0]
  const selectedBill = bills.find((bill) => bill.patientId === selectedPatient?.id)
  const selectedBillAudit = selectedBill ? auditBill(selectedBill) : null
  const selectedTotals = selectedBill ? calculateBillTotals(selectedBill) : null
  const openBillingPaise = bills.reduce((sum, bill) => sum + calculateBillTotals(bill).duePaise, 0)
  const settledBillsCount = bills.filter((bill) => calculateBillTotals(bill).duePaise === 0).length

  const stats = [
    { label: 'Active Patients', value: String(patients.length), trend: '+3 today', icon: FiUsers },
    { label: 'Open Billing', value: formatCurrencyFromPaise(openBillingPaise), trend: `${settledBillsCount}/${bills.length} settled`, icon: FiCreditCard },
    {
      label: 'Billing Audit',
      value: bills.every((bill) => auditBill(bill).isValid) ? 'Passed' : 'Review',
      trend: 'Auto-checking every bill',
      icon: FiActivity,
    },
  ]

  const handleDraftChange = (field: keyof DraftPatient, value: string) => {
    setDraft((current) => ({ ...current, [field]: value }))
  }

  const handleAddPatient = () => {
    if (!draft.name.trim() || !draft.age.trim()) {
      return
    }

    const nextPatientId = `P-${1000 + patients.length + 1}`
    const nextPatient: DemoPatient = {
      id: nextPatientId,
      name: draft.name.trim(),
      age: Number(draft.age) || 0,
      department: draft.department,
      doctor: draft.doctor,
      status: 'Under Review',
    }

    setPatients((current) => [nextPatient, ...current])
    setBills((current) => [getFallbackBill(nextPatientId, current.length + 2), ...current])
    setSelectedPatientId(nextPatient.id)
    setDraft(draftDefaults)
  }

  return (
    <Motion.div initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -18 }} transition={{ duration: 0.35 }}>
      <section className="section-spacing pt-12">
        <Container>
          <div className="max-w-3xl">
            <p className="inline-flex items-center gap-2 rounded-full border border-black/8 bg-white/82 px-4 py-2 text-xs font-semibold uppercase tracking-[0.26em] text-[var(--color-accent-strong)]">
              <span className="h-2 w-2 rounded-full bg-[var(--color-accent)]" />
              Interactive demo
            </p>
            <h1 className="mt-7 font-display text-5xl font-bold leading-[0.97] tracking-[-0.06em] text-black sm:text-6xl">
              HMS by Qode27 demo for patient ops, billing visibility, and admin flow.
            </h1>
            <p className="mt-6 text-lg leading-8 text-neutral-600">
              Billing is now derived from patient-specific line items, adjustments, and payments so the numbers shown in the UI cannot drift from the actual bill structure.
            </p>
          </div>

          {isBooting ? (
            <DemoSkeleton />
          ) : (
            <div className="mt-12 grid gap-6 xl:grid-cols-[0.72fr_1.28fr]">
              <div className="rounded-[2rem] border border-black/6 bg-white p-6 shadow-[0_20px_40px_rgba(15,23,42,0.06)]">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[var(--color-accent-strong)]">Add Patient</p>
                    <h2 className="mt-2 text-2xl font-semibold text-black">Front-desk intake</h2>
                  </div>
                  <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-[var(--color-accent-soft)] text-[var(--color-accent-strong)]">
                    <FiPlus />
                  </div>
                </div>

                <div className="mt-6 grid gap-4">
                  <label className="space-y-2">
                    <span className="text-sm font-medium text-neutral-700">Patient Name</span>
                    <input
                      value={draft.name}
                      onChange={(event) => handleDraftChange('name', event.target.value)}
                      className="w-full rounded-xl border border-black/10 bg-[#f8fbfb] px-4 py-3 text-sm text-black outline-none placeholder:text-neutral-400 focus:border-[var(--color-accent)]"
                      placeholder="Enter patient name"
                    />
                  </label>
                  <label className="space-y-2">
                    <span className="text-sm font-medium text-neutral-700">Age</span>
                    <input
                      value={draft.age}
                      onChange={(event) => handleDraftChange('age', event.target.value)}
                      className="w-full rounded-xl border border-black/10 bg-[#f8fbfb] px-4 py-3 text-sm text-black outline-none placeholder:text-neutral-400 focus:border-[var(--color-accent)]"
                      placeholder="Age"
                    />
                  </label>
                  <label className="space-y-2">
                    <span className="text-sm font-medium text-neutral-700">Department</span>
                    <select
                      value={draft.department}
                      onChange={(event) => handleDraftChange('department', event.target.value)}
                      className="w-full rounded-xl border border-black/10 bg-[#f8fbfb] px-4 py-3 text-sm text-black outline-none focus:border-[var(--color-accent)]"
                    >
                      <option>General Medicine</option>
                      <option>Cardiology</option>
                      <option>Orthopedics</option>
                      <option>Dermatology</option>
                    </select>
                  </label>
                  <label className="space-y-2">
                    <span className="text-sm font-medium text-neutral-700">Consulting Doctor</span>
                    <select
                      value={draft.doctor}
                      onChange={(event) => handleDraftChange('doctor', event.target.value)}
                      className="w-full rounded-xl border border-black/10 bg-[#f8fbfb] px-4 py-3 text-sm text-black outline-none focus:border-[var(--color-accent)]"
                    >
                      <option>Dr. Mehta</option>
                      <option>Dr. Kapoor</option>
                      <option>Dr. Iyer</option>
                    </select>
                  </label>
                </div>

                <Button className="mt-6 w-full justify-center" onClick={handleAddPatient}>
                  Add Patient
                </Button>
                <p className="mt-3 text-sm leading-6 text-neutral-500">
                  Every new patient gets a bill shell with a single starter line item, so the demo never shows an untracked total.
                </p>
              </div>

              <div className="space-y-6">
                <div className="grid gap-4 md:grid-cols-3">
                  {stats.map((stat) => {
                    const Icon = stat.icon

                    return (
                      <div key={stat.label} className="rounded-[1.75rem] border border-black/6 bg-white p-6 shadow-[0_18px_36px_rgba(15,23,42,0.05)]">
                        <div className="flex items-center justify-between">
                          <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-[var(--color-accent-soft)] text-[var(--color-accent-strong)]">
                            <Icon />
                          </div>
                          <span className="rounded-full bg-[#ecfbfb] px-3 py-1 text-xs font-semibold text-[var(--color-accent-strong)]">
                            {stat.trend}
                          </span>
                        </div>
                        <p className="mt-5 text-xs uppercase tracking-[0.24em] text-neutral-500">{stat.label}</p>
                        <p className="mt-2 text-4xl font-semibold tracking-[-0.06em] text-black">{stat.value}</p>
                      </div>
                    )
                  })}
                </div>

                <div className="grid gap-6 lg:grid-cols-[1.06fr_0.94fr]">
                  <div className="rounded-[2rem] border border-black/6 bg-white p-6 shadow-[0_18px_36px_rgba(15,23,42,0.05)]">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[var(--color-accent-strong)]">Patient List</p>
                        <h2 className="mt-2 text-2xl font-semibold text-black">Live registry</h2>
                      </div>
                      <span className="rounded-full bg-[#f3f7f7] px-3 py-1 text-xs font-semibold text-neutral-600">{patients.length} records</span>
                    </div>

                    <div className="mt-6 overflow-hidden rounded-[1.5rem] border border-black/6">
                      <div className="hidden grid-cols-[1.05fr_0.55fr_0.9fr_0.7fr] bg-[#f5f8f9] px-5 py-3 text-xs font-semibold uppercase tracking-[0.18em] text-neutral-500 md:grid">
                        <span>Patient</span>
                        <span>Dept</span>
                        <span>Doctor</span>
                        <span>Status</span>
                      </div>
                      <div className="divide-y divide-black/6">
                        {patients.map((patient) => (
                          <button
                            key={patient.id}
                            type="button"
                            onClick={() => setSelectedPatientId(patient.id)}
                            className={`grid w-full gap-3 px-5 py-4 text-left transition md:grid-cols-[1.05fr_0.55fr_0.9fr_0.7fr] ${
                              patient.id === selectedPatientId ? 'bg-[#f2fcfb]' : 'bg-white hover:bg-[#f8fbfb]'
                            }`}
                          >
                            <div>
                              <p className="font-semibold text-black">{patient.name}</p>
                              <p className="mt-1 text-sm text-neutral-500">
                                {patient.id} · {patient.age} yrs
                              </p>
                            </div>
                            <p className="text-sm text-neutral-600">{patient.department}</p>
                            <p className="text-sm text-neutral-600">{patient.doctor}</p>
                            <div>
                              <span className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${statusToneMap[patient.status] ?? 'bg-neutral-100 text-neutral-700'}`}>
                                {patient.status}
                              </span>
                            </div>
                          </button>
                        ))}
                      </div>
                    </div>
                  </div>

                  <div className="rounded-[2rem] border border-black/6 bg-black p-6 text-white shadow-[0_24px_50px_rgba(15,23,42,0.22)]">
                    <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[var(--color-accent)]">Billing Preview</p>
                    <h2 className="mt-2 text-2xl font-semibold">Selected patient bill</h2>

                    <div className="mt-6 rounded-[1.5rem] border border-white/10 bg-white/5 p-5">
                      <div className="flex flex-wrap items-center justify-between gap-3">
                        <div>
                          <p className="text-lg font-semibold">{selectedPatient?.name ?? 'No patient selected'}</p>
                          <p className="mt-1 text-sm text-white/62">
                            {selectedPatient?.department ?? 'N/A'} · {selectedPatient?.doctor ?? 'N/A'}
                          </p>
                        </div>
                        <div className="text-right">
                          <p className="text-xs uppercase tracking-[0.18em] text-white/48">Invoice</p>
                          <p className="mt-1 font-semibold">{selectedBill?.invoiceNumber ?? 'Pending'}</p>
                        </div>
                      </div>
                    </div>

                    {selectedBill && selectedTotals && selectedBillAudit ? (
                      <>
                        <div className={`mt-4 flex items-start gap-3 rounded-[1.25rem] border px-4 py-3 text-sm ${
                          selectedBillAudit.isValid
                            ? 'border-[#1fb89b]/30 bg-[#1fb89b]/12 text-white'
                            : 'border-[#ff8f87]/35 bg-[#ff8f87]/12 text-white'
                        }`}>
                          <div className="mt-0.5">
                            {selectedBillAudit.isValid ? <FiCheckCircle /> : <FiAlertCircle />}
                          </div>
                          <div>
                            <p className="font-semibold">
                              {selectedBillAudit.isValid ? 'Bill audit passed' : 'Bill audit needs review'}
                            </p>
                            <p className="mt-1 text-white/72">
                              {selectedBillAudit.isValid
                                ? 'Every total is being derived from line items, adjustments, and payments.'
                                : selectedBillAudit.issues[0]}
                            </p>
                          </div>
                        </div>

                        <div className="mt-6 overflow-hidden rounded-[1.5rem] border border-white/10">
                          <div className="grid grid-cols-[1fr_auto_auto] bg-white/6 px-4 py-3 text-xs font-semibold uppercase tracking-[0.18em] text-white/45">
                            <span>Service</span>
                            <span>Qty</span>
                            <span>Amount</span>
                          </div>
                          <div className="divide-y divide-white/10">
                            {selectedBill.lineItems.map((item) => (
                              <div key={item.id} className="grid grid-cols-[1fr_auto_auto] gap-3 px-4 py-3 text-sm">
                                <span className="text-white/78">{item.label}</span>
                                <span className="text-white/52">{item.quantity}</span>
                                <span className="font-semibold text-white">
                                  {formatCurrencyFromPaise(item.unitPricePaise * item.quantity)}
                                </span>
                              </div>
                            ))}
                            {selectedBill.adjustments.map((item) => (
                              <div key={item.id} className="grid grid-cols-[1fr_auto_auto] gap-3 px-4 py-3 text-sm">
                                <span className="text-white/78">{item.label}</span>
                                <span className="text-white/52">{item.type === 'discount' ? '-' : '+'}</span>
                                <span className="font-semibold text-white">
                                  {item.type === 'discount' ? '-' : ''}
                                  {formatCurrencyFromPaise(item.amountPaise)}
                                </span>
                              </div>
                            ))}
                          </div>
                        </div>

                        <div className="mt-6 space-y-3">
                          <div className="flex items-center justify-between rounded-2xl bg-white/5 px-4 py-3 text-sm">
                            <span className="text-white/70">Subtotal</span>
                            <span className="font-semibold text-white">{formatCurrencyFromPaise(selectedTotals.subtotalPaise)}</span>
                          </div>
                          {selectedTotals.chargeAdjustmentsPaise > 0 ? (
                            <div className="flex items-center justify-between rounded-2xl bg-white/5 px-4 py-3 text-sm">
                              <span className="text-white/70">Additional charges</span>
                              <span className="font-semibold text-white">{formatCurrencyFromPaise(selectedTotals.chargeAdjustmentsPaise)}</span>
                            </div>
                          ) : null}
                          {selectedTotals.discountPaise > 0 ? (
                            <div className="flex items-center justify-between rounded-2xl bg-white/5 px-4 py-3 text-sm">
                              <span className="text-white/70">Discounts</span>
                              <span className="font-semibold text-white">-{formatCurrencyFromPaise(selectedTotals.discountPaise)}</span>
                            </div>
                          ) : null}
                          <div className="flex items-center justify-between rounded-2xl bg-white/5 px-4 py-3 text-sm">
                            <span className="text-white/70">Paid</span>
                            <span className="font-semibold text-white">{formatCurrencyFromPaise(selectedTotals.paidPaise)}</span>
                          </div>
                          <div className="flex items-center justify-between rounded-2xl border border-[var(--color-accent)]/30 bg-[var(--color-accent)]/12 px-4 py-3 text-sm">
                            <span className="text-white/72">Due</span>
                            <span className="font-semibold text-white">{formatCurrencyFromPaise(selectedTotals.duePaise)}</span>
                          </div>
                          {selectedTotals.creditPaise > 0 ? (
                            <div className="flex items-center justify-between rounded-2xl border border-[#1fb89b]/30 bg-[#1fb89b]/12 px-4 py-3 text-sm">
                              <span className="text-white/72">Credit balance</span>
                              <span className="font-semibold text-white">{formatCurrencyFromPaise(selectedTotals.creditPaise)}</span>
                            </div>
                          ) : null}
                        </div>

                        <div className="mt-6 rounded-[1.5rem] bg-white px-5 py-4 text-black">
                          <div className="flex items-center justify-between">
                            <span className="text-sm font-medium text-neutral-500">Bill total</span>
                            <span className="text-2xl font-semibold tracking-[-0.04em]">{formatCurrencyFromPaise(selectedTotals.totalPaise)}</span>
                          </div>
                        </div>
                      </>
                    ) : (
                      <div className="mt-6 rounded-[1.5rem] border border-white/10 bg-white/5 p-5 text-sm text-white/70">
                        No billing record is available for the selected patient.
                      </div>
                    )}

                    <div className="mt-6 flex flex-wrap gap-3">
                      <Button href="/pricing" variant="secondary">
                        Get Pricing
                      </Button>
                      <Button href="/contact" variant="ghost">
                        Talk to Sales
                      </Button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </Container>
      </section>
    </Motion.div>
  )
}
