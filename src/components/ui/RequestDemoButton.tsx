import { useState } from 'react'
import type { DemoAppConfig } from '../../config/apps'
import Button from './Button'
import LeadCaptureModal from './LeadCaptureModal'

type RequestDemoButtonProps = {
  app: DemoAppConfig
  label?: string
  variant?: 'primary' | 'secondary' | 'ghost'
  size?: 'sm' | 'md'
  className?: string
}

export default function RequestDemoButton({
  app,
  label = 'Request Demo',
  variant = 'primary',
  size = 'md',
  className = '',
}: RequestDemoButtonProps) {
  const [open, setOpen] = useState(false)

  return (
    <>
      <Button variant={variant} size={size} className={className} onClick={() => setOpen(true)}>
        {label}
      </Button>
      <LeadCaptureModal app={app} open={open} onClose={() => setOpen(false)} />
    </>
  )
}
