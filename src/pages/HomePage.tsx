import { createElement } from 'react'
import { motion as Motion } from 'framer-motion'
import { FiArrowRight, FiCheckCircle, FiPlayCircle } from 'react-icons/fi'
import Button from '../components/ui/Button'
import Container from '../components/ui/Container'
import ProductCard from '../components/ui/ProductCard'
import Reveal from '../components/ui/Reveal'
import SectionHeader from '../components/ui/SectionHeader'
import { heroStats, platformHighlights, pricingPlans, products, trustPoints } from '../data/site'
import { stagger } from '../utils/motion'

function HeroVisual() {
  return (
    <Motion.div
      initial={{ opacity: 0, x: 28 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.45, ease: [0.22, 1, 0.36, 1], delay: 0.12 }}
      className="relative mx-auto w-full max-w-[35rem]"
    >
      <div className="absolute -left-4 top-14 h-28 w-28 rounded-full bg-[var(--color-accent)]/18 blur-3xl" aria-hidden="true" />
      <div className="absolute right-2 top-8 h-40 w-40 rounded-full bg-black/8 blur-3xl" aria-hidden="true" />

      <div className="glass-panel relative overflow-hidden rounded-[2rem] p-6">
        <div className="absolute inset-x-0 top-0 h-28 bg-[linear-gradient(90deg,rgba(19,178,191,0.18),rgba(255,255,255,0))]" />
        <div className="grid gap-4 lg:grid-cols-[1.2fr_0.8fr]">
          <div className="rounded-[1.5rem] bg-black p-6 text-white shadow-[0_28px_55px_rgba(15,23,42,0.22)]">
            <p className="text-xs uppercase tracking-[0.28em] text-white/60">Qode27 Command Center</p>
            <h2 className="mt-4 text-3xl font-semibold tracking-[-0.05em]">One operating layer for daily business flow.</h2>
            <div className="mt-6 grid gap-3">
              {[
                'Patient ops and billing',
                'Leave approvals and people data',
                'Automated internal handoffs',
              ].map((item) => (
                <div key={item} className="flex items-center justify-between rounded-2xl border border-white/8 bg-white/5 px-4 py-3">
                  <span className="text-sm text-white/82">{item}</span>
                  <span className="h-2.5 w-2.5 rounded-full bg-[var(--color-accent)]" />
                </div>
              ))}
            </div>
          </div>
          <div className="space-y-4">
            <div className="rounded-[1.5rem] border border-black/8 bg-white p-5">
              <p className="text-xs uppercase tracking-[0.24em] text-neutral-500">Adoption Score</p>
              <p className="mt-4 text-4xl font-semibold tracking-[-0.06em] text-black">94%</p>
              <p className="mt-2 text-sm leading-6 text-neutral-600">Simple enough for ops teams, polished enough for leadership buy-in.</p>
            </div>
            <div className="rounded-[1.5rem] border border-[var(--color-accent)]/18 bg-[var(--color-accent-soft)] p-5">
              <p className="text-xs uppercase tracking-[0.24em] text-[var(--color-accent-strong)]">Live Visibility</p>
              <p className="mt-3 text-base font-semibold text-black">KPIs, queues, and revenue signals in one glance.</p>
              <div className="mt-5 flex h-24 items-end gap-2">
                {[44, 66, 59, 82, 76].map((height) => (
                  <div
                    key={height}
                    className="w-full rounded-t-2xl bg-[linear-gradient(180deg,var(--color-accent)_0%,#04363a_100%)]"
                    style={{ height: `${height}%` }}
                  />
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </Motion.div>
  )
}

export default function HomePage() {
  return (
    <Motion.div initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -18 }} transition={{ duration: 0.35 }}>
      <section className="pt-8 sm:pt-10">
        <Container className="section-spacing pb-18 lg:pb-24">
          <div className="grid items-center gap-14 lg:grid-cols-[1.05fr_0.95fr]">
            <div className="max-w-2xl">
              <Motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.45, ease: [0.22, 1, 0.36, 1] }}
                className="inline-flex items-center gap-2 rounded-full border border-black/8 bg-white/80 px-4 py-2 text-xs font-semibold uppercase tracking-[0.28em] text-[var(--color-accent-strong)]"
              >
                <span className="h-2 w-2 rounded-full bg-[var(--color-accent)]" />
                Premium SaaS for operations-heavy teams
              </Motion.div>
              <h1 className="mt-7 font-display text-5xl font-bold leading-[0.95] tracking-[-0.06em] text-black sm:text-6xl lg:text-7xl">
                Run serious operations on software that feels product-grade from day one.
              </h1>
              <p className="mt-6 max-w-xl text-lg leading-8 text-neutral-600 sm:text-[1.14rem]">
                Qode27 turns admin-heavy workflows into premium SaaS experiences for healthcare, HR, and automation-first businesses that need speed, clarity, and adoption.
              </p>
              <div className="mt-9 flex flex-col gap-4 sm:flex-row sm:flex-wrap">
                <Button href="/hms/demo" className="sm:min-w-[11rem]">
                  View Demo
                  <FiPlayCircle />
                </Button>
                <Button href="/pricing" variant="secondary" className="sm:min-w-[11rem]">
                  Get Pricing
                  <FiArrowRight />
                </Button>
              </div>
              <div className="mt-8 flex flex-col gap-3 text-sm text-neutral-600 sm:flex-row sm:flex-wrap sm:items-center sm:gap-x-6">
                <span className="inline-flex items-center gap-2">
                  <FiCheckCircle className="text-[var(--color-accent-strong)]" />
                  No bloated enterprise UX
                </span>
                <span className="inline-flex items-center gap-2">
                  <FiCheckCircle className="text-[var(--color-accent-strong)]" />
                  Product-led implementation
                </span>
                <span className="inline-flex items-center gap-2">
                  <FiCheckCircle className="text-[var(--color-accent-strong)]" />
                  Built for real operational teams
                </span>
              </div>
              <div className="mt-10 grid gap-4 sm:grid-cols-3">
                {heroStats.map((stat) => (
                  <div key={stat.label} className="rounded-[1.5rem] border border-black/6 bg-white/76 p-5 shadow-[0_18px_32px_rgba(15,23,42,0.06)]">
                    <p className="text-3xl font-semibold tracking-[-0.06em] text-black">{stat.value}</p>
                    <p className="mt-2 text-sm leading-6 text-neutral-600">{stat.label}</p>
                  </div>
                ))}
              </div>
            </div>

            <HeroVisual />
          </div>
        </Container>
      </section>

      <section className="pb-10">
        <Container>
          <div className="grid gap-3 rounded-[2rem] border border-black/6 bg-white/84 p-6 shadow-[0_18px_40px_rgba(15,23,42,0.05)] lg:grid-cols-4">
            {trustPoints.map((point) => (
              <div key={point} className="rounded-[1.25rem] bg-[#f3f7f7] px-4 py-4 text-sm font-medium leading-6 text-neutral-700">
                {point}
              </div>
            ))}
          </div>
        </Container>
      </section>

      <section className="section-spacing">
        <Container>
          <SectionHeader
            eyebrow="Products"
            title="Product suites designed like modern SaaS, not stitched-together admin screens."
            description="Each Qode27 product is structured around adoption, performance, and clean workflows so teams can move faster without sacrificing control."
          />
          <Motion.div
            variants={stagger}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, amount: 0.16 }}
            className="mt-12 grid gap-6 lg:grid-cols-3"
          >
            {products.map((product) => (
              <Reveal key={product.slug}>
                <ProductCard product={product} />
              </Reveal>
            ))}
          </Motion.div>
        </Container>
      </section>

      <section className="section-spacing bg-[#f7faf9]">
        <Container>
          <SectionHeader
            eyebrow="Why Qode27"
            title="A product-first approach to business software transformation."
            description="We position each rollout around fewer clicks, faster onboarding, cleaner states, and premium UI patterns that leaders are proud to put in front of teams."
          />
          <div className="mt-12 grid gap-6 lg:grid-cols-3">
            {platformHighlights.map((item, index) => (
              <Reveal key={item.title} delay={index * 0.05}>
                <Motion.article
                  whileHover={{ y: -4 }}
                  transition={{ duration: 0.25 }}
                  className="rounded-[1.75rem] border border-black/6 bg-white p-7 shadow-[0_18px_36px_rgba(15,23,42,0.05)]"
                >
                  <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-[var(--color-accent-soft)] text-[var(--color-accent-strong)]">
                    {createElement(item.icon)}
                  </div>
                  <h3 className="mt-6 text-xl font-semibold text-black">{item.title}</h3>
                  <p className="mt-4 text-base leading-7 text-neutral-600">{item.text}</p>
                </Motion.article>
              </Reveal>
            ))}
          </div>
        </Container>
      </section>

      <section className="section-spacing">
        <Container>
          <SectionHeader
            eyebrow="Pricing"
            title="Flexible pricing for serious implementations."
            description="We keep pricing consultative so you can scope the right rollout, modules, and support level without paying for generic enterprise baggage."
          />
          <div className="mt-12 grid gap-6 lg:grid-cols-3">
            {pricingPlans.map((plan) => (
              <Reveal key={plan.name}>
                <Motion.article
                  whileHover={{ y: -5 }}
                  transition={{ duration: 0.25 }}
                  className={`rounded-[1.75rem] border p-7 ${
                    plan.featured
                      ? 'border-[var(--color-accent)]/30 bg-black text-white shadow-[0_24px_50px_rgba(19,178,191,0.18)]'
                      : 'border-black/6 bg-white shadow-[0_18px_36px_rgba(15,23,42,0.05)]'
                  }`}
                >
                  <p className={`text-xs font-semibold uppercase tracking-[0.24em] ${plan.featured ? 'text-[var(--color-accent)]' : 'text-neutral-500'}`}>
                    {plan.name}
                  </p>
                  <p className="mt-4 text-4xl font-semibold tracking-[-0.06em]">{plan.price}</p>
                  <p className={`mt-4 text-sm leading-7 ${plan.featured ? 'text-white/74' : 'text-neutral-600'}`}>{plan.description}</p>
                  <ul className={`mt-6 space-y-3 text-sm ${plan.featured ? 'text-white/84' : 'text-neutral-600'}`}>
                    {plan.features.map((feature) => (
                      <li key={feature} className="flex items-start gap-3">
                        <FiCheckCircle className={`mt-1 shrink-0 ${plan.featured ? 'text-[var(--color-accent)]' : 'text-[var(--color-accent-strong)]'}`} />
                        <span>{feature}</span>
                      </li>
                    ))}
                  </ul>
                  <Button href="/pricing" variant={plan.featured ? 'secondary' : 'primary'} className="mt-8 w-full justify-center">
                    {plan.cta}
                  </Button>
                </Motion.article>
              </Reveal>
            ))}
          </div>
        </Container>
      </section>
    </Motion.div>
  )
}
