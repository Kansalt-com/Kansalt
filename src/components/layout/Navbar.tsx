import { AnimatePresence, motion as Motion } from 'framer-motion'
import { useEffect, useState, type KeyboardEvent as ReactKeyboardEvent } from 'react'
import { NavLink } from 'react-router-dom'
import { FiChevronDown, FiMenu, FiX } from 'react-icons/fi'
import { appCategories, appStoreApps, getAppByKey } from '../../config/apps'
import { navigation } from '../../data/site'
import { useScrolled } from '../../hooks/useScrolled'
import BrandLogo from '../ui/BrandLogo'
import RequestDemoButton from '../ui/RequestDemoButton'
import Container from '../ui/Container'

export default function Navbar() {
  const [open, setOpen] = useState(false)
  const [productsOpen, setProductsOpen] = useState(false)
  const [categoriesOpen, setCategoriesOpen] = useState(false)
  const scrolled = useScrolled()
  const defaultApp = getAppByKey('hms')

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setOpen(false)
        setProductsOpen(false)
        setCategoriesOpen(false)
      }
    }

    document.addEventListener('keydown', onKeyDown)
    return () => document.removeEventListener('keydown', onKeyDown)
  }, [])

  useEffect(() => {
    document.body.style.overflow = open ? 'hidden' : ''

    return () => {
      document.body.style.overflow = ''
    }
  }, [open])

  const closeMenu = () => {
    setOpen(false)
    setProductsOpen(false)
    setCategoriesOpen(false)
  }

  const handleMobileLinkKeyDown = (event: ReactKeyboardEvent<HTMLAnchorElement>) => {
    if (event.key === 'Enter' || event.key === ' ') {
      closeMenu()
    }
  }

  return (
    <header className="sticky top-0 z-50 pt-4">
      <Motion.div
        animate={{ y: scrolled ? 0 : 4, scale: scrolled ? 0.988 : 1 }}
        transition={{ duration: 0.35, ease: 'easeOut' }}
      >
        <Container
          className={`rounded-2xl border px-4 transition-all duration-300 ${
            scrolled
              ? 'border-[var(--color-gold)]/16 bg-white/92 py-2 shadow-[0_20px_55px_rgba(11,11,11,0.08)] backdrop-blur-xl'
              : 'border-[var(--color-gold)]/12 bg-white/76 py-3 backdrop-blur-md'
          }`}
        >
          <div className="flex items-center justify-between gap-4">
            <NavLink to="/" className="flex items-center" aria-label="Qode27 home" onClick={closeMenu}>
              <BrandLogo className="h-11 max-w-[11rem] sm:h-12 sm:max-w-[12rem]" />
            </NavLink>

            <nav className="hidden items-center gap-6 lg:flex" aria-label="Primary navigation">
              {navigation.map((item) => {
                if (item.label === 'Products') {
                  return (
                    <div
                      key={item.label}
                      className="relative"
                      onMouseEnter={() => setProductsOpen(true)}
                      onMouseLeave={() => setProductsOpen(false)}
                    >
                      <button
                        type="button"
                        className={`nav-link inline-flex items-center gap-2 ${productsOpen ? 'active text-black' : ''}`}
                        onClick={() => setProductsOpen((value) => !value)}
                        aria-expanded={productsOpen}
                      >
                        Products
                        <FiChevronDown className={`text-xs transition ${productsOpen ? 'rotate-180' : ''}`} />
                      </button>

                      <AnimatePresence>
                        {productsOpen ? (
                          <Motion.div
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: 8 }}
                            transition={{ duration: 0.2 }}
                            className="absolute left-0 top-full mt-4 w-[21rem] rounded-[1.2rem] border border-[var(--color-gold)]/16 bg-white/96 p-3 shadow-[0_22px_50px_rgba(11,11,11,0.12)] backdrop-blur-xl"
                          >
                            {appStoreApps.map((app) => (
                              <div key={app.key} className="rounded-[1rem] px-2 py-2 hover:bg-[#fbf7eb]">
                                <p className="px-3 text-xs font-semibold uppercase tracking-[0.22em] text-[var(--color-accent-strong)]">
                                  {app.name}
                                </p>
                                <div className="mt-2 grid gap-1">
                                  <NavLink
                                    to={`/products/${app.productSlug}`}
                                    className="rounded-xl px-3 py-2 text-sm font-medium text-neutral-700 hover:bg-white hover:text-black"
                                    onClick={() => setProductsOpen(false)}
                                  >
                                    View Details
                                  </NavLink>
                                  <a
                                    href={app.whatsappUrl}
                                    target="_blank"
                                    rel="noreferrer"
                                    className="rounded-xl px-3 py-2 text-sm font-medium text-neutral-700 hover:bg-white hover:text-black"
                                  >
                                    Try Demo
                                  </a>
                                </div>
                              </div>
                            ))}
                          </Motion.div>
                        ) : null}
                      </AnimatePresence>
                    </div>
                  )
                }

                if (item.label === 'Categories') {
                  return (
                    <div
                      key={item.label}
                      className="relative"
                      onMouseEnter={() => setCategoriesOpen(true)}
                      onMouseLeave={() => setCategoriesOpen(false)}
                    >
                      <button
                        type="button"
                        className={`nav-link inline-flex items-center gap-2 ${categoriesOpen ? 'active text-black' : ''}`}
                        onClick={() => setCategoriesOpen((value) => !value)}
                        aria-expanded={categoriesOpen}
                      >
                        Categories
                        <FiChevronDown className={`text-xs transition ${categoriesOpen ? 'rotate-180' : ''}`} />
                      </button>
                      <AnimatePresence>
                        {categoriesOpen ? (
                          <Motion.div
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: 8 }}
                            transition={{ duration: 0.2 }}
                            className="absolute left-0 top-full mt-4 w-[18rem] rounded-[1.2rem] border border-[var(--color-gold)]/16 bg-white/96 p-3 shadow-[0_22px_50px_rgba(11,11,11,0.12)] backdrop-blur-xl"
                          >
                            {appCategories.map((category) => (
                              <NavLink
                                key={category}
                                to={`/products?category=${encodeURIComponent(category)}`}
                                className="block rounded-xl px-3 py-2 text-sm font-medium text-neutral-700 hover:bg-[#fbf7eb] hover:text-black"
                                onClick={() => setCategoriesOpen(false)}
                              >
                                {category}
                              </NavLink>
                            ))}
                          </Motion.div>
                        ) : null}
                      </AnimatePresence>
                    </div>
                  )
                }

                return (
                  <NavLink
                    key={item.label}
                    to={item.href}
                    className={({ isActive }) => `nav-link ${isActive ? 'active text-black' : ''}`}
                  >
                    {item.label}
                  </NavLink>
                )
              })}
            </nav>

            <div className="hidden lg:flex lg:items-center lg:gap-3">
              {defaultApp ? <RequestDemoButton app={defaultApp} label="Request Demo" size="sm" variant="primary" /> : null}
            </div>

            <button
              type="button"
              className="inline-flex h-11 w-11 items-center justify-center rounded-xl border border-[var(--color-gold)]/16 bg-white/90 text-black shadow-[0_10px_24px_rgba(11,11,11,0.08)] hover:border-[var(--color-accent)] hover:text-[var(--color-accent-strong)] lg:hidden"
              onClick={() => setOpen((value) => !value)}
              aria-label={open ? 'Close navigation menu' : 'Open navigation menu'}
              aria-expanded={open}
            >
              {open ? <FiX className="text-lg" /> : <FiMenu className="text-lg" />}
            </button>
          </div>
        </Container>
      </Motion.div>

      <AnimatePresence>
        {open ? (
          <>
            <Motion.button
              type="button"
              aria-label="Close navigation overlay"
              className="fixed inset-0 bg-black/25 backdrop-blur-[2px] lg:hidden"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              onClick={closeMenu}
            />
            <Motion.div
              initial={{ opacity: 0, y: -12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.25, ease: 'easeOut' }}
              className="relative lg:hidden"
            >
              <Container className="mt-3 rounded-2xl border border-[var(--color-gold)]/14 bg-white/95 p-4 shadow-[0_24px_55px_rgba(11,11,11,0.12)] backdrop-blur-xl">
                <nav className="flex flex-col gap-1" aria-label="Mobile navigation">
                  {navigation.map((item, index) =>
                    item.label === 'Products' ? (
                      <div key={item.label} className="mt-1 rounded-2xl bg-[#fbf7eb] p-3">
                        <p className="px-1 text-xs font-semibold uppercase tracking-[0.22em] text-[var(--color-accent-strong)]">
                          Products
                        </p>
                        <div className="mt-3 grid gap-2">
                          {appStoreApps.map((app) => (
                            <div key={app.key} className="rounded-2xl bg-white p-3">
                              <p className="text-sm font-semibold text-black">{app.name}</p>
                              <div className="mt-2 grid gap-2">
                                <NavLink
                                  to={`/products/${app.productSlug}`}
                                  onClick={closeMenu}
                                  className="rounded-xl px-3 py-2 text-sm font-medium text-neutral-700 hover:bg-neutral-100 hover:text-black"
                                >
                                  View Details
                                </NavLink>
                                <a
                                  href={app.whatsappUrl}
                                  target="_blank"
                                  rel="noreferrer"
                                  className="rounded-xl px-3 py-2 text-sm font-medium text-neutral-700 hover:bg-neutral-100 hover:text-black"
                                >
                                  Try Demo
                                </a>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    ) : item.label === 'Categories' ? (
                      <div key={item.label} className="mt-1 rounded-2xl bg-[#fbf7eb] p-3">
                        <p className="px-1 text-xs font-semibold uppercase tracking-[0.22em] text-[var(--color-accent-strong)]">
                          Categories
                        </p>
                        <div className="mt-3 grid gap-2">
                          {appCategories.map((category) => (
                            <NavLink
                              key={category}
                              to={`/products?category=${encodeURIComponent(category)}`}
                              onClick={closeMenu}
                              className="rounded-xl bg-white px-3 py-2 text-sm font-medium text-neutral-700 hover:bg-neutral-100 hover:text-black"
                            >
                              {category}
                            </NavLink>
                          ))}
                        </div>
                      </div>
                    ) : (
                      <Motion.div
                        key={item.label}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: 8 }}
                        transition={{ delay: 0.04 * index, duration: 0.2 }}
                      >
                        <NavLink
                          to={item.href}
                          onClick={closeMenu}
                          onKeyDown={handleMobileLinkKeyDown}
                          className={({ isActive }) =>
                            `block rounded-2xl px-4 py-3 text-sm font-medium transition ${
                              isActive
                                ? 'bg-black text-white'
                                : 'text-neutral-700 hover:bg-neutral-100 hover:text-black'
                            }`
                          }
                        >
                          {item.label}
                        </NavLink>
                      </Motion.div>
                    ),
                  )}
                  {defaultApp ? (
                    <div className="mt-2">
                      <RequestDemoButton app={defaultApp} label="Request Demo" className="w-full justify-center" size="sm" />
                    </div>
                  ) : null}
                </nav>
              </Container>
            </Motion.div>
          </>
        ) : null}
      </AnimatePresence>
    </header>
  )
}
