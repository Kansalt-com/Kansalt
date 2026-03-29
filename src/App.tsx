import { Suspense, lazy } from 'react'
import Footer from './components/layout/Footer'
import Navbar from './components/layout/Navbar'

const HeroSection = lazy(() => import('./sections/HeroSection'))
const TrustStrip = lazy(() => import('./sections/TrustStrip'))
const ProductsSection = lazy(() => import('./sections/ProductsSection'))
const SolutionsSection = lazy(() => import('./sections/SolutionsSection'))
const FeaturesSection = lazy(() => import('./sections/FeaturesSection'))
const WhyQodeSection = lazy(() => import('./sections/WhyQodeSection'))
const PricingSection = lazy(() => import('./sections/PricingSection'))
const TestimonialsSection = lazy(() => import('./sections/TestimonialsSection'))
const FinalCtaSection = lazy(() => import('./sections/FinalCtaSection'))

function SectionFallback() {
  return <div className="h-24" aria-hidden="true" />
}

export default function App() {
  return (
    <div className="relative min-h-screen bg-white text-neutral-900">
      <a
        href="#main-content"
        className="absolute left-4 top-4 z-[70] -translate-y-20 rounded-xl bg-black px-4 py-2 text-sm font-semibold text-white focus:translate-y-0 focus:outline-none focus:ring-2 focus:ring-brand-300"
      >
        Skip to content
      </a>
      <div
        className="pointer-events-none absolute inset-x-0 top-0 h-[42rem] bg-[radial-gradient(circle_at_top,_rgba(211,161,62,0.13),transparent_34%),radial-gradient(circle_at_18%_20%,_rgba(45,184,182,0.10),transparent_24%),linear-gradient(180deg,_#fcfbf7_0%,_#ffffff_58%)]"
        aria-hidden="true"
      />
      <Navbar />
      <main id="main-content">
        <Suspense fallback={<SectionFallback />}>
          <HeroSection />
          <TrustStrip />
          <ProductsSection />
          <SolutionsSection />
          <FeaturesSection />
          <WhyQodeSection />
          <PricingSection />
          <TestimonialsSection />
          <FinalCtaSection />
        </Suspense>
      </main>
      <Footer />
    </div>
  )
}
