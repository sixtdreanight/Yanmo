import React, { useState } from 'react';
import { SecurityBadge } from '../../shared/SecurityBadge';
import type { Classification } from '../../core/types';

interface EvalResult {
  innovation_score: number;
  rationality_score: number;
  methodology_score: number;
  strengths: string[];
  weaknesses: string[];
  suggestions: string[];
}

export const EvaluatorPanel: React.FC = () => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [classification, setClassification] = useState<Classification>('cautious');
  const [result, setResult] = useState<EvalResult | null>(null);
  const [loading, setLoading] = useState(false);

  const evaluate = async () => {
    if (!description.trim()) return;
    setLoading(true);
    const res = await fetch('http://127.0.0.1:8000/api/evaluator/evaluate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, description }),
    });
    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 700 }}>
      <div style={{ marginBottom: 16, display: 'flex', alignItems: 'center', gap: 8 }}>
        <span style={{ fontSize: 13 }}>Data classification:</span>
        <SecurityBadge classification={classification} onChange={setClassification} />
      </div>

      <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Project name"
        style={{ width: '100%', padding: '8px 12px', border: '1px solid #ddd', borderRadius: 6, fontSize: 14, marginBottom: 12, boxSizing: 'border-box' }} />

      <textarea value={description} onChange={(e) => setDescription(e.target.value)}
        placeholder="Project description (research question, method, innovation, expected results, etc.)"
        rows={8}
        style={{ width: '100%', padding: 12, border: '1px solid #ddd', borderRadius: 8, fontSize: 14, resize: 'vertical', boxSizing: 'border-box' }} />

      <button onClick={evaluate} disabled={loading}
        style={{ marginTop: 12, padding: '8px 24px', background: 'var(--accent)', color: '#fff', border: 'none', borderRadius: 6, cursor: 'pointer', fontSize: 14 }}>
        {loading ? 'Evaluating...' : 'Evaluate'}
      </button>

      {result && (
        <div style={{ marginTop: 20 }}>
          <div style={{ display: 'flex', gap: 16, marginBottom: 20 }}>
            {[
              { label: 'Innovation', score: result.innovation_score, color: 'var(--accent)' },
              { label: 'Rationality', score: result.rationality_score, color: '#188038' },
              { label: 'Methodology', score: result.methodology_score, color: '#e37400' },
            ].map((item) => (
              <div key={item.label} style={{ flex: 1, textAlign: 'center', border: '1px solid #e0e0e0', borderRadius: 8, padding: 12 }}>
                <div style={{ fontSize: 28, fontWeight: 700, color: item.color }}>{item.score}</div>
                <div style={{ fontSize: 12, color: '#888', marginTop: 4 }}>/10 {item.label}</div>
              </div>
            ))}
          </div>
          {result.strengths.length > 0 && (
            <div style={{ marginBottom: 12 }}>
              <strong style={{ color: '#188038' }}>Strengths</strong>
              <ul style={{ margin: '4px 0', paddingLeft: 20, fontSize: 13 }}>{result.strengths.map((s, i) => <li key={i}>{s}</li>)}</ul>
            </div>
          )}
          {result.weaknesses.length > 0 && (
            <div style={{ marginBottom: 12 }}>
              <strong style={{ color: '#d93025' }}>Weaknesses</strong>
              <ul style={{ margin: '4px 0', paddingLeft: 20, fontSize: 13 }}>{result.weaknesses.map((w, i) => <li key={i}>{w}</li>)}</ul>
            </div>
          )}
          {result.suggestions.length > 0 && (
            <div>
              <strong style={{ color: 'var(--accent)' }}>Suggestions</strong>
              <ul style={{ margin: '4px 0', paddingLeft: 20, fontSize: 13 }}>{result.suggestions.map((s, i) => <li key={i}>{s}</li>)}</ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
