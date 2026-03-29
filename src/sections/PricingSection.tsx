import { FiCheck } from 'react-icons/fi'
import { motion as Motion } from 'framer-motion'
import Button from '../components/ui/Button'
import Container from '../components/ui/Container'
import Reveal from '../components/ui/Reveal'
import SectionHeader from '../components/ui/SectionHeader'
import { pricingPlans } from '../data/site'

export default function PricingSection() {
  return (
    <section id="pricing" className="brand-separator section-spacing">
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
                whileHover={{ y: -4 }}
                transition={{ duration: 0.35, ease: 'easeOut' }}
                className={`relative flex h-full flex-col rounded-2xl border p-6 ${
                  plan.featured
                    ? 'border-brand-300 bg-black text-white shadow-[0_24px_80px_rgba(11,11,11,0.20)] ring-1 ring-brand-200/60'
                    : 'border-neutral-200/80 bg-white text-neutral-900 hover:border-brand-200/70 hover:shadow-[0_22px_56px_rgba(11,11,11,0.08)]'
                }`}
              >
                {plan.featured ? (
                  <div className="absolute right-6 top-6 rounded-xl border border-brand-300/50 bg-brand-500 px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em] text-black">
                    Recommended
                  </div>
                ) : null}
                <p className={`text-sm font-semibold uppercase tracking-[0.2em] ${plan.featured ? 'text-brand-200' : 'text-neutral-500'}`}>
                  {plan.name}
                </p>
                <div className="mt-5 inline-flex w-fit rounded-xl border px-3 py-2 text-xs font-semibold uppercase tracking-[0.18em]">
                  <span className={plan.featured ? 'text-brand-100' : 'text-neutral-600'}>Custom consultation</span>
                </div>
                <p className={`mt-5 text-sm leading-7 ${plan.featured ? 'text-white/75' : 'text-neutral-600'}`}>{plan.description}</p>
                <ul className="mt-8 space-y-4">
                  {plan.features.map((feature) => (
                    <li key={feature} className="flex items-start gap-3 text-sm leading-6">
                      <span
                        className={`mt-0.5 inline-flex h-5 w-5 items-center justify-center rounded-full ${
                          plan.featured ? 'bg-brand-500/16 text-brand-200' : 'bg-brand-50 text-brand-600'
                        }`}
                      >
                        <FiCheck className="text-xs" />
                      </span>
                      <span className={plan.featured ? 'text-white/85' : 'text-neutral-700'}>{feature}</span>
                    </li>
                  ))}
                </ul>
                <Button href="#contact" variant={plan.featured ? 'secondary' : 'primary'} className="mt-8 w-full justify-center">
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
