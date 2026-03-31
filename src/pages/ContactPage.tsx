import type { FormEvent } from 'react'
import { AnimatePresence, motion as Motion } from 'framer-motion'
import { useState } from 'react'
import {
  FiArrowRight,
  FiCheckCircle,
  FiClock,
  FiMail,
  FiMessageCircle,
  FiPhone,
  FiShield,
  FiZap,
} from 'react-icons/fi'
import Button from '../components/ui/Button'
import Container from '../components/ui/Container'
import Reveal from '../components/ui/Reveal'

type ContactFormValues = {
  name: string
  company: string
  email: string
  phone: string
  product: string
  message: string
}

type FormErrors = Partial<Record<keyof ContactFormValues, string>>

type GtagWindow = Window & {
  gtag?: (...args: unknown[]) => void
}

const initialValues: ContactFormValues = {
  name: '',
  company: '',
  email: '',
  phone: '',
  product: 'HMS by Qode27',
  message: '',
}

const contactChannels = [
  {
    title: 'WhatsApp',
    value: 'Chat with Qode27',
    description: 'Fastest path for warm leads who want a same-day response.',
    href: 'https://wa.me/917022556960?text=Hi%20Qode27%2C%20I%20want%20a%20free%20demo.',
    icon: FiMessageCircle,
  },
  {
    title: 'Phone',
    value: '+91 7022556960',
    description: 'Best for buyers who want immediate product and pricing clarity.',
    href: 'tel:+917022556960',
    icon: FiPhone,
  },
  {
    title: 'Email',
    value: 'qode27business@gmail.com',
    description: 'Ideal for detailed requirements, procurement, and follow-up.',
    href: 'mailto:qode27business@gmail.com',
    icon: FiMail,
  },
]

const trustSignals = [
  {
    title: 'Built for real operations',
    text: 'We design around day-to-day workflows your team already runs, not generic SaaS templates.',
    icon: FiZap,
  },
  {
    title: 'Fast team adoption',
    text: 'Clean UI and clear workflow states help non-technical teams get comfortable quickly.',
    icon: FiClock,
  },
  {
    title: 'Reliable rollout support',
    text: 'Qode27 works closely with your team to shape the product around measurable business outcomes.',
    icon: FiShield,
  },
]

function validate(values: ContactFormValues) {
  const errors: FormErrors = {}

  if (!values.name.trim()) {
    errors.name = 'Please enter your name.'
  }

  if (!values.company.trim()) {
    errors.company = 'Please enter your company name.'
  }

  if (!values.email.trim()) {
    errors.email = 'Please enter your work email.'
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(values.email)) {
    errors.email = 'Please enter a valid email address.'
  }

  if (!values.phone.trim()) {
    errors.phone = 'Please enter your phone or WhatsApp number.'
  } else if (values.phone.replace(/\D/g, '').length < 10) {
    errors.phone = 'Please enter a valid contact number.'
  }

  if (!values.message.trim()) {
    errors.message = 'Tell us what you want to improve.'
  } else if (values.message.trim().length < 20) {
    errors.message = 'Add a little more detail so we can tailor the demo.'
  }

  return errors
}

function FieldError({ error }: { error?: string }) {
  if (!error) {
    return null
  }

  return <p className="mt-2 text-sm font-medium text-[#cb3a31]">{error}</p>
}

function LoadingSpinner() {
  return <span className="h-4 w-4 animate-spin rounded-full border-2 border-white/35 border-t-white" aria-hidden="true" />
}

