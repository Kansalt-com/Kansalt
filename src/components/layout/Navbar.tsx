import { AnimatePresence, motion as Motion } from 'framer-motion'
import { useEffect, useState, type KeyboardEvent as ReactKeyboardEvent } from 'react'
import { FiMenu, FiX } from 'react-icons/fi'
import { navigation } from '../../data/site'
import { useScrolled } from '../../hooks/useScrolled'
import BrandLogo from '../ui/BrandLogo'
import Button from '../ui/Button'
import Container from '../ui/Container'

export default function Navbar() {
  const [open, setOpen] = useState<boolean>(false)
  const scrolled = useScrolled()

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setOpen(false)
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

  const toggleMenu = () => {
    setOpen((value) => !value)
  }

  const closeMenu = () => {
    setOpen(false)
  }

  const handleMobileLinkKeyDown = (event: ReactKeyboardEvent<HTMLAnchorElement>) => {
    if (event.key === 'Enter' || event.key === ' ') {
      closeMenu()
    }
  }

  return (
    <header className="sticky top-0 z-50 pt-4">
      <Motion.div
        animate={{
          y: scrolled ? 0 : 4,
          scale: scrolled ? 0.985 : 1,
        }}
        transition={{ duration: 0.35, ease: 'easeOut' }}
      >
        <Container
          className={`rounded-2xl border px-4 transition-all duration-300 ${
            scrolled
              ? 'border-neutral-200 bg-white/92 py-2 shadow-[0_14px_42px_rgba(11,11,11,0.08)] backdrop-blur-xl'
              : 'border-white/70 bg-white/76 py-3 backdrop-blur-md'
          }`}
        >
          <div className="flex items-center justify-between gap-4">
            <a href="#home" className="flex items-center" aria-label="Qode27 home">
              <BrandLogo className="h-12 max-w-[15rem] sm:h-[3.25rem] sm:max-w-[18rem]" />
            </a>

            <nav className="hidden items-center gap-6 lg:flex" aria-label="Primary navigation">
              {navigation.map((item) => (
                <a key={item.label} href={item.href} className="nav-link">
                  {item.label}
                </a>
              ))}
            </nav>

            <div className="hidden lg:block">
              <Button href="#contact" size="sm">
                Get Demo
              </Button>
            </div>

            <button
              type="button"
              className="inline-flex h-11 w-11 items-center justify-center rounded-xl border border-neutral-200 bg-white/90 text-black shadow-[0_10px_24px_rgba(11,11,11,0.06)] hover:border-brand-300 hover:text-brand-700 lg:hidden"
              onClick={toggleMenu}
              aria-label={open ? 'Close navigation menu' : 'Open navigation menu'}
              aria-expanded={open}
            >
              {open ? <FiX className="text-lg" /> : <FiMenu className="text-lg" />}
            </button>
          </div>
        </Container>
      </Motion.div>

      <AnimatePresence>
        {open && (
          <>
            <Motion.button
              type="button"
              aria-label="Close navigation overlay"
              className="fixed inset-0 top-0 bg-black/15 backdrop-blur-[2px] lg:hidden"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.25, ease: 'easeOut' }}
              onClick={closeMenu}
            />
            <Motion.div
              initial={{ opacity: 0, y: -12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.3, ease: 'easeOut' }}
              className="relative lg:hidden"
            >
              <Container className="mt-3 rounded-2xl border border-neutral-200 bg-white/95 p-4 shadow-[0_16px_50px_rgba(11,11,11,0.10)] backdrop-blur-xl">
                <nav className="flex flex-col gap-1" aria-label="Mobile navigation">
                  {navigation.map((item, index) => (
                    <Motion.a
                      key={item.label}
                      href={item.href}
                      className="rounded-2xl px-4 py-3 text-sm font-medium text-neutral-700 hover:bg-neutral-100 hover:text-black"
                      onClick={closeMenu}
                      onKeyDown={handleMobileLinkKeyDown}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: 8 }}
                      transition={{ delay: 0.04 * index, duration: 0.2 }}
                    >
                      {item.label}
                    </Motion.a>
                  ))}
                  <Button href="#contact" className="mt-2 w-full justify-center" size="sm" onClick={closeMenu}>
                    Get Demo
                  </Button>
                </nav>
              </Container>
            </Motion.div>
          </>
        )}
      </AnimatePresence>
    </header>
  )
}
