import { motion as Motion } from 'framer-motion'
import { useMemo } from 'react'
import { useSearchParams } from 'react-router-dom'
import Container from '../components/ui/Container'
import ProductCard from '../components/ui/ProductCard'
import Reveal from '../components/ui/Reveal'
import SectionHeader from '../components/ui/SectionHeader'
import { categories, products } from '../data/site'

export default function ProductsPage() {
  const [searchParams, setSearchParams] = useSearchParams()
  const activeCategory = searchParams.get('category')

  const filteredProducts = useMemo(() => {
    if (!activeCategory) {
      return products
    }

    return products.filter((product) => product.categoryKey === activeCategory)
  }, [activeCategory])

  return (
    <Motion.div initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -18 }} transition={{ duration: 0.35 }}>
      <section className="section-spacing pt-12">
        <Container>
          <SectionHeader
            eyebrow="App Store"
            title="Browse Qode27 business applications by category."
            description="A premium marketplace of ready-to-deploy business software for healthcare, HR, finance, and operational teams."
            align="center"
          />

          <div className="mt-10 flex flex-wrap justify-center gap-3">
            <button
              type="button"
              onClick={() => setSearchParams({})}
              className={`rounded-full border px-4 py-2 text-sm font-semibold transition ${
                !activeCategory
                  ? 'border-black bg-black text-white'
                  : 'border-[var(--color-gold)]/18 bg-white text-black hover:border-[var(--color-accent)]'
              }`}
            >
              All Apps
            </button>
            {categories.map((category) => (
              <button
                key={category.key}
                type="button"
                onClick={() => setSearchParams({ category: category.key })}
                className={`rounded-full border px-4 py-2 text-sm font-semibold transition ${
                  activeCategory === category.key
                    ? 'border-black bg-black text-white'
                    : 'border-[var(--color-gold)]/18 bg-white text-black hover:border-[var(--color-accent)]'
                }`}
              >
                {category.key}
              </button>
            ))}
          </div>

          <div className="mt-12 grid gap-6 lg:grid-cols-3">
            {filteredProducts.map((product) => (
              <Reveal key={product.slug}>
                <ProductCard product={product} />
              </Reveal>
            ))}
          </div>
        </Container>
      </section>
    </Motion.div>
  )
}
