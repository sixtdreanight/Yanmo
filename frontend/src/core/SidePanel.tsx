import React from 'react';

interface SidePanelProps {
  children: React.ReactNode;
  width?: number;
}

export const SidePanel: React.FC<SidePanelProps> = ({ children, width = 320 }) => (
  <aside style={{
    width,
    borderLeft: '1px solid var(--border)',
    background: 'var(--bg-sidebar)',
    overflowY: 'auto',
    display: 'flex',
    flexDirection: 'column',
  }}>
    {children}
  </aside>
);
