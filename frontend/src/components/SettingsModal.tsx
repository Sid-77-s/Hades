import React, { useEffect, useState } from 'react';
import { XIcon, CheckCircleIcon, AlertCircleIcon, SettingsIcon } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export function SettingsModal({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) {
  const [skills, setSkills] = useState<Record<string, any>>({});
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setLoading(true);
      fetch('/api/config/status')
        .then(res => res.json())
        .then(data => {
          setSkills(data.skills || {});
          setLoading(false);
        })
        .catch(err => {
          console.error(err);
          setLoading(false);
        });
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-void/80 backdrop-blur-sm p-4">
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.95 }}
          className="relative w-full max-w-2xl rounded-xl border border-ion/30 bg-abyss/90 shadow-2xl p-6 overflow-hidden flex flex-col max-h-[85vh]"
        >
          <div className="flex items-center justify-between border-b border-ion/20 pb-4 mb-4 shrink-0">
            <h2 className="flex items-center gap-2 text-xl font-semibold text-white">
              <SettingsIcon className="text-ion" size={24} />
              System Capabilities & Credentials
            </h2>
            <button onClick={onClose} className="text-slate-400 hover:text-white transition-colors">
              <XIcon size={24} />
            </button>
          </div>
          
          <div className="flex-1 overflow-y-auto scroll-thin pr-2 text-sm text-slate-300">
            <p className="mb-6 text-ion-soft">
              Hades credentials are now securely managed via the <code className="bg-void px-1.5 py-0.5 rounded text-ion border border-ion/30">.env</code> file in the project root. 
              Restart the backend server to apply credential changes.
            </p>
            
            {loading ? (
              <div className="flex justify-center p-8"><div className="h-6 w-6 rounded-full border-2 border-ion border-t-transparent animate-spin" /></div>
            ) : (
              <div className="grid gap-3">
                {Object.entries(skills).map(([id, skill]) => (
                  <div key={id} className="flex items-center justify-between rounded-lg border border-ion/15 bg-panel/40 p-4">
                    <div>
                      <h3 className="font-semibold text-white text-base">{skill.name}</h3>
                      <p className="text-xs text-slate-400 uppercase tracking-wider">{skill.category}</p>
                    </div>
                    <div className="flex items-center gap-2">
                      {skill.status === "READY" ? (
                         <span className="flex items-center gap-1.5 text-online bg-online/10 px-2.5 py-1 rounded-full text-xs font-medium border border-online/20">
                            <CheckCircleIcon size={14} /> Ready
                         </span>
                      ) : skill.status === "PARTIAL" ? (
                         <span className="flex items-center gap-1.5 text-yellow-400 bg-yellow-400/10 px-2.5 py-1 rounded-full text-xs font-medium border border-yellow-400/20">
                            <AlertCircleIcon size={14} /> Fallback Only
                         </span>
                      ) : (
                         <span className="flex items-center gap-1.5 text-alert bg-alert/10 px-2.5 py-1 rounded-full text-xs font-medium border border-alert/20">
                            <AlertCircleIcon size={14} /> Config Required
                         </span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
}
