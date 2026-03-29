import { FiCheck } from 'react-icons/fi'
import { motion as Motion } from 'framer-motion'
import Button from '../components/ui/Button'
import Container from '../components/ui/Container'
import Reveal from '../components/ui/Reveal'
import SectionHeader from '../components/ui/SectionHeader'
import { pricingPlans } from '../data/site'

export default function PricingSection() {
  return (
    <section id="pricing" className="section-spacing">
      <Container>
        <SectionHeader
          eyebrow="Pricing"
          title="Straightforward plans for businesses at different stages"
          description="Choose a plan that matches your current operations and expand as your systems, team, and automation needs grow."
          align="center"
        />

        <div className="mt-12 grid gap-6 xl:grid-cols-3">
          {pricingPlans.map((plan) => (
            <Reveal key={plan.name}>
              <Motion.article
                whileHover={{ y: -8 }}
                transition={{ duration: 0.25, ease: 'easeOut' }}
                className={`relative h-full rounded-[30px] border p-7 ${
                  plan.featured
                    ? 'border-brand-200 bg-slate-950 text-white shadow-[0_24px_80px_rgba(15,23,42,0.18)]'
                    : 'border-slate-200/80 bg-white text-slate-900'
                }`}
              >
                {plan.featured ? (
                  <div className="absolute right-6 top-6 rounded-full bg-brand-500 px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em] text-white">
                    Recommended
                  </div>
                ) : null}
                <p className={`text-sm font-semibold uppercase tracking-[0.2em] ${plan.featured ? 'text-brand-200' : 'text-slate-500'}`}>
                  {plan.name}
                </p>
                <div className="mt-5 flex items-end gap-2">
                  <span className="font-display text-5xl font-semibold tracking-[-0.06em]">{plan.price}</span>
                  <span className={`pb-1 text-sm ${plan.featured ? 'text-white/70' : 'text-slate-500'}`}>{plan.cadence}</span>
                </div>
                <p className={`mt-5 text-sm leading-7 ${plan.featured ? 'text-white/75' : 'text-slate-600'}`}>{plan.description}</p>
                <ul className="mt-8 space-y-4">
                  {plan.features.map((feature) => (
                    <li key={feature} className="flex items-start gap-3 text-sm leading-6">
                      <span
                        className={`mt-0.5 inline-flex h-5 w-5 items-center justify-center rounded-full ${
                          plan.featured ? 'bg-white/12 text-white' : 'bg-brand-50 text-brand-600'
                        }`}
                      >
                        <FiCheck className="text-xs" />
                      </span>
                      <span className={plan.featured ? 'text-white/85' : 'text-slate-700'}>{feature}</span>
                    </li>
                  ))}
                </ul>
                <Button
                  href="#contact"
                  variant={plan.featured ? 'ghost' : 'primary'}
                  className="mt-8 w-full justify-center"
                >
                  {plan.cta}
                </Button>
              </Motion.article>
            </Reveal>
          ))}
        </div>
      </Container>
    </section>
  )
}
