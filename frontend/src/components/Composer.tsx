import React, { useState } from 'react';
import { HashIcon, MicIcon, PaperclipIcon, SendIcon } from 'lucide-react';
import { HadesMark } from './HadesMark';
import { useHades } from '../services/useHades';

const utility =
'flex h-8 w-8 items-center justify-center rounded text-muted transition-colors duration-150 ease-out hover:text-ion focus:outline-none focus-visible:ring-1 focus-visible:ring-ion';

export function Composer() {
  const [value, setValue] = useState('');
  const { sendMessage, isListening, hadesState } = useHades();

  return (
    <form
      onSubmit={(event) => {
        event.preventDefault();
        sendMessage(value);
        setValue('');
      }}
      className="flex items-center gap-3 rounded-full border border-ion/40 bg-panel/80 px-3 py-2.5 shadow-glow backdrop-blur-sm focus-within:border-ion/70">
      
      <span className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-full border border-ion/30 ${hadesState === 'executing' ? 'bg-ion/20 animate-pulse' : 'bg-ion/[0.08]'}`}>
        <HadesMark size={22} />
      </span>

      <label htmlFor="composer" className="sr-only">
        Message Hades
      </label>
      <input
        id="composer"
        value={value}
        onChange={(event) => setValue(event.target.value)}
        placeholder="Message Hades..."
        autoComplete="off"
        className="min-w-0 flex-1 bg-transparent text-[14px] text-slate-100 placeholder:text-slate-500 focus:outline-none" />
      

      <div className="flex items-center gap-1">
        <button type="button" className={utility} aria-label="Insert channel">
          <HashIcon size={16} strokeWidth={1.75} />
        </button>
        <button type="button" className={utility} aria-label="Attach file">
          <PaperclipIcon size={16} strokeWidth={1.75} />
        </button>
        <button type="button" className={`${utility} ${isListening ? 'text-ion animate-pulse' : ''}`} aria-label="Voice input">
          <MicIcon size={16} strokeWidth={1.75} />
        </button>
      </div>

      <button
        type="submit"
        aria-label="Send message"
        disabled={hadesState === 'processing'}
        className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-signal text-white transition-colors duration-150 ease-out hover:bg-ion hover:text-void focus:outline-none focus-visible:ring-2 focus-visible:ring-ion disabled:opacity-50">
        
        <SendIcon size={17} strokeWidth={2} />
      </button>
    </form>);
}