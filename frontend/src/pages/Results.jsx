import { useEffect, useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import Header from "../components/layout/Header";
import SearchBar from "../components/features/SearchBar";
import ProductCard from "../components/features/ProductCard";
import ProductGrid from "../components/features/ProductGrid";
import Filters from "../components/features/Filters";
import ErrorState from "../components/ui/ErrorState";
import EmptyState from "../components/ui/EmptyState";
import { useSearch } from "../hooks/useSearch";

export default function Results() {
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();
  const { results, loading, error, total, query, performSearch } = useSearch();
  const [selectedCategory, setSelectedCategory] = useState(null);
  const urlQuery = searchParams.get("q") || "";

  useEffect(() => {
    if (urlQuery) performSearch(urlQuery, { category: selectedCategory, top_k: 12 });
  }, [urlQuery, selectedCategory]);

  const handleSearch = (newQuery) => { setSearchParams({ q: newQuery }); setSelectedCategory(null); };
  const handleCategoryChange = (cat) => setSelectedCategory(cat);
  const handleRetry = () => { if (urlQuery) performSearch(urlQuery, { category: selectedCategory, top_k: 12 }); };

  return (
    <div style={styles.page}>
      <Header>
        <SearchBar onSearch={handleSearch} loading={loading} initialValue={urlQuery} variant="compact" />
      </Header>

      <div style={styles.body}>
        {/* Sidebar */}
        <Filters selectedCategory={selectedCategory || "All"} onCategoryChange={handleCategoryChange} />

        {/* Main */}
        <main style={styles.main}>
          {/* Results summary */}
          {!loading && query && !error && results.length > 0 && (
            <div style={styles.summaryBar} className="animate-fade-in">
              <p style={styles.summaryText}>
                <span style={styles.summaryCount}>{total}</span> results for
                <span style={styles.summaryQuery}> "{query}"</span>
                {selectedCategory && <span style={styles.summaryCategory}> in {selectedCategory}</span>}
              </p>
              <div style={styles.aiLabel}>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--color-primary-500)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
                </svg>
                <span>AI-Ranked Results</span>
              </div>
            </div>
          )}

          {/* Error */}
          {error && <ErrorState message={error} onRetry={handleRetry} />}

          {/* Loading skeleton grid */}
          {loading && <ProductGrid loading={true} />}

          {/* Results */}
          {!loading && !error && results.length > 0 && (
            <ProductGrid products={
              results.map((product, i) => (
                <ProductCard key={product.id} product={product} index={i} />
              ))
            } />
          )}

          {/* Empty */}
          {!loading && !error && results.length === 0 && query && (
            <EmptyState query={query} />
          )}
        </main>
      </div>
    </div>
  );
}

const styles = {
  page: { minHeight: "100vh", background: "var(--color-neutral-50)" },
  body: {
    display: "flex",
    gap: "var(--space-8)",
    padding: "var(--space-8)",
    maxWidth: 1440,
    margin: "0 auto",
  },
  main: { flex: 1, minWidth: 0 },
  summaryBar: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "var(--space-6)",
    padding: "var(--space-4) var(--space-5)",
    background: "#fff",
    borderRadius: "var(--radius-lg)",
    border: "1px solid var(--color-neutral-100)",
  },
  summaryText: {
    margin: 0,
    fontSize: "var(--text-sm)",
    color: "var(--color-neutral-500)",
  },
  summaryCount: {
    fontWeight: 700,
    color: "var(--color-neutral-800)",
  },
  summaryQuery: {
    fontWeight: 600,
    color: "var(--color-neutral-700)",
  },
  summaryCategory: {
    color: "var(--color-primary-500)",
    fontWeight: 600,
  },
  aiLabel: {
    display: "flex",
    alignItems: "center",
    gap: "var(--space-2)",
    fontSize: "var(--text-xs)",
    fontWeight: 600,
    color: "var(--color-primary-500)",
    background: "var(--color-primary-50)",
    padding: "var(--space-1) var(--space-3)",
    borderRadius: "var(--radius-full)",
  },
};
