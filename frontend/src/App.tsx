import React, { useEffect } from 'react';
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
import { useHades } from './services/useHades';

export function App() {
  const { userName, saveName, init } = useHades();
  const [tempName, setTempName] = React.useState('');

  useEffect(() => {
    if (userName) {
      init();
    }
  }, [userName, init]);

  if (!userName) {
    return (
      <div className="flex h-screen w-full items-center justify-center bg-void text-slate-200">
        <div className="flex flex-col items-center gap-4">
          <h1 className="text-2xl font-semibold tracking-wide text-ion">HADES INIT</h1>
          <form 
            onSubmit={(e) => { e.preventDefault(); saveName(tempName); }}
            className="flex items-center gap-2"
          >
            <input 
              type="text" 
              value={tempName} 
              onChange={e => setTempName(e.target.value)} 
              placeholder="Enter Designation..." 
              className="rounded-md border border-ion/40 bg-abyss/80 px-4 py-2 focus:outline-none focus:border-ion"
            />
            <button type="submit" className="rounded-md bg-ion text-void px-4 py-2 font-semibold hover:bg-ion/90 transition-colors">
              INITIALIZE
            </button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen w-full gap-3 bg-void p-3 font-sans text-slate-200 overflow-hidden">
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
              <div className="mx-auto w-full max-w-2xl h-full flex flex-col justify-end overflow-hidden">
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
    </div>
  );
}