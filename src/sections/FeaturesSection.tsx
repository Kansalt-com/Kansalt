import { createElement } from 'react'
import { motion as Motion } from 'framer-motion'
import Container from '../components/ui/Container'
import Reveal from '../components/ui/Reveal'
import SectionHeader from '../components/ui/SectionHeader'
import { features } from '../data/site'

export default function FeaturesSection() {
  return (
    <section className="brand-separator section-spacing">
      <Container>
        <SectionHeader
          eyebrow="Features"
          title="Everything business owners need to trust the system"
          description="The experience is designed to feel premium, but the real value is how quickly your team can use it, rely on it, and grow with it."
        />

        <div className="mt-12 grid gap-6 sm:grid-cols-2 xl:grid-cols-3">
          {features.map(({ icon, title, text }) => (
            <Reveal key={title}>
              <Motion.article whileHover={{ y: -4 }} transition={{ duration: 0.35, ease: 'easeOut' }} className="system-card">
                <div className="system-icon">{createElement(icon)}</div>
                <h3 className="mt-5 text-xl font-semibold text-black">{title}</h3>
                <p className="mt-3 text-base text-neutral-600">{text}</p>
              </Motion.article>
            </Reveal>
          ))}
        </div>
      </Container>
    </section>
  )
}
