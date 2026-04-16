import { useDeferredValue, useMemo, useState, type FormEvent } from 'react'
import { FiBarChart2, FiClock, FiDollarSign, FiDownload, FiLayers, FiSearch, FiUserPlus, FiUsers } from 'react-icons/fi'
import {
  DemoBadge,
  DemoDataTable,
  DemoEmptyState,
  DemoMetricGrid,
  DemoPanel,
  DemoShell,
  DemoToastStack,
  DemoTrendChart,
} from '../../../components/demo/DemoPrimitives'
import { buildDemoRequestPath, buildDemoWhatsAppHref } from '../../../config/demo-apps'
import { createHrmsState, hrmsUsers, type HrmsCandidate } from '../../../data/demo/hrms'
import { buildToast, createCsvFromRows, downloadSampleFile } from '../../../lib/demo/mock'
import { useDemoAppState } from '../../../lib/demo/useDemoAppState'
import { useDemoNetworkGuard } from '../../../lib/demo/useDemoNetworkGuard'
import type { DemoAppRouteProps, DemoMetric, DemoNavItem } from '../../../lib/demo/types'
import Seo from '../../../components/ui/Seo'

const sections: DemoNavItem[] = [
  { slug: 'dashboard', label: 'Dashboard', icon: FiBarChart2, description: 'Leadership summary across people ops and approvals.' },
  { slug: 'employees', label: 'Employees', icon: FiUsers, description: 'Directory, employee records, and organization-facing details.' },
  { slug: 'payroll', label: 'Payroll', icon: FiDollarSign, description: 'Monthly runs, payout readiness, and finance alignment.' },
  { slug: 'recruitment', label: 'Recruitment', icon: FiUserPlus, description: 'Hiring pipeline and internal talent coordination.' },
]

const orgCards = [
  { title: 'Leadership visibility', copy: 'Headcount, attendance, payroll readiness, and approval health in one layer.' },
  { title: 'People operations', copy: 'Leave, attendance, and employee experience summaries organized for fast HR review.' },
  { title: 'Recruitment pulse', copy: 'Candidate stages, owner visibility, and hiring velocity aligned to business growth.' },
]

