import { createElement } from 'react'
import { motion as Motion } from 'framer-motion'
import Container from '../components/ui/Container'
import Reveal from '../components/ui/Reveal'
import SectionHeader from '../components/ui/SectionHeader'
import { differentiators } from '../data/site'

export default function WhyQodeSection() {
  return (
    <section className="brand-separator section-spacing bg-neutral-50/60">
      <Container>
        <div className="grid gap-12 lg:grid-cols-[0.9fr_1.1fr] lg:items-start">
          <SectionHeader
            eyebrow="Why Qode27"
            title="A better fit than generic software vendors"
            description="Businesses do not need more complexity. They need software that feels clear, dependable, and aligned with how teams already operate."
          />

          <div className="grid gap-6 sm:grid-cols-2">
            {differentiators.map(({ icon, title, text }) => (
              <Reveal key={title}>
                <Motion.article whileHover={{ y: -4 }} transition={{ duration: 0.35, ease: 'easeOut' }} className="system-card">
                  <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-black text-brand-200">
                    {createElement(icon)}
                  </div>
                  <h3 className="mt-5 text-xl font-semibold text-black">{title}</h3>
                  <p className="mt-3 text-base text-neutral-600">{text}</p>
                </Motion.article>
              </Reveal>
            ))}
          </div>
        </div>
      </Container>
    </section>
  )
}
