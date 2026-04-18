import { useNavigate } from "react-router-dom";
import SearchBar from "../components/features/SearchBar";

const SUGGESTED = [
  "wireless headphones",
  "noise cancelling earbuds",
  "4K smart TV",
  "yoga mat",
  "cordless vacuum",
  "running shoes under $100",
];

const FEATURES = [
  {
    icon: (
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="var(--color-primary-500)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
        <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
        <polyline points="3.27 6.96 12 12.01 20.73 6.96" /><line x1="12" y1="22.08" x2="12" y2="12" />
      </svg>
    ),
    title: "Semantic Search",
    desc: "AI understands meaning, not just keywords. Search naturally like you'd ask a friend.",
  },
  {
    icon: (
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="var(--color-accent-500)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
        <polyline points="4 17 10 11 4 5" /><line x1="12" y1="19" x2="20" y2="19" />
      </svg>
    ),
    title: "Keyword Precision",
    desc: "BM25 ranking ensures exact brand names and model numbers always surface.",
  },
  {
    icon: (
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="var(--color-primary-500)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
      </svg>
    ),
    title: "Hybrid Fusion",
    desc: "Best of both worlds — semantic + keyword scores fused with Reciprocal Rank Fusion.",
  },
  {
    icon: (
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="var(--color-accent-500)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
        <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
      </svg>
    ),
    title: "Smart Ranking",
    desc: "Results re-ranked by ratings, stock, and relevance for high-conversion ordering.",
  },
];

const STATS = [
  { value: "450+", label: "Products" },
  { value: "384D", label: "Vectors" },
  { value: "<50ms", label: "Latency" },
  { value: "3", label: "Search Modes" },
];

