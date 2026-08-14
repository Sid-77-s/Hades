import { useState, useEffect } from 'react';
import { hadesService, HadesState, ChatMessage, ExecutionEvent } from './HadesService';

export function useHades() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [executionEvents, setExecutionEvents] = useState<ExecutionEvent[]>([]);
  const [hadesState, setHadesState] = useState<HadesState>('idle');
  const [isListening, setIsListening] = useState<boolean>(false);
  const [userName, setUserName] = useState<string | null>(hadesService.userName);

  useEffect(() => {
    const updateState = () => {
      setMessages([...hadesService.messages]);
      setExecutionEvents([...hadesService.executionEvents]);
      setHadesState(hadesService.hadesState);
      setIsListening(hadesService.isListening);
      setUserName(hadesService.userName);
    };

    const unsubscribe = hadesService.subscribe(updateState);
    updateState();

    return () => unsubscribe();
  }, []);

  return {
    messages,
    executionEvents,
    hadesState,
    isListening,
    userName,
    sendMessage: (text: string) => hadesService.sendMessage(text),
    saveName: (name: string) => hadesService.saveName(name),
    init: () => hadesService.init(),
  };
}
