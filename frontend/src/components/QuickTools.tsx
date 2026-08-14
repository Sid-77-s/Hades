import React from 'react';
import { quickTools } from '../data/dashboard';
import { Panel } from './Panel';

export function QuickTools() {
  return (
    <Panel title="Quick Tools">
      <ul className="grid grid-cols-4 gap-2">
        {quickTools.map((tool) => {
          const Icon = tool.icon;
          return (
            <li key={tool.label}>
              <button
                type="button"
                className="flex w-full flex-col items-center gap-2 rounded-md border border-ion/15 bg-ion/[0.04] px-1 py-3 transition-colors duration-150 ease-out hover:border-ion/50 hover:bg-ion/[0.09] focus:outline-none focus-visible:ring-1 focus-visible:ring-ion">
                
                <Icon size={20} strokeWidth={1.5} className="text-ion" />
                <span className="text-center text-[9px] font-medium leading-tight text-slate-300">
                  {tool.label}
                </span>
              </button>
            </li>);

        })}
      </ul>
    </Panel>);

}