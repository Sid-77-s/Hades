import React from 'react';
import { userAvatar } from '../data/dashboard';
import { HadesMark } from './HadesMark';
import { useHades } from '../services/useHades';
import { ChatMessage } from '../services/HadesService';

export function ChatPanel() {
  const { messages, hadesState } = useHades();
  const bottomRef = React.useRef<HTMLDivElement>(null);

  React.useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="rounded-md border border-ion/20 bg-panel/70 px-5 py-4 backdrop-blur-sm h-full overflow-y-auto scroll-thin flex flex-col gap-6">
      {messages.length === 0 ? (
        <div className="flex-1 flex items-center justify-center text-slate-500 text-sm">
          No messages yet. Send a message to start.
        </div>
      ) : (
        messages.map((msg: ChatMessage) => (
          msg.sender === 'hades' ? (
            <div key={msg.id} className="flex gap-3">
              <span className={`mt-0.5 flex h-9 w-9 shrink-0 items-center justify-center rounded-full border ${msg.isError ? 'border-red-500/50 bg-red-500/10' : 'border-ion/30 bg-ion/[0.07]'}`}>
                <HadesMark size={22} />
              </span>
              <div className="min-w-0 flex-1">
                <p className="flex items-baseline gap-2">
                  <span className={`text-[12px] font-semibold tracking-wide ${msg.isError ? 'text-red-400' : 'text-ion-soft'}`}>HADES</span>
                  <span className="text-[10px] text-muted">
                    {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </span>
                </p>
                <div className="mt-2 space-y-1.5 text-[13px] leading-relaxed text-slate-200">
                  <div dangerouslySetInnerHTML={{ __html: msg.text.replace(/\n/g, '<br/>') }} />
                  {msg.devError && (
                    <div className="mt-2 p-2 bg-red-900/30 border border-red-500/30 rounded text-xs text-red-200">
                      <strong>Developer Error:</strong><br/>
                      Type: {msg.devError.type}<br/>
                      Provider: {msg.devError.provider}<br/>
                      Reason: {msg.devError.reason}
                    </div>
                  )}
                </div>
              </div>
            </div>
          ) : (
            <div key={msg.id} className="mt-4 flex justify-end">
              <div className="flex items-end gap-2.5">
                <div className="text-right">
                  <p className="mb-1.5 text-[11px] text-muted">You</p>
                  <p className="rounded-md rounded-br-sm border border-ion/30 bg-ion/[0.08] px-3.5 py-2 text-[13px] text-slate-100">
                    {msg.text}
                  </p>
                </div>
                <img
                  src={userAvatar}
                  alt=""
                  className="h-9 w-9 rounded-full border border-ion/30 object-cover" />
              </div>
            </div>
          )
        ))
      )}
      {hadesState === 'processing' && (
        <div className="flex gap-3 animate-pulse">
           <span className="mt-0.5 flex h-9 w-9 shrink-0 items-center justify-center rounded-full border border-ion/30 bg-ion/[0.07]">
             <HadesMark size={22} />
           </span>
           <div className="min-w-0 flex-1">
              <p className="flex items-baseline gap-2">
                <span className="text-[12px] font-semibold tracking-wide text-ion-soft">HADES</span>
              </p>
              <div className="mt-2 text-[13px] text-slate-400">Processing...</div>
           </div>
        </div>
      )}
      <div ref={bottomRef} />
    </div>
  );
}