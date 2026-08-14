import {
  FileTextIcon,
  GlobeIcon,
  ClipboardListIcon,
  FileBarChartIcon,
  MailIcon,
  UploadIcon,
  CameraIcon,
  MicIcon } from
'lucide-react';
import type {
  ActivityItem,
  AgendaItem,
  Metric,
  QuickTool,
  StatusItem } from
'../types/dashboard';

export const systemStatus: StatusItem[] = [
{ label: 'Core Systems', state: 'Online' },
{ label: 'Memory Engine', state: 'Online' },
{ label: 'Execution Engine', state: 'Online' },
{ label: 'Security Layer', state: 'Online' }];


export const agenda: AgendaItem[] = [
{ title: 'Team Standup', time: '10:00 AM', color: '#22d3ee' },
{ title: 'Product Review', time: '02:00 PM', color: '#ef4444' },
{ title: 'Investor Call', time: '04:30 PM', color: '#22d3ee' },
{ title: 'Gym', time: '07:00 PM', color: '#3b82f6' }];


export const metrics: Metric[] = [
{ label: 'CPU', value: '23%' },
{ label: 'Memory', value: '45%' },
{ label: 'Tasks', value: '7' },
{ label: 'Models', value: '5' }];


export const throughput: number[] = [
18, 22, 16, 26, 21, 34, 28, 24, 30, 27, 38, 31, 26, 33, 29, 41, 35, 30, 37, 32, 28, 36, 30, 34,
27, 31, 25, 33, 29, 35];


export const recentActivity: ActivityItem[] = [
{ action: 'Created file', target: 'dashboard.tsx', time: '2m ago', icon: FileTextIcon, tone: '#22d3ee' },
{ action: 'Researched', target: 'AI operating systems', time: '15m ago', icon: GlobeIcon, tone: '#3b82f6' },
{ action: 'Updated mission', target: 'AI OS Dashboard', time: '32m ago', icon: ClipboardListIcon, tone: '#22d3ee' },
{ action: 'Generated report', target: 'market-analysis.pdf', time: '1h ago', icon: FileBarChartIcon, tone: '#ef4444' }];


export const quickTools: QuickTool[] = [
{ label: 'New Mission', icon: MailIcon },
{ label: 'Upload File', icon: UploadIcon },
{ label: 'Capture', icon: CameraIcon },
{ label: 'Voice Input', icon: MicIcon }];


export const suggestions: string[] = [
'What features will it include?',
'Any specific design preferences?',
"Who's the primary user?"];


export const heroImage = "/d95ea0d7-e7ed-4fe3-8d04-4a5cd2331770.jpg";


export const userAvatar = "/6ba22144-3b1e-4fb7-b42e-45944cdaf6d0.jpg";