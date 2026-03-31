import { createElement } from 'react'
import { motion as Motion } from 'framer-motion'
import { FiCheckCircle } from 'react-icons/fi'
import Button from '../components/ui/Button'
import Container from '../components/ui/Container'
import Reveal from '../components/ui/Reveal'
import SectionHeader from '../components/ui/SectionHeader'
import { pricingNotes, pricingPlans } from '../data/site'

export default function PricingPage() {
  return (
    <Motion.div initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -18 }} transition={{ duration: 0.35 }}>
      <section className="section-spacing pt-12">
        <Container>
          <SectionHeader
            eyebrow="Pricing"
            title="Premium app-store pricing built for SME decision-making."
            description="Qode27 pricing is scoped around the applications, rollout support, and deployment pace your business actually needs."
            align="center"
          />
          <div className="mt-12 grid gap-6 lg:grid-cols-3">
            {pricingPlans.map((plan) => (
              <Reveal key={plan.name}>
                <Motion.article
                  whileHover={{ y: -5 }}
                  transition={{ duration: 0.25 }}
                  className={`rounded-[1.8rem] border p-7 ${
                    plan.featured
                      ? 'border-[var(--color-accent)]/26 bg-black text-white shadow-[0_24px_54px_rgba(19,178,191,0.18)]'
                      : 'border-black/6 bg-white shadow-[0_18px_38px_rgba(15,23,42,0.05)]'
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

          <div className="mt-14 grid gap-6 lg:grid-cols-3">
            {pricingNotes.map((note) => (
              <Reveal key={note.title}>
                <article className="rounded-[1.75rem] border border-black/6 bg-[#f6f8f8] p-6">
                  <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-white text-[var(--color-accent-strong)] shadow-[0_10px_24px_rgba(15,23,42,0.05)]">
                    {createElement(note.icon)}
                  </div>
                  <h3 className="mt-5 text-xl font-semibold text-black">{note.title}</h3>
                  <p className="mt-3 text-sm leading-7 text-neutral-600">{note.text}</p>
                </article>
              </Reveal>
            ))}
          </div>
        </Container>
      </section>
    </Motion.div>
  )
}
