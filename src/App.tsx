import { Suspense, lazy } from 'react'
import { Navigate, Route, Routes, useLocation } from 'react-router-dom'
import { AnimatePresence } from 'framer-motion'
import SiteLayout from './components/layout/SiteLayout'
import PageSkeleton from './components/ui/PageSkeleton'

const HomePage = lazy(() => import('./pages/HomePage'))
const ProductsPage = lazy(() => import('./pages/ProductsPage'))
const PricingPage = lazy(() => import('./pages/PricingPage'))
const ContactPage = lazy(() => import('./pages/ContactPage'))
const ProductDetailPage = lazy(() => import('./pages/ProductDetailPage'))

export default function App() {
  const location = useLocation()

  return (
    <div className="relative min-h-screen bg-[var(--color-page)] text-[var(--color-copy)]">
      <a
        href="#main-content"
        className="absolute left-4 top-4 z-[80] -translate-y-20 rounded-xl bg-black px-4 py-2 text-sm font-semibold text-white focus:translate-y-0 focus:outline-none focus:ring-2 focus:ring-[var(--color-accent)]"
      >
        Skip to content
      </a>
      <div className="pointer-events-none absolute inset-x-0 top-0 h-[38rem] bg-[radial-gradient(circle_at_top,_rgba(212,175,55,0.14),transparent_40%),linear-gradient(180deg,_rgba(255,255,255,0.98)_0%,_rgba(250,248,243,0.96)_48%,_rgba(255,255,255,1)_100%)]" />
      <Suspense fallback={<PageSkeleton />}>
        <AnimatePresence mode="wait">
          <Routes location={location} key={location.pathname}>
            <Route element={<SiteLayout />}>
              <Route index element={<HomePage />} />
              <Route path="/products" element={<ProductsPage />} />
              <Route path="/products/:slug" element={<ProductDetailPage />} />
              <Route path="/pricing" element={<PricingPage />} />
              <Route path="/contact" element={<ContactPage />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Route>
          </Routes>
        </AnimatePresence>
      </Suspense>
    </div>
  )
}
