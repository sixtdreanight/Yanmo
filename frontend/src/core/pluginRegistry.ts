import React from 'react';

interface PluginEntry {
  name: string;
  displayName: string;
  component: React.ComponentType;
  icon: string;
}

const registry = new Map<string, PluginEntry>();

export function registerPlugin(entry: PluginEntry): void {
  registry.set(entry.name, entry);
}

export function getPlugin(name: string): PluginEntry | undefined {
  return registry.get(name);
}

export function allPlugins(): PluginEntry[] {
  return Array.from(registry.values());
}
