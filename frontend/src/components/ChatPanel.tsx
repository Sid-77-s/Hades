import React, { useRef } from 'react';
import { userAvatar } from '../data/dashboard';
import { HadesMark } from './HadesMark';
import { useHades } from '../services/useHades';
import { ChatMessage } from '../services/HadesService';
import { InfoIcon, ChevronDownIcon, ChevronUpIcon } from 'lucide-react';

export function ChatPanel() {
  const { messages, hadesState } = useHades();
  const bottomRef = useRef<HTMLDivElement>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);
  const isScrolledUp = useRef(false);
  const [expandedDetails, setExpandedDetails] = React.useState<Record<string, boolean>>({});

  const handleScroll = () => {
    if (!chatContainerRef.current) return;
    const { scrollTop, scrollHeight, clientHeight } = chatContainerRef.current;
    isScrolledUp.current = scrollHeight - scrollTop - clientHeight > 100;
  };

  React.useEffect(() => {
    // Slight delay ensures the DOM has fully rendered the new content before scrolling
    setTimeout(() => {
      bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, 50);
  }, [messages, hadesState]);

  const toggleDetails = (id: string) => {
    setExpandedDetails(prev => ({ ...prev, [id]: !prev[id] }));
  };

  return (
    <div 
      ref={chatContainerRef}
      onScroll={handleScroll}
      className="rounded-md border border-ion/20 bg-panel/70 px-5 py-4 backdrop-blur-sm h-full overflow-y-auto scroll-thin flex flex-col gap-6"
    >
      {messages.length === 0 ? (
        <div className="flex-1 flex items-center justify-center text-slate-500 text-sm">
          No messages yet. Send a message to start communicating with Hades.
        </div>
      ) : (
        messages.map((msg: ChatMessage) => (
          msg.sender === 'hades' ? (
            <div key={msg.id} className="flex gap-3 min-w-0">
              <span className={`mt-0.5 flex h-9 w-9 shrink-0 items-center justify-center rounded-full border ${msg.isError ? 'border-red-500/50 bg-red-500/10' : 'border-ion/30 bg-ion/[0.07]'}`}>
                <HadesMark size={22} />
              </span>
              <div className="min-w-0 flex-1 overflow-hidden">
                <div className="flex items-baseline justify-between gap-2">
                  <p className="flex items-baseline gap-2">
                    <span className={`text-[12px] font-semibold tracking-wide ${msg.isError ? 'text-red-400' : 'text-ion-soft'}`}>HADES</span>
                    <span className="text-[10px] text-muted">
                      {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </p>
                  
                  {/* Subtle optional transparency toggle */}
                  <button 
                    onClick={() => toggleDetails(msg.id)}
                    className="flex items-center gap-1 text-[10px] text-slate-500 hover:text-ion transition-colors focus:outline-none"
                    title="View internal details"
                  >
                    <InfoIcon size={12} />
                    <span>{expandedDetails[msg.id] ? 'Hide details' : "What's happening?"}</span>
                    {expandedDetails[msg.id] ? <ChevronUpIcon size={10} /> : <ChevronDownIcon size={10} />}
                  </button>
                </div>

                <div className="mt-2 text-[13px] leading-relaxed text-slate-200 break-words whitespace-pre-wrap">
                  {msg.text}
                </div>

                {/* Optional Inspection Layer */}
                {expandedDetails[msg.id] && (
                  <div className="mt-3 rounded border border-ion/20 bg-void/70 p-3 text-[11px] text-slate-400 space-y-1.5 animate-fadeIn">
                    <div className="font-semibold text-ion-soft flex items-center justify-between">
                      <span>Internal Inspection</span>
                      <span className="text-[9px] px-1.5 py-0.5 rounded bg-ion/10 text-ion border border-ion/20">Operational</span>
                    </div>
                    <div>Model: <span className="text-slate-200">Gemini Flash (Latest)</span></div>
                    <div>Routing: <span className="text-slate-200">Conversational Partner Brain</span></div>
                    <div>Status: <span className="text-online">Verified</span></div>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div key={msg.id} className="mt-2 flex justify-end min-w-0">
              <div className="flex items-end gap-2.5 max-w-[85%] min-w-0">
                <div className="text-right min-w-0 overflow-hidden">
                  <p className="mb-1.5 text-[11px] text-muted">You</p>
                  {msg.imagePreview && (
                    <div className="mb-2 flex justify-end">
                      <img 
                        src={msg.imagePreview} 
                        alt="Attached" 
                        className="max-h-40 rounded-md border border-ion/30 object-cover shadow-md" 
                      />
                    </div>
                  )}
                  <p className="rounded-md rounded-br-sm border border-ion/30 bg-ion/[0.08] px-3.5 py-2 text-[13px] text-slate-100 break-words text-left inline-block">
                    {msg.text}
                  </p>
                </div>
                <img
                  src={userAvatar}
                  alt=""
                  className="h-9 w-9 shrink-0 rounded-full border border-ion/30 object-cover" />
              </div>
            </div>
          )
        ))
      )}
      {hadesState === 'processing' && (
        <div className="flex gap-3 animate-pulse min-w-0">
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