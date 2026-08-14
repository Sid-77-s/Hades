import React from 'react';
import { agenda } from '../data/dashboard';
import { Panel } from './Panel';

export function AgendaCard() {
  return (
    <Panel
      title="Today's Agenda"
      action={
      <button
        type="button"
        className="text-[10px] font-medium text-ion transition-colors duration-150 ease-out hover:text-white focus:outline-none focus-visible:ring-1 focus-visible:ring-ion">
        
          View all
        </button>
      }>
      
      <ul className="space-y-2.5">
        {agenda.map((item) =>
        <li key={item.title} className="flex items-center justify-between gap-3">
            <span className="flex items-center gap-2.5 text-[12px] text-slate-300">
              <span
              className="h-1.5 w-1.5 rounded-full"
              style={{ backgroundColor: item.color, boxShadow: `0 0 6px ${item.color}` }} />
            
              {item.title}
            </span>
            <span className="text-[11px] tabular-nums text-muted">{item.time}</span>
          </li>
        )}
      </ul>
    </Panel>);

}