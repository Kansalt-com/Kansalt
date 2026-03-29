import { createElement } from 'react'
import { FiInstagram, FiLinkedin, FiMail, FiTwitter } from 'react-icons/fi'
import { footerLinks } from '../../data/site'
import Container from '../ui/Container'

const socials = [
  { icon: FiLinkedin, href: '#contact', label: 'LinkedIn' },
  { icon: FiTwitter, href: '#contact', label: 'X' },
  { icon: FiInstagram, href: '#contact', label: 'Instagram' },
  { icon: FiMail, href: 'mailto:hello@qode27.com', label: 'Email' },
]

export default function Footer() {
  return (
    <footer id="contact" className="border-t border-slate-200/80 bg-slate-50/80">
      <Container className="py-10 sm:py-14">
        <div className="grid gap-10 lg:grid-cols-[1.2fr_0.8fr_0.8fr]">
          <div className="max-w-md">
            <a href="#home" className="font-display text-2xl font-semibold tracking-[-0.04em] text-slate-950">
              Qode27
            </a>
            <p className="mt-4 text-sm leading-7 text-slate-600">
              Premium software and automation for businesses that want simpler operations, clearer systems, and room to grow.
            </p>
            <p className="mt-4 text-sm font-semibold uppercase tracking-[0.28em] text-brand-600">Just Code IT</p>
          </div>

          <div>
            <h3 className="text-sm font-semibold uppercase tracking-[0.2em] text-slate-500">Navigation</h3>
            <div className="mt-4 flex flex-col gap-3">
              {footerLinks.map((link) => (
                <a key={link.label} href={link.href} className="text-sm text-slate-600 hover:text-slate-950">
                  {link.label}
                </a>
              ))}
            </div>
          </div>

          <div>
            <h3 className="text-sm font-semibold uppercase tracking-[0.2em] text-slate-500">Contact</h3>
            <div className="mt-4 space-y-3 text-sm text-slate-600">
              <p>hello@qode27.com</p>
              <p>+91 00000 00000</p>
              <p>Business software for hospitals, firms, and growth-focused teams.</p>
            </div>
            <div className="mt-5 flex items-center gap-3">
              {socials.map(({ icon, href, label }) => (
                <a
                  key={label}
                  href={href}
                  aria-label={label}
                  className="inline-flex h-10 w-10 items-center justify-center rounded-full border border-slate-200 bg-white text-slate-700 hover:-translate-y-0.5 hover:border-brand-300 hover:text-brand-600"
                >
                  {createElement(icon)}
                </a>
              ))}
            </div>
          </div>
        </div>
      </Container>
    </footer>
  )
}
