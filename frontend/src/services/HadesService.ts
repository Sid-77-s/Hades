export interface DeveloperError {
  type: string;
  provider: string;
  reason: string;
}

export interface ChatMessage {
  id: string;
  sender: 'user' | 'hades';
  text: string;
  isError?: boolean;
  devError?: DeveloperError;
  timestamp: Date;
}

export interface ExecutionEvent {
  id: string;
  text: string;
  type: 'info' | 'error';
  timestamp: Date;
}

export type HadesState = 'idle' | 'processing' | 'executing' | 'error';

type StateUpdateCallback = () => void;

class HadesService {
  public sessionId: string | null = null;
  public userName: string | null = null;
  public isProcessing: boolean = false;
  public activeMissionId: string | null = null;
  public devMode: boolean = false;
  public wakeWord: string = 'Hades';
  public hadesState: HadesState = 'idle';

  public messages: ChatMessage[] = [];
  public executionEvents: ExecutionEvent[] = [];

  private listeners: StateUpdateCallback[] = [];
  private eventSource: EventSource | null = null;
  private recognition: any = null;
  public isListening: boolean = false;

  constructor() {
    this.sessionId = localStorage.getItem('hades_session_id') || null;
    this.userName = localStorage.getItem('hades_user_name') || null;
    this.devMode = localStorage.getItem('hades_dev_mode') === 'true';
    this.wakeWord = localStorage.getItem('hades_wake_word') || 'Hades';
  }

  public subscribe(callback: StateUpdateCallback) {
    this.listeners.push(callback);
    return () => {
      this.listeners = this.listeners.filter(cb => cb !== callback);
    };
  }

  private notify() {
    this.listeners.forEach(cb => cb());
  }

  public init() {
    this.initSSE();
    this.initVoice();
    this.notify();
  }

  private initSSE() {
    if (this.eventSource) return;
    this.eventSource = new EventSource('/api/events');
    
    this.eventSource.onmessage = (e) => {
      const data = JSON.parse(e.data);
      this.handleBackgroundEvent(data);
    };
  }

  private logExecutionEvent(text: string, type: 'info' | 'error' = 'info') {
    this.executionEvents.push({
      id: Math.random().toString(36).substring(7),
      text,
      type,
      timestamp: new Date()
    });
    this.notify();
  }

  private handleBackgroundEvent(event: any) {
    const type = event.type;
    const payload = event.data;
    
    if (type === 'MISSION_STATUS_UPDATED') {
      this.activeMissionId = payload.mission_id;
      if (payload.status === 'EXECUTING') {
        this.hadesState = 'executing';
        this.logExecutionEvent("Execution Brain took control.", "info");
      }
    } else if (type === 'PLAN_CREATED') {
      this.logExecutionEvent(`Plan created with ${payload.tasks} task(s).`);
    } else if (type === 'TASK_STARTED') {
      this.logExecutionEvent(`Started task: ${payload.objective}`);
    } else if (type === 'CAPABILITY_SELECTED') {
      this.logExecutionEvent(`Using capability: ${payload.adapter}`);
    } else if (type === 'TASK_COMPLETED') {
      this.logExecutionEvent(`Task completed: ${payload.result}`);
    } else if (type === 'TASK_FAILED') {
      this.logExecutionEvent(`Task failed: ${payload.error}`, "error");
    } else if (type === 'USER_INTERVENTION_REQUIRED') {
      this.logExecutionEvent(`Blocker Hit: ${payload.details}`, "error");
      this.hadesState = 'error';
      this.appendMessage('hades', `**I've hit a blocker.**\n\n${payload.details}\n\nFallback protocols available.`);
    } else if (type === 'MISSION_COMPLETED') {
      this.hadesState = 'idle';
      this.appendMessage('hades', `**Mission Complete.**\n\n${payload.result}`);
      this.logExecutionEvent(`Mission Delivered.`, "info");
      setTimeout(() => {
        this.activeMissionId = null;
        this.notify();
      }, 8000);
    }
    this.notify();
  }

  public appendMessage(sender: 'user' | 'hades', text: string, isError: boolean = false, devError: DeveloperError | null = null) {
    this.messages.push({
      id: Math.random().toString(36).substring(7),
      sender,
      text,
      isError,
      devError: devError || undefined,
      timestamp: new Date()
    });

    if (sender === 'hades') {
      this.speakText(text);
    }
    this.notify();
  }

