import { AnimatePresence, motion as Motion } from 'framer-motion'
import { useMemo, useState, type FormEvent } from 'react'
import { FiArrowRight, FiCheckCircle, FiX } from 'react-icons/fi'
import type { DemoAppConfig } from '../../config/apps'

type LeadCaptureModalProps = {
  app: DemoAppConfig
  open: boolean
  onClose: () => void
}

type FormValues = {
  name: string
  businessType: string
  phone: string
}

type FormErrors = Partial<Record<keyof FormValues, string>>

const initialValues: FormValues = {
  name: '',
  businessType: '',
  phone: '',
}

function validate(values: FormValues) {
  const errors: FormErrors = {}

  if (!values.name.trim()) {
    errors.name = 'Please enter your name.'
  }

  if (!values.businessType.trim()) {
    errors.businessType = 'Please enter your business type.'
  }

  if (!values.phone.trim()) {
    errors.phone = 'Please enter your phone number.'
  } else if (values.phone.replace(/\D/g, '').length < 10) {
    errors.phone = 'Please enter a valid phone number.'
  }

  return errors
}

export default function LeadCaptureModal({ app, open, onClose }: LeadCaptureModalProps) {
  const [values, setValues] = useState<FormValues>(initialValues)
  const [errors, setErrors] = useState<FormErrors>({})
  const [isSubmitting, setIsSubmitting] = useState(false)

  const whatsappUrl = useMemo(() => {
    const suffix = `\nName: ${values.name.trim() || '-'}\nBusiness Type: ${values.businessType.trim() || '-'}\nPhone: ${values.phone.trim() || '-'}`
    return `https://wa.me/917022556960?text=${encodeURIComponent(`${app.whatsappText}${suffix}`)}`
  }, [app.whatsappText, values])

  const setFieldValue = (field: keyof FormValues, value: string) => {
    setValues((current) => ({ ...current, [field]: value }))
    setErrors((current) => ({ ...current, [field]: undefined }))
  }

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    const nextErrors = validate(values)
    setErrors(nextErrors)

    if (Object.keys(nextErrors).length > 0) {
      return
    }

    setIsSubmitting(true)
    const storageKey = 'qode27-demo-leads'
    const existingLeads = window.localStorage.getItem(storageKey)
    const parsedLeads = existingLeads ? JSON.parse(existingLeads) : []
    const nextLead = {
      app: app.name,
      name: values.name.trim(),
      businessType: values.businessType.trim(),
      phone: values.phone.trim(),
      createdAt: new Date().toISOString(),
    }
    window.localStorage.setItem(storageKey, JSON.stringify([nextLead, ...parsedLeads]))
    window.open(whatsappUrl, '_blank', 'noopener,noreferrer')
    setIsSubmitting(false)
    onClose()
  }

  return (
    <AnimatePresence>
      {open ? (
        <>
          <Motion.button
            type="button"
            className="fixed inset-0 z-[90] bg-black/55 backdrop-blur-[3px]"
            aria-label="Close request demo modal"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />
          <div className="fixed inset-0 z-[100] flex items-center justify-center px-4 py-8">
            <Motion.div
              initial={{ opacity: 0, y: 22, scale: 0.98 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: 18, scale: 0.98 }}
              transition={{ duration: 0.24 }}
              className="w-full max-w-2xl rounded-[1.5rem] border border-[var(--color-gold)]/18 bg-[#111111] p-6 text-white shadow-[0_34px_70px_rgba(11,11,11,0.42)] sm:p-8"
            >
              <div className="flex items-start justify-between gap-4">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-[0.28em] text-[var(--color-accent-strong)]">Request Demo</p>
                  <h2 className="mt-3 text-3xl font-semibold tracking-[-0.05em]">{app.displayName}</h2>
                  <p className="mt-3 max-w-xl text-sm leading-7 text-white/70">
                    Demo access is shared on request. Leave your details and we'll continue the conversation on WhatsApp.
                  </p>
                </div>
                <button
                  type="button"
                  onClick={onClose}
                  className="inline-flex h-10 w-10 items-center justify-center rounded-xl border border-white/10 bg-white/5 text-white/74 hover:border-[var(--color-accent)] hover:text-white"
                >
                  <FiX />
                </button>
              </div>

              <div className="mt-6 rounded-[1.25rem] border border-[var(--color-gold)]/12 bg-[linear-gradient(135deg,rgba(212,175,55,0.14),rgba(212,175,55,0.04))] p-4">
                <div className="flex items-start gap-3">
                  <FiCheckCircle className="mt-1 shrink-0 text-[var(--color-accent)]" />
                  <p className="text-sm leading-7 text-white/78">
                    You'll be redirected to WhatsApp with a prefilled message for {app.name}, making it easy to start the demo conversation immediately.
                  </p>
                </div>
              </div>

              <form className="mt-6 grid gap-4" onSubmit={handleSubmit} noValidate>
                <div className="grid gap-4 sm:grid-cols-2">
                  <label className="space-y-2">
                    <span className="text-sm font-medium text-white/82">Name</span>
                    <input
                      value={values.name}
                      onChange={(event) => setFieldValue('name', event.target.value)}
                      className="w-full rounded-xl border border-white/10 bg-white/6 px-4 py-3 text-sm text-white outline-none placeholder:text-white/34 focus:border-[var(--color-accent)]"
                      placeholder="Your name"
                    />
                    {errors.name ? <p className="text-sm text-[#ff9e8a]">{errors.name}</p> : null}
                  </label>
                  <label className="space-y-2">
                    <span className="text-sm font-medium text-white/82">Business Type</span>
                    <input
                      value={values.businessType}
                      onChange={(event) => setFieldValue('businessType', event.target.value)}
                      className="w-full rounded-xl border border-white/10 bg-white/6 px-4 py-3 text-sm text-white outline-none placeholder:text-white/34 focus:border-[var(--color-accent)]"
                      placeholder="Hospital, SME, Services..."
                    />
                    {errors.businessType ? <p className="text-sm text-[#ff9e8a]">{errors.businessType}</p> : null}
                  </label>
                </div>

                <label className="space-y-2">
                  <span className="text-sm font-medium text-white/82">Phone</span>
                  <input
                    value={values.phone}
                    onChange={(event) => setFieldValue('phone', event.target.value)}
                    className="w-full rounded-xl border border-white/10 bg-white/6 px-4 py-3 text-sm text-white outline-none placeholder:text-white/34 focus:border-[var(--color-accent)]"
                    placeholder="+91 98765 43210"
                  />
                  {errors.phone ? <p className="text-sm text-[#ff9e8a]">{errors.phone}</p> : null}
                </label>

                <div className="flex flex-col gap-3 sm:flex-row">
                  <button
                    type="submit"
                    disabled={isSubmitting}
                    className="button-glow inline-flex min-h-12 items-center justify-center gap-2 rounded-xl border border-[var(--color-accent)] bg-[var(--color-accent)] px-6 py-3 text-sm font-semibold text-black hover:-translate-y-0.5 hover:shadow-[0_18px_36px_rgba(212,175,55,0.26)] disabled:cursor-not-allowed disabled:opacity-80"
                  >
                    {isSubmitting ? 'Preparing WhatsApp...' : 'Request Demo on WhatsApp'}
                    <FiArrowRight />
                  </button>
                  <button
                    type="button"
                    onClick={onClose}
                    className="inline-flex min-h-12 items-center justify-center rounded-xl border border-white/12 bg-white/6 px-6 py-3 text-sm font-semibold text-white hover:-translate-y-0.5 hover:border-[var(--color-accent)]"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </Motion.div>
          </div>
        </>
      ) : null}
    </AnimatePresence>
  )
}
