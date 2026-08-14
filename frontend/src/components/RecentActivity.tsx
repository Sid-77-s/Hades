import React from 'react';
import { ActivityIcon, AlertCircleIcon } from 'lucide-react';
import { Panel } from './Panel';
import { useHades } from '../services/useHades';

export function RecentActivity() {
  const { executionEvents } = useHades();

  return (
    <Panel
      title="Execution Events"
      action={
      <button
        type="button"
        className="text-[10px] font-medium text-ion transition-colors duration-150 ease-out hover:text-white focus:outline-none focus-visible:ring-1 focus-visible:ring-ion">
        
          View all
        </button>
      }>
      
      <ul className="space-y-2.5 max-h-[300px] overflow-y-auto scroll-thin">
        {executionEvents.length === 0 && (
          <li className="text-[11px] text-muted text-center py-2">No recent events</li>
        )}
        {executionEvents.slice().reverse().map((item) => {
          const Icon = item.type === 'error' ? AlertCircleIcon : ActivityIcon;
          const tone = item.type === 'error' ? '#ef4444' : '#22d3ee';
          return (
            <li key={item.id} className="flex items-start gap-2.5">
              <span
                className="mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded border border-ion/15 bg-ion/[0.05]"
                style={{ color: tone }}>
                
                <Icon size={14} strokeWidth={1.75} />
              </span>
              <span className="min-w-0 flex-1 leading-tight">
                <span className="flex items-baseline justify-between gap-2">
                  <span className="text-[12px] font-medium text-slate-200">{item.type === 'error' ? 'Error' : 'Event'}</span>
                  <span className="shrink-0 text-[10px] text-muted">
                    {item.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </span>
                </span>
                <span className="mt-0.5 block text-[11px] text-ion">{item.text}</span>
              </span>
            </li>);

        })}
      </ul>
    </Panel>);
}