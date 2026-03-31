import type { IconType } from 'react-icons'
import type { AppCategory, AppKey } from '../config/apps'
import {
  FiArrowRight,
  FiBriefcase,
  FiCheckCircle,
  FiClock,
  FiCreditCard,
  FiDollarSign,
  FiHeart,
  FiLayers,
  FiMail,
  FiSettings,
  FiShield,
  FiTrendingUp,
  FiUsers,
  FiZap,
} from 'react-icons/fi'

export type NavItem = {
  label: string
  href: string
}

export type Product = {
  slug: string
  appKey?: AppKey
  categoryKey: AppCategory
  icon: IconType
  name: string
  category: string
  headline: string
  description: string
  features: string[]
  benefits: string[]
  screenshots: string[]
  metrics: { label: string; value: string }[]
  primaryCta: { label: string; href: string }
  secondaryCta: { label: string; href: string }
}

export type PricingPlan = {
  name: string
  price: string
  description: string
  features: string[]
  cta: string
  featured?: boolean
}

export type ContactMethod = {
  title: string
  value: string
  description: string
  href: string
  icon: IconType
}

export const navigation: NavItem[] = [
  { label: 'Home', href: '/' },
  { label: 'Products', href: '/products' },
  { label: 'Categories', href: '/products' },
  { label: 'Contact', href: '/contact' },
]

export const heroStats = [
  { label: 'Business apps in one place', value: '4+' },
  { label: 'Fast deployment window', value: '7-10 days' },
  { label: 'Teams launched faster', value: '45%' },
]

export const platformHighlights = [
  {
    icon: FiLayers,
    title: 'Built for Indian businesses',
    text: 'Qode27 packages business software around local workflows, real teams, and practical operational constraints.',
  },
  {
    icon: FiClock,
    title: 'Fast deployment',
    text: 'Focused implementations help teams go live in days, not quarters, while preserving product quality.',
  },
  {
    icon: FiDollarSign,
    title: 'Affordable SaaS solutions',
    text: 'Premium software experience without enterprise bloat makes adoption easier for SMEs and growing companies.',
  },
]

export const categories = [
  { key: 'Healthcare', icon: FiHeart, description: 'Hospital and clinic operations software for patient-facing teams.' },
  { key: 'Business', icon: FiBriefcase, description: 'Everyday business apps for HR, admin, and SME operations.' },
  { key: 'Finance', icon: FiCreditCard, description: 'Finance-focused workflow tools built for visibility and control.' },
  { key: 'Operations', icon: FiSettings, description: 'Automation and workflow systems for teams that run on process discipline.' },
] as const

export const products: Product[] = [
  {
    slug: 'hms',
    appKey: 'hms',
    categoryKey: 'Healthcare',
    icon: FiHeart,
    name: 'HMS by Qode27',
    category: 'Healthcare',
    headline: 'Hospital workflow software for front-desk speed, billing accuracy, and admin visibility.',
    description:
      'A premium hospital management application for admissions, billing, patient records, and daily operations designed for Indian healthcare teams.',
    features: ['Patient registry and admissions', 'Billing and payment visibility', 'Operational dashboard for administrators'],
    benefits: [
      'Streamline front-desk and billing coordination',
      'Reduce manual handoffs across patient workflows',
      'Give administrators a clean daily operating view',
    ],
    screenshots: ['Operations dashboard', 'Patient intake screen', 'Billing summary view'],
    metrics: [
      { label: 'Deployment window', value: '7-10 days' },
      { label: 'Billing accuracy focus', value: 'High' },
      { label: 'Ops visibility', value: 'Real-time' },
    ],
    primaryCta: { label: 'Request Demo', href: '/contact' },
    secondaryCta: { label: 'View Products', href: '/products' },
  },
  {
    slug: 'hrms',
    appKey: 'hrms',
    categoryKey: 'Business',
    icon: FiUsers,
    name: 'HRMS by Qode27',
    category: 'Business',
    headline: 'People operations software that keeps employee workflows organized and payroll-ready.',
    description:
      'A premium HRMS for SMEs and growing companies that want cleaner people operations across attendance, leave, approvals, and employee records.',
    features: ['Employee records and directory', 'Leave and approval workflows', 'Payroll-ready attendance visibility'],
    benefits: [
      'Reduce back-and-forth in manager approvals',
      'Keep employee data centralized and up to date',
      'Support faster admin cycles for payroll preparation',
    ],
    screenshots: ['People operations dashboard', 'Leave approval workflow', 'Employee directory experience'],
    metrics: [
      { label: 'Manager response lift', value: '2x faster' },
      { label: 'Payroll prep flow', value: 'Streamlined' },
      { label: 'SME fit', value: 'Excellent' },
    ],
    primaryCta: { label: 'Request Demo', href: '/contact' },
    secondaryCta: { label: 'View Products', href: '/products' },
  },
  {
    slug: 'automation-suite',
    categoryKey: 'Operations',
    icon: FiZap,
    name: 'Automation Suite by Qode27',
    category: 'Operations',
    headline: 'Business automation apps for approvals, reminders, and daily process execution.',
    description:
      'An automation suite for SMEs that want clean internal workflow systems for approvals, reminders, and high-visibility operations.',
    features: ['Approval routing engine', 'Automated reminders and follow-ups', 'Process dashboards and logs'],
    benefits: [
      'Remove repetitive coordination work',
      'Keep process ownership visible across teams',
      'Turn fragile routines into repeatable app-driven flows',
    ],
    screenshots: ['Workflow dashboard', 'Approval automation view', 'Operational activity feed'],
    metrics: [
      { label: 'Manual follow-ups reduced', value: '-61%' },
      { label: 'Operational clarity', value: 'High' },
      { label: 'Automation fit', value: 'SME-ready' },
    ],
    primaryCta: { label: 'Request Demo', href: '/contact' },
    secondaryCta: { label: 'View Products', href: '/products' },
  },
]

