import React from 'react';
import { CircleDotIcon } from 'lucide-react';
import { Panel } from './Panel';
import { useHades } from '../services/useHades';

export function SystemStatusCard() {
  const { hadesState } = useHades();
  const statusColor = hadesState === 'error' ? 'text-red-500' : 'text-online';
  const statusText = hadesState === 'idle' ? 'Online' : hadesState === 'processing' ? 'Processing' : hadesState === 'executing' ? 'Executing' : 'Error';

  return (
    <Panel title="System Status">
      <ul className="space-y-2.5">
          <li className="flex items-center justify-between gap-3">
            <span className="flex items-center gap-2 text-[12px] text-slate-300">
              <CircleDotIcon size={13} className={statusColor} strokeWidth={1.75} />
              Core Systems
            </span>
            <span className={`text-[11px] font-medium ${statusColor}`}>{statusText}</span>
          </li>
          <li className="flex items-center justify-between gap-3">
            <span className="flex items-center gap-2 text-[12px] text-slate-300">
              <CircleDotIcon size={13} className="text-online" strokeWidth={1.75} />
              Memory Engine
            </span>
            <span className="text-[11px] font-medium text-online">Online</span>
          </li>
          <li className="flex items-center justify-between gap-3">
            <span className="flex items-center gap-2 text-[12px] text-slate-300">
              <CircleDotIcon size={13} className="text-online" strokeWidth={1.75} />
              Execution Engine
            </span>
            <span className="text-[11px] font-medium text-online">Online</span>
          </li>
      </ul>
    </Panel>);
}