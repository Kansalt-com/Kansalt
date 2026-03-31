type GtagWindow = Window & {
  gtag?: (...args: unknown[]) => void
}

export function trackEvent(eventName: string, payload: Record<string, unknown>) {
  const analyticsWindow = window as GtagWindow
  analyticsWindow.gtag?.('event', eventName, payload)
}
