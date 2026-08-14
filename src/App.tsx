import React from 'react';
import { AgendaCard } from './components/AgendaCard';
import { ChatPanel } from './components/ChatPanel';
import { Composer } from './components/Composer';
import { HeroCore } from './components/HeroCore';
import { MissionCard } from './components/MissionCard';
import { QuickTools } from './components/QuickTools';
import { RecentActivity } from './components/RecentActivity';
import { SystemMetrics } from './components/SystemMetrics';
import { SystemStatusCard } from './components/SystemStatusCard';
import { TopBar } from './components/TopBar';

export function App() {
  return (
    <div className="flex h-full min-h-[880px] w-full gap-3 bg-void p-3 font-sans text-slate-200">
      <div className="relative flex min-w-0 flex-1 gap-0 overflow-hidden rounded-md border border-ion/20 bg-abyss/70">
        <div className="relative flex min-w-0 flex-1 flex-col gap-4 overflow-hidden p-4">
          <HeroCore />
          <TopBar />

          <div className="relative z-10 grid min-h-0 flex-1 grid-cols-1 gap-5 lg:grid-cols-[280px_minmax(0,1fr)]">
            <div className="flex flex-col gap-3">
              <MissionCard />
              <SystemStatusCard />
              <div className="mt-auto">
                <AgendaCard />
              </div>
            </div>

            <main className="flex min-w-0 flex-col justify-end">
              <div className="mx-auto w-full max-w-2xl">
                <ChatPanel />
              </div>
            </main>
          </div>

          <div className="relative z-10 grid grid-cols-1 gap-5 lg:grid-cols-[280px_minmax(0,1fr)]">
            <div className="hidden lg:block" aria-hidden="true" />
            <div className="mx-auto w-full max-w-2xl">
              <Composer />
              <p className="mt-2.5 text-center text-[11px] text-slate-500">
                Hades can make mistakes. Always review important information.
              </p>
            </div>
          </div>
        </div>

        <aside className="relative z-10 hidden w-[300px] shrink-0 flex-col gap-3 overflow-y-auto border-l border-ion/15 bg-abyss/85 p-3 scroll-thin lg:flex">
          <SystemMetrics />
          <RecentActivity />
          <div className="mt-auto">
            <QuickTools />
          </div>
        </aside>
      </div>
    </div>);

}