export const pricingPlans: PricingPlan[] = [
  {
    name: 'Starter',
    price: 'Custom',
    description: 'A clean launch plan for SMEs adopting packaged business software for the first time.',
    features: ['Core app setup', 'Guided onboarding', 'WhatsApp support', 'Business-friendly deployment'],
    cta: 'Request Demo',
  },
  {
    name: 'Growth',
    price: 'Custom',
    description: 'For companies that want stronger visibility, broader workflows, and app-store style scalability.',
    features: ['Expanded modules', 'Priority support', 'Operational reporting', 'Multi-team rollout'],
    cta: 'Request Demo',
    featured: true,
  },
  {
    name: 'Enterprise',
    price: 'Custom',
    description: 'For larger businesses that need implementation support, configuration depth, and tailored rollout.',
    features: ['Custom rollout planning', 'Advanced support', 'Workflow consulting', 'Long-term partnership'],
    cta: 'Request Demo',
  },
]

export const contactMethods: ContactMethod[] = [
  {
    title: 'WhatsApp',
    value: '+91 7022556960',
    description: 'Primary demo request channel for fast responses and product conversations.',
    href: 'https://wa.me/917022556960?text=Hello%20Qode27,%20I%20would%20like%20a%20demo',
    icon: FiArrowRight,
  },
  {
    title: 'Phone',
    value: '+91 7022556960',
    description: 'Call for direct discussion on deployment, fit, and pricing.',
    href: 'tel:+917022556960',
    icon: FiUsers,
  },
  {
    title: 'Email',
    value: 'qode27business@gmail.com',
    description: 'For procurement notes, detailed requirements, and follow-up.',
    href: 'mailto:qode27business@gmail.com',
    icon: FiMail,
  },
]

export const trustPoints = [
  'All your business software in one place',
  'From HR to Hospital — we’ve got you covered',
  'Built for Indian businesses and SME realities',
  'Premium apps with fast deployment and practical pricing',
]

export const pricingNotes = [
  {
    icon: FiCheckCircle,
    title: 'Built for Indian businesses',
    text: 'Each app is packaged for teams that need practical adoption, clear workflows, and dependable support.',
  },
  {
    icon: FiClock,
    title: 'Fast deployment (7–10 days)',
    text: 'Focused rollout plans help your team move from interest to implementation quickly.',
  },
  {
    icon: FiTrendingUp,
    title: 'Affordable SaaS solutions',
    text: 'Qode27 keeps the product experience premium while staying commercially realistic for SMEs.',
  },
]

export const footerLinks = navigation.filter((item) => item.label !== 'Categories')

export function getProductBySlug(slug?: string) {
  return products.find((product) => product.slug === slug)
}
