import React from 'react';
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
      
      <div className="py-4 text-center text-[11px] text-slate-500">
        No agenda items available.
      </div>
    </Panel>);
}