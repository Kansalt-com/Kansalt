interface BrandLogoProps {
  className?: string
  iconOnly?: boolean
  dark?: boolean
}

export default function BrandLogo({
  className = '',
  iconOnly = false,
  dark = false,
}: BrandLogoProps) {
  const src = iconOnly ? '/qode27-icon-cropped.png' : '/qode27-wordmark-cropped.png'
  const alt = iconOnly ? 'Qode27 icon logo' : 'Qode27.com logo'

  return (
    <img
      src={src}
      alt={alt}
      className={`${iconOnly ? 'h-11 w-11 object-contain' : 'h-11 w-auto max-w-[16rem] object-contain sm:h-12 sm:max-w-[18rem]'} ${dark && iconOnly ? 'rounded-2xl' : ''} ${className}`.trim()}
      loading="eager"
      decoding="async"
    />
  )
}
