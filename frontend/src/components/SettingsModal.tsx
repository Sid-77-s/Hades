import React, { useEffect, useState } from 'react';
import { 
  XIcon, CheckCircleIcon, AlertCircleIcon, SettingsIcon, 
  CpuIcon, Volume2Icon, ShieldCheckIcon, PlayIcon, PlusIcon, Trash2Icon 
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export function SettingsModal({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) {
  const [activeTab, setActiveTab] = useState<'workers' | 'skills' | 'voice' | 'general'>('workers');
  const [skills, setSkills] = useState<Record<string, any>>({});
  const [workers, setWorkers] = useState<any[]>([]);
  const [voiceSettings, setVoiceSettings] = useState<any>({ enabled: true, rate: 180, volume: 0.9 });
  const [loading, setLoading] = useState(false);
  const [testResult, setTestResult] = useState<Record<string, string>>({});
  
  // New Worker Form state
  const [showAddWorker, setShowAddWorker] = useState(false);
  const [newWorker, setNewWorker] = useState({
    provider: 'openai',
    model_name: '',
    display_name: '',
    specialization: 'Reasoning / General',
    capabilities: ['general', 'reasoning'],
    env_key: 'OPENAI_API_KEY'
  });

  const loadStatus = () => {
    setLoading(true);
    fetch('/api/config/status')
      .then(res => res.json())
      .then(data => {
        setSkills(data.skills || {});
        setWorkers(data.workers || []);
        if (data.voice) setVoiceSettings(data.voice);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  };

  useEffect(() => {
    if (isOpen) {
      loadStatus();
    }
  }, [isOpen]);

  const handleTestWorker = async (modelName: string, id: string) => {
    setTestResult(prev => ({ ...prev, [id]: 'Testing...' }));
    try {
      const res = await fetch('/api/workers/test', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ model_name: modelName })
      });
      const data = await res.json();
      if (data.success) {
        setTestResult(prev => ({ ...prev, [id]: 'Operational' }));
      } else {
        setTestResult(prev => ({ ...prev, [id]: 'Failed: ' + (data.error || 'Check backend key') }));
      }
    } catch (err) {
      setTestResult(prev => ({ ...prev, [id]: 'Network Error' }));
    }
  };

  const handleTestVoice = async () => {
    try {
      await fetch('/api/voice/test', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: "Hades voice audio synthesis operational." })
      });
    } catch (e) {
      console.error(e);
    }
  };

  const handleSaveVoice = async (newSettings: any) => {
    setVoiceSettings(newSettings);
    await fetch('/api/voice/settings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newSettings)
    });
  };

  const handleAddWorkerSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newWorker.model_name) return;
    await fetch('/api/workers/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newWorker)
    });
    setShowAddWorker(false);
    setNewWorker({
      provider: 'openai',
      model_name: '',
      display_name: '',
      specialization: 'Reasoning / General',
      capabilities: ['general', 'reasoning'],
      env_key: 'OPENAI_API_KEY'
    });
    loadStatus();
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-void/80 backdrop-blur-sm p-4">
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.95 }}
          className="relative w-full max-w-3xl rounded-xl border border-ion/30 bg-abyss/95 shadow-2xl p-6 overflow-hidden flex flex-col max-h-[88vh]"
        >
          {/* Header */}
          <div className="flex items-center justify-between border-b border-ion/20 pb-4 mb-4 shrink-0">
            <div className="flex items-center gap-2">
              <SettingsIcon className="text-ion" size={22} />
              <h2 className="text-lg font-semibold text-white">Hades Configuration & Workforce</h2>
            </div>
            <button onClick={onClose} className="text-slate-400 hover:text-white transition-colors focus:outline-none">
              <XIcon size={22} />
            </button>
          </div>

          {/* Navigation Tabs */}
          <div className="flex items-center gap-2 border-b border-ion/15 pb-3 mb-4 text-xs font-medium text-slate-400 shrink-0">
            <button 
              onClick={() => setActiveTab('workers')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md transition-colors ${activeTab === 'workers' ? 'bg-ion text-void font-semibold' : 'hover:text-slate-200 bg-panel/40'}`}
            >
              <CpuIcon size={14} /> AI Workers
            </button>
            <button 
              onClick={() => setActiveTab('skills')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md transition-colors ${activeTab === 'skills' ? 'bg-ion text-void font-semibold' : 'hover:text-slate-200 bg-panel/40'}`}
            >
              <ShieldCheckIcon size={14} /> Skill Registry
            </button>
            <button 
              onClick={() => setActiveTab('voice')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md transition-colors ${activeTab === 'voice' ? 'bg-ion text-void font-semibold' : 'hover:text-slate-200 bg-panel/40'}`}
            >
              <Volume2Icon size={14} /> Voice & Audio
            </button>
          </div>
          
          {/* Tab Content */}
          <div className="flex-1 overflow-y-auto scroll-thin pr-2 text-sm text-slate-300">
            {loading ? (
              <div className="flex justify-center p-12">
                <div className="h-7 w-7 rounded-full border-2 border-ion border-t-transparent animate-spin" />
              </div>
            ) : (
              <>
                {/* WORKERS TAB */}
                {activeTab === 'workers' && (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <p className="text-xs text-ion-soft">
                        Configured AI workforce. Hades automatically routes tasks to the best worker.
                      </p>
                      <button 
                        onClick={() => setShowAddWorker(!showAddWorker)}
                        className="flex items-center gap-1 text-xs px-2.5 py-1 rounded bg-ion/20 text-ion border border-ion/30 hover:bg-ion/30 transition-colors"
                      >
                        <PlusIcon size={13} /> Add Worker
                      </button>
                    </div>

                    {showAddWorker && (
                      <form onSubmit={handleAddWorkerSubmit} className="rounded-lg border border-ion/30 bg-panel/60 p-4 space-y-3">
                        <h4 className="text-xs font-semibold text-white">Add New Model Worker</h4>
                        <div className="grid grid-cols-2 gap-3">
                          <div>
                            <label className="text-[11px] text-slate-400 block mb-1">Provider</label>
                            <select 
                              value={newWorker.provider}
                              onChange={e => setNewWorker({ ...newWorker, provider: e.target.value, env_key: e.target.value === 'google' ? 'GEMINI_API_KEY' : e.target.value === 'anthropic' ? 'ANTHROPIC_API_KEY' : 'OPENAI_API_KEY' })}
                              className="w-full bg-abyss border border-ion/20 rounded px-2.5 py-1.5 text-xs text-white"
                            >
                              <option value="google">Google</option>
                              <option value="openai">OpenAI</option>
                              <option value="anthropic">Anthropic</option>
                              <option value="local">Local Model / Ollama</option>
                            </select>
                          </div>
                          <div>
                            <label className="text-[11px] text-slate-400 block mb-1">Model Name (API format)</label>
                            <input 
                              type="text"
                              value={newWorker.model_name}
                              onChange={e => setNewWorker({ ...newWorker, model_name: e.target.value })}
                              placeholder="e.g. gpt-4o, gemini/gemini-flash-latest"
                              className="w-full bg-abyss border border-ion/20 rounded px-2.5 py-1.5 text-xs text-white"
                              required
                            />
                          </div>
                        </div>
                        <div className="flex justify-end gap-2 pt-2">
                          <button type="button" onClick={() => setShowAddWorker(false)} className="text-xs px-3 py-1 text-slate-400">Cancel</button>
                          <button type="submit" className="text-xs px-3 py-1 bg-ion text-void rounded font-semibold">Save Worker</button>
                        </div>
                      </form>
                    )}

                    <div className="grid gap-3">
                      {workers.map((w: any) => (
                        <div key={w.id} className="flex items-center justify-between rounded-lg border border-ion/15 bg-panel/40 p-3.5">
                          <div>
                            <div className="flex items-center gap-2">
                              <h3 className="font-semibold text-white text-sm">{w.display_name}</h3>
                              <span className="text-[10px] px-2 py-0.5 rounded bg-abyss text-slate-300 border border-ion/20">{w.provider}</span>
                            </div>
                            <p className="text-xs text-slate-400 mt-1">{w.specialization}</p>
                            <div className="flex gap-1 mt-1.5">
                              {w.capabilities.map((c: string) => (
                                <span key={c} className="text-[9px] px-1.5 py-0.5 rounded bg-ion/10 text-ion border border-ion/20">{c}</span>
                              ))}
                            </div>
                          </div>

                          <div className="flex items-center gap-3">
                            <div className="text-right">
                              {w.status === 'OPERATIONAL' ? (
                                <span className="flex items-center gap-1 text-online text-xs font-medium">
                                  <CheckCircleIcon size={13} /> Operational
                                </span>
                              ) : w.status === 'CONFIGURED' ? (
                                <span className="flex items-center gap-1 text-online text-xs font-medium">
                                  <CheckCircleIcon size={13} /> Configured
                                </span>
                              ) : w.status === 'DEPRECATED' ? (
                                <span className="flex items-center gap-1 text-alert text-xs font-medium">
                                  <AlertCircleIcon size={13} /> Deprecated
                                </span>
                              ) : w.status === 'FAILED' ? (
                                <span className="flex items-center gap-1 text-alert text-xs font-medium">
                                  <AlertCircleIcon size={13} /> Failed
                                </span>
                              ) : (
                                <span className="flex items-center gap-1 text-slate-500 text-xs font-medium">
                                  <AlertCircleIcon size={13} /> Unconfigured
                                </span>
                              )}
                              {testResult[w.id] && (
                                <p className={`text-[10px] mt-1 ${testResult[w.id] === 'Operational' ? 'text-online' : 'text-alert'}`}>
                                  {testResult[w.id]}
                                </p>
                              )}
                            </div>
                            <button 
                              onClick={() => handleTestWorker(w.model_name, w.id)}
                              className="px-2.5 py-1 rounded bg-abyss border border-ion/30 text-xs text-ion hover:bg-ion/10 transition-colors focus:outline-none"
                            >
                              Test
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* SKILLS TAB */}
                {activeTab === 'skills' && (
                  <div className="space-y-4">
                    <p className="text-xs text-ion-soft">
                      Hades Autonomous Skills. Secrets stay safely stored in backend <code className="bg-void px-1 rounded text-ion">.env</code>.
                    </p>
                    <div className="grid gap-3">
                      {Object.entries(skills).map(([id, skill]: [string, any]) => (
                        <div key={id} className="flex items-center justify-between rounded-lg border border-ion/15 bg-panel/40 p-3.5">
                          <div>
                            <h3 className="font-semibold text-white text-sm">{skill.name}</h3>
                            <p className="text-xs text-slate-400 uppercase tracking-wider mt-0.5">{skill.category}</p>
                          </div>
                          <div className="flex items-center gap-2">
                            {skill.status === "READY" ? (
                               <span className="flex items-center gap-1.5 text-online bg-online/10 px-2.5 py-1 rounded-full text-xs font-medium border border-online/20">
                                  <CheckCircleIcon size={13} /> Ready
                               </span>
                            ) : skill.status === "PARTIAL" ? (
                               <span className="flex items-center gap-1.5 text-yellow-400 bg-yellow-400/10 px-2.5 py-1 rounded-full text-xs font-medium border border-yellow-400/20">
                                  <AlertCircleIcon size={13} /> Fallback Only
                               </span>
                            ) : (
                               <span className="flex items-center gap-1.5 text-alert bg-alert/10 px-2.5 py-1 rounded-full text-xs font-medium border border-alert/20">
                                  <AlertCircleIcon size={13} /> Config Required
                               </span>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* VOICE TAB */}
                {activeTab === 'voice' && (
                  <div className="space-y-5">
                    <div className="flex items-center justify-between rounded-lg border border-ion/15 bg-panel/40 p-4">
                      <div>
                        <h4 className="font-semibold text-white text-sm">Hades Voice Feedback</h4>
                        <p className="text-xs text-slate-400">Offline speech generation powered by local TTS</p>
                      </div>
                      <button 
                        onClick={() => handleSaveVoice({ ...voiceSettings, enabled: !voiceSettings.enabled })}
                        className={`px-3 py-1 rounded text-xs font-semibold transition-colors ${voiceSettings.enabled ? 'bg-online text-void' : 'bg-slate-700 text-slate-300'}`}
                      >
                        {voiceSettings.enabled ? 'Enabled' : 'Disabled'}
                      </button>
                    </div>

                    <div className="rounded-lg border border-ion/15 bg-panel/40 p-4 space-y-4">
                      <div>
                        <div className="flex justify-between text-xs text-slate-300 mb-1">
                          <span>Speech Speed ({voiceSettings.rate} WPM)</span>
                        </div>
                        <input 
                          type="range" 
                          min="120" 
                          max="240" 
                          value={voiceSettings.rate || 180} 
                          onChange={e => handleSaveVoice({ ...voiceSettings, rate: Number(e.target.value) })}
                          className="w-full accent-ion" 
                        />
                      </div>

                      <div>
                        <div className="flex justify-between text-xs text-slate-300 mb-1">
                          <span>Volume ({Math.round((voiceSettings.volume || 0.9) * 100)}%)</span>
                        </div>
                        <input 
                          type="range" 
                          min="0" 
                          max="1" 
                          step="0.05"
                          value={voiceSettings.volume || 0.9} 
                          onChange={e => handleSaveVoice({ ...voiceSettings, volume: Number(e.target.value) })}
                          className="w-full accent-ion" 
                        />
                      </div>

                      <div className="pt-2">
                        <button 
                          onClick={handleTestVoice}
                          className="flex items-center gap-1.5 px-3 py-1.5 rounded bg-ion/20 text-ion border border-ion/30 hover:bg-ion/30 transition-colors text-xs font-medium"
                        >
                          <PlayIcon size={14} /> Test Hades Voice Audio
                        </button>
                      </div>
                    </div>
                  </div>
                )}
              </>
            )}
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
}
