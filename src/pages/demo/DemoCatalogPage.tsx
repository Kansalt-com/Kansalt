import { motion as Motion } from 'framer-motion'
import { FiArrowRight, FiMessageSquare } from 'react-icons/fi'
import { demoApps, getDemoRoute, buildDemoRequestPath } from '../../config/demo-apps'
import { DemoProductPreview } from '../../components/demo/DemoPrimitives'
import Container from '../../components/ui/Container'
import Seo from '../../components/ui/Seo'
import Button from '../../components/ui/Button'

export default function DemoCatalogPage() {
  return (
    <Motion.div initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -18 }} transition={{ duration: 0.35 }}>
      <Seo
        title="Interactive Product Demos | Qode27"
        description="Explore Qode27 interactive demos for HRMS, hospital management, inventory management, and truck parking operations."
        canonicalPath="/demo"
      />

      <section className="section-spacing pt-12">
        <Container>
          <div className="rounded-[2rem] border border-slate-200/80 bg-white/88 p-8 shadow-[0_28px_70px_rgba(15,23,42,0.1)] backdrop-blur-xl sm:p-10">
            <p className="text-xs font-semibold uppercase tracking-[0.28em] text-[var(--color-accent)]">Qode27 Demo Mode</p>
            <h1 className="mt-5 max-w-4xl font-display text-4xl font-semibold tracking-[-0.06em] text-slate-950 sm:text-5xl">
              Real-feeling product walkthroughs, running inside qode27.com with zero new infrastructure.
            </h1>
            <p className="mt-5 max-w-3xl text-base leading-8 text-slate-600">
              These demos are frontend-only sandboxes with premium UI, realistic sample data, mock login personas, local-only forms, and a hard guard against live production API calls.
            </p>
            <div className="mt-8 flex flex-col gap-4 sm:flex-row">
              <Button href="/solutions">View solutions</Button>
              <Button href="/request-demo" variant="secondary">
                Book tailored demo
              </Button>
            </div>
          </div>

          <div className="mt-10 grid gap-6 xl:grid-cols-2">
            {demoApps.map((app) => {
              const Icon = app.icon
              return (
                <Motion.article
                  key={app.slug}
                  whileHover={{ y: -4 }}
                  transition={{ duration: 0.22 }}
                  className="overflow-hidden rounded-[1.8rem] border border-slate-200/80 bg-white shadow-[0_24px_60px_rgba(15,23,42,0.08)]"
                >
                  <div className="p-7 text-white" style={{ background: app.accent.gradient }}>
                    <div className="inline-flex h-14 w-14 items-center justify-center rounded-2xl bg-white/12 text-2xl backdrop-blur-sm">
                      <Icon />
                    </div>
                    <p className="mt-5 text-xs font-semibold uppercase tracking-[0.24em] text-white/66">{app.category}</p>
                    <h2 className="mt-3 text-3xl font-semibold tracking-[-0.05em]">{app.name}</h2>
                    <p className="mt-3 max-w-2xl text-sm leading-7 text-white/74">{app.summary}</p>
                  </div>
                  <div className="space-y-5 p-7">
                    <DemoProductPreview app={app} />
                    <p className="text-xs font-medium uppercase tracking-[0.18em] text-slate-500">{app.identity.productHint}</p>
                    <div className="grid gap-3 sm:grid-cols-3">
                      {app.heroMetrics.map((metric) => (
                        <div key={metric.label} className="rounded-[1.2rem] bg-slate-50 p-4">
                          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">{metric.label}</p>
                          <p className="mt-3 text-xl font-semibold tracking-[-0.04em] text-slate-950">{metric.value}</p>
                          <p className="mt-2 text-sm text-slate-600">{metric.change}</p>
                        </div>
                      ))}
                    </div>
                    <div className="flex flex-col gap-3 sm:flex-row">
                      {app.demoEnabled && !app.requestDemoOnly ? (
                        <Button href={getDemoRoute(app.slug)} size="sm">
                          Try interactive demo
                          <FiArrowRight />
                        </Button>
                      ) : null}
                      <Button href={buildDemoRequestPath(app.name)} variant="secondary" size="sm">
                        Request demo
                        <FiMessageSquare />
                      </Button>
                    </div>
                  </div>
                </Motion.article>
              )
            })}
          </div>
        </Container>
      </section>
    </Motion.div>
  )
}
