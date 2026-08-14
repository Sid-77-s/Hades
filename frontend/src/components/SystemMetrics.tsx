import React from 'react';
import { Panel } from './Panel';

export function SystemMetrics() {
  return (
    <Panel
      title="System Metrics"
      action={
      <span className="flex items-center gap-1.5 text-[10px] text-muted">
          Live
          <span className="h-1.5 w-1.5 rounded-full bg-ion shadow-[0_0_6px_#22d3ee]" />
        </span>
      }>
      
      <div className="py-4 text-center text-[11px] text-slate-500">
        System metrics are currently unavailable.
      </div>

    </Panel>);
}