export default function ContactPage() {
  const [values, setValues] = useState<ContactFormValues>(initialValues)
  const [errors, setErrors] = useState<FormErrors>({})
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isSuccess, setIsSuccess] = useState(false)
  const [submitError, setSubmitError] = useState<string | null>(null)

  const formId = import.meta.env.VITE_FORMSPREE_FORM_ID
  const formspreeEndpoint = formId ? `https://formspree.io/f/${formId}` : null

  const setFieldValue = (field: keyof ContactFormValues, value: string) => {
    setValues((current) => ({ ...current, [field]: value }))
    setErrors((current) => ({ ...current, [field]: undefined }))
    setSubmitError(null)
  }

  const trackLeadEvent = () => {
    const analyticsWindow = window as GtagWindow

    analyticsWindow.gtag?.('event', 'generate_lead', {
      event_category: 'contact',
      event_label: values.product,
      value: 1,
    })
  }

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()

    const nextErrors = validate(values)
    setErrors(nextErrors)
    setSubmitError(null)

    if (Object.keys(nextErrors).length > 0) {
      return
    }

    if (!formspreeEndpoint) {
      setSubmitError('Form is not connected yet. Add VITE_FORMSPREE_FORM_ID to enable submissions.')
      return
    }

    setIsSubmitting(true)

    try {
      const response = await fetch(formspreeEndpoint, {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: values.name,
          company: values.company,
          email: values.email,
          phone: values.phone,
          product: values.product,
          message: values.message,
          source: 'qode27-contact-page',
        }),
      })

      const payload = (await response.json().catch(() => null)) as { errors?: { message?: string }[] } | null

      if (!response.ok) {
        const formError = payload?.errors?.[0]?.message ?? 'Something went wrong. Please try again or contact us on WhatsApp.'
        throw new Error(formError)
      }

      trackLeadEvent()
      setIsSuccess(true)
      setValues(initialValues)
      setErrors({})
    } catch (error) {
      setSubmitError(error instanceof Error ? error.message : 'Unable to submit the form right now.')
      setIsSuccess(false)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <Motion.div initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -18 }} transition={{ duration: 0.35 }}>
      <section className="section-spacing pt-12">
        <Container>
          <div className="mx-auto max-w-3xl text-center">
            <p className="inline-flex items-center gap-2 rounded-full border border-black/8 bg-white/82 px-4 py-2 text-xs font-semibold uppercase tracking-[0.26em] text-[var(--color-accent-strong)]">
              <span className="h-2 w-2 rounded-full bg-[var(--color-accent)]" />
              Book your Qode27 walkthrough
            </p>
            <h1 className="mt-7 font-display text-5xl font-bold leading-[0.97] tracking-[-0.06em] text-black sm:text-6xl">
              See how Qode27 can turn your workflow into a premium SaaS experience.
            </h1>
            <p className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-neutral-600">
              Book a free demo to explore your use case, see the product in action, and get a rollout recommendation built around your team, not a generic template.
            </p>
          </div>

          <div className="mt-12 grid gap-4 md:grid-cols-3">
            {contactChannels.map((channel) => {
              const Icon = channel.icon

              return (
                <Reveal key={channel.title}>
                  <a
                    href={channel.href}
                    target={channel.href.startsWith('https://') ? '_blank' : undefined}
                    rel={channel.href.startsWith('https://') ? 'noreferrer' : undefined}
                    className="group rounded-[1.6rem] border border-black/6 bg-white p-6 shadow-[0_16px_34px_rgba(15,23,42,0.05)] transition hover:-translate-y-1 hover:border-[var(--color-accent)]/30 hover:shadow-[0_20px_40px_rgba(19,178,191,0.12)]"
                  >
                    <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-[var(--color-accent-soft)] text-[var(--color-accent-strong)]">
                      <Icon />
                    </div>
                    <h2 className="mt-5 text-xl font-semibold text-black">{channel.title}</h2>
                    <p className="mt-2 text-base font-medium text-neutral-800">{channel.value}</p>
                    <p className="mt-3 text-sm leading-7 text-neutral-600">{channel.description}</p>
                  </a>
                </Reveal>
              )
            })}
          </div>

          <div className="mt-8 grid gap-6 lg:grid-cols-[1.05fr_0.95fr]">
            <Reveal>
              <div className="rounded-[2rem] border border-black/6 bg-black p-6 text-white shadow-[0_30px_60px_rgba(15,23,42,0.2)] sm:p-7">
                <div className="max-w-xl">
                  <p className="text-xs font-semibold uppercase tracking-[0.28em] text-[var(--color-accent)]">Free demo form</p>
                  <h2 className="mt-4 text-3xl font-semibold tracking-[-0.05em] sm:text-[2rem]">Tell us about your workflow and we’ll tailor the walkthrough.</h2>
                  <p className="mt-4 text-sm leading-7 text-white/72">
                    Buyers convert faster when the first conversation is relevant. Give us a little context and we’ll come prepared with the right product path.
                  </p>
                </div>

                <form className="mt-8 grid gap-4" noValidate onSubmit={handleSubmit}>
                  <div className="grid gap-4 sm:grid-cols-2">
                    <label className="space-y-2">
                      <span className="text-sm font-medium text-white/82">Full name</span>
                      <input
                        value={values.name}
                        onChange={(event) => setFieldValue('name', event.target.value)}
                        className="w-full rounded-xl border border-white/10 bg-white/6 px-4 py-3 text-sm text-white outline-none placeholder:text-white/34 focus:border-[var(--color-accent)]"
                        placeholder="Your name"
                        aria-invalid={Boolean(errors.name)}
                      />
                      <FieldError error={errors.name} />
                    </label>
                    <label className="space-y-2">
                      <span className="text-sm font-medium text-white/82">Company</span>
                      <input
                        value={values.company}
                        onChange={(event) => setFieldValue('company', event.target.value)}
                        className="w-full rounded-xl border border-white/10 bg-white/6 px-4 py-3 text-sm text-white outline-none placeholder:text-white/34 focus:border-[var(--color-accent)]"
                        placeholder="Company name"
                        aria-invalid={Boolean(errors.company)}
                      />
                      <FieldError error={errors.company} />
                    </label>
                  </div>

                  <div className="grid gap-4 sm:grid-cols-2">
                    <label className="space-y-2">
                      <span className="text-sm font-medium text-white/82">Work email</span>
                      <input
                        type="email"
                        value={values.email}
                        onChange={(event) => setFieldValue('email', event.target.value)}
                        className="w-full rounded-xl border border-white/10 bg-white/6 px-4 py-3 text-sm text-white outline-none placeholder:text-white/34 focus:border-[var(--color-accent)]"
                        placeholder="name@company.com"
                        aria-invalid={Boolean(errors.email)}
                      />
                      <FieldError error={errors.email} />
                    </label>
                    <label className="space-y-2">
                      <span className="text-sm font-medium text-white/82">Phone / WhatsApp</span>
                      <input
                        value={values.phone}
                        onChange={(event) => setFieldValue('phone', event.target.value)}
                        className="w-full rounded-xl border border-white/10 bg-white/6 px-4 py-3 text-sm text-white outline-none placeholder:text-white/34 focus:border-[var(--color-accent)]"
                        placeholder="+91 98765 43210"
                        aria-invalid={Boolean(errors.phone)}
                      />
                      <FieldError error={errors.phone} />
                    </label>
                  </div>

                  <label className="space-y-2">
                    <span className="text-sm font-medium text-white/82">Product interest</span>
                    <select
                      value={values.product}
                      onChange={(event) => setFieldValue('product', event.target.value)}
                      className="w-full rounded-xl border border-white/10 bg-white/6 px-4 py-3 text-sm text-white outline-none focus:border-[var(--color-accent)]"
                    >
                      <option className="text-black">HMS by Qode27</option>
                      <option className="text-black">HRMS by Qode27</option>
                      <option className="text-black">Automation Suite</option>
                    </select>
                  </label>

                  <label className="space-y-2">
                    <span className="text-sm font-medium text-white/82">What do you want to improve?</span>
                    <textarea
                      value={values.message}
                      onChange={(event) => setFieldValue('message', event.target.value)}
                      className="min-h-36 w-full rounded-xl border border-white/10 bg-white/6 px-4 py-3 text-sm text-white outline-none placeholder:text-white/34 focus:border-[var(--color-accent)]"
                      placeholder="Tell us about your current workflow, where the friction is, and what kind of demo would help you evaluate Qode27."
                      aria-invalid={Boolean(errors.message)}
                    />
                    <FieldError error={errors.message} />
                  </label>

                  {submitError ? <p className="text-sm font-medium text-[#ff8f87]">{submitError}</p> : null}

                  <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
                    <button
                      type="submit"
                      disabled={isSubmitting}
                      className="inline-flex min-h-12 items-center justify-center gap-2 rounded-xl border border-[var(--color-accent)] bg-[var(--color-accent)] px-6 py-3 text-sm font-semibold text-black transition hover:-translate-y-0.5 hover:bg-[#20c7d5] disabled:cursor-not-allowed disabled:opacity-70 sm:w-auto"
                    >
                      {isSubmitting ? <LoadingSpinner /> : null}
                      {isSubmitting ? 'Sending your request...' : 'Get Free Demo'}
                    </button>
                    <a
                      href="https://wa.me/917022556960?text=Hi%20Qode27%2C%20I%20want%20a%20free%20demo."
                      target="_blank"
                      rel="noreferrer"
                      className="inline-flex min-h-12 items-center justify-center gap-2 rounded-xl border border-white/12 bg-white/6 px-6 py-3 text-sm font-semibold text-white transition hover:-translate-y-0.5 hover:border-[var(--color-accent)] sm:w-auto"
                    >
                      WhatsApp Instead
                      <FiArrowRight />
                    </a>
                  </div>

                  <AnimatePresence>
                    {isSuccess ? (
                      <Motion.div
                        initial={{ opacity: 0, y: 14, scale: 0.98 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: -8 }}
                        transition={{ duration: 0.28, ease: 'easeOut' }}
                        className="rounded-[1.4rem] border border-[var(--color-accent)]/30 bg-[var(--color-accent)]/12 p-4"
                      >
                        <div className="flex items-start gap-3">
                          <div className="mt-0.5 flex h-10 w-10 items-center justify-center rounded-full bg-[var(--color-accent)] text-black">
                            <FiCheckCircle />
                          </div>
                          <div>
                            <p className="font-semibold text-white">Demo request received.</p>
                            <p className="mt-1 text-sm leading-6 text-white/74">
                              We’ll reach out shortly to schedule your free demo and discuss the best-fit product path.
                            </p>
                          </div>
                        </div>
                      </Motion.div>
                    ) : null}
                  </AnimatePresence>
                </form>
              </div>
            </Reveal>

            <div className="grid gap-6">
              <Reveal>
                <div className="rounded-[2rem] border border-black/6 bg-white p-6 shadow-[0_18px_36px_rgba(15,23,42,0.05)]">
                  <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[var(--color-accent-strong)]">Why choose Qode27</p>
                  <h2 className="mt-3 text-3xl font-semibold tracking-[-0.05em] text-black">A trusted product partner for operational teams.</h2>
                  <div className="mt-6 space-y-4">
                    {trustSignals.map((signal) => {
                      const Icon = signal.icon

                      return (
                        <div key={signal.title} className="rounded-[1.4rem] bg-[#f4f8f8] p-4">
                          <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-white text-[var(--color-accent-strong)] shadow-[0_10px_24px_rgba(15,23,42,0.05)]">
                            <Icon />
                          </div>
                          <h3 className="mt-4 text-lg font-semibold text-black">{signal.title}</h3>
                          <p className="mt-2 text-sm leading-7 text-neutral-600">{signal.text}</p>
                        </div>
                      )
                    })}
                  </div>
                </div>
              </Reveal>

              <Reveal>
                <div className="rounded-[2rem] border border-black/6 bg-[#f5f8f9] p-6 shadow-[0_18px_36px_rgba(15,23,42,0.04)]">
                  <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[var(--color-accent-strong)]">What happens next</p>
                  <div className="mt-5 space-y-4">
                    {[
                      'We review your workflow and identify the most relevant product path.',
                      'You get a focused demo tailored to your business use case.',
                      'We share rollout recommendations and pricing guidance after the call.',
                    ].map((step) => (
                      <div key={step} className="flex items-start gap-3">
                        <FiCheckCircle className="mt-1 shrink-0 text-[var(--color-accent-strong)]" />
                        <p className="text-sm leading-7 text-neutral-600">{step}</p>
                      </div>
                    ))}
                  </div>
                  <div className="mt-6 rounded-[1.4rem] bg-white p-4">
                    <p className="text-sm font-medium text-black">Prefer a direct channel?</p>
                    <p className="mt-2 text-sm leading-7 text-neutral-600">
                      Message us on WhatsApp or call directly if you want to shorten the sales cycle and move straight into a live conversation.
                    </p>
                  </div>
                </div>
              </Reveal>

              <Reveal>
                <div className="rounded-[2rem] border border-black/6 bg-white p-6 shadow-[0_18px_36px_rgba(15,23,42,0.05)]">
                  <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[var(--color-accent-strong)]">Need pricing now?</p>
                  <h2 className="mt-3 text-2xl font-semibold tracking-[-0.04em] text-black">Explore package direction before the demo.</h2>
                  <p className="mt-3 text-sm leading-7 text-neutral-600">
                    If your buying team wants budget clarity early, you can review the pricing page before or after booking the walkthrough.
                  </p>
                  <div className="mt-5">
                    <Button href="/pricing" variant="secondary">
                      View Pricing
                    </Button>
                  </div>
                </div>
              </Reveal>
            </div>
          </div>
        </Container>
      </section>
    </Motion.div>
  )
}
