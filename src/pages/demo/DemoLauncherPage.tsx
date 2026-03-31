import { useEffect } from 'react'
import { AnimatePresence, motion as Motion } from 'framer-motion'
import { FiArrowUpRight, FiCheckCircle } from 'react-icons/fi'
import { Link, Navigate, useParams } from 'react-router-dom'
import { getAppByKey } from '../../config/apps'
import Container from '../../components/ui/Container'
import { trackEvent } from '../../utils/analytics'

export default function DemoLauncherPage() {
  const { appKey } = useParams()
  const app = getAppByKey(appKey)

  useEffect(() => {
    if (!app) {
      return
    }

    trackEvent('demo_launch', { app: app.key })

    const timer = window.setTimeout(() => {
      window.location.assign(app.demoUrl)
    }, 1500)

    return () => window.clearTimeout(timer)
  }, [app])

  if (!app) {
    return <Navigate to="/products" replace />
  }

  return (
    <Motion.div
      initial={{ opacity: 0, y: 18 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -18 }}
      transition={{ duration: 0.35 }}
      className="relative z-10 flex min-h-screen items-center"
    >
      <Container className="py-16">
        <div className="mx-auto max-w-4xl rounded-[2rem] border border-black/6 bg-white/92 p-8 shadow-[0_28px_60px_rgba(15,23,42,0.08)] backdrop-blur-xl sm:p-10">
          <div className="grid items-center gap-10 lg:grid-cols-[0.95fr_1.05fr]">
            <div>
              <p className="inline-flex items-center gap-2 rounded-full border border-black/8 bg-[#f3f8f8] px-4 py-2 text-xs font-semibold uppercase tracking-[0.26em] text-[var(--color-accent-strong)]">
                <span className="h-2 w-2 rounded-full bg-[var(--color-accent)]" />
                {app.displayName}
              </p>
              <h1 className="mt-6 font-display text-4xl font-bold tracking-[-0.06em] text-black sm:text-5xl">
                {app.launchTitle}
              </h1>
              <p className="mt-4 text-lg leading-8 text-neutral-600">
                {app.launchSubtitle}
              </p>

              <div className="mt-8 space-y-3">
                {app.features.map((feature) => (
                  <div key={feature} className="flex items-start gap-3 rounded-[1.2rem] bg-[#f6f9f9] px-4 py-4">
                    <FiCheckCircle className="mt-1 shrink-0 text-[var(--color-accent-strong)]" />
                    <span className="text-sm leading-7 text-neutral-700">{feature}</span>
                  </div>
                ))}
              </div>

              <div className="mt-8 flex flex-wrap gap-3">
                <a
                  href={app.demoUrl}
                  className="button-glow inline-flex min-h-12 items-center justify-center gap-2 rounded-xl border border-black bg-black px-6 py-3 text-sm font-semibold text-white transition hover:-translate-y-0.5 hover:border-[var(--color-accent)]"
                >
                  Open Now
                  <FiArrowUpRight />
                </a>
                <Link
                  to={`/products/${app.productSlug}`}
                  className="inline-flex min-h-12 items-center justify-center rounded-xl border border-black/10 bg-white px-6 py-3 text-sm font-semibold text-black transition hover:-translate-y-0.5 hover:border-[var(--color-accent)]"
                >
                  Back to Product
                </Link>
              </div>
            </div>

            <div className="relative overflow-hidden rounded-[2rem] bg-black p-8 text-white shadow-[0_30px_60px_rgba(15,23,42,0.22)]">
              <div className="absolute inset-x-0 top-0 h-28 bg-[linear-gradient(90deg,rgba(19,178,191,0.26),rgba(255,255,255,0))]" />
              <div className="relative">
                <div className="mx-auto flex h-28 w-28 items-center justify-center rounded-full border border-white/10 bg-white/6">
                  <div className="flex h-16 w-16 items-center justify-center rounded-full border-4 border-white/14 border-t-[var(--color-accent)] animate-spin" />
                </div>
                <p className="mt-8 text-center text-xl font-semibold">🚀 Launching Demo Environment...</p>
                <p className="mt-3 text-center text-sm leading-7 text-white/68">
                  {app.launchSubtitle}
                </p>

                <AnimatePresence>
                  <Motion.div
                    initial={{ opacity: 0, y: 12 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2, duration: 0.3 }}
                    className="mt-8 rounded-[1.4rem] border border-white/10 bg-white/5 p-4"
                  >
                    <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[var(--color-accent)]">Demo Mode Enabled</p>
                    <p className="mt-3 text-sm leading-7 text-white/72">
                      We append <code>?demo=true</code> to the deployed application URL so users can jump straight into a ready-to-explore environment.
                    </p>
                  </Motion.div>
                </AnimatePresence>
              </div>
            </div>
          </div>
        </div>
      </Container>
    </Motion.div>
  )
}
