export default function Container({ children, className = '' }) {
  return <div className={`section-shell ${className}`.trim()}>{children}</div>
}
