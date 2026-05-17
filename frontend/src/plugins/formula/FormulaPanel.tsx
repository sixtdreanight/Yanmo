import React, { useState } from 'react';

interface VerificationResult {
  basic: { is_valid: boolean; errors: string[]; warnings: string[]; suggestions: string[] };
  sympy: { is_valid: boolean; errors: string[]; suggestions: string[] };
  cross_validated: boolean;
}

export const FormulaPanel: React.FC = () => {
  const [latex, setLatex] = useState('');
  const [result, setResult] = useState<VerificationResult | null>(null);
  const [loading, setLoading] = useState(false);

  const verify = async () => {
    if (!latex.trim()) return;
    setLoading(true);
    const res = await fetch('http://127.0.0.1:8000/api/formula/verify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ expression: latex }),
    });
    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 800 }}>
      <div style={{ fontSize: 13, color: '#666', marginBottom: 12 }}>
        Pure local computation (SymPy + SciPy). Does not use LLM. Data never leaves your machine.
      </div>

      <div style={{ display: 'flex', gap: 16 }}>
        <div style={{ flex: 1 }}>
          <label style={{ fontWeight: 600, fontSize: 14, display: 'block', marginBottom: 8 }}>LaTeX Source</label>
          <textarea
            value={latex}
            onChange={(e) => setLatex(e.target.value)}
            placeholder={"Paste LaTeX formula...\ne.g. \\frac{-b + \\sqrt{b^2 - 4ac}}{2a}"}
            rows={6}
            style={{ width: '100%', padding: 12, border: '1px solid #ddd', borderRadius: 8, fontSize: 14, resize: 'vertical', boxSizing: 'border-box', fontFamily: 'monospace' }} />
          <button onClick={verify} disabled={loading}
            style={{ marginTop: 12, padding: '8px 24px', background: 'var(--accent)', color: '#fff', border: 'none', borderRadius: 6, cursor: 'pointer', fontSize: 14 }}>
            {loading ? 'Verifying...' : 'Cross-Validate'}
          </button>
        </div>

        <div style={{ flex: 1, border: '1px solid #e0e0e0', borderRadius: 8, padding: 16, background: '#fafafa', minHeight: 200 }}>
          <div style={{ fontWeight: 600, fontSize: 14, marginBottom: 8 }}>Preview</div>
          <div style={{ fontSize: 20, textAlign: 'center', padding: '20px 0', color: '#333' }}>
            {latex || '...'}
          </div>
        </div>
      </div>

      {result && (
        <div style={{ marginTop: 20 }}>
          <div style={{
            padding: '12px 16px', borderRadius: 8, marginBottom: 12,
            background: result.cross_validated ? '#e6f4ea' : '#fce8e6',
            border: `1px solid ${result.cross_validated ? '#188038' : '#d93025'}`,
            color: result.cross_validated ? '#188038' : '#d93025',
            fontWeight: 600,
          }}>
            {result.cross_validated ? 'Dual-channel verification passed' : 'Verification found issues'}
          </div>
          {result.basic.errors.length > 0 && (
            <div style={{ fontSize: 13, color: '#d93025', marginBottom: 8 }}>
              Basic check: {result.basic.errors.join('; ')}
            </div>
          )}
          {result.basic.warnings.length > 0 && (
            <div style={{ fontSize: 13, color: '#e37400', marginBottom: 8 }}>
              Warning: {result.basic.warnings.join('; ')}
            </div>
          )}
          {result.sympy.suggestions.length > 0 && (
            <div style={{ fontSize: 13, color: '#555' }}>
              {result.sympy.suggestions.join('; ')}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
