import React from 'react';
import { useHades } from '../services/useHades';

export function HadesPresence() {
  const { hadesState } = useHades();
  
  let message = "Hades is here";
  let statusColor = "bg-online shadow-[0_0_8px_#22c55e]";
  
  if (hadesState === 'processing' || hadesState === 'executing') {
    message = "Hades is working";
    statusColor = "bg-ion shadow-[0_0_8px_#0ea5e9] animate-pulse";
  } else if (hadesState === 'error') {
    message = "Hades needs you";
    statusColor = "bg-alert shadow-[0_0_8px_#ef4444]";
  }

  return (
    <div className="flex items-center gap-3 self-start rounded-md border border-ion/25 bg-panel/60 px-4 py-3">
      <div className={`h-2.5 w-2.5 rounded-full ${statusColor}`} />
      <span className="font-display text-[14px] font-semibold tracking-wide text-white">
        {message}
      </span>
    </div>
  );
}
