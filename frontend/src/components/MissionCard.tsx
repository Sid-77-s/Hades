import React from 'react';
import { ChevronRightIcon, PlayCircleIcon } from 'lucide-react';
import { Panel } from './Panel';
import { useHades } from '../services/useHades';

export function MissionCard() {
  const { activeMissionId, hadesState } = useHades();
  const isActive = activeMissionId !== null;

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
      
      {!isActive ? (
        <div className="py-4 text-center text-sm text-slate-500">
          No active missions.
        </div>
      ) : (
        <>
          <h3 className="text-[15px] font-semibold text-white">Mission Executing</h3>

          <p className="mt-2.5 flex items-center gap-2 text-[11px] font-medium text-ion">
            <span className={`h-1.5 w-1.5 rounded-full bg-ion shadow-[0_0_6px_#22d3ee] ${hadesState === 'executing' ? 'animate-pulse' : ''}`} />
            {hadesState === 'executing' ? 'Executing' : 'Active'}
          </p>

          <div className="mt-2.5 flex items-center gap-3">
            <div className="h-1 flex-1 overflow-hidden rounded-full bg-ion/15">
              <div className="h-full rounded-full bg-ion" style={{ width: `50%` }} />
            </div>
            <span className="text-[11px] font-semibold text-slate-300">...</span>
          </div>

          <div className="mt-3.5 border-t border-ion/10 pt-3">
            <p className="text-[10px] uppercase tracking-[0.14em] text-muted">ID</p>
            <div className="mt-1 flex items-baseline justify-between gap-2">
              <p className="text-[10px] font-medium text-slate-400">{activeMissionId}</p>
            </div>
          </div>
        </>
      )}
    </Panel>);
}