import React from 'react';
import { motion } from 'framer-motion';
import { heroImage } from '../data/dashboard';

export function HeroCore() {
  return (
    <div className="pointer-events-none absolute inset-0 overflow-hidden" aria-hidden="true">
      <div className="absolute inset-0 hud-grid opacity-50" />

      <motion.div
        initial={{ opacity: 0, scale: 0.97 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.3, ease: [0.23, 1, 0.32, 1] }}
        className="absolute left-1/2 top-[34%] h-[clamp(360px,52vh,540px)] w-[clamp(360px,52vh,540px)] -translate-x-1/2 -translate-y-1/2">
        
        <img
          src={heroImage}
          alt=""
          className="h-full w-full object-contain opacity-90 mix-blend-screen"
          style={{
            maskImage:
            'radial-gradient(circle at 50% 44%, #000 46%, rgba(0,0,0,0.35) 62%, transparent 74%)',
            WebkitMaskImage:
            'radial-gradient(circle at 50% 44%, #000 46%, rgba(0,0,0,0.35) 62%, transparent 74%)'
          }} />
        
      </motion.div>

      <div className="absolute left-1/2 top-[34%] -translate-x-1/2 -translate-y-1/2 text-center">
        <span className="font-display text-[34px] font-extrabold tracking-[0.14em] text-white drop-shadow-[0_0_18px_rgba(34,211,238,0.85)]">
          HADES
        </span>
      </div>

      <div className="absolute inset-x-0 bottom-0 h-1/3 bg-gradient-to-t from-abyss to-transparent" />
    </div>);

}