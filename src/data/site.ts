import type { IconType } from 'react-icons'
import {
  FiActivity,
  FiArrowRight,
  FiBarChart2,
  FiBriefcase,
  FiCheckCircle,
  FiClock,
  FiCpu,
  FiCreditCard,
  FiFolder,
  FiHeart,
  FiLock,
  FiRefreshCw,
  FiShield,
  FiSliders,
  FiTrendingUp,
  FiUserCheck,
  FiUsers,
  FiZap,
} from 'react-icons/fi'

export type NavItem = {
  label: string
  href: string
}

export type ContentCard = {
  icon: IconType
  title: string
  text: string
}

export type Product = {
  icon: IconType
  title: string
  description: string
  highlights: string[]
}

export type PricingPlan = {
  name: string
  price: string
  cadence: string
  description: string
  features: string[]
  cta: string
  featured: boolean
}

export type Testimonial = {
  quote: string
  name: string
  role: string
}

export const navigation: NavItem[] = [
  { label: 'Home', href: '#home' },
  { label: 'Products', href: '#products' },
  { label: 'Solutions', href: '#solutions' },
  { label: 'Pricing', href: '#pricing' },
  { label: 'Contact', href: '#contact' },
]

export const trustLabels: string[] = ['Hospitals', 'CA Firms', 'SMEs', 'Clinics', 'Operations Teams']

export const products: Product[] = [
  {
    icon: FiHeart,
    title: 'Hospital Management System (SIMS)',
    description: 'Manage billing, patients, workflows, and reports from one system your team can learn quickly.',
    highlights: ['Patient records and admissions', 'Billing and insurance workflows', 'Real-time admin reporting'],
  },
  {
    icon: FiUsers,
    title: 'HRMS',
    description: 'Bring attendance, payroll, employee records, and approvals into one clear workflow.',
    highlights: ['Leave and attendance tracking', 'Payroll-ready employee data', 'Simple manager approvals'],
  },
  {
    icon: FiZap,
    title: 'Business Automation Tools',
    description: 'Reduce repetitive work with practical automations that keep operations moving without extra overhead.',
    highlights: ['Task and follow-up automation', 'Approval and reminder flows', 'Custom process dashboards'],
  },
]

export const industries: ContentCard[] = [
  {
    icon: FiActivity,
    title: 'Hospitals',
    text: 'Manage patients, billing, prescriptions, staff coordination, and operations in one place.',
  },
  {
    icon: FiFolder,
    title: 'CA Firms',
    text: 'Organize client work, documents, deadlines, and approvals with less manual follow-up.',
  },
  {
    icon: FiTrendingUp,
    title: 'SMEs',
    text: 'Replace scattered spreadsheets with clear systems for finance, people, and daily operations.',
  },
  {
    icon: FiBriefcase,
    title: 'Service Businesses',
    text: 'Track work, teams, billing, and customer requests with software built around your process.',
  },
]

export const features: ContentCard[] = [
  {
    icon: FiClock,
    title: 'Fast Setup',
    text: 'Launch quickly with a clear rollout process that keeps your business moving.',
  },
  {
    icon: FiShield,
    title: 'Secure Access',
    text: 'Protect business data with role-based visibility and dependable controls.',
  },
  {
    icon: FiSliders,
    title: 'Easy to Use',
    text: 'Clean screens and simple actions make adoption easier for non-technical teams.',
  },
  {
    icon: FiCpu,
    title: 'Scalable Systems',
    text: 'Start with what you need today and expand as operations become more complex.',
  },
  {
    icon: FiRefreshCw,
    title: 'Smart Automation',
    text: 'Remove repetitive work from approvals, follow-ups, reminders, and reporting.',
  },
  {
    icon: FiCreditCard,
    title: 'Affordable Growth',
    text: 'Business-friendly pricing keeps premium software within reach for growing teams.',
  },
]

export const differentiators: ContentCard[] = [
  {
    icon: FiCheckCircle,
    title: 'Built for real business workflows',
    text: 'We design around the day-to-day work your team already does, not generic software assumptions.',
  },
  {
    icon: FiUserCheck,
    title: 'Clean and simple user experience',
    text: 'Your staff should not need technical training just to complete routine work.',
  },
  {
    icon: FiArrowRight,
    title: 'Custom-fit where it matters',
    text: 'We keep the product streamlined while tailoring the parts that affect your operations most.',
  },
  {
    icon: FiBarChart2,
    title: 'Business-first visibility',
    text: 'Reports and dashboards focus on decisions, not noise, so owners and managers see what matters quickly.',
  },
  {
    icon: FiLock,
    title: 'Reliable foundations',
    text: 'We build for stability, clarity, and long-term usefulness rather than short-term complexity.',
  },
  {
    icon: FiHeart,
    title: 'Support mindset',
    text: 'Qode27 works like a partner that wants your systems to keep improving as your company grows.',
  },
]

export const pricingPlans: PricingPlan[] = [
  {
    name: 'Basic',
    price: '\u20B919k',
    cadence: '/month',
    description: 'A clean starting point for businesses moving from manual work to organized software.',
    features: ['Core workflows', 'Up to 10 team members', 'Email support', 'Basic reports'],
    cta: 'Get Started',
    featured: false,
  },
  {
    name: 'Pro',
    price: '\u20B949k',
    cadence: '/month',
    description: 'Ideal for growing teams that need automation, stronger visibility, and better coordination.',
    features: ['Advanced automations', 'Up to 50 team members', 'Priority support', 'Custom dashboards'],
    cta: 'Book Demo',
    featured: true,
  },
  {
    name: 'Enterprise',
    price: 'Custom',
    cadence: '',
    description: 'For larger or more complex operations that need tailored workflows, onboarding, and support.',
    features: ['Custom implementation', 'Unlimited users', 'Dedicated support', 'Process consulting'],
    cta: 'Talk to Sales',
    featured: false,
  },
]

export const testimonials: Testimonial[] = [
  {
    quote:
      'Qode27 helped us bring patient operations and billing into one clean workflow. Our team picked it up quickly, and day-to-day coordination became far easier.',
    name: 'Ritika Sharma',
    role: 'Hospital Administrator',
  },
  {
    quote:
      'We wanted software that felt practical, not complicated. The system gave our CA office better visibility without making the team change everything at once.',
    name: 'Naveen Patel',
    role: 'CA Firm Owner',
  },
  {
    quote:
      'The biggest difference was speed. Repetitive operational work became simpler, and we finally had a system that felt built for a growing business.',
    name: 'Aman Khurana',
    role: 'SME Founder',
  },
]

export const footerLinks: NavItem[] = [
  { label: 'Home', href: '#home' },
  { label: 'Products', href: '#products' },
  { label: 'Solutions', href: '#solutions' },
  { label: 'Pricing', href: '#pricing' },
  { label: 'Contact', href: '#contact' },
]
