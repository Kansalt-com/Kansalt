import { FiArrowRight, FiMail } from 'react-icons/fi'
import Button from '../components/ui/Button'
import Container from '../components/ui/Container'
import Reveal from '../components/ui/Reveal'

export default function FinalCtaSection() {
  return (
    <section className="section-spacing">
      <Container>
        <Reveal>
          <div className="relative overflow-hidden rounded-[36px] bg-slate-950 px-6 py-12 text-white sm:px-10 lg:px-14 lg:py-16">
            <div
              className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,_rgba(58,167,255,0.32),transparent_28%),radial-gradient(circle_at_left,_rgba(24,169,153,0.18),transparent_24%)]"
              aria-hidden="true"
            />
            <div className="relative flex flex-col gap-8 lg:flex-row lg:items-center lg:justify-between">
              <div className="max-w-2xl">
                <p className="text-xs font-semibold uppercase tracking-[0.26em] text-brand-200">Ready to grow</p>
                <h2 className="mt-4 font-display text-4xl font-semibold tracking-[-0.05em] text-white sm:text-5xl">
                  Start growing your business with Qode27
                </h2>
                <p className="mt-5 text-base leading-8 text-white/72 sm:text-lg">
                  Modern software and automation built for the way real businesses work.
                </p>
              </div>

              <div className="flex flex-col gap-4 sm:flex-row">
                <Button href="#contact" variant="ghost">
                  Book a Demo
                  <FiArrowRight />
                </Button>
                <Button href="mailto:hello@qode27.com" variant="secondary" className="border-white/18 bg-white text-slate-950">
                  <FiMail />
                  Contact Us
                </Button>
              </div>
            </div>
          </div>
        </Reveal>
      </Container>
    </section>
  )
}
