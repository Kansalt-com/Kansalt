import { FiActivity, FiBox, FiHeart, FiTruck } from 'react-icons/fi'
import type { SolutionSlug } from '../data/solutions'
import { buildWhatsAppHref } from '../lib/demo/mock'
import type { DemoAppConfig, DemoAppSlug } from '../lib/demo/types'

export const demoApps: DemoAppConfig[] = [
  {
    slug: 'hrms',
    solutionSlug: 'hrms',
    name: 'HRMS Demo',
    shortName: 'HRMS',
    category: 'Internal Operations',
    tagline: 'People operations, attendance, payroll, and hiring in one polished walkthrough.',
    summary: 'Show workforce visibility, approvals, payroll health, and hiring momentum with safe in-browser mock state.',
    accent: {
      primary: '#3659d9',
      secondary: '#7c8efc',
      surface: 'rgba(54, 89, 217, 0.1)',
      gradient: 'linear-gradient(135deg, #172554 0%, #22346a 46%, #3659d9 100%)',
      ink: '#0f172a',
      page: '#f5f8ff',
      panel: 'rgba(255,255,255,0.88)',
      line: 'rgba(148,163,184,0.22)',
    },
    icon: FiActivity,
    identity: {
      navStyle: 'enterprise-sidebar',
      densityMode: 'comfortable',
      cardStyle: 'soft',
      tableStyle: 'clean',
      previewVariant: 'hrms',
      typography: 'corporate',
      dashboardLabel: 'People command overview',
      motionStyle: 'calm',
      productHint: 'Corporate HR cockpit',
    },
    heroMetrics: [
      { label: 'Employees', value: '248', change: '+12 this quarter', tone: 'positive' },
      { label: 'Attendance', value: '96.4%', change: '+1.8% vs last month', tone: 'positive' },
      { label: 'Payroll Health', value: 'On track', change: 'Zero pending approvals', tone: 'neutral' },
    ],
    demoEnabled: true,
    requestDemoOnly: false,
    modulePath: () => import('../pages/demo/apps/HrmsDemoPage'),
  },
  {
    slug: 'hms',
    solutionSlug: 'healthcare-management',
    name: 'Hospital Management Demo',
    shortName: 'HMS',
    category: 'Healthcare',
    tagline: 'Front desk, appointments, billing, and ward operations with a client-ready hospital flow.',
    summary: 'Demonstrate patient movement, doctor schedules, collections, and occupancy without touching live records.',
    accent: {
      primary: '#0d9488',
      secondary: '#34d399',
      surface: 'rgba(13, 148, 136, 0.12)',
      gradient: 'linear-gradient(135deg, #083344 0%, #0f4f5f 46%, #0d9488 100%)',
      ink: '#082f49',
      page: '#f3fbfb',
      panel: 'rgba(255,255,255,0.92)',
      line: 'rgba(148,163,184,0.18)',
    },
    icon: FiHeart,
    identity: {
      navStyle: 'workflow-topbar',
      densityMode: 'compact',
      cardStyle: 'clinical',
      tableStyle: 'clinical',
      previewVariant: 'hms',
      typography: 'clinical',
      dashboardLabel: 'Clinical flow board',
      motionStyle: 'precise',
      productHint: 'Reception-to-billing flow',
    },
    heroMetrics: [
      { label: 'Today Appointments', value: '126', change: '14 walk-ins added', tone: 'neutral' },
      { label: 'Collections', value: 'Rs 4.8L', change: '+9% vs yesterday', tone: 'positive' },
      { label: 'Ward Occupancy', value: '82%', change: '12 beds available', tone: 'warning' },
    ],
    demoEnabled: true,
    requestDemoOnly: false,
    modulePath: () => import('../pages/demo/apps/HmsDemoPage'),
  },
  {
    slug: 'inventory',
    solutionSlug: 'inventory-management',
    name: 'Inventory Demo',
    shortName: 'Inventory',
    category: 'Distribution',
    tagline: 'Warehouse visibility, vendor coordination, and order control from one demo workspace.',
    summary: 'Demonstrate stock accuracy, purchase flow, vendor SLAs, and sample exports with static data and local state.',
    accent: {
      primary: '#ea580c',
      secondary: '#f59e0b',
      surface: 'rgba(234, 88, 12, 0.1)',
      gradient: 'linear-gradient(135deg, #111827 0%, #2b2f36 36%, #ea580c 100%)',
      ink: '#111827',
      page: '#f5f6f7',
      panel: 'rgba(255,255,255,0.95)',
      line: 'rgba(71,85,105,0.24)',
    },
    icon: FiBox,
    identity: {
      navStyle: 'operations-rail',
      densityMode: 'dense',
      cardStyle: 'industrial',
      tableStyle: 'warehouse',
      previewVariant: 'inventory',
      typography: 'operational',
      dashboardLabel: 'Warehouse control layer',
      motionStyle: 'mechanical',
      productHint: 'Stock and movement control',
    },
    heroMetrics: [
      { label: 'Active SKUs', value: '1,486', change: '98 flagged for reorder', tone: 'warning' },
      { label: 'Order Fill Rate', value: '97.1%', change: '+2.1% this week', tone: 'positive' },
      { label: 'Warehouse Value', value: 'Rs 2.7Cr', change: 'Across 4 storage zones', tone: 'neutral' },
    ],
    demoEnabled: true,
    requestDemoOnly: false,
    modulePath: () => import('../pages/demo/apps/InventoryDemoPage'),
  },
  {
    slug: 'truck-parking',
    solutionSlug: 'parking-management',
    name: 'Truck Parking Demo',
    shortName: 'Parking',
    category: 'Operations',
    tagline: 'Live bay occupancy, entries, exits, and revenue flow in a premium operations shell.',
    summary: 'Show parking movement, bay allocation, occupancy, and billing with realistic local-only datasets.',
    accent: {
      primary: '#facc15',
      secondary: '#fb923c',
      surface: 'rgba(250, 204, 21, 0.14)',
      gradient: 'linear-gradient(135deg, #111111 0%, #232323 42%, #44403c 100%)',
      ink: '#fafaf9',
      page: '#121212',
      panel: 'rgba(23,23,23,0.88)',
      line: 'rgba(250,204,21,0.18)',
    },
    icon: FiTruck,
    identity: {
      navStyle: 'command-center',
      densityMode: 'live',
      cardStyle: 'tactical',
      tableStyle: 'board',
      previewVariant: 'truck-parking',
      typography: 'command',
      dashboardLabel: 'Live yard board',
      motionStyle: 'urgent',
      productHint: 'Occupancy and movement board',
    },
    heroMetrics: [
      { label: 'Current Occupancy', value: '78%', change: '52 of 67 bays used', tone: 'warning' },
      { label: 'Daily Revenue', value: 'Rs 1.46L', change: '+11% vs avg day', tone: 'positive' },
      { label: 'Average Turnaround', value: '6h 12m', change: '2 fast-lane exits pending', tone: 'neutral' },
    ],
    demoEnabled: true,
    requestDemoOnly: false,
    modulePath: () => import('../pages/demo/apps/TruckParkingDemoPage'),
  },
]

export function getDemoAppBySlug(slug?: string) {
  return demoApps.find((app) => app.slug === slug)
}

export function getDemoAppBySolutionSlug(solutionSlug?: SolutionSlug) {
  return demoApps.find((app) => app.solutionSlug === solutionSlug)
}

export function getDemoRoute(slug: DemoAppSlug) {
  return `/demo/${slug}`
}

export function buildDemoRequestPath(appName?: string) {
  return appName ? `/request-demo?industry=${encodeURIComponent(appName)}&source=interactive-demo` : '/request-demo'
}

export function buildDemoWhatsAppHref(appName: string) {
  return buildWhatsAppHref(`Hi Qode27, I would like a tailored walkthrough for the ${appName} demo.`)
}
