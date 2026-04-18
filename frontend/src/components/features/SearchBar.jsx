import { useState, useEffect, useRef, useCallback } from "react";

const SUGGESTIONS = [
  "wireless bluetooth headphones",
  "noise cancelling earbuds",
  "4K smart TV under $500",
  "comfortable yoga mat",
  "cordless vacuum cleaner",
  "running shoes for men",
  "waterproof jacket",
  "gaming keyboard mechanical",
];

export default function SearchBar({ onSearch, loading = false, initialValue = "", variant = "default" }) {
  const [inputValue, setInputValue] = useState(initialValue);
  const [isFocused, setIsFocused] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [filteredSuggestions, setFilteredSuggestions] = useState([]);
  const inputRef = useRef(null);
  const formRef = useRef(null);

  useEffect(() => { if (variant === "hero") inputRef.current?.focus(); }, [variant]);
  useEffect(() => { setInputValue(initialValue); }, [initialValue]);

  useEffect(() => {
    if (inputValue.length > 0 && isFocused) {
      const filtered = SUGGESTIONS.filter(s =>
        s.toLowerCase().includes(inputValue.toLowerCase()) && s.toLowerCase() !== inputValue.toLowerCase()
      ).slice(0, 5);
      setFilteredSuggestions(filtered);
      setShowSuggestions(filtered.length > 0);
    } else {
      setShowSuggestions(false);
    }
  }, [inputValue, isFocused]);

  // Close suggestions on outside click
  useEffect(() => {
    const handleClick = (e) => {
      if (formRef.current && !formRef.current.contains(e.target)) setShowSuggestions(false);
    };
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  const handleSubmit = useCallback((e) => {
    e.preventDefault();
    if (inputValue.trim()) { onSearch(inputValue.trim()); setShowSuggestions(false); }
  }, [inputValue, onSearch]);

  const handleSuggestionClick = useCallback((s) => {
    setInputValue(s);
    onSearch(s);
    setShowSuggestions(false);
  }, [onSearch]);

  const handleClear = () => { setInputValue(""); inputRef.current?.focus(); };

  const isHero = variant === "hero";

  return (
    <form ref={formRef} onSubmit={handleSubmit} role="search" style={{
      ...styles.form,
      ...(isHero ? styles.formHero : {}),
    }}>
      <div style={{
        ...styles.inputContainer,
        ...(isFocused ? styles.inputContainerFocused : {}),
        ...(isHero ? styles.inputContainerHero : {}),
      }}>
        {/* Search icon */}
        <div style={styles.iconLeft}>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke={isFocused ? "var(--color-primary-500)" : "var(--color-neutral-400)"} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ transition: "stroke var(--transition-fast)" }}>
            <circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
          </svg>
        </div>

        <input
          ref={inputRef}
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setTimeout(() => setIsFocused(false), 150)}
          placeholder={isHero ? "Search with AI — try 'comfortable running shoes under $100'" : "Search products..."}
          aria-label="Search products"
          style={{ ...styles.input, ...(isHero ? styles.inputHero : {}) }}
        />

        {/* AI badge inside input */}
        {isHero && !inputValue && (
          <span style={styles.aiBadge}>AI</span>
        )}

        {/* Clear button */}
        {inputValue && (
          <button type="button" onClick={handleClear} style={styles.clearBtn} aria-label="Clear search">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
        )}

        {/* Submit button inside input */}
        <button type="submit" disabled={loading || !inputValue.trim()} style={{
          ...styles.submitBtn,
          ...(loading || !inputValue.trim() ? styles.submitBtnDisabled : {}),
        }}>
          {loading ? (
            <div style={styles.spinner} />
          ) : (
            <>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
              </svg>
              <span style={{ marginLeft: 6 }}>{isHero ? "Search" : ""}</span>
            </>
          )}
        </button>

        {/* Autocomplete dropdown */}
        {showSuggestions && (
          <div style={styles.suggestions} className="animate-slide-down">
            {filteredSuggestions.map((s) => (
              <button key={s} type="button" onClick={() => handleSuggestionClick(s)} style={styles.suggestionItem}>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--color-neutral-400)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ flexShrink: 0 }}>
                  <circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
                </svg>
                <span>{s}</span>
              </button>
            ))}
          </div>
        )}
      </div>
    </form>
  );
}

