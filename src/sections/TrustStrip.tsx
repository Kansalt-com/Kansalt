import { motion as Motion } from 'framer-motion'
import Container from '../components/ui/Container'
import { trustLabels } from '../data/site'

export default function TrustStrip() {
  return (
    <section className="pb-6 sm:pb-10">
      <Container>
        <Motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{ duration: 0.6, ease: 'easeOut' }}
          className="rounded-2xl border border-neutral-200/80 bg-neutral-50/90 px-6 py-5 shadow-[0_12px_32px_rgba(11,11,11,0.04)]"
        >
          <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <p className="text-sm font-semibold uppercase tracking-[0.22em] text-neutral-500">
              Trusted by growing businesses
            </p>
            <div className="flex flex-wrap gap-3">
              {trustLabels.map((label) => (
                <div
                  key={label}
                  className="rounded-xl border border-neutral-200 bg-white px-4 py-2 text-sm font-medium text-neutral-700 hover:border-brand-200 hover:text-brand-700"
                >
                  {label}
                </div>
              ))}
            </div>
          </div>
        </Motion.div>
      </Container>
    </section>
  )
}
