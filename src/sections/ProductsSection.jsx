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
              <Motion.article
                whileHover={{ y: -8 }}
                transition={{ duration: 0.25, ease: 'easeOut' }}
                className="gradient-border card-surface h-full rounded-[30px] p-7"
              >
                <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-brand-50 text-2xl text-brand-600">
                  {createElement(icon)}
                </div>
                <h3 className="mt-6 text-2xl font-semibold tracking-[-0.04em] text-slate-950">{title}</h3>
                <p className="mt-4 text-base leading-7 text-slate-600">{description}</p>
                <ul className="mt-6 space-y-3">
                  {highlights.map((item) => (
                    <li key={item} className="flex items-start gap-3 text-sm leading-6 text-slate-600">
                      <span className="mt-1 inline-flex h-5 w-5 items-center justify-center rounded-full bg-brand-50 text-brand-600">
                        <FiCheck className="text-xs" />
                      </span>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
                <a
                  href="#contact"
                  className="mt-8 inline-flex items-center gap-2 text-sm font-semibold text-slate-950 hover:gap-3 hover:text-brand-600"
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
