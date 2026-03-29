import { motion as Motion } from 'framer-motion'
import Container from '../components/ui/Container'
import Reveal from '../components/ui/Reveal'
import SectionHeader from '../components/ui/SectionHeader'
import { testimonials } from '../data/site'

export default function TestimonialsSection() {
  return (
    <section className="section-spacing bg-slate-50/70">
      <Container>
        <SectionHeader
          eyebrow="Testimonials"
          title="Trusted by teams that want software to feel practical and premium"
          description="These are sample client stories, written to reflect the kind of operational value Qode27 is built to deliver."
          align="center"
        />

        <div className="mt-12 grid gap-6 lg:grid-cols-3">
          {testimonials.map((item) => (
            <Reveal key={item.name}>
              <Motion.blockquote
                whileHover={{ y: -6 }}
                transition={{ duration: 0.25, ease: 'easeOut' }}
                className="card-surface h-full rounded-[30px] p-7"
              >
                <p className="text-lg leading-8 text-slate-700">“{item.quote}”</p>
                <footer className="mt-8 border-t border-slate-200 pt-5">
                  <p className="font-semibold text-slate-950">{item.name}</p>
                  <p className="mt-1 text-sm text-slate-500">{item.role}</p>
                </footer>
              </Motion.blockquote>
            </Reveal>
          ))}
        </div>
      </Container>
    </section>
  )
}
