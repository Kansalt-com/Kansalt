import { createElement } from 'react'
import { motion as Motion } from 'framer-motion'
import { contactMethods } from '../data/site'
import Button from '../components/ui/Button'
import Container from '../components/ui/Container'
import Reveal from '../components/ui/Reveal'

export default function ContactPage() {
  return (
    <Motion.div initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -18 }} transition={{ duration: 0.35 }}>
      <section className="section-spacing pt-12">
        <Container>
          <div className="mx-auto max-w-3xl text-center">
            <p className="inline-flex items-center gap-2 rounded-full border border-[var(--color-gold)]/18 bg-[#fffaf0] px-4 py-2 text-xs font-semibold uppercase tracking-[0.26em] text-[var(--color-accent-strong)]">
              <span className="h-2 w-2 rounded-full bg-[var(--color-accent)]" />
              Contact Qode27
            </p>
            <h1 className="mt-7 font-display text-5xl font-bold leading-[0.97] tracking-[-0.06em] text-black sm:text-6xl">
              Request a demo for the app your business needs next.
            </h1>
            <p className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-neutral-600">
              Reach Qode27 on WhatsApp, phone, or email to explore apps for HR, Healthcare, Finance, and Operations with a premium, SME-first rollout approach.
            </p>
          </div>

          <div className="mt-12 grid gap-4 md:grid-cols-3">
            {contactMethods.map((method) => {
              const Icon = method.icon

              return (
                <Reveal key={method.title}>
                  <a
                    href={method.href}
                    target={method.href.startsWith('https://') ? '_blank' : undefined}
                    rel={method.href.startsWith('https://') ? 'noreferrer' : undefined}
                    className="group rounded-[1.1rem] border border-[var(--color-gold)]/12 bg-white p-6 shadow-[0_16px_34px_rgba(11,11,11,0.05)] transition hover:-translate-y-1 hover:border-[var(--color-accent)]/40 hover:shadow-[0_20px_40px_rgba(212,175,55,0.14)]"
                  >
                    <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-[var(--color-accent-soft)] text-[var(--color-accent-strong)]">
                      <Icon />
                    </div>
                    <h2 className="mt-5 text-xl font-semibold text-black">{method.title}</h2>
                    <p className="mt-2 text-base font-medium text-neutral-800">{method.value}</p>
                    <p className="mt-3 text-sm leading-7 text-neutral-600">{method.description}</p>
                  </a>
                </Reveal>
              )
            })}
          </div>

          <div className="mt-8 grid gap-6 lg:grid-cols-[1.05fr_0.95fr]">
            <Reveal>
              <div className="rounded-[1.2rem] border border-[var(--color-gold)]/14 bg-black p-6 text-white shadow-[0_30px_60px_rgba(11,11,11,0.2)] sm:p-7">
                <div className="max-w-xl">
                  <p className="text-xs font-semibold uppercase tracking-[0.28em] text-[var(--color-accent)]">Request Demo</p>
                  <h2 className="mt-4 text-3xl font-semibold tracking-[-0.05em] sm:text-[2rem]">The fastest route to a demo is WhatsApp.</h2>
                  <p className="mt-4 text-sm leading-7 text-white/72">
                    Share your app interest, business type, and contact number. We’ll guide you to the right Qode27 product and arrange the demo flow from there.
                  </p>
                </div>

                <div className="mt-8 grid gap-4 sm:grid-cols-2">
                  {[
                    'Built for Indian Businesses',
                    'Fast Deployment (7–10 days)',
                    'Affordable SaaS Solutions',
                    'Premium app-store experience',
                  ].map((item) => (
                    <div key={item} className="rounded-[1rem] border border-white/10 bg-white/5 px-4 py-4 text-sm font-medium text-white/82">
                      {item}
                    </div>
                  ))}
                </div>

                <div className="mt-8 flex flex-col gap-3 sm:flex-row">
                  <a
                    href="https://wa.me/917022556960?text=Hello%20Qode27,%20I%20would%20like%20a%20demo"
                    target="_blank"
                    rel="noreferrer"
                    className="button-glow inline-flex min-h-12 items-center justify-center rounded-xl border border-[var(--color-accent)] bg-[var(--color-accent)] px-6 py-3 text-sm font-semibold text-black hover:-translate-y-0.5 hover:shadow-[0_18px_36px_rgba(212,175,55,0.26)]"
                  >
                    Request Demo
                  </a>
                  <Button href="tel:+917022556960" variant="ghost">
                    Call Qode27
                  </Button>
                </div>
              </div>
            </Reveal>

            <div className="grid gap-6">
              <Reveal>
                <div className="rounded-[1.2rem] border border-[var(--color-gold)]/12 bg-white p-6 shadow-[0_18px_36px_rgba(11,11,11,0.05)]">
                  <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[var(--color-accent-strong)]">Qode27 HQ</p>
                  <h2 className="mt-3 text-3xl font-semibold tracking-[-0.05em] text-black">Hyderabad, India</h2>
                  <p className="mt-4 text-sm leading-7 text-neutral-600">
                    Serving Indian SMEs with premium business software for healthcare, HR, finance, and operational teams.
                  </p>
                </div>
              </Reveal>

              <Reveal>
                <div className="rounded-[1.2rem] border border-[var(--color-gold)]/12 bg-[#fbf7eb] p-6">
                  <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[var(--color-accent-strong)]">What happens next</p>
                  <div className="mt-5 space-y-4">
                    {[
                      'We understand which app category fits your business best.',
                      'We arrange the right demo path for your team and workflow.',
                      'We discuss deployment timing, pricing, and rollout readiness.',
                    ].map((step) => (
                      <div key={step} className="flex items-start gap-3">
                        <div className="mt-1 h-2.5 w-2.5 rounded-full bg-[var(--color-accent)]" />
                        <p className="text-sm leading-7 text-neutral-600">{step}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </Reveal>

              <Reveal>
                <div className="rounded-[1.2rem] border border-[var(--color-gold)]/12 bg-white p-6 shadow-[0_18px_36px_rgba(11,11,11,0.05)]">
                  <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[var(--color-accent-strong)]">Email</p>
                  <p className="mt-3 text-lg font-semibold text-black">qode27business@gmail.com</p>
                  <p className="mt-3 text-sm leading-7 text-neutral-600">
                    Ideal for procurement notes, vendor onboarding requests, and detailed product requirement conversations.
                  </p>
                </div>
              </Reveal>
            </div>
          </div>
        </Container>
      </section>
    </Motion.div>
  )
}
