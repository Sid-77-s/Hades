import React from 'react';

interface PanelProps {
  title?: string;
  action?: React.ReactNode;
  className?: string;
  bodyClassName?: string;
  children: React.ReactNode;
}

export function Panel({ title, action, className = '', bodyClassName = '', children }: PanelProps) {
  return (
    <section
      className={`relative rounded-md border border-ion/20 bg-panel/60 backdrop-blur-sm ${className}`}>
      
      <span className="pointer-events-none absolute -left-px -top-px h-3 w-3 border-l border-t border-ion/70" />
      <span className="pointer-events-none absolute -right-px -top-px h-3 w-3 border-r border-t border-ion/70" />
      <span className="pointer-events-none absolute -bottom-px -left-px h-3 w-3 border-b border-l border-ion/70" />
      <span className="pointer-events-none absolute -bottom-px -right-px h-3 w-3 border-b border-r border-ion/70" />

      {title ?
      <header className="flex items-center justify-between gap-3 border-b border-ion/10 px-4 py-2.5">
          <h2 className="text-[10px] font-semibold uppercase tracking-[0.18em] text-ion-soft">
            {title}
          </h2>
          {action}
        </header> :
      null}
      <div className={`px-4 py-3 ${bodyClassName}`}>{children}</div>
    </section>);

}