  public async sendMessage(text: string) {
    if (!text.trim() || this.isProcessing) return;
    
    this.isProcessing = true;
    this.appendMessage('user', text);
    this.hadesState = 'processing';
    this.notify();

    try {
      const payload: any = { message: text, user_name: this.userName };
      if (this.sessionId) payload.session_id = this.sessionId;

      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await res.json();
      
      if (data.session_id) {
        this.sessionId = data.session_id;
        localStorage.setItem('hades_session_id', this.sessionId);
      }

      this.appendMessage('hades', data.response, data.is_error, data.developer_error);
      
      if (data.mission_status !== "LOCKED" && data.mission_status !== "EXECUTING") {
        this.hadesState = 'idle';
      }
      
      this.isProcessing = false;
      this.notify();
    } catch (err) {
      console.error("API Error", err);
      this.hadesState = 'error';
      this.appendMessage('hades', "I encountered an error connecting to my core processing system.", true);
      this.isProcessing = false;
      this.notify();
    }
  }

  public saveName(name: string) {
    const val = name.trim();
    if (val) {
      this.userName = val;
      localStorage.setItem('hades_user_name', this.userName);
      this.notify();
      this.init();
      this.appendMessage('hades', `Good to meet you, ${this.userName}.\n\nWhat are we working on?`);
    }
  }

  private speakText(text: string) {
    if (!('speechSynthesis' in window)) return;
    const cleanText = text.replace(/[*_#`~]/g, '');
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.rate = 1.05;
    utterance.pitch = 0.9;
    const voices = window.speechSynthesis.getVoices();
    const enVoice = voices.find(v => v.lang.startsWith('en') && v.name.includes('Male')) || voices.find(v => v.lang.startsWith('en'));
    if (enVoice) utterance.voice = enVoice;
    
    window.speechSynthesis.speak(utterance);
  }

  private initVoice() {
    const windowAny = window as any;
    if ('webkitSpeechRecognition' in windowAny || 'SpeechRecognition' in windowAny) {
      const SpeechRecognition = windowAny.SpeechRecognition || windowAny.webkitSpeechRecognition;
      this.recognition = new SpeechRecognition();
      this.recognition.continuous = true;
      this.recognition.interimResults = false;
      
      this.recognition.onstart = () => {
        if (!this.isProcessing && this.hadesState !== 'executing') {
          this.hadesState = 'idle';
        }
        this.isListening = true;
        this.notify();
      };
      
      this.recognition.onresult = (event: any) => {
        const results = event.results;
        const transcript = results[results.length - 1][0].transcript.trim();
        
        if (transcript.length > 0) {
          window.speechSynthesis.cancel();
        }

        const lowerTranscript = transcript.toLowerCase();
        const lowerWake = this.wakeWord.toLowerCase();
        
        if (lowerTranscript.includes(lowerWake)) {
          const wakeIndex = lowerTranscript.indexOf(lowerWake);
          const command = transcript.substring(wakeIndex + this.wakeWord.length).trim();
          
          if (command.length > 0) {
            this.sendMessage(command);
          }
        }
      };
      
      this.recognition.onend = () => {
        this.isListening = false;
        this.notify();
        try {
          this.recognition.start();
        } catch (e) {}
      };

      try {
        this.recognition.start();
      } catch (e) {}
    }
  }

  public async testApi(geminiKey: string) {
    const res = await fetch('/api/settings/ai/test', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ gemini_key: geminiKey })
    });
    return await res.json();
  }

  public async saveSettings(geminiKey: string, wakeWord: string, devMode: boolean) {
    this.wakeWord = wakeWord.trim() || 'Hades';
    this.devMode = devMode;
    localStorage.setItem('hades_wake_word', this.wakeWord);
    localStorage.setItem('hades_dev_mode', String(this.devMode));

    if (geminiKey) {
      await fetch('/api/settings/ai', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ gemini_key: geminiKey })
      });
    }
    this.appendMessage('hades', 'Systems updated. New configuration applied.');
    this.notify();
  }
}

export const hadesService = new HadesService();
