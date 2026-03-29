import { createElement } from 'react'
import { motion as Motion } from 'framer-motion'
import Container from '../components/ui/Container'
import Reveal from '../components/ui/Reveal'
import SectionHeader from '../components/ui/SectionHeader'
import { industries } from '../data/site'

export default function SolutionsSection() {
  return (
    <section id="solutions" className="section-spacing bg-slate-50/70">
      <Container>
        <SectionHeader
          eyebrow="Solutions"
          title="Built for the way different businesses actually work"
          description="Every industry runs on its own routines, approvals, bottlenecks, and reporting needs. Qode27 fits the system around the business, not the other way around."
          align="center"
        />

        <div className="mt-12 grid gap-6 md:grid-cols-2">
          {industries.map(({ icon, title, text }) => (
            <Reveal key={title}>
              <Motion.article
                whileHover={{ y: -6 }}
                transition={{ duration: 0.25, ease: 'easeOut' }}
                className="card-surface flex h-full gap-5 rounded-[30px] p-7"
              >
                <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-slate-950 text-xl text-white">
                  {createElement(icon)}
                </div>
                <div>
                  <h3 className="text-2xl font-semibold tracking-[-0.04em] text-slate-950">{title}</h3>
                  <p className="mt-3 text-base leading-7 text-slate-600">{text}</p>
                </div>
              </Motion.article>
            </Reveal>
          ))}
        </div>
      </Container>
    </section>
  )
}
