import React from 'react';
import { CircleDotIcon } from 'lucide-react';
import { systemStatus } from '../data/dashboard';
import { Panel } from './Panel';

export function SystemStatusCard() {
  return (
    <Panel title="System Status">
      <ul className="space-y-2.5">
        {systemStatus.map((item) =>
        <li key={item.label} className="flex items-center justify-between gap-3">
            <span className="flex items-center gap-2 text-[12px] text-slate-300">
              <CircleDotIcon size={13} className="text-online" strokeWidth={1.75} />
              {item.label}
            </span>
            <span className="text-[11px] font-medium text-online">{item.state}</span>
          </li>
        )}
      </ul>
    </Panel>);

}