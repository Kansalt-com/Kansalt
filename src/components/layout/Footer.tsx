import { createElement } from 'react'
import { NavLink } from 'react-router-dom'
import { FiArrowUpRight, FiLinkedin, FiMail, FiPhone } from 'react-icons/fi'
import { footerLinks } from '../../data/site'
import BrandLogo from '../ui/BrandLogo'
import Container from '../ui/Container'

const socials = [
  { icon: FiLinkedin, href: '/contact', label: 'LinkedIn' },
  { icon: FiMail, href: 'mailto:qode27business@gmail.com', label: 'Email' },
  { icon: FiPhone, href: 'tel:+917022556960', label: 'Phone' },
]

export default function Footer() {
  return (
    <footer className="relative z-10 border-t border-[var(--color-gold)]/12 bg-[#faf7ee]">
      <Container className="py-12">
        <div className="grid gap-10 lg:grid-cols-[1.15fr_0.85fr_0.9fr]">
          <div className="max-w-md">
            <NavLink to="/" className="inline-flex items-center" aria-label="Qode27 home">
              <BrandLogo className="h-12 sm:h-14 max-w-[12rem] sm:max-w-[14rem]" />
            </NavLink>
            <p className="mt-4 text-sm leading-7 text-neutral-600">
              Qode27 is a premium business software app store for SMEs looking for healthcare, HR, finance, and operations applications in one place.
            </p>
            <p className="mt-4 text-xs font-semibold uppercase tracking-[0.28em] text-[var(--color-accent-strong)]">
              Business software app store
            </p>
          </div>

          <div>
            <h3 className="text-sm font-semibold uppercase tracking-[0.2em] text-neutral-500">Navigation</h3>
            <div className="mt-4 flex flex-col gap-3">
              {footerLinks.map((link) => (
                <NavLink key={link.label} to={link.href} className="text-sm text-neutral-600 hover:text-black">
                  {link.label}
                </NavLink>
              ))}
            </div>
          </div>

          <div>
            <h3 className="text-sm font-semibold uppercase tracking-[0.2em] text-neutral-500">Reach Qode27</h3>
            <div className="mt-4 space-y-3 text-sm text-neutral-600">
              <p>qode27business@gmail.com</p>
              <p>+91 7022556960</p>
              <p>Hyderabad, India</p>
            </div>
            <div className="mt-5 flex items-center gap-3">
              {socials.map(({ icon, href, label }) => {
                const content = (
                  <>
                    {createElement(icon)}
                    {label === 'LinkedIn' ? <FiArrowUpRight className="text-xs opacity-60" /> : null}
                  </>
                )

                if (href.startsWith('/')) {
                  return (
                    <NavLink
                      key={label}
                      to={href}
                      aria-label={label}
                      className="inline-flex h-10 w-10 items-center justify-center gap-1 rounded-xl border border-black/10 bg-white text-neutral-700 hover:-translate-y-0.5 hover:border-[var(--color-accent)] hover:text-[var(--color-accent-strong)]"
                    >
                      {content}
                    </NavLink>
                  )
                }

                return (
                  <a
                    key={label}
                    href={href}
                    aria-label={label}
                    className="inline-flex h-10 w-10 items-center justify-center gap-1 rounded-xl border border-black/10 bg-white text-neutral-700 hover:-translate-y-0.5 hover:border-[var(--color-accent)] hover:text-[var(--color-accent-strong)]"
                  >
                    {content}
                  </a>
                )
              })}
            </div>
          </div>
        </div>
      </Container>
    </footer>
  )
}
