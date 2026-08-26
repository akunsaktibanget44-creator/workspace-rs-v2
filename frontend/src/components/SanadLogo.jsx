import { cn } from "@/lib/utils";

/**
 * Sanad Logo — shield with crescent + accent dot.
 * Props: size (px), variant ("light" | "dark").
 */
export default function SanadLogo({ size = 40, variant = "dark", className }) {
  const bg = variant === "light" ? "#FFFFFF" : "#064E3B";
  const moon = variant === "light" ? "#064E3B" : "#FFFFFF";
  const dot = "#FBBF24";
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 40 40"
      xmlns="http://www.w3.org/2000/svg"
      className={cn("shrink-0", className)}
      aria-label="Sanad"
      role="img"
    >
      <defs>
        <linearGradient id="sanad-grad" x1="0" x2="1" y1="0" y2="1">
          <stop offset="0" stopColor={bg} />
          <stop offset="1" stopColor={variant === "light" ? "#F0FDF4" : "#022C22"} />
        </linearGradient>
      </defs>
      <rect x="0" y="0" width="40" height="40" rx="10" fill="url(#sanad-grad)" />
      {/* Crescent: outer circle then subtract via inner */}
      <circle cx="22" cy="22" r="11" fill={moon} />
      <circle cx="26" cy="24" r="10" fill={bg} />
      {/* Accent dot */}
      <circle cx="13" cy="13" r="2" fill={dot} />
    </svg>
  );
}