export default function HrmsDemoPage({ app, section }: DemoAppRouteProps) {
  useDemoNetworkGuard()

  const { state, patchState, currentUser, users, switchUser, resetDemo, refreshDemo, isRefreshing, toasts, addToast } = useDemoAppState({
    storageKey: 'qode27-demo-hrms',
    createInitialState: createHrmsState,
    users: hrmsUsers,
  })

  const activeSection = sections.some((item) => item.slug === section) ? section ?? 'dashboard' : 'dashboard'
  const [searchQuery, setSearchQuery] = useState('')
  const deferredSearch = useDeferredValue(searchQuery)
  const [candidateForm, setCandidateForm] = useState({ name: '', role: '', owner: currentUser.name })

  const filteredEmployees = useMemo(() => {
    const term = deferredSearch.trim().toLowerCase()
    if (!term) return state.employees
    return state.employees.filter((employee) => [employee.name, employee.department, employee.location, employee.role].some((value) => value.toLowerCase().includes(term)))
  }, [deferredSearch, state.employees])

  const metrics: DemoMetric[] = [
    { label: 'Total Employees', value: '248', change: '12 new joins this quarter', tone: 'positive' },
    { label: 'Attendance Consistency', value: '96.4%', change: 'Strong weekly compliance', tone: 'positive' },
    { label: 'Pending Approvals', value: String(state.leaveRequests.filter((item) => item.status === 'Pending').length), change: 'Needs manager action', tone: 'warning' },
    { label: 'Open Hiring Tracks', value: `${state.candidates.length}`, change: 'Hiring pipeline remains active', tone: 'neutral' },
  ]

  const handleUserSwitch = (email: string) => {
    switchUser(email)
    setCandidateForm((current) => ({ ...current, owner: users.find((user) => user.email === email)?.name ?? current.owner }))
    addToast(buildToast('Persona switched', 'HRMS demo permissions updated for the selected mock user.', 'info'))
  }

  const handleReset = () => {
    resetDemo()
    addToast(buildToast('Demo reset', 'HRMS sample data has been restored.', 'success'))
  }

  const handleRefresh = () => {
    refreshDemo()
    addToast(buildToast('Workspace refreshed', 'The people operations dashboard was refreshed locally.', 'info'))
  }

  const handleApproveLeave = (requestId: string) => {
    patchState((current) => ({
      ...current,
      leaveRequests: current.leaveRequests.map((request) => (request.id === requestId ? { ...request, status: 'Approved' } : request)),
    }))
    addToast(buildToast('Leave approved', 'This approval is stored only in local demo state.', 'success'))
  }

  const handleCandidateSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!candidateForm.name.trim() || !candidateForm.role.trim()) {
      addToast(buildToast('Form incomplete', 'Add candidate name and role to continue.', 'warning'))
      return
    }

    const newCandidate: HrmsCandidate = {
      id: `CAN-${Date.now()}`,
      name: candidateForm.name,
      role: candidateForm.role,
      stage: 'Profile Review',
      score: 'Pending',
      owner: candidateForm.owner,
    }

    patchState((current) => ({ ...current, candidates: [newCandidate, ...current.candidates] }))
    setCandidateForm({ name: '', role: '', owner: currentUser.name })
    addToast(buildToast('Candidate added', 'The profile entered the local recruitment pipeline.', 'success'))
  }

  const exportEmployees = () => {
    downloadSampleFile(
      'qode27-hrms-directory.csv',
      createCsvFromRows(
        state.employees.map((employee) => ({
          id: employee.id,
          name: employee.name,
          department: employee.department,
          role: employee.role,
          location: employee.location,
          attendance: employee.attendance,
          status: employee.status,
        })),
      ),
      'text/csv;charset=utf-8',
    )
    addToast(buildToast('Directory exported', 'A sample employee directory CSV was generated in-browser.', 'success'))
  }

  return (
    <>
      <Seo title="HRMS Interactive Demo | Qode27" description="Interactive frontend-only HRMS demo with employee operations, attendance, payroll, and recruitment." canonicalPath={activeSection === 'dashboard' ? '/demo/hrms' : `/demo/hrms/${activeSection}`} />

      <DemoShell
        app={app}
        sections={sections}
        activeSection={activeSection}
        title="A structured HRMS built for clarity, approvals, and workforce visibility."
        subtitle="This product feels like an internal enterprise system: measured, clean, and people-centric. Attendance, leave, payroll, and hiring all update in a safe browser-only sandbox."
        currentUser={currentUser}
        onSwitchUser={handleUserSwitch}
        users={users}
        onReset={handleReset}
        onRefresh={handleRefresh}
        isRefreshing={isRefreshing}
        actions={[
          { label: 'Request tailored HRMS demo', href: buildDemoRequestPath('HRMS Demo') },
          { label: 'WhatsApp Qode27', href: buildDemoWhatsAppHref('HRMS Demo'), variant: 'secondary' },
        ]}
      >
        <DemoMetricGrid app={app} items={metrics} isRefreshing={isRefreshing} />

        {activeSection === 'dashboard' ? (
          <>
            <div className="mt-4 grid gap-4 xl:grid-cols-[1.15fr_0.85fr]">
              <DemoPanel app={app} title="Workforce health" subtitle="Attendance and approval movement organized for HR leadership.">
                <DemoTrendChart app={app} title="Weekly attendance trend" valueSuffix="%" data={state.attendanceTrend} mode="lineish" />
              </DemoPanel>
              <DemoPanel app={app} title="HR office notes" subtitle="Strategic highlights surfaced like a formal internal admin panel.">
                <div className="grid gap-3">
                  {orgCards.map((card) => (
                    <div key={card.title} className="rounded-[1.2rem] border border-indigo-100 bg-indigo-50/60 p-4">
                      <p className="text-sm font-semibold text-slate-950">{card.title}</p>
                      <p className="mt-2 text-sm leading-6 text-slate-600">{card.copy}</p>
                    </div>
                  ))}
                </div>
              </DemoPanel>
            </div>

            <div className="mt-4 grid gap-4 xl:grid-cols-[1.15fr_0.85fr]">
              <DemoPanel app={app} title="Department overview" subtitle="Representative organization summary with attendance and location balance.">
                <div className="grid gap-4 md:grid-cols-3">
                  {[
                    { label: 'Engineering', value: '84', note: '97% attendance' },
                    { label: 'Operations', value: '52', note: '4 implementation leads active' },
                    { label: 'Finance & HR', value: '31', note: 'Zero payroll blockers' },
                  ].map((item) => (
                    <div key={item.label} className="rounded-[1.2rem] border border-slate-200 bg-slate-50 p-4">
                      <p className="text-xs font-semibold uppercase tracking-[0.2em] text-indigo-700">{item.label}</p>
                      <p className="mt-4 text-3xl font-semibold tracking-[-0.05em] text-slate-950">{item.value}</p>
                      <p className="mt-2 text-sm text-slate-600">{item.note}</p>
                    </div>
                  ))}
                </div>
              </DemoPanel>

              <DemoPanel app={app} title="Approval queue" subtitle="Requests and actions aligned to manager workflows.">
                <div className="space-y-3">
                  {state.leaveRequests.map((request) => (
                    <div key={request.id} className="rounded-[1.2rem] border border-slate-200 bg-slate-50 p-4">
                      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                        <div>
                          <p className="text-sm font-semibold text-slate-950">{request.employee}</p>
                          <p className="mt-1 text-sm text-slate-600">{request.type} · {request.duration}</p>
                        </div>
                        <div className="flex items-center gap-3">
                          <DemoBadge app={app} value={request.status} tone={request.status === 'Pending' ? 'warning' : request.status === 'Approved' ? 'positive' : 'neutral'} />
                          {request.status === 'Pending' ? (
                            <button type="button" onClick={() => handleApproveLeave(request.id)} className="rounded-xl bg-[var(--demo-primary)] px-4 py-2 text-sm font-semibold text-white">
                              Approve
                            </button>
                          ) : null}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </DemoPanel>
            </div>
          </>
        ) : null}

        {activeSection === 'employees' ? (
          <div className="mt-4 space-y-4">
            <DemoPanel
              app={app}
              title="Employee directory"
              subtitle="A polished enterprise directory with soft search and export controls."
              action={
                <button type="button" onClick={exportEmployees} className="inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-900 hover:border-[var(--demo-primary)] hover:text-[var(--demo-primary)]">
                  <FiDownload />
                  Export directory
                </button>
              }
            >
              <div className="mb-4 flex items-center gap-3 rounded-[1.2rem] border border-slate-200 bg-slate-50 px-4 py-3">
                <FiSearch className="text-slate-500" />
                <input value={searchQuery} onChange={(event) => setSearchQuery(event.target.value)} placeholder="Search employees, departments, locations" className="w-full bg-transparent text-sm text-slate-900 outline-none placeholder:text-slate-400" />
              </div>

              {filteredEmployees.length > 0 ? (
                <DemoDataTable
                  app={app}
                  columns={[
                    { key: 'employee', header: 'Employee', render: (row) => <div><p className="font-semibold text-slate-950">{row.name}</p><p className="text-xs text-slate-500">{row.role}</p></div> },
                    { key: 'department', header: 'Department', render: (row) => row.department },
                    { key: 'location', header: 'Location', render: (row) => row.location },
                    { key: 'attendance', header: 'Attendance', render: (row) => row.attendance },
                    { key: 'leave', header: 'Leave', render: (row) => `${row.leaveBalance} days` },
                    { key: 'status', header: 'Status', render: (row) => <DemoBadge app={app} value={row.status} tone={row.status === 'Active' ? 'positive' : 'warning'} /> },
                  ]}
                  rows={filteredEmployees}
                />
              ) : (
                <DemoEmptyState app={app} title="No employees matched" description="Adjust the query to bring back the employee list." />
              )}
            </DemoPanel>
          </div>
        ) : null}

        {activeSection === 'payroll' ? (
          <div className="mt-4 grid gap-4 xl:grid-cols-[1.15fr_0.85fr]">
            <DemoPanel app={app} title="Payroll schedule" subtitle="Finance-facing monthly close summary.">
              <DemoDataTable
                app={app}
                columns={[
                  { key: 'month', header: 'Month', render: (row) => row.month },
                  { key: 'total', header: 'Total Payroll', render: (row) => <span className="font-semibold text-slate-950">{row.total}</span> },
                  { key: 'variance', header: 'Variance', render: (row) => row.variance },
                  { key: 'status', header: 'Status', render: (row) => <DemoBadge app={app} value={row.status} tone={row.status === 'Closed' ? 'positive' : 'warning'} /> },
                ]}
                rows={state.payrollRuns.map((item) => ({ ...item, id: item.month }))}
              />
            </DemoPanel>
            <DemoPanel app={app} title="Payroll readiness" subtitle="Executive notes for a calmer finance workflow.">
              <div className="grid gap-3">
                {[
                  ['Attendance close', '5 departments locked and reconciled'],
                  ['Variable pay', 'Sales and operations inputs received'],
                  ['Bank file', 'Disabled in demo mode by design'],
                ].map(([label, value]) => (
                  <div key={label} className="rounded-[1.2rem] border border-slate-200 bg-slate-50 p-4">
                    <p className="text-xs font-semibold uppercase tracking-[0.2em] text-indigo-700">{label}</p>
                    <p className="mt-2 text-sm leading-6 text-slate-600">{value}</p>
                  </div>
                ))}
              </div>
            </DemoPanel>
          </div>
        ) : null}

        {activeSection === 'recruitment' ? (
          <div className="mt-4 grid gap-4 xl:grid-cols-[1.1fr_0.9fr]">
            <DemoPanel app={app} title="Recruitment pipeline" subtitle="Hiring appears as a structured internal workflow, not a generic kanban.">
              <div className="grid gap-3 md:grid-cols-3">
                {[
                  { label: 'Review', stages: ['Profile Review'] },
                  { label: 'Assessment', stages: ['Assignment Review', 'Panel Interview'] },
                  { label: 'Close', stages: ['Offer Discussion'] },
                ].map((lane) => (
                  <div key={lane.label} className="rounded-[1.2rem] border border-slate-200 bg-slate-50 p-4">
                    <p className="text-xs font-semibold uppercase tracking-[0.2em] text-indigo-700">{lane.label}</p>
                    <div className="mt-4 space-y-3">
                      {state.candidates.filter((candidate) => lane.stages.includes(candidate.stage)).map((candidate) => (
                        <div key={candidate.id} className="rounded-xl border border-white bg-white p-3 shadow-[0_10px_24px_rgba(15,23,42,0.05)]">
                          <p className="text-sm font-semibold text-slate-950">{candidate.name}</p>
                          <p className="mt-1 text-sm text-slate-600">{candidate.role}</p>
                          <div className="mt-3 flex items-center justify-between text-xs text-slate-500">
                            <span>{candidate.owner}</span>
                            <span>{candidate.score}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </DemoPanel>

            <DemoPanel app={app} title="Add candidate" subtitle="Local-only intake form for HR walkthroughs.">
              <form className="grid gap-4" onSubmit={handleCandidateSubmit}>
                <label className="space-y-2">
                  <span className="text-sm font-medium text-slate-700">Candidate name</span>
                  <input value={candidateForm.name} onChange={(event) => setCandidateForm((current) => ({ ...current, name: event.target.value }))} className="w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none focus:border-[var(--demo-primary)]" />
                </label>
                <label className="space-y-2">
                  <span className="text-sm font-medium text-slate-700">Role</span>
                  <input value={candidateForm.role} onChange={(event) => setCandidateForm((current) => ({ ...current, role: event.target.value }))} className="w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none focus:border-[var(--demo-primary)]" />
                </label>
                <label className="space-y-2">
                  <span className="text-sm font-medium text-slate-700">Owner</span>
                  <select value={candidateForm.owner} onChange={(event) => setCandidateForm((current) => ({ ...current, owner: event.target.value }))} className="w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none focus:border-[var(--demo-primary)]">
                    {users.map((user) => (
                      <option key={user.email} value={user.name}>
                        {user.name}
                      </option>
                    ))}
                  </select>
                </label>
                <button type="submit" className="inline-flex min-h-12 items-center justify-center rounded-xl bg-[var(--demo-primary)] px-5 text-sm font-semibold text-white">
                  Save to pipeline
                </button>
              </form>
            </DemoPanel>
          </div>
        ) : null}
      </DemoShell>

      <DemoToastStack toasts={toasts} />
    </>
  )
}
