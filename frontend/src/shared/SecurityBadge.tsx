import React from 'react';
import type { Classification } from '../core/types';

interface Props {
  classification: Classification;
  onChange?: (c: Classification) => void;
  readonly?: boolean;
}

const styles: Record<Classification, { bg: string; text: string; border: string }> = {
  secret: { bg: 'var(--red-bg)', text: 'var(--red)', border: '#fecaca' },
  cautious: { bg: 'var(--amber-bg)', text: 'var(--amber)', border: '#fde68a' },
  public: { bg: 'var(--green-bg)', text: 'var(--green)', border: '#bbf7d0' },
};

const labels: Record<Classification, string> = {
  secret: '机密',
  cautious: '审慎',
  public: '公开',
};

export const SecurityBadge: React.FC<Props> = ({ classification, onChange, readonly }) => {
  const s = styles[classification];

  if (readonly) {
    return (
      <span className="badge" style={{
        background: s.bg,
        color: s.text,
        border: `1px solid ${s.border}`,
      }}>
        {labels[classification]}
      </span>
    );
  }

  return (
    <select
      value={classification}
      onChange={(e) => onChange?.(e.target.value as Classification)}
      style={{
        padding: '5px 10px',
        borderRadius: 'var(--radius-sm)',
        border: `1px solid ${s.border}`,
        background: s.bg,
        color: s.text,
        fontWeight: 600,
        fontSize: 12,
        cursor: 'pointer',
      }}
    >
      <option value="secret">机密</option>
      <option value="cautious">审慎</option>
      <option value="public">公开</option>
    </select>
  );
};
