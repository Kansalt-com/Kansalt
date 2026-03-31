import type { IconType } from 'react-icons'
import type { AppKey } from '../config/apps'
import {
  FiArrowRight,
  FiBriefcase,
  FiCheckCircle,
  FiClock,
  FiCreditCard,
  FiHeart,
  FiLayers,
  FiMail,
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
  icon: IconType
  name: string
  category: string
  headline: string
  description: string
  features: string[]
  benefits: string[]
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
  { label: 'Pricing', href: '/pricing' },
  { label: 'Contact', href: '/contact' },
]

export const heroStats = [
  { label: 'Teams launched faster', value: '45%' },
  { label: 'Operational visibility', value: '24/7' },
  { label: 'Average workflow adoption', value: '94%' },
]

export const platformHighlights = [
  {
    icon: FiLayers,
    title: 'Product-led rollout',
    text: 'Every flow is designed to feel intuitive on day one, so teams spend less time learning and more time shipping work.',
  },
  {
    icon: FiShield,
    title: 'Trusted operating core',
    text: 'Role-aware views, clean permissions, and clear process states make mission-critical operations easier to trust.',
  },
  {
    icon: FiTrendingUp,
    title: 'Built to scale with process maturity',
    text: 'Start with a focused workflow, then expand into automation, reporting, and multi-team coordination without redesigning the stack.',
  },
]

export const products: Product[] = [
  {
    slug: 'hms',
    appKey: 'hms',
    icon: FiHeart,
    name: 'HMS by Qode27',
    category: 'Healthcare Operations',
    headline: 'Run patient, billing, and front-desk workflows from one clean operating layer.',
    description:
      'A hospital management platform that gives admins, reception teams, and finance staff a single source of truth for appointments, admissions, billing, and daily operations.',
    features: ['Live patient registry', 'Billing and payment previews', 'Admin dashboard with operational KPIs'],
    benefits: [
      'Reduce front-desk handoff delays across admissions and billing',
      'Give administrators a simple dashboard for daily performance',
      'Replace spreadsheet-heavy patient tracking with a product workflow',
    ],
    metrics: [
      { label: 'Admissions tracked', value: '1.8k/mo' },
      { label: 'Billing completion lift', value: '+31%' },
      { label: 'Admin time saved', value: '12 hrs/wk' },
    ],
    primaryCta: { label: 'Try Live Demo', href: '/hms/demo' },
    secondaryCta: { label: 'Get Pricing', href: '/pricing' },
  },
  {
    slug: 'hrms',
    appKey: 'hrms',
    icon: FiUsers,
    name: 'HRMS by Qode27',
    category: 'People Operations',
    headline: 'Bring people ops, leave approvals, and payroll readiness into one workflow.',
    description:
      'A streamlined HR platform for growing companies that want better visibility across attendance, leave, approvals, and employee records without a heavy enterprise setup.',
    features: ['Employee directory and records', 'Leave and approval workflows', 'Payroll-ready attendance data'],
    benefits: [
      'Make team operations faster with cleaner approval flows',
      'Give managers a simple review surface instead of chat-based requests',
      'Keep people data current without duplicate admin work',
    ],
    metrics: [
      { label: 'Manager response time', value: '-53%' },
      { label: 'Payroll prep cycle', value: '2x faster' },
      { label: 'Employee visibility', value: '100%' },
    ],
    primaryCta: { label: 'Try Live Demo', href: '/hrms/demo' },
    secondaryCta: { label: 'Get Pricing', href: '/pricing' },
  },
  {
    slug: 'automation-suite',
    icon: FiZap,
    name: 'Qode27 Automation Suite',
    category: 'Operations Automation',
    headline: 'Automate reminders, approvals, and internal process handoffs without adding complexity.',
    description:
      'A modular automation layer for finance, admin, and service teams that want to remove repetitive work while keeping full visibility over every operational step.',
    features: ['Approval routing engine', 'Automated reminders and follow-ups', 'Process dashboards and activity logs'],
    benefits: [
      'Eliminate repetitive manual coordination across internal teams',
      'Keep leaders informed with lightweight operational dashboards',
      'Turn fragile process knowledge into repeatable product workflows',
    ],
    metrics: [
      { label: 'Manual follow-ups reduced', value: '-61%' },
      { label: 'Approval SLA', value: '<4 hrs' },
      { label: 'Operational clarity', value: 'High' },
    ],
    primaryCta: { label: 'Talk to Qode27', href: '/contact' },
    secondaryCta: { label: 'Get Pricing', href: '/pricing' },
  },
]

export const pricingPlans: PricingPlan[] = [
  {
    name: 'Starter',
    price: 'Custom',
    description: 'For smaller teams moving from spreadsheets to a dependable product workflow.',
    features: ['Core modules', 'Guided onboarding', 'Email support', 'Usage-based expansion'],
    cta: 'Talk to Sales',
  },
  {
    name: 'Growth',
    price: 'Custom',
    description: 'For scaling teams that want automation, reporting, and stronger operational control.',
    features: ['Workflow automation', 'Advanced analytics', 'Priority support', 'Multi-team permissions'],
    cta: 'Get Pricing',
    featured: true,
  },
  {
    name: 'Enterprise',
    price: 'Custom',
    description: 'For complex orgs that need tailored rollout, governance, and process design support.',
    features: ['Custom implementation', 'Executive onboarding', 'Dedicated success partner', 'Operational consulting'],
    cta: 'Book Strategy Call',
  },
]

export const contactMethods: ContactMethod[] = [
  {
    title: 'Email',
    value: 'qode27business@gmail.com',
    description: 'Best for demos, pricing conversations, and product discovery.',
    href: 'mailto:qode27business@gmail.com',
    icon: FiMail,
  },
  {
    title: 'Phone',
    value: '+91 7022556960',
    description: 'Reach Qode27 directly for implementation or procurement discussions.',
    href: 'tel:+917022556960',
    icon: FiArrowRight,
  },
  {
    title: 'Strategy Intro',
    value: 'Product-first rollout',
    description: 'We position each implementation around adoption, speed, and measurable process wins.',
    href: '/pricing',
    icon: FiBriefcase,
  },
]

export const trustPoints = [
  'Healthcare, finance, and operations-friendly workflows',
  'Fast adoption for non-technical teams',
  'Premium visual polish with practical admin UX',
  'Implementation support that stays grounded in real operations',
]

export const pricingNotes = [
  {
    icon: FiClock,
    title: 'Fast rollout',
    text: 'Scoped launches keep the first version narrow, useful, and ready for team adoption.',
  },
  {
    icon: FiCheckCircle,
    title: 'Clear fit',
    text: 'We recommend only the modules and workflows that make sense for your current stage.',
  },
  {
    icon: FiCreditCard,
    title: 'Practical pricing',
    text: 'Engagements are structured around value and rollout complexity, not bloated enterprise overhead.',
  },
]

export const footerLinks = navigation

export function getProductBySlug(slug?: string) {
  return products.find((product) => product.slug === slug)
}
