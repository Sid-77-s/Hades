import React from 'react';
import { metrics, throughput } from '../data/dashboard';
import { Panel } from './Panel';

function sparkPath(values: number[], width: number, height: number): string {
  const max = Math.max(...values);
  const min = Math.min(...values);
  const span = max - min || 1;
  return values.
  map((value, index) => {
    const x = index / (values.length - 1) * width;
    const y = height - (value - min) / span * (height - 4) - 2;
    return `${index === 0 ? 'M' : 'L'}${x.toFixed(1)} ${y.toFixed(1)}`;
  }).
  join(' ');
}

export function SystemMetrics() {
  const path = sparkPath(throughput, 260, 54);

  return (
    <Panel
      title="System Metrics"
      action={
      <span className="flex items-center gap-1.5 text-[10px] text-muted">
          Live
          <span className="h-1.5 w-1.5 rounded-full bg-ion shadow-[0_0_6px_#22d3ee]" />
        </span>
      }>
      
      <dl className="grid grid-cols-4 gap-2">
        {metrics.map((metric) =>
        <div
          key={metric.label}
          className="rounded border border-ion/15 bg-ion/[0.04] px-2 py-2 text-center">
          
            <dt className="text-[9px] font-semibold uppercase tracking-[0.1em] text-muted">
              {metric.label}
            </dt>
            <dd className="mt-1 text-[15px] font-semibold tabular-nums text-white">
              {metric.value}
            </dd>
          </div>
        )}
      </dl>

      <svg
        viewBox="0 0 260 54"
        preserveAspectRatio="none"
        className="mt-3 h-14 w-full"
        aria-hidden="true">
        
        <path d={`${path} L260 54 L0 54 Z`} fill="rgba(34,211,238,0.10)" />
        <path d={path} fill="none" stroke="#22d3ee" strokeWidth="1.2" />
      </svg>
    </Panel>);

}