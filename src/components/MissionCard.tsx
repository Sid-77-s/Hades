import React from 'react';
import { ChevronRightIcon, PlayCircleIcon } from 'lucide-react';
import { Panel } from './Panel';

export function MissionCard() {
  const progress = 42;

  return (
    <Panel
      title="Active Mission"
      action={
      <button
        type="button"
        className="text-muted transition-colors duration-150 ease-out hover:text-ion focus:outline-none focus-visible:ring-1 focus-visible:ring-ion"
        aria-label="Open missions">
        
          <ChevronRightIcon size={14} strokeWidth={2} />
        </button>
      }>
      
      <h3 className="text-[15px] font-semibold text-white">AI OS Dashboard</h3>

      <p className="mt-2.5 flex items-center gap-2 text-[11px] font-medium text-ion">
        <span className="h-1.5 w-1.5 rounded-full bg-ion shadow-[0_0_6px_#22d3ee]" />
        Planning
      </p>

      <div className="mt-2.5 flex items-center gap-3">
        <div className="h-1 flex-1 overflow-hidden rounded-full bg-ion/15">
          <div className="h-full rounded-full bg-ion" style={{ width: `${progress}%` }} />
        </div>
        <span className="text-[11px] font-semibold text-slate-300">{progress}%</span>
      </div>

      <div className="mt-3.5 border-t border-ion/10 pt-3">
        <p className="text-[10px] uppercase tracking-[0.14em] text-muted">Next step</p>
        <div className="mt-1 flex items-baseline justify-between gap-2">
          <p className="text-[12px] font-medium text-slate-200">Design system architecture</p>
          <span className="shrink-0 text-[10px] text-muted">ETA 18m</span>
        </div>
      </div>

      <button
        type="button"
        className="mt-3.5 flex w-full items-center justify-center gap-2 rounded-md border border-ion/30 bg-ion/[0.07] py-2 text-[12px] font-medium text-ion-soft transition-colors duration-150 ease-out hover:border-ion/60 hover:text-white focus:outline-none focus-visible:ring-1 focus-visible:ring-ion">
        
        <PlayCircleIcon size={14} strokeWidth={1.75} />
        View Mission
      </button>
    </Panel>);

}