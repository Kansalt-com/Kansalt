import { createElement } from 'react'
import { motion as Motion } from 'framer-motion'
import { FiCheckCircle } from 'react-icons/fi'
import { Navigate, useParams } from 'react-router-dom'
import { getAppByProductSlug } from '../config/apps'
import Button from '../components/ui/Button'
import Container from '../components/ui/Container'
import RequestDemoButton from '../components/ui/RequestDemoButton'
import Reveal from '../components/ui/Reveal'
import { getProductBySlug } from '../data/site'

export default function ProductDetailPage() {
  const { slug } = useParams()
  const product = getProductBySlug(slug)
  const app = getAppByProductSlug(slug)

  if (!product) {
    return <Navigate to="/products" replace />
  }

  return (
    <Motion.div initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -18 }} transition={{ duration: 0.35 }}>
      <section className="section-spacing pt-12">
        <Container>
          <div className="grid gap-10 lg:grid-cols-[1.05fr_0.95fr]">
            <div className="max-w-2xl">
              <div className="inline-flex items-center gap-3 rounded-full border border-[var(--color-gold)]/18 bg-[#fffaf0] px-4 py-2 text-xs font-semibold uppercase tracking-[0.26em] text-[var(--color-accent-strong)]">
                <span className="flex h-8 w-8 items-center justify-center rounded-full bg-[var(--color-accent-soft)] text-base">
                  {createElement(product.icon)}
                </span>
                {product.category}
              </div>
              <h1 className="mt-7 font-display text-5xl font-bold leading-[0.98] tracking-[-0.06em] text-black sm:text-6xl">
                {product.name}
              </h1>
              <p className="mt-6 text-lg leading-8 text-neutral-600">{product.description}</p>
              <div className="mt-9 flex flex-col gap-4 sm:flex-row">
                {app ? <RequestDemoButton app={app} label="Request Demo on WhatsApp" /> : null}
                <Button href="/products" variant="secondary">
                  View Products
                </Button>
              </div>
            </div>

            <div className="grid gap-4">
              {product.metrics.map((metric) => (
                <div key={metric.label} className="rounded-[1.1rem] border border-[var(--color-gold)]/12 bg-white p-6 shadow-[0_18px_36px_rgba(11,11,11,0.05)]">
                  <p className="text-xs uppercase tracking-[0.24em] text-neutral-500">{metric.label}</p>
                  <p className="mt-4 text-4xl font-semibold tracking-[-0.06em] text-black">{metric.value}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="mt-14 grid gap-6 lg:grid-cols-2">
            <Reveal>
              <div className="rounded-[1.2rem] border border-[var(--color-gold)]/12 bg-white p-8 shadow-[0_20px_42px_rgba(11,11,11,0.05)]">
                <h2 className="text-2xl font-semibold text-black">Features</h2>
                <ul className="mt-6 space-y-4">
                  {product.features.map((feature) => (
                    <li key={feature} className="flex items-start gap-3 text-base leading-7 text-neutral-600">
                      <FiCheckCircle className="mt-1 shrink-0 text-[var(--color-accent-strong)]" />
                      <span>{feature}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </Reveal>
            <Reveal>
              <div className="rounded-[1.2rem] border border-[var(--color-gold)]/14 bg-black p-8 text-white shadow-[0_28px_55px_rgba(11,11,11,0.22)]">
                <h2 className="text-2xl font-semibold">Benefits</h2>
                <ul className="mt-6 space-y-4">
                  {product.benefits.map((benefit) => (
                    <li key={benefit} className="flex items-start gap-3 text-base leading-7 text-white/82">
                      <FiCheckCircle className="mt-1 shrink-0 text-[var(--color-accent)]" />
                      <span>{benefit}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </Reveal>
          </div>

          <div className="mt-6 grid gap-6 lg:grid-cols-2">
            <Reveal>
              <div className="rounded-[1.2rem] border border-[var(--color-gold)]/12 bg-[#fbf7eb] p-8">
                <h2 className="text-2xl font-semibold text-black">Overview</h2>
                <p className="mt-4 text-base leading-8 text-neutral-600">
                  {product.name} sits inside the Qode27 App Store as a premium packaged business application for teams that want faster adoption, cleaner workflows, and dependable rollout support.
                </p>
              </div>
            </Reveal>
            <Reveal>
              <div className="rounded-[1.2rem] border border-[var(--color-gold)]/12 bg-white p-8 shadow-[0_20px_42px_rgba(11,11,11,0.05)]">
                <h2 className="text-2xl font-semibold text-black">Screenshots</h2>
                <div className="mt-6 space-y-3">
                  {product.screenshots.map((item) => (
                    <div key={item} className="rounded-[1rem] border border-[var(--color-gold)]/12 bg-[#fffaf0] px-4 py-4 text-sm font-medium text-neutral-700">
                      {item}
                    </div>
                  ))}
                </div>
              </div>
            </Reveal>
          </div>
        </Container>
      </section>
    </Motion.div>
  )
}
