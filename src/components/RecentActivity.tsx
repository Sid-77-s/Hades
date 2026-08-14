import React from 'react';
import { recentActivity } from '../data/dashboard';
import { Panel } from './Panel';

export function RecentActivity() {
  return (
    <Panel
      title="Recent Activity"
      action={
      <button
        type="button"
        className="text-[10px] font-medium text-ion transition-colors duration-150 ease-out hover:text-white focus:outline-none focus-visible:ring-1 focus-visible:ring-ion">
        
          View all
        </button>
      }>
      
      <ul className="space-y-2.5">
        {recentActivity.map((item) => {
          const Icon = item.icon;
          return (
            <li key={item.target} className="flex items-start gap-2.5">
              <span
                className="mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded border border-ion/15 bg-ion/[0.05]"
                style={{ color: item.tone }}>
                
                <Icon size={14} strokeWidth={1.75} />
              </span>
              <span className="min-w-0 flex-1 leading-tight">
                <span className="flex items-baseline justify-between gap-2">
                  <span className="text-[12px] font-medium text-slate-200">{item.action}</span>
                  <span className="shrink-0 text-[10px] text-muted">{item.time}</span>
                </span>
                <span className="mt-0.5 block truncate text-[11px] text-ion">{item.target}</span>
              </span>
            </li>);

        })}
      </ul>
    </Panel>);

}