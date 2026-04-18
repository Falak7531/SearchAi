import { useState, useCallback, useRef } from "react";
import { searchProducts } from "../services/api";

export function useSearch() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [total, setTotal] = useState(0);
  const [query, setQuery] = useState("");
  const requestRef = useRef(null);

  const performSearch = useCallback(async (searchQuery, options = {}) => {
    if (!searchQuery.trim()) return;
    const requestId = Symbol();
    requestRef.current = requestId;
    setQuery(searchQuery);
    setLoading(true);
    setError(null);
    try {
      const data = await searchProducts(searchQuery, options);
      if (requestRef.current === requestId) {
        setResults(data.results || []);
        setTotal(data.total || (data.results ? data.results.length : 0));
      }
    } catch (err) {
      if (requestRef.current === requestId) {
        setError(err.response?.data?.detail || err.message || "Search failed. Please try again.");
        setResults([]);
        setTotal(0);
      }
    } finally {
      if (requestRef.current === requestId) setLoading(false);
    }
  }, []);

  const clearResults = useCallback(() => {
    setResults([]); setTotal(0); setQuery(""); setError(null);
  }, []);

  return { results, loading, error, total, query, performSearch, clearResults };
}
