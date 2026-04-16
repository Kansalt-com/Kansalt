import { useDeferredValue, useMemo, useState, type FormEvent } from 'react'
import { FiAlertTriangle, FiBarChart2, FiBox, FiDownload, FiLayers, FiShoppingCart, FiTruck, FiUsers } from 'react-icons/fi'
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
import { createInventoryState, inventoryUsers } from '../../../data/demo/inventory'
import { buildToast, createCsvFromRows, downloadSampleFile } from '../../../lib/demo/mock'
import { useDemoAppState } from '../../../lib/demo/useDemoAppState'
import { useDemoNetworkGuard } from '../../../lib/demo/useDemoNetworkGuard'
import type { DemoAppRouteProps, DemoMetric, DemoNavItem } from '../../../lib/demo/types'
import Seo from '../../../components/ui/Seo'

const sections: DemoNavItem[] = [
  { slug: 'dashboard', label: 'Control', icon: FiBarChart2, description: 'Warehouse value, fill rate, and alert state.' },
  { slug: 'stock', label: 'Stock', icon: FiBox, description: 'SKU-led stock visibility with denser operational detail.' },
  { slug: 'purchase-orders', label: 'Purchase Orders', icon: FiShoppingCart, description: 'Procurement actions and inbound readiness.' },
  { slug: 'vendors', label: 'Vendors', icon: FiUsers, description: 'Supplier performance and receivables context.' },
]

