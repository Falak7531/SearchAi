export default function ErrorState({ message, onRetry }) {
  return (
    <div style={styles.container} className="animate-fade-in">
      <div style={styles.iconWrapper}>
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="var(--color-error-500)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="12" cy="12" r="10" />
          <line x1="12" y1="8" x2="12" y2="12" />
          <line x1="12" y1="16" x2="12.01" y2="16" />
        </svg>
      </div>
      <h3 style={styles.title}>Something went wrong</h3>
      <p style={styles.message}>{message || "An unexpected error occurred. Please try again."}</p>
      {onRetry && (
        <button onClick={onRetry} style={styles.retryButton}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ marginRight: 6 }}>
            <polyline points="23 4 23 10 17 10" /><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10" />
          </svg>
          Try Again
        </button>
      )}
    </div>
  );
}

const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    padding: "var(--space-16) var(--space-8)",
    textAlign: "center",
  },
  iconWrapper: {
    width: 80, height: 80, borderRadius: "var(--radius-full)",
    background: "var(--color-error-50)", display: "flex",
    alignItems: "center", justifyContent: "center", marginBottom: "var(--space-6)",
  },
  title: {
    fontSize: "var(--text-xl)", fontWeight: 700, color: "var(--color-neutral-800)",
    marginBottom: "var(--space-2)",
  },
  message: {
    fontSize: "var(--text-sm)", color: "var(--color-neutral-500)",
    maxWidth: 400, lineHeight: 1.6, marginBottom: "var(--space-6)",
  },
  retryButton: {
    display: "inline-flex", alignItems: "center",
    padding: "var(--space-3) var(--space-6)",
    background: "var(--color-primary-500)", color: "#fff",
    border: "none", borderRadius: "var(--radius-md)",
    fontSize: "var(--text-sm)", fontWeight: 600, cursor: "pointer",
    transition: "background var(--transition-fast)",
  },
};
