import { useState } from "react";

const CATEGORIES = [
  { label: "All", icon: "📦" },
  { label: "Electronics", icon: "💻" },
  { label: "Footwear", icon: "👟" },
  { label: "Clothing", icon: "👕" },
  { label: "Kitchen", icon: "🍳" },
  { label: "Sports", icon: "⚽" },
  { label: "Home", icon: "🏠" },
];

export default function Filters({ selectedCategory = "All", onCategoryChange }) {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside style={styles.sidebar} className="animate-fade-in">
      <div style={styles.header}>
        <h3 style={styles.heading}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ marginRight: 8 }}>
            <line x1="4" y1="21" x2="4" y2="14" /><line x1="4" y1="10" x2="4" y2="3" />
            <line x1="12" y1="21" x2="12" y2="12" /><line x1="12" y1="8" x2="12" y2="3" />
            <line x1="20" y1="21" x2="20" y2="16" /><line x1="20" y1="12" x2="20" y2="3" />
          </svg>
          Filters
        </h3>
        <button onClick={() => setCollapsed(!collapsed)} style={styles.collapseBtn} aria-label="Toggle filters">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ transform: collapsed ? "rotate(180deg)" : "rotate(0deg)", transition: "transform var(--transition-fast)" }}>
            <polyline points="18 15 12 9 6 15" />
          </svg>
        </button>
      </div>

      {!collapsed && (
        <div className="animate-slide-down">
          <div style={styles.section}>
            <h4 style={styles.label}>Category</h4>
            <ul style={styles.list}>
              {CATEGORIES.map(({ label, icon }) => {
                const isActive = selectedCategory === label;
                return (
                  <li key={label}>
                    <button
                      style={{ ...styles.catBtn, ...(isActive ? styles.catBtnActive : {}) }}
                      onClick={() => onCategoryChange(label === "All" ? null : label)}
                    >
                      <span style={styles.catIcon}>{icon}</span>
                      <span>{label}</span>
                      {isActive && (
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" style={{ marginLeft: "auto" }}>
                          <polyline points="20 6 9 17 4 12" />
                        </svg>
                      )}
                    </button>
                  </li>
                );
              })}
            </ul>
          </div>

          <div style={styles.divider} />

          <div style={styles.section}>
            <h4 style={styles.label}>Search Type</h4>
            <div style={styles.typeInfo}>
              <div style={styles.typeItem}>
                <span style={{ ...styles.typeDot, background: "var(--color-primary-500)" }} />
                <span style={styles.typeText}>Hybrid AI</span>
              </div>
              <p style={styles.typeDesc}>Combines semantic understanding with keyword matching for best results</p>
            </div>
          </div>
        </div>
      )}
    </aside>
  );
}

const styles = {
  sidebar: {
    width: 240,
    flexShrink: 0,
    background: "#fff",
    borderRadius: "var(--radius-lg)",
    padding: "var(--space-5)",
    boxShadow: "var(--shadow-sm)",
    border: "1px solid var(--color-neutral-100)",
    alignSelf: "flex-start",
    position: "sticky",
    top: 88,
  },
  header: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    marginBottom: "var(--space-5)",
  },
  heading: {
    display: "flex",
    alignItems: "center",
    margin: 0,
    fontSize: "var(--text-base)",
    fontWeight: 700,
    color: "var(--color-neutral-800)",
  },
  collapseBtn: {
    background: "none",
    border: "none",
    cursor: "pointer",
    color: "var(--color-neutral-400)",
    padding: 4,
    display: "flex",
  },
  section: { marginBottom: "var(--space-4)" },
  label: {
    fontSize: "var(--text-xs)",
    fontWeight: 600,
    color: "var(--color-neutral-400)",
    textTransform: "uppercase",
    letterSpacing: "0.5px",
    marginBottom: "var(--space-3)",
    margin: "0 0 var(--space-3) 0",
  },
  list: {
    listStyle: "none",
    margin: 0,
    padding: 0,
    display: "flex",
    flexDirection: "column",
    gap: "var(--space-1)",
  },
  catBtn: {
    width: "100%",
    display: "flex",
    alignItems: "center",
    gap: "var(--space-3)",
    textAlign: "left",
    background: "none",
    border: "none",
    padding: "var(--space-2) var(--space-3)",
    borderRadius: "var(--radius-md)",
    cursor: "pointer",
    fontSize: "var(--text-sm)",
    color: "var(--color-neutral-600)",
    transition: "all var(--transition-fast)",
    fontWeight: 500,
  },
  catBtnActive: {
    background: "var(--color-primary-50)",
    color: "var(--color-primary-600)",
    fontWeight: 600,
  },
  catIcon: { fontSize: "16px" },
  divider: {
    height: 1,
    background: "var(--color-neutral-100)",
    margin: "var(--space-4) 0",
  },
  typeInfo: {},
  typeItem: {
    display: "flex",
    alignItems: "center",
    gap: "var(--space-2)",
    marginBottom: "var(--space-2)",
  },
  typeDot: {
    width: 8,
    height: 8,
    borderRadius: "var(--radius-full)",
  },
  typeText: {
    fontSize: "var(--text-sm)",
    fontWeight: 600,
    color: "var(--color-neutral-700)",
  },
  typeDesc: {
    margin: 0,
    fontSize: "var(--text-xs)",
    color: "var(--color-neutral-400)",
    lineHeight: 1.5,
  },
};
