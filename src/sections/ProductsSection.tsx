import { createElement } from 'react'
import { motion as Motion } from 'framer-motion'
import { FiArrowRight, FiCheck } from 'react-icons/fi'
import Reveal from '../components/ui/Reveal'
import SectionHeader from '../components/ui/SectionHeader'
import Container from '../components/ui/Container'
import { products } from '../data/site'
import { stagger } from '../utils/motion'

export default function ProductsSection() {
  return (
    <section id="products" className="section-spacing">
      <Container>
        <SectionHeader
          eyebrow="Products"
          title="Practical products for businesses that need clarity and control"
          description="Qode27 products are designed to remove friction from day-to-day work so your team can operate with more confidence and less manual effort."
        />

        <Motion.div
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.2 }}
          className="mt-12 grid gap-6 lg:grid-cols-3"
        >
          {products.map(({ icon, title, description, highlights }) => (
            <Reveal key={title}>
              <Motion.article whileHover={{ y: -4 }} transition={{ duration: 0.35, ease: 'easeOut' }} className="gradient-border system-card flex h-full flex-col">
                <div className="system-icon">
                  {createElement(icon)}
                </div>
                <h3 className="mt-6 text-xl font-semibold text-black">{title}</h3>
                <p className="mt-4 text-base leading-7 text-neutral-600">{description}</p>
                <ul className="mt-6 space-y-3">
                  {highlights.map((item) => (
                    <li key={item} className="flex items-start gap-3 text-sm leading-6 text-neutral-600">
                      <span className="mt-1 inline-flex h-5 w-5 items-center justify-center rounded-full bg-brand-50 text-brand-700">
                        <FiCheck className="text-xs" />
                      </span>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
                <a
                  href="#contact"
                  className="mt-auto inline-flex items-center gap-2 pt-8 text-sm font-semibold text-black hover:gap-3 hover:text-brand-700"
                >
                  View Demo
                  <FiArrowRight />
                </a>
              </Motion.article>
            </Reveal>
          ))}
        </Motion.div>
      </Container>
    </section>
  )
}
