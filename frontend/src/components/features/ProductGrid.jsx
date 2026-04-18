import { SkeletonCard } from "../ui/Skeleton";

export default function ProductGrid({ products, loading, columns = 3 }) {
  if (loading) {
    return (
      <div style={{ ...styles.grid, gridTemplateColumns: `repeat(auto-fill, minmax(280px, 1fr))` }}>
        {Array.from({ length: 6 }).map((_, i) => (
          <SkeletonCard key={i} />
        ))}
      </div>
    );
  }

  return (
    <div style={{ ...styles.grid, gridTemplateColumns: `repeat(auto-fill, minmax(280px, 1fr))` }}>
      {products}
    </div>
  );
}

const styles = {
  grid: {
    display: "grid",
    gap: "var(--space-6)",
    width: "100%",
  },
};
