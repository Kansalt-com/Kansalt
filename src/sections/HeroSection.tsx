import { motion as Motion } from 'framer-motion'
import { FiArrowRight, FiCheckCircle, FiPlayCircle } from 'react-icons/fi'
import BrandLogo from '../components/ui/BrandLogo'
import Button from '../components/ui/Button'
import Container from '../components/ui/Container'

function HeroVisual() {
  return (
    <Motion.div
      initial={{ opacity: 0, x: 28 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1], delay: 0.12 }}
      className="relative mx-auto w-full max-w-[34rem] lg:mr-0"
    >
      <div className="brand-orb absolute -left-8 top-16 h-32 w-32 rounded-full" aria-hidden="true" />
      <div className="absolute right-4 top-2 h-40 w-40 rounded-full bg-teal-500/15 blur-3xl" aria-hidden="true" />
      <div className="brand-circuit pointer-events-none absolute inset-0 opacity-60" aria-hidden="true" />
      <div className="pointer-events-none absolute -right-5 bottom-8 opacity-[0.12]" aria-hidden="true">
        <BrandLogo iconOnly className="h-24 w-24 blur-[0.3px]" />
      </div>

      <div className="card-surface gradient-border grid-pattern relative overflow-hidden rounded-2xl p-6">
        <div className="absolute inset-x-0 top-0 h-20 bg-gradient-to-r from-brand-500/10 via-transparent to-teal-500/10" />
        <div className="relative flex items-center justify-between rounded-2xl border border-neutral-200/80 bg-white/92 px-4 py-3">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.24em] text-neutral-500">Workflow Snapshot</p>
            <p className="mt-2 text-base font-semibold text-black">Operations moving without bottlenecks</p>
          </div>
          <div className="rounded-xl bg-brand-50 px-3 py-1 text-sm font-semibold text-brand-700">Live</div>
        </div>

        <div className="mt-5 grid gap-4 sm:grid-cols-[1.3fr_0.7fr]">
          <div className="rounded-2xl bg-black p-6 text-white shadow-[0_24px_50px_rgba(11,11,11,0.22)]">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs uppercase tracking-[0.22em] text-white/60">Automation Queue</p>
                <p className="mt-3 text-2xl font-semibold">27 active flows</p>
              </div>
              <div className="rounded-xl bg-white/10 px-3 py-1 text-sm">+18%</div>
            </div>
            <div className="mt-6 space-y-3">
              {['Invoice follow-ups', 'Admission approvals', 'Payroll reminders'].map((item) => (
                <div key={item} className="flex items-center justify-between rounded-2xl bg-white/6 px-4 py-3">
                  <span className="text-sm text-white/80">{item}</span>
                  <span className="h-2.5 w-2.5 rounded-full bg-teal-500" />
                </div>
              ))}
            </div>
          </div>

          <div className="space-y-4">
            <div className="rounded-2xl border border-neutral-200 bg-neutral-50 p-6">
              <p className="text-xs uppercase tracking-[0.22em] text-neutral-500">Team Adoption</p>
              <p className="mt-3 text-3xl font-semibold tracking-[-0.05em] text-black">94%</p>
              <p className="mt-2 max-w-[16rem] text-sm leading-6 text-neutral-600">Simple interfaces that teams can use with confidence.</p>
            </div>
            <div className="rounded-2xl border border-brand-100 bg-brand-50/70 p-6 shadow-[0_18px_40px_rgba(211,161,62,0.10)]">
              <p className="text-xs uppercase tracking-[0.22em] text-brand-700">Business Visibility</p>
              <p className="mt-3 text-base font-semibold text-black">Billing, operations, and reporting in one view</p>
              <div className="mt-4 h-24 rounded-2xl bg-[linear-gradient(180deg,rgba(211,161,62,0.18),rgba(45,184,182,0.04))] p-4">
                <div className="flex h-full items-end gap-2">
                  {[52, 68, 61, 79, 88].map((height) => (
                    <div
                      key={height}
                      className="w-full rounded-t-2xl bg-gradient-to-t from-brand-600 via-brand-400 to-teal-500"
                      style={{ height: `${height}%` }}
                    />
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Motion.div>
  )
}

export default function HeroSection() {
  return (
    <section id="home" className="relative overflow-hidden pt-6 sm:pt-8">
      <Container className="section-spacing pb-16 sm:pb-20 lg:pb-24">
        <div className="grid items-center gap-14 lg:grid-cols-[1.05fr_0.95fr] lg:gap-10">
          <Motion.div
            initial={{ opacity: 0, y: 32 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
            className="max-w-2xl"
          >
            <div className="inline-flex items-center gap-2 rounded-xl border border-brand-100 bg-white/82 px-4 py-2 text-xs font-semibold uppercase tracking-[0.24em] text-brand-700 backdrop-blur">
              <span className="h-2 w-2 rounded-full bg-teal-500" />
              Business software for real operations
            </div>

            <h1 className="mt-7 font-display text-5xl font-bold leading-tight tracking-[-0.05em] text-black sm:text-6xl lg:text-7xl">
              We Build Software That Grows Your Business
            </h1>

            <p className="mt-6 max-w-xl text-lg leading-8 text-neutral-600 sm:text-[1.18rem]">
              Simple, powerful business software and automation tools for modern companies.
            </p>

            <div className="mt-9 flex flex-col gap-4 sm:flex-row sm:flex-wrap">
              <Button href="#contact" className="sm:min-w-[10.5rem]">
                Get Demo
                <FiArrowRight />
              </Button>
              <Button href="#products" variant="secondary" className="sm:min-w-[10.5rem]">
                <FiPlayCircle />
                View Products
              </Button>
            </div>

            <div className="mt-8 flex flex-col gap-3 text-sm text-neutral-600 sm:flex-row sm:flex-wrap sm:items-center sm:gap-x-6">
              <span className="font-medium text-black">Built for hospitals, firms, and growing businesses</span>
              <span className="inline-flex items-center gap-2">
                <FiCheckCircle className="text-teal-500" />
                Fast setup
              </span>
              <span className="inline-flex items-center gap-2">
                <FiCheckCircle className="text-teal-500" />
                Business-first design
              </span>
            </div>
          </Motion.div>

          <HeroVisual />
        </div>
      </Container>
    </section>
  )
}
