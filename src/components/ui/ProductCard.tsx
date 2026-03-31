import { createElement } from 'react'
import { motion as Motion } from 'framer-motion'
import { FiCheck, FiLock } from 'react-icons/fi'
import { Link } from 'react-router-dom'
import { getAppByProductSlug } from '../../config/apps'
import type { Product } from '../../data/site'
import RequestDemoButton from './RequestDemoButton'

interface ProductCardProps {
  product: Product
}

export default function ProductCard({ product }: ProductCardProps) {
  const app = getAppByProductSlug(product.slug)

  return (
    <Motion.article
      whileHover={{ y: -6, scale: 1.01 }}
      transition={{ duration: 0.25, ease: 'easeOut' }}
      className="product-card flex h-full flex-col rounded-[1.1rem] border border-black/8 bg-white p-7"
    >
      <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-[var(--color-accent-soft)] text-xl text-[var(--color-accent-strong)]">
        {createElement(product.icon)}
      </div>
      <div className="mt-6">
        <p className="inline-flex rounded-full bg-[var(--color-accent-soft)] px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-[var(--color-accent-strong)]">
          {product.category}
        </p>
        <h3 className="mt-4 text-2xl font-semibold tracking-[-0.03em] text-black">{product.name}</h3>
        <p className="mt-4 text-base leading-7 text-neutral-600">{product.description}</p>
      </div>
      <ul className="mt-6 space-y-3">
        {product.features.map((feature) => (
          <li key={feature} className="flex items-start gap-3 text-sm leading-6 text-neutral-600">
            <span className="mt-1 inline-flex h-5 w-5 items-center justify-center rounded-full bg-black text-white">
              <FiCheck className="text-[0.7rem]" />
            </span>
            <span>{feature}</span>
          </li>
        ))}
      </ul>
      <div className="mt-6 rounded-[1rem] border border-[var(--color-gold)]/18 bg-[linear-gradient(135deg,rgba(212,175,55,0.12),rgba(212,175,55,0.04))] px-4 py-3">
        <p className="inline-flex items-center gap-2 text-sm font-medium text-black">
          <FiLock className="text-[var(--color-accent-strong)]" />
          Demo available on request
        </p>
      </div>
      <div className="mt-auto flex flex-wrap items-center gap-4 pt-8">
        <Link
          to={`/products/${product.slug}`}
          className="inline-flex items-center gap-2 text-sm font-semibold text-black hover:gap-3 hover:text-[var(--color-accent-strong)]"
        >
          Explore Product
        </Link>
        {app ? <RequestDemoButton app={app} label="Request Demo" size="sm" variant="secondary" /> : null}
      </div>
    </Motion.article>
  )
}
