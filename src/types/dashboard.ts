import type { LucideIcon } from 'lucide-react';

export interface StatusItem {
  label: string;
  state: 'Online' | 'Degraded' | 'Offline';
}

export interface AgendaItem {
  title: string;
  time: string;
  color: string;
}

export interface ActivityItem {
  action: string;
  target: string;
  time: string;
  icon: LucideIcon;
  tone: string;
}

export interface QuickTool {
  label: string;
  icon: LucideIcon;
}

export interface Metric {
  label: string;
  value: string;
}