import React, { useState, useRef } from 'react';
import { MicIcon, PaperclipIcon, SendIcon, XIcon, ImageIcon } from 'lucide-react';
import { HadesMark } from './HadesMark';
import { useHades } from '../services/useHades';

const utility =
'flex h-8 w-8 items-center justify-center rounded text-muted transition-colors duration-150 ease-out hover:text-ion focus:outline-none focus-visible:ring-1 focus-visible:ring-ion cursor-pointer';

export function Composer() {
  const [value, setValue] = useState('');
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { sendMessage, isListening, toggleListening, hadesState } = useHades();

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        if (event.target?.result) {
          setSelectedImage(event.target.result as string);
        }
      };
      reader.readAsDataURL(file);
    }
  };

  const removeImage = () => {
    setSelectedImage(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="flex flex-col gap-2">
      {selectedImage && (
        <div className="relative inline-flex self-start items-center gap-2 rounded-lg border border-ion/30 bg-abyss/90 p-1.5 shadow-md">
          <img src={selectedImage} alt="Attachment preview" className="h-14 w-14 rounded object-cover" />
          <div className="text-xs text-slate-300 pr-6">
            <p className="font-semibold text-ion-soft">Image attached</p>
            <p className="text-[10px] text-muted">Ready for visual context</p>
          </div>
          <button 
            type="button" 
            onClick={removeImage}
            className="absolute top-1 right-1 p-1 text-slate-400 hover:text-red-400 focus:outline-none"
            aria-label="Remove image"
          >
            <XIcon size={14} />
          </button>
        </div>
      )}

      <form
        onSubmit={(event) => {
          event.preventDefault();
          if (!value.trim() && !selectedImage) return;
          sendMessage(value, selectedImage || undefined);
          setValue('');
          removeImage();
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
        
        <input 
          type="file" 
          ref={fileInputRef} 
          onChange={handleImageSelect} 
          accept="image/*" 
          className="hidden" 
          id="image-upload" 
        />

        <div className="flex items-center gap-1">
          <button 
            type="button" 
            onClick={() => fileInputRef.current?.click()} 
            className={utility} 
            aria-label="Attach image"
            title="Attach image"
          >
            <ImageIcon size={16} strokeWidth={1.75} />
          </button>
          
          <button 
            type="button" 
            onClick={() => fileInputRef.current?.click()} 
            className={utility} 
            aria-label="Attach file"
            title="Attach file"
          >
            <PaperclipIcon size={16} strokeWidth={1.75} />
          </button>
          
          <button 
            type="button" 
            onClick={toggleListening}
            className={`${utility} ${isListening ? 'text-ion bg-ion/20 animate-pulse' : ''}`} 
            aria-label="Toggle voice input"
            title={isListening ? "Listening... click to stop" : "Voice input"}
          >
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
      </form>
    </div>
  );
}