import { createElement } from 'react'
import type { IconType } from 'react-icons'
import { FiInstagram, FiLinkedin, FiMail, FiTwitter } from 'react-icons/fi'
import { footerLinks } from '../../data/site'
import BrandLogo from '../ui/BrandLogo'
import Container from '../ui/Container'

type SocialLink = {
  icon: IconType
  href: string
  label: string
}

const socials: SocialLink[] = [
  { icon: FiLinkedin, href: '#contact', label: 'LinkedIn' },
  { icon: FiTwitter, href: '#contact', label: 'X' },
  { icon: FiInstagram, href: '#contact', label: 'Instagram' },
  { icon: FiMail, href: 'mailto:qode27business@gmail.com', label: 'Email' },
]

export default function Footer() {
  return (
    <footer id="contact" className="border-t border-neutral-200/80 bg-neutral-50">
      <Container className="py-12">
        <div className="grid gap-10 lg:grid-cols-[1.2fr_0.8fr_0.8fr]">
          <div className="max-w-md">
            <a href="#home" className="inline-flex items-center">
              <BrandLogo className="h-12 sm:h-14 max-w-[16rem] sm:max-w-[20rem]" />
            </a>
            <p className="mt-4 text-sm leading-7 text-neutral-600">
              Premium software and automation for businesses that want simpler operations, clearer systems, and room to grow.
            </p>
            <p className="mt-4 text-sm font-medium uppercase tracking-[0.32em] text-brand-700">Just Code IT</p>
          </div>

          <div>
            <h3 className="text-sm font-semibold uppercase tracking-[0.2em] text-neutral-500">Navigation</h3>
            <div className="mt-4 flex flex-col gap-3">
              {footerLinks.map((link) => (
                <a key={link.label} href={link.href} className="text-sm text-neutral-600 hover:text-black">
                  {link.label}
                </a>
              ))}
            </div>
          </div>

          <div>
            <h3 className="text-sm font-semibold uppercase tracking-[0.2em] text-neutral-500">Contact</h3>
            <div className="mt-4 space-y-3 text-sm text-neutral-600">
              <p>qode27business@gmail.com</p>
              <p>+91 7022556960</p>
              <p>Business software for hospitals, firms, and growth-focused teams.</p>
            </div>
            <div className="mt-5 flex items-center gap-3">
              {socials.map(({ icon, href, label }) => (
                <a
                  key={label}
                  href={href}
                  aria-label={label}
                  className="inline-flex h-10 w-10 items-center justify-center rounded-xl border border-neutral-200 bg-white text-neutral-700 hover:-translate-y-0.5 hover:border-brand-300 hover:text-brand-700"
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
