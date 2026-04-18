import { useState, memo, useCallback } from "react";

function StarRating({ rating }) {
  const stars = [];
  const full = Math.floor(rating);
  const hasHalf = rating - full >= 0.3;
  for (let i = 0; i < 5; i++) {
    if (i < full) stars.push(<span key={i} style={{ color: "var(--color-warning-500)" }}>★</span>);
    else if (i === full && hasHalf) stars.push(<span key={i} style={{ color: "var(--color-warning-500)" }}>★</span>);
    else stars.push(<span key={i} style={{ color: "var(--color-neutral-300)" }}>★</span>);
  }
  return <span style={{ fontSize: "var(--text-sm)", letterSpacing: 1 }}>{stars} <span style={{ color: "var(--color-neutral-500)", fontSize: "var(--text-xs)", fontWeight: 500 }}>{rating.toFixed(1)}</span></span>;
}

const ProductCard = memo(function ProductCard({ product, index = 0 }) {
  const { name, description, category, price, brand, rating, image_url, score, tags = [] } = product;
  const [imageLoaded, setImageLoaded] = useState(false);
  const [hovered, setHovered] = useState(false);

  const truncate = useCallback((str, n) => str && str.length > n ? str.slice(0, n) + "…" : str, []);
  const matchPercent = score ? Math.round(score * 100) : null;

  return (
    <div
      className={`animate-fade-in-up stagger-${Math.min(index + 1, 8)}`}
      style={{
        ...styles.card,
        ...(hovered ? styles.cardHovered : {}),
      }}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      {/* Image */}
      <div style={styles.imageWrapper}>
        {!imageLoaded && <div style={styles.imagePlaceholder} />}
        <img
          src={image_url || `https://placehold.co/400x280/f1f5f9/94a3b8?text=${encodeURIComponent(name)}`}
          alt={name}
          loading="lazy"
          onLoad={() => setImageLoaded(true)}
          style={{
            ...styles.image,
            opacity: imageLoaded ? 1 : 0,
            transform: hovered ? "scale(1.05)" : "scale(1)",
          }}
        />
        {/* Score badge */}
        {matchPercent !== null && (
          <span style={{
            ...styles.scoreBadge,
            background: matchPercent > 70
              ? "linear-gradient(135deg, var(--color-success-500), #16a34a)"
              : matchPercent > 40
                ? "linear-gradient(135deg, var(--color-primary-500), var(--color-accent-500))"
                : "var(--color-neutral-600)",
          }}>
            {matchPercent}% match
          </span>
        )}
        {/* Category pill on image */}
        <span style={styles.categoryOnImage}>{category}</span>
      </div>

      {/* Body */}
      <div style={styles.body}>
        {/* Brand */}
        {brand && <span style={styles.brand}>{brand}</span>}

        {/* Name */}
        <h3 style={styles.name}>{truncate(name, 50)}</h3>

        {/* Description */}
        <p style={styles.description}>{truncate(description, 90)}</p>

        {/* Tags */}
        {tags.length > 0 && (
          <div style={styles.tags}>
            {tags.slice(0, 3).map((tag) => (
              <span key={tag} style={styles.tag}>{tag}</span>
            ))}
          </div>
        )}

        {/* Footer: price + rating */}
        <div style={styles.footer}>
          <div>
            <span style={styles.price}>${price.toFixed(2)}</span>
          </div>
          {rating && <StarRating rating={rating} />}
        </div>

        {/* CTA */}
        <button style={{
          ...styles.cta,
          ...(hovered ? styles.ctaHovered : {}),
        }}>
          View Details
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" style={{ marginLeft: 6, transition: "transform var(--transition-fast)", transform: hovered ? "translateX(3px)" : "translateX(0)" }}>
            <line x1="5" y1="12" x2="19" y2="12" /><polyline points="12 5 19 12 12 19" />
          </svg>
        </button>
      </div>
    </div>
  );
});

export default ProductCard;

const styles = {
  card: {
    background: "#fff",
    borderRadius: "var(--radius-lg)",
    overflow: "hidden",
    boxShadow: "var(--shadow-sm)",
    border: "1px solid var(--color-neutral-100)",
    display: "flex",
    flexDirection: "column",
    transition: "all var(--transition-base)",
    cursor: "pointer",
  },
  cardHovered: {
    boxShadow: "var(--shadow-lg)",
    transform: "translateY(-4px)",
    borderColor: "var(--color-primary-200)",
  },
  imageWrapper: {
    position: "relative",
    overflow: "hidden",
    aspectRatio: "4/3",
    background: "var(--color-neutral-100)",
  },
  imagePlaceholder: {
    position: "absolute",
    inset: 0,
    background: "linear-gradient(90deg, var(--color-neutral-200) 25%, var(--color-neutral-100) 50%, var(--color-neutral-200) 75%)",
    backgroundSize: "200% 100%",
    animation: "shimmer 1.5s ease-in-out infinite",
  },
  image: {
    width: "100%",
    height: "100%",
    objectFit: "cover",
    transition: "all var(--transition-slow)",
  },
  scoreBadge: {
    position: "absolute",
    top: 12,
    right: 12,
    color: "#fff",
    fontSize: "var(--text-xs)",
    fontWeight: 700,
    padding: "4px 10px",
    borderRadius: "var(--radius-full)",
    backdropFilter: "blur(8px)",
    letterSpacing: "0.3px",
  },
  categoryOnImage: {
    position: "absolute",
    bottom: 12,
    left: 12,
    background: "rgba(255,255,255,0.92)",
    backdropFilter: "blur(8px)",
    color: "var(--color-neutral-700)",
    fontSize: "var(--text-xs)",
    fontWeight: 600,
    padding: "4px 10px",
    borderRadius: "var(--radius-full)",
  },
  body: {
    padding: "var(--space-5)",
    display: "flex",
    flexDirection: "column",
    gap: "var(--space-2)",
    flex: 1,
  },
  brand: {
    fontSize: "var(--text-xs)",
    fontWeight: 600,
    color: "var(--color-primary-500)",
    textTransform: "uppercase",
    letterSpacing: "0.5px",
  },
  name: {
    margin: 0,
    fontSize: "var(--text-base)",
    fontWeight: 700,
    color: "var(--color-neutral-800)",
    lineHeight: 1.3,
  },
  description: {
    margin: 0,
    fontSize: "var(--text-sm)",
    color: "var(--color-neutral-500)",
    lineHeight: 1.5,
  },
  tags: {
    display: "flex",
    flexWrap: "wrap",
    gap: "var(--space-1)",
    marginTop: "var(--space-1)",
  },
  tag: {
    background: "var(--color-primary-50)",
    color: "var(--color-primary-600)",
    fontSize: "11px",
    padding: "2px 8px",
    borderRadius: "var(--radius-full)",
    fontWeight: 500,
  },
  footer: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginTop: "auto",
    paddingTop: "var(--space-3)",
  },
  price: {
    fontSize: "var(--text-xl)",
    fontWeight: 800,
    color: "var(--color-neutral-900)",
  },
  cta: {
    display: "inline-flex",
    alignItems: "center",
    justifyContent: "center",
    marginTop: "var(--space-3)",
    padding: "var(--space-3) var(--space-5)",
    background: "var(--color-neutral-900)",
    color: "#fff",
    border: "none",
    borderRadius: "var(--radius-md)",
    fontSize: "var(--text-sm)",
    fontWeight: 600,
    cursor: "pointer",
    transition: "all var(--transition-fast)",
    width: "100%",
  },
  ctaHovered: {
    background: "var(--color-primary-600)",
  },
};
