const baseStyles =
  'inline-flex items-center gap-2 rounded-full font-semibold transition duration-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-300'

const variants = {
  primary:
    'bg-slate-950 px-6 py-3 text-white shadow-[0_12px_30px_rgba(15,23,42,0.18)] hover:-translate-y-0.5 hover:bg-brand-600',
  secondary:
    'border border-slate-200 bg-white px-6 py-3 text-slate-900 hover:-translate-y-0.5 hover:border-brand-300 hover:text-brand-600',
  ghost:
    'border border-white/60 bg-white/80 px-5 py-3 text-slate-900 hover:-translate-y-0.5 hover:border-brand-300 hover:bg-white',
}

const sizes = {
  sm: 'text-sm',
  md: 'text-sm sm:text-base',
}

export default function Button({
  children,
  href,
  variant = 'primary',
  size = 'md',
  className = '',
}) {
  const classes = `${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`.trim()

  if (href) {
    return (
      <a href={href} className={classes}>
        {children}
      </a>
    )
  }

  return (
    <button type="button" className={classes}>
      {children}
    </button>
  )
}
