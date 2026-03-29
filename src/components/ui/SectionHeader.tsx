import Reveal from './Reveal'

interface SectionHeaderProps {
  eyebrow?: string
  title: string
  description: string
  align?: 'left' | 'center'
}

export default function SectionHeader({
  eyebrow,
  title,
  description,
  align = 'left',
}: SectionHeaderProps) {
  const alignment = align === 'center' ? 'mx-auto text-center' : ''
  const width = align === 'center' ? 'max-w-3xl' : 'max-w-2xl'

  return (
    <Reveal className={`${width} ${alignment}`.trim()}>
      {eyebrow ? (
        <p className="mb-4 text-xs font-semibold uppercase tracking-[0.28em] text-brand-700">{eyebrow}</p>
      ) : null}
      <h2 className="font-display text-3xl font-semibold text-black">{title}</h2>
      <p className="mt-5 text-base leading-8 text-neutral-600 sm:text-lg">{description}</p>
    </Reveal>
  )
}
