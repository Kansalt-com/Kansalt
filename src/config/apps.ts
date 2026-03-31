export type AppKey = 'hms' | 'hrms'
export type AppCategory = 'Healthcare' | 'Business' | 'Finance' | 'Operations'

export type DemoAppConfig = {
  key: AppKey
  name: string
  displayName: string
  category: AppCategory
  productSlug: string
  tagline: string
  whatsappText: string
  whatsappUrl: string
  features: string[]
  benefits: string[]
  screenshots: string[]
}

function buildWhatsappUrl(message: string) {
  return `https://wa.me/917022556960?text=${encodeURIComponent(message)}`
}

export const apps: Record<AppKey, DemoAppConfig> = {
  hrms: {
    key: 'hrms',
    name: 'HRMS',
    displayName: 'HRMS by Qode27',
    category: 'Business',
    productSlug: 'hrms',
    tagline: 'People operations software for growing teams that want clarity, speed, and control.',
    whatsappText: 'Hello Qode27, I would like a demo for HRMS',
    whatsappUrl: buildWhatsappUrl('Hello Qode27, I would like a demo for HRMS'),
    features: ['Employee records and directory', 'Leave and attendance workflows', 'Payroll-ready admin visibility'],
    benefits: ['Reduce approval delays across teams', 'Keep employee data structured and current', 'Prepare payroll with less manual effort'],
    screenshots: ['People dashboard overview', 'Attendance and leave approvals', 'Employee records and lifecycle tracking'],
  },
  hms: {
    key: 'hms',
    name: 'HMS',
    displayName: 'HMS by Qode27',
    category: 'Healthcare',
    productSlug: 'hms',
    tagline: 'Hospital workflow software built for front-desk speed, billing accuracy, and admin visibility.',
    whatsappText: 'Hello Qode27, I would like a demo for HMS',
    whatsappUrl: buildWhatsappUrl('Hello Qode27, I would like a demo for HMS'),
    features: ['Patient ops and front-desk flow', 'Billing and payment visibility', 'Hospital admin dashboard'],
    benefits: ['Reduce admission and billing bottlenecks', 'Keep daily operations visible in one place', 'Improve hospital workflow accuracy and speed'],
    screenshots: ['Hospital operations dashboard', 'Patient intake and registry', 'Billing and payment summary'],
  },
}

export const appStoreApps = Object.values(apps)
export const appCategories: AppCategory[] = ['Healthcare', 'Business', 'Finance', 'Operations']

export function getAppByKey(key?: string) {
  if (!key) {
    return null
  }

  return apps[key as AppKey] ?? null
}

export function getAppByProductSlug(slug?: string) {
  return appStoreApps.find((app) => app.productSlug === slug) ?? null
}
