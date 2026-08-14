import React from 'react';

interface HadesMarkProps {
  size?: number;
  className?: string;
}

export function HadesMark({ size = 28, className = '' }: HadesMarkProps) {
  return (
    <svg
      viewBox="0 0 40 40"
      width={size}
      height={size}
      aria-hidden="true"
      className={className}
      fill="none">
      
      <circle cx="20" cy="20" r="18" stroke="rgba(34,211,238,0.35)" strokeWidth="1" />
      <circle
        cx="20"
        cy="20"
        r="13"
        stroke="rgba(34,211,238,0.55)"
        strokeWidth="1"
        strokeDasharray="5 4" />
      
      <circle cx="20" cy="20" r="7" stroke="#22d3ee" strokeWidth="1.5" />
      <circle cx="20" cy="20" r="2.4" fill="#67e8f9" />
      <path d="M20 1v6M20 33v6M1 20h6M33 20h6" stroke="rgba(34,211,238,0.7)" strokeWidth="1.2" />
    </svg>);

}