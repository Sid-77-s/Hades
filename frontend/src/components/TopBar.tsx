import React from 'react';
import { BellIcon, ChevronDownIcon, SearchIcon, SettingsIcon, SunIcon } from 'lucide-react';
import { userAvatar } from '../data/dashboard';
import { HadesMark } from './HadesMark';

const iconButton =
'flex h-9 w-9 items-center justify-center rounded-md border border-ion/25 bg-panel/60 text-ion-soft transition-colors duration-150 ease-out hover:border-ion/60 hover:text-white focus:outline-none focus-visible:ring-1 focus-visible:ring-ion';

export function TopBar() {
  return (
    <header className="grid grid-cols-[240px_1fr_240px] items-start gap-6">
      <div className="flex items-center gap-3 self-start rounded-md border border-ion/25 bg-panel/60 px-3 py-2">
        <HadesMark size={26} />
        <div className="leading-tight">
          <p className="font-display text-[15px] font-extrabold tracking-[0.14em] text-white">
            HADES
          </p>
          <p className="mt-0.5 flex items-center gap-1.5 text-[10px] text-muted">
            Online
            <span className="h-1.5 w-1.5 rounded-full bg-online shadow-[0_0_6px_#22c55e]" />
          </p>
        </div>
      </div>

      <div className="pt-1 text-center">
        <h1 className="text-xl font-semibold text-white">Good evening, Alex.</h1>
        <p className="mt-1 text-[13px] text-slate-400">
          What shall we build, solve, or create today?
        </p>
      </div>

      <div className="flex items-center justify-end gap-2">
        <button type="button" className={iconButton} aria-label="Search">
          <SearchIcon size={16} strokeWidth={1.75} />
        </button>
        <button type="button" className={`${iconButton} relative`} aria-label="Notifications">
          <BellIcon size={16} strokeWidth={1.75} />
          <span className="absolute right-1.5 top-1.5 h-1.5 w-1.5 rounded-full bg-alert" />
        </button>
        <button type="button" className={iconButton} aria-label="Toggle theme">
          <SunIcon size={16} strokeWidth={1.75} />
        </button>
        <button type="button" className={iconButton} aria-label="Settings">
          <SettingsIcon size={16} strokeWidth={1.75} />
        </button>
        <button
          type="button"
          className="flex items-center gap-2.5 rounded-md border border-ion/25 bg-panel/60 py-1.5 pl-1.5 pr-2.5 text-left transition-colors duration-150 ease-out hover:border-ion/60 focus:outline-none focus-visible:ring-1 focus-visible:ring-ion">
          
          <img
            src={userAvatar}
            alt=""
            className="h-8 w-8 rounded-full border border-ion/40 object-cover" />
          
          <span className="leading-tight">
            <span className="block text-[12px] font-semibold text-white">Alex</span>
            <span className="block text-[10px] text-ion">Pro Plan</span>
          </span>
          <ChevronDownIcon size={14} className="text-muted" strokeWidth={1.75} />
        </button>
      </div>
    </header>);

}