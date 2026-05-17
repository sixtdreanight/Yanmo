export type Classification = 'secret' | 'cautious' | 'public';

export interface PluginManifest {
  name: string;
  displayName: string;
  version: string;
}

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export interface SecurityBadgeProps {
  classification: Classification;
  onChange: (c: Classification) => void;
}

export interface PluginPanelProps {
  storage: StorageAPI;
  security: SecurityAPI;
  llm: LLMAPI;
  bus: EventBusAPI;
}

export interface StorageAPI {
  query: (sql: string, params?: unknown[]) => Promise<Record<string, unknown>[]>;
  search: (collection: string, query: string, n: number) => Promise<string[][]>;
}

export interface SecurityAPI {
  classify: (docId: string, level: Classification) => Promise<void>;
  allowCloud: (docId: string) => Promise<boolean>;
}

export interface LLMAPI {
  chat: (messages: ChatMessage[], classification: Classification, docId: string) => Promise<string>;
}

export interface EventBusAPI {
  emit: (event: string, data: Record<string, unknown>) => Promise<void>;
}
