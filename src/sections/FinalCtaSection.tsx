import { FiArrowRight, FiMail } from 'react-icons/fi'
import Button from '../components/ui/Button'
import Container from '../components/ui/Container'
import Reveal from '../components/ui/Reveal'

export default function FinalCtaSection() {
  return (
    <section className="section-spacing">
      <Container>
        <Reveal>
          <div className="relative overflow-hidden rounded-2xl bg-black px-6 py-12 text-white sm:px-8 lg:px-10 lg:py-16">
            <div
              className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,_rgba(211,161,62,0.26),transparent_28%),radial-gradient(circle_at_left,_rgba(45,184,182,0.16),transparent_24%)]"
              aria-hidden="true"
            />
            <div className="relative flex flex-col gap-8 lg:flex-row lg:items-center lg:justify-between">
              <div className="max-w-2xl">
                <p className="text-xs font-semibold uppercase tracking-[0.26em] text-brand-200">Ready to grow</p>
                <h2 className="mt-4 font-display text-3xl font-semibold tracking-[-0.05em] text-white sm:text-4xl lg:text-5xl">
                  Start growing your business with Qode27
                </h2>
                <p className="mt-5 text-base leading-8 text-white/72 sm:text-lg">
                  Modern software and automation built for the way real businesses work.
                </p>
              </div>

              <div className="flex flex-col gap-4 sm:flex-row sm:flex-wrap">
                <Button href="#contact" variant="ghost" className="sm:min-w-[10.5rem]">
                  Book a Demo
                  <FiArrowRight />
                </Button>
                <Button
                  href="mailto:qode27business@gmail.com"
                  variant="secondary"
                  className="border-white/18 bg-white text-black sm:min-w-[10.5rem]"
                >
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
