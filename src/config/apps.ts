export type AppKey = 'hms' | 'hrms'

export type DemoAppConfig = {
  key: AppKey
  name: string
  displayName: string
  productSlug: string
  demoPath: string
  demoUrl: string
  launchTitle: string
  launchSubtitle: string
  features: string[]
}

export const apps: Record<AppKey, DemoAppConfig> = {
  hrms: {
    key: 'hrms',
    name: 'HRMS',
    displayName: 'HRMS by Qode27',
    productSlug: 'hrms',
    demoPath: '/hrms/demo',
    demoUrl: 'https://hrms-260324.azurewebsites.net/dashboard?demo=true',
    launchTitle: 'Launching Demo Environment...',
    launchSubtitle: 'No login required • Sample data loaded',
    features: ['Employee records and directory', 'Leave and attendance workflows', 'Payroll-ready admin visibility'],
  },
  hms: {
    key: 'hms',
    name: 'HMS',
    displayName: 'HMS by Qode27',
    productSlug: 'hms',
    demoPath: '/hms/demo',
    demoUrl: 'https://sims-hospital-demo-260324.azurewebsites.net/?demo=true',
    launchTitle: 'Launching Demo Environment...',
    launchSubtitle: 'No login required • Sample data loaded',
    features: ['Patient ops and front-desk flow', 'Billing and payment visibility', 'Hospital admin dashboard'],
  },
}

export const demoApps = Object.values(apps)

export function getAppByKey(key?: string) {
  if (!key) {
    return null
  }

  return apps[key as AppKey] ?? null
}

export function getAppByProductSlug(slug?: string) {
  return demoApps.find((app) => app.productSlug === slug) ?? null
}