export default function Home() {
  const navigate = useNavigate();
  const handleSearch = (query) => navigate(`/results?q=${encodeURIComponent(query)}`);

  return (
    <div style={styles.page}>
      {/* Nav */}
      <nav style={styles.nav}>
        <div style={styles.navInner}>
          <div style={styles.navLogo}>
            <div style={styles.logoIcon}>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
              </svg>
            </div>
            <span style={styles.logoText}>SearchAI</span>
          </div>
          <div style={styles.navRight}>
            <span style={styles.navStatus}><span style={styles.navDot} />System Online</span>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section style={styles.hero}>
        <div style={styles.heroContent} className="animate-fade-in-up">
          <div style={styles.badge}><span style={styles.badgeDot} />Powered by Hybrid AI Search</div>
          <h1 style={styles.heading}>
            Find exactly what<br />
            <span style={styles.headingAccent}>you're looking for</span>
          </h1>
          <p style={styles.subtitle}>
            Semantic understanding meets keyword precision — one intelligent search
            that actually gets what you mean.
          </p>
          <SearchBar onSearch={handleSearch} variant="hero" />
          <div style={styles.chips}>
            <span style={styles.chipsLabel}>Popular:</span>
            {SUGGESTED.map((s) => (
              <button key={s} style={styles.chip} onClick={() => handleSearch(s)}>{s}</button>
            ))}
          </div>
        </div>
        <div style={styles.bgShape1} />
        <div style={styles.bgShape2} />
      </section>

      {/* Stats */}
      <section style={styles.statsBar}>
        {STATS.map((s) => (
          <div key={s.label} style={styles.stat}>
            <span style={styles.statValue}>{s.value}</span>
            <span style={styles.statLabel}>{s.label}</span>
          </div>
        ))}
      </section>

      {/* Features */}
      <section style={styles.features}>
        <div style={styles.featuresHeader}>
          <h2 style={styles.featuresTitle}>How it works</h2>
          <p style={styles.featuresSubtitle}>Four layers of intelligence working together to find your perfect product</p>
        </div>
        <div style={styles.featureGrid}>
          {FEATURES.map((f, i) => (
            <div key={f.title} style={styles.featureCard} className={`animate-fade-in-up stagger-${i + 1}`}>
              <div style={styles.featureIconWrap}>{f.icon}</div>
              <h3 style={styles.featureTitle}>{f.title}</h3>
              <p style={styles.featureDesc}>{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer style={styles.footer}>
        <p style={styles.footerText}>Built with FAISS · Sentence Transformers · Groq · FastAPI · React</p>
      </footer>
    </div>
  );
}

const styles = {
  page: { minHeight: "100vh", background: "var(--color-neutral-50)", position: "relative", overflow: "hidden" },
  nav: { position: "fixed", top: 0, left: 0, right: 0, zIndex: 50, background: "rgba(255,255,255,0.8)", backdropFilter: "blur(12px)", borderBottom: "1px solid var(--color-neutral-100)" },
  navInner: { display: "flex", alignItems: "center", justifyContent: "space-between", padding: "var(--space-3) var(--space-8)", maxWidth: 1200, margin: "0 auto" },
  navLogo: { display: "flex", alignItems: "center", gap: "var(--space-3)" },
  logoIcon: { width: 32, height: 32, borderRadius: "var(--radius-sm)", background: "linear-gradient(135deg, var(--color-primary-500), var(--color-accent-500))", display: "flex", alignItems: "center", justifyContent: "center" },
  logoText: { fontSize: "var(--text-lg)", fontWeight: 800, color: "var(--color-neutral-900)", letterSpacing: "-0.5px" },
  navRight: { display: "flex", alignItems: "center", gap: "var(--space-4)" },
  navStatus: { display: "flex", alignItems: "center", gap: "var(--space-2)", fontSize: "var(--text-xs)", fontWeight: 600, color: "var(--color-neutral-500)" },
  navDot: { width: 7, height: 7, borderRadius: "var(--radius-full)", background: "var(--color-success-500)", animation: "pulse 2s infinite", display: "inline-block" },
  hero: { position: "relative", display: "flex", alignItems: "center", justifyContent: "center", minHeight: "75vh", padding: "120px var(--space-8) var(--space-12)" },
  heroContent: { display: "flex", flexDirection: "column", alignItems: "center", textAlign: "center", maxWidth: 780, width: "100%", position: "relative", zIndex: 1 },
  badge: { display: "inline-flex", alignItems: "center", gap: "var(--space-2)", background: "var(--color-primary-50)", color: "var(--color-primary-600)", fontSize: "var(--text-xs)", fontWeight: 700, padding: "var(--space-2) var(--space-4)", borderRadius: "var(--radius-full)", marginBottom: "var(--space-6)", border: "1px solid var(--color-primary-100)" },
  badgeDot: { width: 6, height: 6, borderRadius: "var(--radius-full)", background: "var(--color-primary-500)", animation: "pulse 2s infinite", display: "inline-block" },
  heading: { fontSize: "clamp(2.5rem, 5.5vw, 4rem)", fontWeight: 900, color: "var(--color-neutral-900)", lineHeight: 1.1, letterSpacing: "-1.5px", marginBottom: "var(--space-6)" },
  headingAccent: { background: "linear-gradient(135deg, var(--color-primary-500), var(--color-accent-500))", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent", backgroundClip: "text" },
  subtitle: { fontSize: "var(--text-lg)", color: "var(--color-neutral-500)", lineHeight: 1.6, maxWidth: 560, marginBottom: "var(--space-10)" },
  chips: { display: "flex", flexWrap: "wrap", gap: "var(--space-2)", justifyContent: "center", marginTop: "var(--space-6)", alignItems: "center" },
  chipsLabel: { fontSize: "var(--text-xs)", color: "var(--color-neutral-400)", fontWeight: 600 },
  chip: { background: "#fff", border: "1px solid var(--color-neutral-200)", borderRadius: "var(--radius-full)", padding: "var(--space-2) var(--space-4)", fontSize: "var(--text-xs)", color: "var(--color-neutral-600)", cursor: "pointer", transition: "all var(--transition-fast)", fontWeight: 500 },
  bgShape1: { position: "absolute", top: "10%", right: "-5%", width: 400, height: 400, borderRadius: "50%", background: "radial-gradient(circle, rgba(99,102,241,0.08) 0%, transparent 70%)", pointerEvents: "none" },
  bgShape2: { position: "absolute", bottom: "5%", left: "-5%", width: 300, height: 300, borderRadius: "50%", background: "radial-gradient(circle, rgba(139,92,246,0.06) 0%, transparent 70%)", pointerEvents: "none" },
  statsBar: { display: "flex", justifyContent: "center", gap: "var(--space-12)", padding: "var(--space-10) var(--space-8)", borderTop: "1px solid var(--color-neutral-100)", borderBottom: "1px solid var(--color-neutral-100)", background: "#fff", flexWrap: "wrap" },
  stat: { display: "flex", flexDirection: "column", alignItems: "center", gap: "var(--space-1)" },
  statValue: { fontSize: "var(--text-2xl)", fontWeight: 800, color: "var(--color-neutral-900)" },
  statLabel: { fontSize: "var(--text-xs)", fontWeight: 600, color: "var(--color-neutral-400)", textTransform: "uppercase", letterSpacing: "0.5px" },
  features: { padding: "var(--space-20) var(--space-8)", maxWidth: 1100, margin: "0 auto" },
  featuresHeader: { textAlign: "center", marginBottom: "var(--space-12)" },
  featuresTitle: { fontSize: "var(--text-3xl)", fontWeight: 800, color: "var(--color-neutral-900)", letterSpacing: "-0.5px", marginBottom: "var(--space-3)" },
  featuresSubtitle: { fontSize: "var(--text-base)", color: "var(--color-neutral-500)", maxWidth: 480, margin: "0 auto" },
  featureGrid: { display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: "var(--space-6)" },
  featureCard: { background: "#fff", borderRadius: "var(--radius-lg)", padding: "var(--space-8) var(--space-6)", border: "1px solid var(--color-neutral-100)", textAlign: "center", transition: "all var(--transition-base)" },
  featureIconWrap: { width: 56, height: 56, borderRadius: "var(--radius-lg)", background: "var(--color-primary-50)", display: "flex", alignItems: "center", justifyContent: "center", margin: "0 auto var(--space-5)" },
  featureTitle: { margin: "0 0 var(--space-2)", fontSize: "var(--text-base)", fontWeight: 700, color: "var(--color-neutral-800)" },
  featureDesc: { margin: 0, fontSize: "var(--text-sm)", color: "var(--color-neutral-500)", lineHeight: 1.6 },
  footer: { textAlign: "center", padding: "var(--space-10) var(--space-8)", borderTop: "1px solid var(--color-neutral-100)" },
  footerText: { fontSize: "var(--text-xs)", color: "var(--color-neutral-400)", fontWeight: 500 },
};
