import { useState, type FormEvent } from 'react'
import { FiBarChart2, FiCreditCard, FiGrid, FiMap, FiTruck, FiWatch } from 'react-icons/fi'
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
import { createTruckParkingState, truckParkingUsers } from '../../../data/demo/truckParking'
import { buildToast, createCsvFromRows, downloadSampleFile } from '../../../lib/demo/mock'
import { useDemoAppState } from '../../../lib/demo/useDemoAppState'
import { useDemoNetworkGuard } from '../../../lib/demo/useDemoNetworkGuard'
import type { DemoAppRouteProps, DemoMetric, DemoNavItem } from '../../../lib/demo/types'
import Seo from '../../../components/ui/Seo'

const sections: DemoNavItem[] = [
  { slug: 'dashboard', label: 'Live Board', icon: FiBarChart2, description: 'Real-time occupancy, yard activity, and earnings.' },
  { slug: 'bays', label: 'Bay Map', icon: FiGrid, description: 'Slot allocation and availability by yard zone.' },
  { slug: 'movement', label: 'Movement', icon: FiTruck, description: 'Truck entries, exits, and queue state.' },
  { slug: 'revenue', label: 'Revenue', icon: FiCreditCard, description: 'Daily earnings, pending payments, and receipts.' },
]

export default function TruckParkingDemoPage({ app, section }: DemoAppRouteProps) {
  useDemoNetworkGuard()

  const { state, patchState, currentUser, users, switchUser, resetDemo, refreshDemo, isRefreshing, toasts, addToast } = useDemoAppState({
    storageKey: 'qode27-demo-truck-parking',
    createInitialState: createTruckParkingState,
    users: truckParkingUsers,
  })

  const activeSection = sections.some((item) => item.slug === section) ? section ?? 'dashboard' : 'dashboard'
  const [movementForm, setMovementForm] = useState({ truckNumber: '', transporter: '', bay: 'B-12' })

  const metrics: DemoMetric[] = [
    { label: 'Occupied Bays', value: `${state.bays.filter((bay) => bay.status === 'Occupied').length}/67`, change: '2 lanes near capacity', tone: 'warning' },
    { label: 'Queued Trucks', value: `${state.movements.filter((movement) => movement.status === 'Queued').length}`, change: 'Gate load is manageable', tone: 'neutral' },
    { label: 'Daily Revenue', value: 'Rs 1.46L', change: '11% above average day', tone: 'positive' },
    { label: 'Avg Stay', value: '6h 12m', change: 'Turnaround trending better', tone: 'positive' },
  ]

  const handleUserSwitch = (email: string) => {
    switchUser(email)
    addToast(buildToast('Operator switched', 'Live board updated for the selected mock yard role.', 'info'))
  }

  const handleReset = () => {
    resetDemo()
    addToast(buildToast('Yard reset', 'Truck parking sample data was restored.', 'success'))
  }

  const handleRefresh = () => {
    refreshDemo()
    addToast(buildToast('Board refreshed', 'Live yard signals refreshed locally only.', 'info'))
  }

  const handleMovementSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!movementForm.truckNumber.trim() || !movementForm.transporter.trim()) {
      addToast(buildToast('Incomplete entry', 'Add truck number and transporter to continue.', 'warning'))
      return
    }

    patchState((current) => ({
      ...current,
      movements: [
        { id: `MOV-${Date.now()}`, truckNumber: movementForm.truckNumber, transporter: movementForm.transporter, bay: movementForm.bay, duration: '00h 05m', status: 'Queued' },
        ...current.movements,
      ],
      bays: current.bays.map((bay) => (bay.id === movementForm.bay ? { ...bay, status: 'Reserved', eta: 'Arriving now' } : bay)),
    }))
    setMovementForm({ truckNumber: '', transporter: '', bay: 'B-12' })
    addToast(buildToast('Truck queued', 'Vehicle movement was added to the local yard board.', 'success'))
  }

  const markInvoicePaid = (invoiceId: string) => {
    patchState((current) => ({
      ...current,
      invoices: current.invoices.map((invoice) => (invoice.id === invoiceId ? { ...invoice, status: 'Paid' } : invoice)),
    }))
    addToast(buildToast('Receipt updated', 'Revenue status changed in the local sandbox.', 'success'))
  }

  const exportMovements = () => {
    downloadSampleFile(
      'qode27-yard-movements.csv',
      createCsvFromRows(
        state.movements.map((movement) => ({
          id: movement.id,
          truckNumber: movement.truckNumber,
          transporter: movement.transporter,
          bay: movement.bay,
          duration: movement.duration,
          status: movement.status,
        })),
      ),
      'text/csv;charset=utf-8',
    )
    addToast(buildToast('Movement sheet ready', 'Export generated from demo-only yard data.', 'success'))
  }

  return (
    <>
      <Seo title="Truck Parking Interactive Demo | Qode27" description="Interactive frontend-only truck parking demo with live occupancy, movement, bay allocation, and revenue." canonicalPath={activeSection === 'dashboard' ? '/demo/truck-parking' : `/demo/truck-parking/${activeSection}`} />

      <DemoShell
        app={app}
        sections={sections}
        activeSection={activeSection}
        title="A rugged command-center product for occupancy, movement, and revenue control."
        subtitle="This product intentionally feels nothing like HRMS or HMS. It behaves like a live yard board: darker, bolder, more status-driven, and more focused on movement than on traditional office dashboards."
        currentUser={currentUser}
        onSwitchUser={handleUserSwitch}
        users={users}
        onReset={handleReset}
        onRefresh={handleRefresh}
        isRefreshing={isRefreshing}
        actions={[
          { label: 'Request parking rollout demo', href: buildDemoRequestPath('Truck Parking Demo') },
          { label: 'WhatsApp Qode27', href: buildDemoWhatsAppHref('Truck Parking Demo'), variant: 'secondary' },
        ]}
      >
        <DemoMetricGrid app={app} items={metrics} isRefreshing={isRefreshing} columnsClass="md:grid-cols-2 xl:grid-cols-4" />

        {activeSection === 'dashboard' ? (
          <>
            <div className="mt-4 grid gap-4 xl:grid-cols-[1.1fr_0.9fr]">
              <DemoPanel
                app={app}
                title="Occupancy signal"
                subtitle="The first screen behaves like a live command board, not a corporate dashboard."
                action={
                  <button type="button" onClick={exportMovements} className="inline-flex items-center gap-2 rounded-xl border border-white/10 bg-white/5 px-4 py-2 text-sm font-semibold text-white">
                    <FiMap />
                    Export movement log
                  </button>
                }
              >
                <DemoTrendChart app={app} title="Occupied bays by hour" data={state.occupancyTrend} />
              </DemoPanel>
              <DemoPanel app={app} title="Yard status stack" subtitle="Live activity is front and center with high-contrast signals.">
                <div className="space-y-3">
                  {[
                    ['North yard', 'Full trailers approaching threshold', 'warning'],
                    ['Central lane', 'Fastest turnover zone today', 'positive'],
                    ['South yard', 'Spare capacity available now', 'neutral'],
                  ].map(([title, note, tone]) => (
                    <div key={title} className="rounded-[1rem] border border-white/10 bg-white/5 p-4">
                      <div className="flex items-center justify-between gap-3">
                        <p className="text-sm font-semibold text-white">{title}</p>
                        <DemoBadge app={app} value={tone === 'positive' ? 'Live' : tone === 'warning' ? 'Busy' : 'Stable'} tone={tone as 'neutral' | 'positive' | 'warning'} />
                      </div>
                      <p className="mt-2 text-sm leading-6 text-white/68">{note}</p>
                    </div>
                  ))}
                </div>
              </DemoPanel>
            </div>

            <div className="mt-4 grid gap-4 xl:grid-cols-[1.05fr_0.95fr]">
              <DemoPanel app={app} title="Current vehicle movement" subtitle="Bigger status visibility and less office-style softness.">
                <DemoDataTable
                  app={app}
                  columns={[
                    { key: 'truck', header: 'Truck', render: (row) => <div><p className="font-semibold text-white">{row.truckNumber}</p><p className="text-xs text-white/55">{row.transporter}</p></div> },
                    { key: 'bay', header: 'Bay', render: (row) => row.bay },
                    { key: 'duration', header: 'Duration', render: (row) => row.duration },
                    { key: 'status', header: 'Status', render: (row) => <DemoBadge app={app} value={row.status} tone={row.status === 'Parked' ? 'positive' : row.status === 'Queued' ? 'warning' : 'neutral'} /> },
                  ]}
                  rows={state.movements.map((movement) => ({ ...movement, id: movement.id }))}
                />
              </DemoPanel>
              <DemoPanel app={app} title="Revenue monitor" subtitle="Collections are shown like a live operations finance board.">
                <div className="space-y-3">
                  {state.invoices.map((invoice) => (
                    <div key={invoice.id} className="rounded-[1rem] border border-white/10 bg-white/5 p-4">
                      <div className="flex items-center justify-between gap-3">
                        <div>
                          <p className="text-sm font-semibold text-white">{invoice.transporter}</p>
                          <p className="mt-1 text-sm text-white/68">{invoice.amount} · {invoice.mode}</p>
                        </div>
                        <DemoBadge app={app} value={invoice.status} tone={invoice.status === 'Paid' ? 'positive' : 'warning'} />
                      </div>
                    </div>
                  ))}
                </div>
              </DemoPanel>
            </div>
          </>
        ) : null}

        {activeSection === 'bays' ? (
          <div className="mt-4">
            <DemoPanel app={app} title="Yard bay map" subtitle="A stronger command-center grid replaces soft admin cards.">
              <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
                {state.bays.map((bay) => (
                  <div key={bay.id} className="rounded-[1rem] border border-white/10 bg-white/5 p-4">
                    <div className="flex items-center justify-between gap-3">
                      <p className="text-lg font-semibold tracking-[-0.03em] text-white">{bay.id}</p>
                      <DemoBadge app={app} value={bay.status} tone={bay.status === 'Available' ? 'positive' : bay.status === 'Reserved' ? 'warning' : 'neutral'} />
                    </div>
                    <p className="mt-4 text-sm text-white/68">{bay.zone}</p>
                    <p className="mt-1 text-sm text-white/54">{bay.truckType}</p>
                    <p className="mt-4 text-xs font-medium uppercase tracking-[0.18em] text-amber-300">{bay.eta}</p>
                  </div>
                ))}
              </div>
            </DemoPanel>
          </div>
        ) : null}

        {activeSection === 'movement' ? (
          <div className="mt-4 grid gap-4 xl:grid-cols-[1.1fr_0.9fr]">
            <DemoPanel app={app} title="Movement register" subtitle="Entries and exits shown like a live yard board.">
              <DemoDataTable
                app={app}
                columns={[
                  { key: 'truckNumber', header: 'Truck', render: (row) => row.truckNumber },
                  { key: 'transporter', header: 'Transporter', render: (row) => row.transporter },
                  { key: 'bay', header: 'Bay', render: (row) => row.bay },
                  { key: 'duration', header: 'Duration', render: (row) => row.duration },
                  { key: 'status', header: 'Status', render: (row) => <DemoBadge app={app} value={row.status} tone={row.status === 'Parked' ? 'positive' : row.status === 'Queued' ? 'warning' : 'neutral'} /> },
                ]}
                rows={state.movements.map((movement) => ({ ...movement, id: movement.id }))}
              />
            </DemoPanel>
            <DemoPanel app={app} title="Queue truck" subtitle="High-contrast movement form for live operator walkthroughs.">
              <form className="grid gap-4" onSubmit={handleMovementSubmit}>
                <label className="space-y-2">
                  <span className="text-sm font-medium text-white/72">Truck number</span>
                  <input value={movementForm.truckNumber} onChange={(event) => setMovementForm((current) => ({ ...current, truckNumber: event.target.value }))} className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-white outline-none focus:border-amber-300" />
                </label>
                <label className="space-y-2">
                  <span className="text-sm font-medium text-white/72">Transporter</span>
                  <input value={movementForm.transporter} onChange={(event) => setMovementForm((current) => ({ ...current, transporter: event.target.value }))} className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-white outline-none focus:border-amber-300" />
                </label>
                <label className="space-y-2">
                  <span className="text-sm font-medium text-white/72">Preferred bay</span>
                  <select value={movementForm.bay} onChange={(event) => setMovementForm((current) => ({ ...current, bay: event.target.value }))} className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-white outline-none focus:border-amber-300">
                    {state.bays.map((bay) => (
                      <option key={bay.id} value={bay.id} className="text-slate-900">
                        {bay.id} · {bay.zone}
                      </option>
                    ))}
                  </select>
                </label>
                <button type="submit" className="inline-flex min-h-12 items-center justify-center rounded-xl bg-amber-400 px-5 text-sm font-semibold text-black">
                  Add to queue
                </button>
              </form>
            </DemoPanel>
          </div>
        ) : null}

        {activeSection === 'revenue' ? (
          <div className="mt-4 grid gap-4 xl:grid-cols-[1.05fr_0.95fr]">
            <DemoPanel app={app} title="Receipts and pending payments" subtitle="Bolder status blocks emphasize cash movement and pending settlement.">
              <div className="space-y-3">
                {state.invoices.map((invoice) => (
                  <div key={invoice.id} className="rounded-[1rem] border border-white/10 bg-white/5 p-4">
                    <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                      <div>
                        <p className="text-sm font-semibold text-white">{invoice.transporter}</p>
                        <p className="mt-1 text-sm text-white/68">{invoice.id} · {invoice.amount}</p>
                      </div>
                      <div className="flex items-center gap-3">
                        <DemoBadge app={app} value={invoice.status} tone={invoice.status === 'Paid' ? 'positive' : 'warning'} />
                        {invoice.status === 'Pending' ? (
                          <button type="button" onClick={() => markInvoicePaid(invoice.id)} className="rounded-xl bg-amber-400 px-4 py-2 text-sm font-semibold text-black">
                            Mark paid
                          </button>
                        ) : null}
                      </div>
                    </div>
                    <p className="mt-3 text-xs text-white/50">Mode: {invoice.mode}</p>
                  </div>
                ))}
              </div>
            </DemoPanel>
            <DemoPanel app={app} title="Operator notes" subtitle="Movement and revenue stay tightly linked in this product identity.">
              <div className="space-y-3">
                {[
                  'Every receipt here is mock-only and safe to click during a live pitch.',
                  'The bay map, movement queue, and revenue desk all share the same frontend-only state.',
                  'This darker command-center style is intentionally distinct from the calmer HRMS and HMS products.',
                ].map((item) => (
                  <div key={item} className="rounded-[1rem] border border-white/10 bg-white/5 p-4 text-sm leading-6 text-white/68">
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
