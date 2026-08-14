import React from 'react';
import { motion } from 'framer-motion';
import { heroImage } from '../data/dashboard';
import { useHades } from '../services/useHades';

export function HeroCore() {
  const { hadesState } = useHades();
  
  const stateColor = hadesState === 'executing' ? 'rgba(239,68,68,0.85)' : hadesState === 'processing' ? 'rgba(250,204,21,0.85)' : hadesState === 'error' ? 'rgba(239,68,68,0.85)' : 'rgba(34,211,238,0.85)';
  const imageOpacity = hadesState === 'idle' ? 0.9 : 1.0;
  
  return (
    <div className="pointer-events-none absolute inset-0 overflow-hidden" aria-hidden="true">
      <div className="absolute inset-0 hud-grid opacity-50" />

      <motion.div
        initial={{ opacity: 0, scale: 0.97 }}
        animate={{ 
          opacity: imageOpacity, 
          scale: hadesState === 'executing' ? [1, 1.02, 1] : 1 
        }}
        transition={{ 
          duration: hadesState === 'executing' ? 1.5 : 0.3, 
          ease: "easeInOut",
          repeat: hadesState === 'executing' || hadesState === 'processing' ? Infinity : 0
        }}
        className="absolute left-1/2 top-[34%] h-[clamp(360px,52vh,540px)] w-[clamp(360px,52vh,540px)] -translate-x-1/2 -translate-y-1/2">
        
        <img
          src={heroImage}
          alt=""
          className={`h-full w-full object-contain mix-blend-screen transition-opacity duration-300 ${hadesState === 'processing' ? 'animate-pulse' : ''}`}
          style={{
            maskImage:
            'radial-gradient(circle at 50% 44%, #000 46%, rgba(0,0,0,0.35) 62%, transparent 74%)',
            WebkitMaskImage:
            'radial-gradient(circle at 50% 44%, #000 46%, rgba(0,0,0,0.35) 62%, transparent 74%)'
          }} />
        
      </motion.div>

      <div className="absolute left-1/2 top-[34%] -translate-x-1/2 -translate-y-1/2 text-center">
        <span 
          className="font-display text-[34px] font-extrabold tracking-[0.14em] text-white transition-all duration-300"
          style={{ textShadow: `0 0 18px ${stateColor}` }}
        >
          HADES
        </span>
      </div>

      <div className="absolute inset-x-0 bottom-0 h-1/3 bg-gradient-to-t from-abyss to-transparent" />
    </div>);
}