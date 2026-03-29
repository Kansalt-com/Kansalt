import Reveal from './Reveal'

export default function SectionHeader({ eyebrow, title, description, align = 'left' }) {
  const alignment = align === 'center' ? 'mx-auto text-center' : ''
  const width = align === 'center' ? 'max-w-3xl' : 'max-w-2xl'

  return (
    <Reveal className={`${width} ${alignment}`.trim()}>
      {eyebrow ? (
        <p className="mb-4 text-xs font-semibold uppercase tracking-[0.28em] text-brand-600">{eyebrow}</p>
      ) : null}
      <h2 className="font-display text-3xl font-semibold tracking-[-0.05em] text-slate-950 sm:text-4xl lg:text-5xl">
        {title}
      </h2>
      <p className="mt-5 text-base leading-8 text-slate-600 sm:text-lg">{description}</p>
    </Reveal>
  )
}
