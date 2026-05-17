import React from 'react';

export interface Tab {
  key: string;
  label: string;
}

interface TabBarProps {
  tabs: Tab[];
  active: string;
  onSelect: (key: string) => void;
}

export const TabBar: React.FC<TabBarProps> = ({ tabs, active, onSelect }) => (
  <nav style={{
    display: 'flex',
    gap: 4,
    borderBottom: '1px solid var(--border)',
    padding: '6px 20px',
    background: 'var(--bg-surface)',
    flexShrink: 0,
    overflowX: 'auto',
  }}>
    {tabs.map((tab) => {
      const isActive = active === tab.key;
      return (
        <button
          key={tab.key}
          onClick={() => onSelect(tab.key)}
          style={{
            padding: '10px 22px',
            cursor: 'pointer',
            border: 'none',
            borderRadius: 'var(--radius-sm)',
            background: isActive ? 'var(--accent-light)' : 'transparent',
            color: isActive ? 'var(--accent)' : 'var(--text-secondary)',
            fontWeight: isActive ? 600 : 400,
            fontSize: 14,
            fontFamily: 'var(--font-sans)',
            transition: 'all var(--transition)',
            letterSpacing: '0.02em',
            whiteSpace: 'nowrap',
          }}
          onMouseEnter={(e) => {
            if (!isActive) e.currentTarget.style.color = 'var(--text-primary)';
          }}
          onMouseLeave={(e) => {
            if (!isActive) e.currentTarget.style.color = 'var(--text-secondary)';
          }}
        >
          {tab.label}
        </button>
      );
    })}
  </nav>
);
