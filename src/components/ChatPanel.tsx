import React from 'react';
import { suggestions, userAvatar } from '../data/dashboard';
import { HadesMark } from './HadesMark';

export function ChatPanel() {
  return (
    <div className="rounded-md border border-ion/20 bg-panel/70 px-5 py-4 backdrop-blur-sm">
      <div className="flex gap-3">
        <span className="mt-0.5 flex h-9 w-9 shrink-0 items-center justify-center rounded-full border border-ion/30 bg-ion/[0.07]">
          <HadesMark size={22} />
        </span>
        <div className="min-w-0 flex-1">
          <p className="flex items-baseline gap-2">
            <span className="text-[12px] font-semibold tracking-wide text-ion-soft">HADES</span>
            <span className="text-[10px] text-muted">2m ago</span>
          </p>
          <div className="mt-2 space-y-1.5 text-[13px] leading-relaxed text-slate-200">
            <p>I&apos;ve reviewed your requirements for the AI OS Dashboard.</p>
            <p>
              Before I start building, I&apos;d like to clarify a few things to make sure we&apos;re
              aligned on the vision.
            </p>
            <p>Mind if I ask a few questions?</p>
          </div>
        </div>
      </div>

      <div className="mt-4 flex justify-end">
        <div className="flex items-end gap-2.5">
          <div className="text-right">
            <p className="mb-1.5 text-[11px] text-muted">You</p>
            <p className="rounded-md rounded-br-sm border border-ion/30 bg-ion/[0.08] px-3.5 py-2 text-[13px] text-slate-100">
              Sure, go ahead.
            </p>
          </div>
          <img
            src={userAvatar}
            alt=""
            className="h-9 w-9 rounded-full border border-ion/30 object-cover" />
          
        </div>
      </div>

      <ul className="mt-4 flex flex-wrap items-center justify-center gap-2.5">
        {suggestions.map((suggestion) =>
        <li key={suggestion}>
            <button
            type="button"
            className="rounded-md border border-ion/25 bg-panel/80 px-3.5 py-2 text-[12px] text-slate-300 transition-colors duration-150 ease-out hover:border-ion/60 hover:text-white focus:outline-none focus-visible:ring-1 focus-visible:ring-ion">
            
              {suggestion}
            </button>
          </li>
        )}
      </ul>
    </div>);

}