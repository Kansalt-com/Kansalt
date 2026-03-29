import { createElement } from 'react'
import { motion as Motion } from 'framer-motion'
import Container from '../components/ui/Container'
import Reveal from '../components/ui/Reveal'
import SectionHeader from '../components/ui/SectionHeader'
import { differentiators } from '../data/site'

export default function WhyQodeSection() {
  return (
    <section className="section-spacing bg-[linear-gradient(180deg,#ffffff_0%,#f8fbff_100%)]">
      <Container>
        <div className="grid gap-12 lg:grid-cols-[0.9fr_1.1fr] lg:items-start">
          <SectionHeader
            eyebrow="Why Qode27"
            title="A better fit than generic software vendors"
            description="Businesses do not need more complexity. They need software that feels clear, dependable, and aligned with how teams already operate."
          />

          <div className="grid gap-5 sm:grid-cols-2">
            {differentiators.map(({ icon, title, text }) => (
              <Reveal key={title}>
                <Motion.article
                  whileHover={{ y: -5 }}
                  transition={{ duration: 0.25, ease: 'easeOut' }}
                  className="rounded-[28px] border border-slate-200/80 bg-white p-6 shadow-[0_14px_40px_rgba(15,23,42,0.05)]"
                >
                  <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-slate-950 text-white">
                    {createElement(icon)}
                  </div>
                  <h3 className="mt-5 text-lg font-semibold text-slate-950">{title}</h3>
                  <p className="mt-3 text-sm leading-7 text-slate-600">{text}</p>
                </Motion.article>
              </Reveal>
            ))}
          </div>
        </div>
      </Container>
    </section>
  )
}
