import { createElement } from 'react'
import { motion as Motion } from 'framer-motion'
import { FiArrowRight, FiCheckCircle } from 'react-icons/fi'
import { apps } from '../config/apps'
import Button from '../components/ui/Button'
import Container from '../components/ui/Container'
import ProductCard from '../components/ui/ProductCard'
import RequestDemoButton from '../components/ui/RequestDemoButton'
import Reveal from '../components/ui/Reveal'
import SectionHeader from '../components/ui/SectionHeader'
import { categories, heroStats, platformHighlights, pricingPlans, products, trustPoints } from '../data/site'
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
      <div className="absolute right-2 top-8 h-40 w-40 rounded-full bg-[var(--color-gold)]/14 blur-3xl" aria-hidden="true" />

      <div className="glass-panel relative overflow-hidden rounded-[1.5rem] p-6">
        <div className="absolute inset-x-0 top-0 h-28 bg-[linear-gradient(90deg,rgba(212,175,55,0.16),rgba(255,255,255,0))]" />
        <div className="grid gap-4 lg:grid-cols-[1.15fr_0.85fr]">
          <div className="rounded-[1.3rem] bg-black p-6 text-white shadow-[0_28px_55px_rgba(11,11,11,0.22)]">
            <p className="text-xs uppercase tracking-[0.28em] text-white/60">Qode27 App Store</p>
            <h2 className="mt-4 text-3xl font-semibold tracking-[-0.05em]">All your business software in one place.</h2>
            <div className="mt-6 grid gap-3">
              {['Healthcare apps', 'Business and HR apps', 'Operations and automation apps'].map((item) => (
                <div key={item} className="flex items-center justify-between rounded-2xl border border-white/8 bg-white/5 px-4 py-3">
                  <span className="text-sm text-white/82">{item}</span>
                  <span className="h-2.5 w-2.5 rounded-full bg-[var(--color-accent)]" />
                </div>
              ))}
            </div>
          </div>
          <div className="space-y-4">
            <div className="rounded-[1.3rem] border border-[var(--color-gold)]/18 bg-[linear-gradient(135deg,rgba(212,175,55,0.18),rgba(255,255,255,0.85))] p-5">
              <p className="text-xs uppercase tracking-[0.24em] text-[var(--color-accent-strong)]">Marketplace Fit</p>
              <p className="mt-4 text-4xl font-semibold tracking-[-0.06em] text-black">SME-first</p>
              <p className="mt-2 text-sm leading-6 text-neutral-700">Curated business applications with premium UI and fast rollout.</p>
            </div>
            <div className="rounded-[1.3rem] border border-black/8 bg-white p-5">
              <p className="text-xs uppercase tracking-[0.24em] text-neutral-500">Coverage</p>
              <div className="mt-4 space-y-3">
                {categories.map((category) => (
                  <div key={category.key} className="flex items-center justify-between rounded-2xl bg-[#faf7ee] px-4 py-3 text-sm font-medium text-neutral-700">
                    <span>{category.key}</span>
                    <span className="text-[var(--color-accent-strong)]">Active</span>
                  </div>
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
                className="inline-flex items-center gap-2 rounded-full border border-[var(--color-gold)]/22 bg-[#fffaf0] px-4 py-2 text-xs font-semibold uppercase tracking-[0.28em] text-[var(--color-accent-strong)]"
              >
                <span className="h-2 w-2 rounded-full bg-[var(--color-accent)]" />
                Qode27 - Business Software App Store for SMEs
              </Motion.div>
              <h1 className="mt-7 font-display text-5xl font-bold leading-[0.95] tracking-[-0.06em] text-black sm:text-6xl lg:text-7xl">
                Your Business, Powered by Smart Software
              </h1>
              <p className="mt-6 max-w-xl text-lg leading-8 text-neutral-600 sm:text-[1.14rem]">
                Explore ready-to-use applications for healthcare, HR, finance, and more, all packaged under one premium Qode27 marketplace experience.
              </p>
              <div className="mt-9 flex flex-col gap-4 sm:flex-row sm:flex-wrap">
                <Button href="/products" className="sm:min-w-[11rem]">
                  View Products
                  <FiArrowRight />
                </Button>
                <RequestDemoButton app={apps.hms} label="Request Demo" variant="secondary" className="sm:min-w-[11rem]" />
              </div>
              <div className="mt-8 flex flex-col gap-3 text-sm text-neutral-600 sm:flex-row sm:flex-wrap sm:items-center sm:gap-x-6">
                <span className="inline-flex items-center gap-2">
                  <FiCheckCircle className="text-[var(--color-accent-strong)]" />
                  From HR to Hospital - we've got you covered
                </span>
                <span className="inline-flex items-center gap-2">
                  <FiCheckCircle className="text-[var(--color-accent-strong)]" />
                  Premium SaaS with luxury feel
                </span>
                <span className="inline-flex items-center gap-2">
                  <FiCheckCircle className="text-[var(--color-accent-strong)]" />
                  Demo available on request
                </span>
              </div>
              <div className="mt-10 grid gap-4 sm:grid-cols-3">
                {heroStats.map((stat) => (
                  <div key={stat.label} className="rounded-[1rem] border border-[var(--color-gold)]/14 bg-white/90 p-5 shadow-[0_18px_32px_rgba(11,11,11,0.06)]">
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
          <div className="grid gap-3 rounded-[1.5rem] border border-[var(--color-gold)]/14 bg-white/88 p-6 shadow-[0_18px_40px_rgba(11,11,11,0.05)] lg:grid-cols-4">
            {trustPoints.map((point) => (
              <div key={point} className="rounded-[1rem] bg-[#fbf7eb] px-4 py-4 text-sm font-medium leading-6 text-neutral-700">
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
            title="A premium app store for everyday business applications."
            description="Browse Qode27 applications by category and request demos for the products that match your workflow, business model, and deployment needs."
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

      <section className="section-spacing bg-[#f8f5ec]">
        <Container>
          <SectionHeader
            eyebrow="Trust"
            title="Designed to help Indian businesses adopt software with confidence."
            description="Qode27 blends app-store clarity, premium design, and practical implementation so SMEs can modernize without buying into heavyweight enterprise complexity."
          />
          <div className="mt-12 grid gap-6 lg:grid-cols-3">
            {platformHighlights.map((item, index) => (
              <Reveal key={item.title} delay={index * 0.05}>
                <Motion.article
                  whileHover={{ y: -4 }}
                  transition={{ duration: 0.25 }}
                  className="rounded-[1.1rem] border border-[var(--color-gold)]/14 bg-white p-7 shadow-[0_18px_36px_rgba(11,11,11,0.05)]"
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
            eyebrow="Plans"
            title="App-store style packaging for businesses that want clarity before they commit."
            description="Choose the right level of rollout support, then request a demo to see which apps fit your workflows best."
          />
          <div className="mt-12 grid gap-6 lg:grid-cols-3">
            {pricingPlans.map((plan) => (
              <Reveal key={plan.name}>
                <Motion.article
                  whileHover={{ y: -5 }}
                  transition={{ duration: 0.25 }}
                  className={`rounded-[1.1rem] border p-7 ${
                    plan.featured
                      ? 'border-[var(--color-gold)]/26 bg-black text-white shadow-[0_24px_50px_rgba(212,175,55,0.18)]'
                      : 'border-[var(--color-gold)]/12 bg-white shadow-[0_18px_36px_rgba(11,11,11,0.05)]'
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
                  <Button href="/contact" variant={plan.featured ? 'secondary' : 'primary'} className="mt-8 w-full justify-center">
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
