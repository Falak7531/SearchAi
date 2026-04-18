export default function EmptyState({ query }) {
  return (
    <div style={styles.container} className="animate-fade-in">
      <div style={styles.iconWrapper}>
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="var(--color-neutral-400)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
          <line x1="8" y1="11" x2="14" y2="11" />
        </svg>
      </div>
      <h3 style={styles.title}>No products found</h3>
      <p style={styles.message}>
        We couldn't find anything matching <strong>"{query}"</strong>.
        <br />Try different keywords or remove some filters.
      </p>
      <div style={styles.suggestions}>
        <span style={styles.tip}>💡 Tips:</span>
        <ul style={styles.tipList}>
          <li>Use broader search terms</li>
          <li>Check for typos</li>
          <li>Try natural language like "comfortable running shoes"</li>
        </ul>
      </div>
    </div>
  );
}

const styles = {
  container: {
    display: "flex", flexDirection: "column", alignItems: "center",
    justifyContent: "center", padding: "var(--space-16) var(--space-8)", textAlign: "center",
  },
  iconWrapper: {
    width: 80, height: 80, borderRadius: "var(--radius-full)",
    background: "var(--color-neutral-100)", display: "flex",
    alignItems: "center", justifyContent: "center", marginBottom: "var(--space-6)",
  },
  title: {
    fontSize: "var(--text-xl)", fontWeight: 700, color: "var(--color-neutral-800)",
    marginBottom: "var(--space-2)",
  },
  message: {
    fontSize: "var(--text-sm)", color: "var(--color-neutral-500)",
    maxWidth: 400, lineHeight: 1.7, marginBottom: "var(--space-6)",
  },
  suggestions: {
    background: "var(--color-primary-50)", borderRadius: "var(--radius-lg)",
    padding: "var(--space-5) var(--space-6)", textAlign: "left", maxWidth: 360,
  },
  tip: { fontSize: "var(--text-sm)", fontWeight: 600, color: "var(--color-primary-600)" },
  tipList: {
    margin: "var(--space-2) 0 0 var(--space-5)", fontSize: "var(--text-sm)",
    color: "var(--color-neutral-600)", lineHeight: 1.8, listStyle: "disc",
  },
};
