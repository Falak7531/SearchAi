import { memo } from "react";

const SKELETON_STYLES = {
  base: {
    background: "linear-gradient(90deg, var(--color-neutral-200) 25%, var(--color-neutral-100) 50%, var(--color-neutral-200) 75%)",
    backgroundSize: "200% 100%",
    animation: "shimmer 1.5s ease-in-out infinite",
    borderRadius: "var(--radius-md)",
  },
};

export const SkeletonCard = memo(function SkeletonCard() {
  return (
    <div style={{
      background: "#fff",
      borderRadius: "var(--radius-lg)",
      overflow: "hidden",
      boxShadow: "var(--shadow-sm)",
    }}>
      <div style={{ ...SKELETON_STYLES.base, height: 200, borderRadius: 0 }} />
      <div style={{ padding: "var(--space-5)" }}>
        <div style={{ ...SKELETON_STYLES.base, height: 12, width: "40%", marginBottom: "var(--space-3)" }} />
        <div style={{ ...SKELETON_STYLES.base, height: 16, width: "80%", marginBottom: "var(--space-2)" }} />
        <div style={{ ...SKELETON_STYLES.base, height: 14, width: "100%", marginBottom: "var(--space-2)" }} />
        <div style={{ ...SKELETON_STYLES.base, height: 14, width: "60%", marginBottom: "var(--space-4)" }} />
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <div style={{ ...SKELETON_STYLES.base, height: 24, width: "30%" }} />
          <div style={{ ...SKELETON_STYLES.base, height: 18, width: "20%" }} />
        </div>
        <div style={{ ...SKELETON_STYLES.base, height: 42, width: "100%", marginTop: "var(--space-3)", borderRadius: "var(--radius-md)" }} />
      </div>
    </div>
  );
});

export const SkeletonText = memo(function SkeletonText({ width = "100%", height = 14 }) {
  return <div style={{ ...SKELETON_STYLES.base, height, width, marginBottom: "var(--space-2)" }} />;
});