export default function InventoryDemoPage({ app, section }: DemoAppRouteProps) {
  useDemoNetworkGuard()

  const { state, patchState, currentUser, users, switchUser, resetDemo, refreshDemo, isRefreshing, toasts, addToast } = useDemoAppState({
    storageKey: 'qode27-demo-inventory',
    createInitialState: createInventoryState,
    users: inventoryUsers,
  })

  const activeSection = sections.some((item) => item.slug === section) ? section ?? 'dashboard' : 'dashboard'
  const [stockQuery, setStockQuery] = useState('')
  const [poForm, setPoForm] = useState({ vendor: state.vendors[0]?.name ?? '', eta: '27 Apr', amount: 'Rs 1.2L' })
  const deferredQuery = useDeferredValue(stockQuery)

  const filteredItems = useMemo(() => {
    const term = deferredQuery.trim().toLowerCase()
    if (!term) return state.items
    return state.items.filter((item) => [item.sku, item.name, item.zone].some((value) => value.toLowerCase().includes(term)))
  }, [deferredQuery, state.items])

  const criticalItems = state.items.filter((item) => item.status !== 'Healthy')
  const metrics: DemoMetric[] = [
    { label: 'Warehouse Value', value: 'Rs 2.7Cr', change: 'Across 4 active zones', tone: 'neutral' },
    { label: 'SKU Alerts', value: String(criticalItems.length), change: 'Requires reorder review', tone: 'warning' },
    { label: 'Dispatch Fill Rate', value: '97.1%', change: 'Strong outbound discipline', tone: 'positive' },
    { label: 'Pending Receivables', value: `${state.invoices.filter((invoice) => invoice.status === 'Pending').length}`, change: 'Commercial follow-up active', tone: 'warning' },
  ]

  const handleUserSwitch = (email: string) => {
    switchUser(email)
    addToast(buildToast('Persona switched', 'Warehouse control permissions updated.', 'info'))
  }

  const handleReset = () => {
    resetDemo()
    addToast(buildToast('Demo reset', 'Inventory sample state has been restored.', 'success'))
  }

  const handleRefresh = () => {
    refreshDemo()
    addToast(buildToast('Control board refreshed', 'Warehouse telemetry refreshed locally only.', 'info'))
  }

  const handlePurchaseOrderSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    patchState((current) => ({
      ...current,
      purchaseOrders: [
        { id: `PO-${Date.now()}`, vendor: poForm.vendor, eta: poForm.eta, amount: poForm.amount, status: 'Draft' },
        ...current.purchaseOrders,
      ],
    }))
    addToast(buildToast('Purchase order drafted', 'PO created inside local demo state.', 'success'))
  }

  const approvePurchaseOrder = (purchaseOrderId: string) => {
    patchState((current) => ({
      ...current,
      purchaseOrders: current.purchaseOrders.map((purchaseOrder) => (purchaseOrder.id === purchaseOrderId ? { ...purchaseOrder, status: 'Approved' } : purchaseOrder)),
    }))
    addToast(buildToast('PO approved', 'Approval saved in the demo workspace only.', 'success'))
  }

  const exportStock = () => {
    downloadSampleFile(
      'qode27-inventory-stock.csv',
      createCsvFromRows(
        state.items.map((item) => ({
          sku: item.sku,
          name: item.name,
          zone: item.zone,
          onHand: item.onHand,
          reorderPoint: item.reorderPoint,
          status: item.status,
        })),
      ),
      'text/csv;charset=utf-8',
    )
    addToast(buildToast('Stock export ready', 'Warehouse stock sheet generated from mock data.', 'success'))
  }

  return (
    <>
      <Seo title="Inventory Interactive Demo | Qode27" description="Interactive frontend-only inventory demo with stock control, procurement, and vendor operations." canonicalPath={activeSection === 'dashboard' ? '/demo/inventory' : `/demo/inventory/${activeSection}`} />

      <DemoShell
        app={app}
        sections={sections}
        activeSection={activeSection}
        title="An industrial-grade inventory system with denser operations and stronger control-room energy."
        subtitle="This product is intentionally more data-heavy than HRMS or HMS. It prioritizes stock accuracy, reorder signals, throughput, and vendor follow-through with stronger contrast and less decorative softness."
        currentUser={currentUser}
        onSwitchUser={handleUserSwitch}
        users={users}
        onReset={handleReset}
        onRefresh={handleRefresh}
        isRefreshing={isRefreshing}
        actions={[
          { label: 'Request inventory rollout demo', href: buildDemoRequestPath('Inventory Demo') },
          { label: 'WhatsApp Qode27', href: buildDemoWhatsAppHref('Inventory Demo'), variant: 'secondary' },
        ]}
      >
        <DemoMetricGrid app={app} items={metrics} isRefreshing={isRefreshing} columnsClass="md:grid-cols-2 xl:grid-cols-4" />

        {activeSection === 'dashboard' ? (
          <>
            <div className="mt-4 grid gap-4 xl:grid-cols-[1.15fr_0.85fr]">
              <DemoPanel
                app={app}
                title="Throughput"
                subtitle="Inbound and outbound movement rendered like an operational control layer."
                action={
                  <button type="button" onClick={exportStock} className="inline-flex items-center gap-2 rounded-xl border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-900 hover:border-orange-500 hover:text-orange-600">
                    <FiDownload />
                    Export stock
                  </button>
                }
              >
                <DemoTrendChart app={app} title="Units processed per day" data={state.throughputTrend} />
              </DemoPanel>
              <DemoPanel app={app} title="Alert stack" subtitle="High-priority signals appear before softer summaries.">
                <div className="space-y-3">
                  {criticalItems.map((item) => (
                    <div key={item.sku} className="rounded-[1rem] border border-slate-300 bg-slate-50 p-4">
                      <div className="flex items-center justify-between gap-3">
                        <div>
                          <p className="text-sm font-semibold text-slate-950">{item.name}</p>
                          <p className="mt-1 text-sm text-slate-600">{item.sku} · Zone {item.zone}</p>
                        </div>
                        <DemoBadge app={app} value={item.status} tone="warning" />
                      </div>
                      <p className="mt-3 text-xs text-slate-500">On hand {item.onHand} · Reorder point {item.reorderPoint}</p>
                    </div>
                  ))}
                </div>
              </DemoPanel>
            </div>

            <div className="mt-4 grid gap-4 xl:grid-cols-[1.1fr_0.9fr]">
              <DemoPanel app={app} title="Warehouse zones" subtitle="Zone occupancy and movement posture shown before marketing-style summaries.">
                <div className="grid gap-3 md:grid-cols-4">
                  {[
                    ['Zone A', 'High turnover', '184 active units'],
                    ['Zone B', 'Replenishment due', '62 active units'],
                    ['Zone C', 'Critical reorder', '28 active units'],
                    ['Zone D', 'Stable', '48 active units'],
                  ].map(([title, stateLabel, note]) => (
                    <div key={title} className="rounded-[1rem] border border-slate-300 bg-white p-4">
                      <p className="text-xs font-semibold uppercase tracking-[0.2em] text-orange-600">{title}</p>
                      <p className="mt-3 text-lg font-semibold text-slate-950">{stateLabel}</p>
                      <p className="mt-2 text-sm text-slate-600">{note}</p>
                    </div>
                  ))}
                </div>
              </DemoPanel>
              <DemoPanel app={app} title="Commercial watchlist" subtitle="Receivables and vendor health shown as practical operator cards.">
                <div className="space-y-3">
                  {state.invoices.map((invoice) => (
                    <div key={invoice.id} className="rounded-[1rem] border border-slate-300 bg-white p-4">
                      <div className="flex items-center justify-between gap-3">
                        <div>
                          <p className="text-sm font-semibold text-slate-950">{invoice.customer}</p>
                          <p className="mt-1 text-sm text-slate-600">{invoice.amount}</p>
                        </div>
                        <DemoBadge app={app} value={invoice.status} tone={invoice.status === 'Paid' ? 'positive' : 'warning'} />
                      </div>
                      <p className="mt-3 text-xs text-slate-500">Due date {invoice.dueDate}</p>
                    </div>
                  ))}
                </div>
              </DemoPanel>
            </div>
          </>
        ) : null}

        {activeSection === 'stock' ? (
          <div className="mt-4">
            <DemoPanel app={app} title="Stock ledger" subtitle="The densest screen in the system, built to feel practical and operations-heavy.">
              <div className="mb-4 flex items-center gap-3 rounded-[1rem] border border-slate-300 bg-slate-50 px-4 py-3">
                <FiLayers className="text-orange-600" />
                <input value={stockQuery} onChange={(event) => setStockQuery(event.target.value)} placeholder="Search SKU, item name, zone" className="w-full bg-transparent text-sm text-slate-900 outline-none placeholder:text-slate-400" />
              </div>
              {filteredItems.length > 0 ? (
                <DemoDataTable
                  app={app}
                  columns={[
                    { key: 'sku', header: 'SKU', render: (row) => <span className="font-semibold text-slate-950">{row.sku}</span> },
                    { key: 'name', header: 'Item', render: (row) => row.name },
                    { key: 'zone', header: 'Zone', render: (row) => row.zone },
                    { key: 'onHand', header: 'On Hand', render: (row) => row.onHand },
                    { key: 'reorderPoint', header: 'Reorder Point', render: (row) => row.reorderPoint },
                    { key: 'status', header: 'State', render: (row) => <DemoBadge app={app} value={row.status} tone={row.status === 'Healthy' ? 'positive' : 'warning'} /> },
                  ]}
                  rows={filteredItems.map((item) => ({ ...item, id: item.sku }))}
                />
              ) : (
                <DemoEmptyState app={app} title="No stock items matched" description="Try another SKU, zone, or product keyword." />
              )}
            </DemoPanel>
          </div>
        ) : null}

        {activeSection === 'purchase-orders' ? (
          <div className="mt-4 grid gap-4 xl:grid-cols-[1.15fr_0.85fr]">
            <DemoPanel app={app} title="Procurement queue" subtitle="PO review is presented as a fast action board, not a generic list of cards.">
              <div className="space-y-3">
                {state.purchaseOrders.map((purchaseOrder) => (
                  <div key={purchaseOrder.id} className="rounded-[1rem] border border-slate-300 bg-white p-4">
                    <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                      <div>
                        <p className="text-sm font-semibold text-slate-950">{purchaseOrder.vendor}</p>
                        <p className="mt-1 text-sm text-slate-600">{purchaseOrder.id} · ETA {purchaseOrder.eta}</p>
                      </div>
                      <div className="flex items-center gap-3">
                        <DemoBadge app={app} value={purchaseOrder.status} tone={purchaseOrder.status === 'Approved' ? 'positive' : purchaseOrder.status === 'Draft' ? 'warning' : 'neutral'} />
                        {purchaseOrder.status !== 'Approved' ? (
                          <button type="button" onClick={() => approvePurchaseOrder(purchaseOrder.id)} className="rounded-xl bg-orange-500 px-4 py-2 text-sm font-semibold text-white">
                            Approve
                          </button>
                        ) : null}
                      </div>
                    </div>
                    <p className="mt-3 text-xs text-slate-500">{purchaseOrder.amount}</p>
                  </div>
                ))}
              </div>
            </DemoPanel>
            <DemoPanel app={app} title="Create purchase order" subtitle="Procurement flow remains local-only and safe to demonstrate live.">
              <form className="grid gap-4" onSubmit={handlePurchaseOrderSubmit}>
                <label className="space-y-2">
                  <span className="text-sm font-medium text-slate-700">Vendor</span>
                  <select value={poForm.vendor} onChange={(event) => setPoForm((current) => ({ ...current, vendor: event.target.value }))} className="w-full rounded-xl border border-slate-300 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none focus:border-orange-500">
                    {state.vendors.map((vendor) => (
                      <option key={vendor.id} value={vendor.name}>
                        {vendor.name}
                      </option>
                    ))}
                  </select>
                </label>
                <label className="space-y-2">
                  <span className="text-sm font-medium text-slate-700">ETA</span>
                  <input value={poForm.eta} onChange={(event) => setPoForm((current) => ({ ...current, eta: event.target.value }))} className="w-full rounded-xl border border-slate-300 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none focus:border-orange-500" />
                </label>
                <label className="space-y-2">
                  <span className="text-sm font-medium text-slate-700">Amount</span>
                  <input value={poForm.amount} onChange={(event) => setPoForm((current) => ({ ...current, amount: event.target.value }))} className="w-full rounded-xl border border-slate-300 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none focus:border-orange-500" />
                </label>
                <button type="submit" className="inline-flex min-h-12 items-center justify-center rounded-xl bg-orange-500 px-5 text-sm font-semibold text-white">
                  Save draft PO
                </button>
              </form>
            </DemoPanel>
          </div>
        ) : null}

        {activeSection === 'vendors' ? (
          <div className="mt-4 grid gap-4 xl:grid-cols-[1.1fr_0.9fr]">
            <DemoPanel app={app} title="Vendor performance" subtitle="Supplier health is treated like an operations metric, not just a marketing summary.">
              <DemoDataTable
                app={app}
                columns={[
                  { key: 'vendor', header: 'Vendor', render: (row) => row.name },
                  { key: 'category', header: 'Category', render: (row) => row.category },
                  { key: 'fillRate', header: 'Fill Rate', render: (row) => row.fillRate },
                  { key: 'leadTime', header: 'Lead Time', render: (row) => row.leadTime },
                ]}
                rows={state.vendors.map((vendor) => ({ ...vendor, id: vendor.id }))}
              />
            </DemoPanel>
            <DemoPanel app={app} title="Receivables" subtitle="Commercial follow-up remains visible next to supplier performance.">
              <div className="space-y-3">
                {state.invoices.map((invoice) => (
                  <div key={invoice.id} className="rounded-[1rem] border border-slate-300 bg-white p-4">
                    <div className="flex items-center justify-between gap-3">
                      <div>
                        <p className="text-sm font-semibold text-slate-950">{invoice.customer}</p>
                        <p className="mt-1 text-sm text-slate-600">{invoice.amount}</p>
                      </div>
                      <DemoBadge app={app} value={invoice.status} tone={invoice.status === 'Paid' ? 'positive' : 'warning'} />
                    </div>
                    <p className="mt-3 text-xs text-slate-500">Due date {invoice.dueDate}</p>
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
