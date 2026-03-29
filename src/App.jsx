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
    <div className="relative min-h-screen bg-white text-slate-900">
      <div
        className="pointer-events-none absolute inset-x-0 top-0 h-[42rem] bg-[radial-gradient(circle_at_top,_rgba(40,124,255,0.12),transparent_38%),radial-gradient(circle_at_20%_20%,_rgba(46,184,166,0.10),transparent_26%),linear-gradient(180deg,_#f8fbff_0%,_#ffffff_55%)]"
        aria-hidden="true"
      />
      <Navbar />
      <main>
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
