import { AnimatePresence, motion as Motion } from 'framer-motion'
import { useState } from 'react'
import { FiMenu, FiX } from 'react-icons/fi'
import { navigation } from '../../data/site'
import { useScrolled } from '../../hooks/useScrolled'
import Button from '../ui/Button'
import Container from '../ui/Container'

export default function Navbar() {
  const [open, setOpen] = useState(false)
  const scrolled = useScrolled()

  return (
    <header className="sticky top-0 z-50 px-4 pt-4 sm:px-6">
      <Motion.div
        animate={{
          y: scrolled ? 0 : 4,
          scale: scrolled ? 0.985 : 1,
        }}
        transition={{ duration: 0.3, ease: 'easeOut' }}
      >
        <Container
          className={`rounded-full border px-4 py-3 transition-all duration-300 sm:px-6 ${
            scrolled
              ? 'border-slate-200/80 bg-white/88 shadow-[0_12px_40px_rgba(15,23,42,0.08)] backdrop-blur-xl'
              : 'border-white/70 bg-white/70 backdrop-blur-md'
          }`}
        >
          <div className="flex items-center justify-between gap-4">
            <a
              href="#home"
              className="font-display text-lg font-semibold tracking-[-0.04em] text-slate-950"
              aria-label="Qode27 home"
            >
              Qode27
            </a>

            <nav className="hidden items-center gap-7 lg:flex" aria-label="Primary navigation">
              {navigation.map((item) => (
                <a
                  key={item.label}
                  href={item.href}
                  className="text-sm font-medium text-slate-600 hover:text-slate-950"
                >
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
              className="inline-flex h-11 w-11 items-center justify-center rounded-full border border-slate-200 text-slate-900 lg:hidden"
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
        {open && (
          <Motion.div
            initial={{ opacity: 0, y: -12 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.25, ease: 'easeOut' }}
            className="lg:hidden"
          >
            <Container className="mt-3 rounded-[28px] border border-slate-200/80 bg-white/95 p-4 shadow-[0_16px_50px_rgba(15,23,42,0.10)] backdrop-blur-xl">
              <nav className="flex flex-col gap-1" aria-label="Mobile navigation">
                {navigation.map((item) => (
                  <a
                    key={item.label}
                    href={item.href}
                    className="rounded-2xl px-4 py-3 text-sm font-medium text-slate-700 hover:bg-slate-100 hover:text-slate-950"
                    onClick={() => setOpen(false)}
                  >
                    {item.label}
                  </a>
                ))}
                <Button href="#contact" className="mt-2 w-full justify-center" size="sm">
                  Get Demo
                </Button>
              </nav>
            </Container>
          </Motion.div>
        )}
      </AnimatePresence>
    </header>
  )
}
