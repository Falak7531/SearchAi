import { useNavigate } from "react-router-dom";

export default function Header({ children }) {
  const navigate = useNavigate();

  return (
    <header style={styles.header}>
      <div style={styles.inner}>
        <div style={styles.logo} onClick={() => navigate("/")}>
          <div style={styles.logoIcon}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
            </svg>
          </div>
          <span style={styles.logoText}>SearchAI</span>
        </div>
        <div style={styles.searchSlot}>{children}</div>
        <div style={styles.actions}>
          <span style={styles.statusDot} />
          <span style={styles.statusText}>AI Active</span>
        </div>
      </div>
    </header>
  );
}

const styles = {
  header: {
    position: "sticky",
    top: 0,
    zIndex: 100,
    background: "rgba(255, 255, 255, 0.85)",
    backdropFilter: "blur(12px)",
    borderBottom: "1px solid var(--color-neutral-100)",
  },
  inner: {
    display: "flex",
    alignItems: "center",
    gap: "var(--space-6)",
    padding: "var(--space-3) var(--space-8)",
    maxWidth: 1440,
    margin: "0 auto",
  },
  logo: {
    display: "flex",
    alignItems: "center",
    gap: "var(--space-3)",
    cursor: "pointer",
    flexShrink: 0,
  },
  logoIcon: {
    width: 36,
    height: 36,
    borderRadius: "var(--radius-md)",
    background: "linear-gradient(135deg, var(--color-primary-500), var(--color-accent-500))",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },
  logoText: {
    fontSize: "var(--text-lg)",
    fontWeight: 800,
    color: "var(--color-neutral-900)",
    letterSpacing: "-0.5px",
  },
  searchSlot: { flex: 1, display: "flex", justifyContent: "center" },
  actions: {
    display: "flex",
    alignItems: "center",
    gap: "var(--space-2)",
    flexShrink: 0,
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: "var(--radius-full)",
    background: "var(--color-success-500)",
    animation: "pulse 2s infinite",
  },
  statusText: {
    fontSize: "var(--text-xs)",
    fontWeight: 600,
    color: "var(--color-neutral-500)",
  },
};
