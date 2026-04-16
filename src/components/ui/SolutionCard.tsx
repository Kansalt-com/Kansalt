import { createElement } from 'react'
import { motion as Motion } from 'framer-motion'
import { FiArrowRight } from 'react-icons/fi'
import { Link } from 'react-router-dom'
import { DemoProductPreview } from '../demo/DemoPrimitives'
import { getDemoAppBySolutionSlug, getDemoRoute } from '../../config/demo-apps'
import type { Solution } from '../../data/solutions'
import { buildRequestDemoPath } from '../../data/solutions'
import Button from './Button'

type SolutionCardProps = {
  solution: Solution
  featured?: boolean
}

export default function SolutionCard({ solution, featured = false }: SolutionCardProps) {
  const demoApp = getDemoAppBySolutionSlug(solution.slug)
  const hasInteractiveDemo = Boolean(demoApp?.demoEnabled && !demoApp.requestDemoOnly)
  const demoRoute = hasInteractiveDemo && demoApp ? getDemoRoute(demoApp.slug) : null

  return (
    <Motion.article
      whileHover={{ y: -6 }}
      transition={{ duration: 0.25 }}
      className={`product-card flex h-full flex-col rounded-[1.5rem] border border-slate-200/70 bg-white p-7 ${
        featured ? 'shine-border shadow-[0_26px_60px_rgba(15,23,42,0.1)]' : 'shadow-[0_18px_45px_rgba(15,23,42,0.07)]'
      }`}
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-[var(--color-accent-soft)] text-xl text-[var(--color-accent)] transition duration-300 group-hover:scale-105">
          {createElement(solution.icon)}
        </div>
        {featured ? (
          <span className="rounded-full border border-[var(--color-accent)]/20 bg-[var(--color-accent-soft)] px-3 py-1 text-[0.7rem] font-semibold uppercase tracking-[0.22em] text-[var(--color-accent)]">
            Popular
          </span>
        ) : null}
      </div>
      <p className="mt-6 text-xs font-semibold uppercase tracking-[0.24em] text-[var(--color-accent)]">{solution.category}</p>
      {demoApp ? (
        <div className="mt-3">
          <span className="inline-flex rounded-full bg-slate-100 px-3 py-1 text-[0.7rem] font-semibold uppercase tracking-[0.18em] text-slate-600">
            {hasInteractiveDemo ? 'Interactive Demo Available' : 'Request Demo Only'}
          </span>
        </div>
      ) : null}
      <h3 className="mt-3 text-[1.7rem] font-semibold tracking-[-0.04em] text-slate-950">{solution.name}</h3>
      <p className="mt-4 text-base leading-7 text-slate-600">{solution.cardDescription}</p>
      {demoApp ? (
        <div className="mt-6">
          <DemoProductPreview app={demoApp} />
          <p className="mt-3 text-xs font-medium uppercase tracking-[0.18em] text-slate-500">{demoApp.identity.productHint}</p>
        </div>
      ) : null}
      <div className="mt-6 space-y-5 rounded-[1.3rem] bg-slate-50 p-5">
        <div>
          <p className="text-[0.7rem] font-semibold uppercase tracking-[0.22em] text-slate-500">Problem</p>
          <p className="mt-2 text-sm leading-6 text-slate-600">{solution.problems[0]}</p>
        </div>
        <div>
          <p className="text-[0.7rem] font-semibold uppercase tracking-[0.22em] text-slate-500">System</p>
          <p className="mt-2 text-sm leading-6 text-slate-600">{solution.approach[0]}</p>
        </div>
        <div>
          <p className="text-[0.7rem] font-semibold uppercase tracking-[0.22em] text-slate-500">Outcome</p>
          <p className="mt-2 text-sm leading-6 text-slate-600">{solution.benefits[0]}</p>
        </div>
      </div>
      <div className="mt-auto flex flex-col gap-3 pt-8">
        {demoRoute ? (
          <Button href={demoRoute} variant="primary" size="sm" className="justify-center">
            Try Interactive Demo
            <FiArrowRight />
          </Button>
        ) : null}
        <div className="flex flex-col gap-3 sm:flex-row">
          <Link
            to={`/solutions/${solution.slug}`}
            className="inline-flex min-h-12 items-center justify-center gap-2 rounded-xl border border-slate-200 px-5 py-3 text-sm font-semibold text-slate-900 hover:border-[var(--color-accent)] hover:text-[var(--color-accent)]"
          >
            View Details
            <FiArrowRight />
          </Link>
          <Button href={buildRequestDemoPath(solution.name)} variant="primary" size="sm" className="justify-center">
            Request Demo
          </Button>
        </div>
      </div>
    </Motion.article>
  )
}