const styles = {
  form: {
    width: "100%",
    maxWidth: 680,
    position: "relative",
  },
  formHero: {
    maxWidth: 720,
  },
  inputContainer: {
    position: "relative",
    display: "flex",
    alignItems: "center",
    background: "#fff",
    borderRadius: "var(--radius-lg)",
    border: "2px solid var(--color-neutral-200)",
    transition: "all var(--transition-fast)",
    boxShadow: "var(--shadow-sm)",
  },
  inputContainerFocused: {
    borderColor: "var(--color-primary-400)",
    boxShadow: "0 0 0 4px rgba(99, 102, 241, 0.1), var(--shadow-md)",
  },
  inputContainerHero: {
    borderRadius: "var(--radius-xl)",
    border: "2px solid var(--color-neutral-200)",
    boxShadow: "var(--shadow-lg)",
  },
  iconLeft: {
    position: "absolute",
    left: 16,
    display: "flex",
    alignItems: "center",
    pointerEvents: "none",
    zIndex: 1,
  },
  input: {
    width: "100%",
    padding: "14px 120px 14px 48px",
    fontSize: "var(--text-base)",
    border: "none",
    outline: "none",
    background: "transparent",
    color: "var(--color-neutral-800)",
    fontFamily: "var(--font-sans)",
  },
  inputHero: {
    padding: "18px 140px 18px 48px",
    fontSize: "var(--text-lg)",
  },
  aiBadge: {
    position: "absolute",
    right: 120,
    background: "linear-gradient(135deg, var(--color-primary-500), var(--color-accent-500))",
    color: "#fff",
    fontSize: "10px",
    fontWeight: 800,
    padding: "3px 8px",
    borderRadius: "var(--radius-full)",
    letterSpacing: "0.5px",
    pointerEvents: "none",
  },
  clearBtn: {
    position: "absolute",
    right: 100,
    background: "none",
    border: "none",
    cursor: "pointer",
    color: "var(--color-neutral-400)",
    padding: 4,
    display: "flex",
    alignItems: "center",
    transition: "color var(--transition-fast)",
  },
  submitBtn: {
    position: "absolute",
    right: 6,
    display: "inline-flex",
    alignItems: "center",
    justifyContent: "center",
    padding: "10px 20px",
    background: "var(--color-primary-500)",
    color: "#fff",
    border: "none",
    borderRadius: "var(--radius-md)",
    fontSize: "var(--text-sm)",
    fontWeight: 600,
    cursor: "pointer",
    transition: "all var(--transition-fast)",
    whiteSpace: "nowrap",
    minWidth: 44,
  },
  submitBtnDisabled: {
    opacity: 0.5,
    cursor: "not-allowed",
  },
  spinner: {
    width: 18,
    height: 18,
    border: "2px solid rgba(255,255,255,0.3)",
    borderTopColor: "#fff",
    borderRadius: "50%",
    animation: "spin 0.6s linear infinite",
  },
  suggestions: {
    position: "absolute",
    top: "calc(100% + 6px)",
    left: 0,
    right: 0,
    background: "#fff",
    borderRadius: "var(--radius-lg)",
    boxShadow: "var(--shadow-lg)",
    border: "1px solid var(--color-neutral-200)",
    zIndex: 50,
    overflow: "hidden",
  },
  suggestionItem: {
    display: "flex",
    alignItems: "center",
    gap: "var(--space-3)",
    width: "100%",
    padding: "var(--space-3) var(--space-4)",
    background: "none",
    border: "none",
    cursor: "pointer",
    fontSize: "var(--text-sm)",
    color: "var(--color-neutral-600)",
    textAlign: "left",
    transition: "background var(--transition-fast)",
  },
};

// Add spin keyframe
if (typeof document !== "undefined") {
  const style = document.createElement("style");
  style.textContent = `@keyframes spin { to { transform: rotate(360deg); } }`;
  document.head.appendChild(style);
}
