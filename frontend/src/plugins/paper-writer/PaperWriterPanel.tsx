import React, { useState } from 'react';

interface OutlineSection {
  title: string;
  key_points: string[];
  estimated_words: number;
}

interface BibEntry {
  cite_key: string;
  title: string;
  author: string;
  year: string;
  journal: string;
}

export const PaperWriterPanel: React.FC = () => {
  const [topic, setTopic] = useState('');
  const [outline, setOutline] = useState<OutlineSection[]>([]);
  const [bibtex, setBibtex] = useState('');
  const [entries, setEntries] = useState<BibEntry[]>([]);
  const [loading, setLoading] = useState(false);

  const generateOutline = async () => {
    if (!topic.trim()) return;
    setLoading(true);
    const res = await fetch('http://127.0.0.1:8000/api/paper-writer/outline', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topic }),
    });
    const data = await res.json();
    setOutline(data.sections);
    setLoading(false);
  };

  const parseBibtex = async () => {
    if (!bibtex.trim()) return;
    const res = await fetch('http://127.0.0.1:8000/api/paper-writer/citation/parse', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ bibtex }),
    });
    const data = await res.json();
    setEntries(data.entries);
  };

  const totalWords = outline.reduce((sum, s) => sum + s.estimated_words, 0);

  return (
    <div style={{ maxWidth: 800 }}>
      <div style={{ marginBottom: 24 }}>
        <h3 style={{ fontSize: 16, marginBottom: 12 }}>Outline Generator</h3>
        <div style={{ display: 'flex', gap: 8 }}>
          <input value={topic} onChange={(e) => setTopic(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && generateOutline()}
            placeholder="Paper title..."
            style={{ flex: 1, padding: '8px 12px', border: '1px solid #ddd', borderRadius: 6, fontSize: 14 }} />
          <button onClick={generateOutline} disabled={loading}
            style={{ padding: '8px 20px', background: 'var(--accent)', color: '#fff', border: 'none', borderRadius: 6, cursor: 'pointer' }}>
            {loading ? 'Generating...' : 'Generate Outline'}
          </button>
        </div>

        {outline.length > 0 && (
          <div style={{ marginTop: 16 }}>
            <div style={{ fontSize: 13, color: '#888', marginBottom: 12 }}>Estimated total: {totalWords} words</div>
            {outline.map((s, i) => (
              <div key={i} style={{ border: '1px solid #e0e0e0', borderRadius: 8, padding: 12, marginBottom: 8 }}>
                <div style={{ fontWeight: 600, marginBottom: 6 }}>{s.title} <span style={{ fontWeight: 400, fontSize: 12, color: '#888' }}>(~{s.estimated_words} words)</span></div>
                <ul style={{ margin: 0, paddingLeft: 20, fontSize: 13, color: '#555' }}>
                  {s.key_points.map((kp, j) => <li key={j}>{kp}</li>)}
                </ul>
              </div>
            ))}
          </div>
        )}
      </div>

      <div>
        <h3 style={{ fontSize: 16, marginBottom: 12 }}>Citation Manager</h3>
        <textarea value={bibtex} onChange={(e) => setBibtex(e.target.value)}
          placeholder="Paste BibTeX entries..."
          rows={6}
          style={{ width: '100%', padding: 12, border: '1px solid #ddd', borderRadius: 8, fontSize: 13, resize: 'vertical', boxSizing: 'border-box', fontFamily: 'monospace' }} />
        <button onClick={parseBibtex}
          style={{ marginTop: 8, padding: '6px 16px', background: 'var(--accent)', color: '#fff', border: 'none', borderRadius: 6, cursor: 'pointer', fontSize: 13 }}>
          Parse
        </button>

        {entries.length > 0 && (
          <div style={{ marginTop: 16 }}>
            {entries.map((e, i) => (
              <div key={i} style={{ border: '1px solid #e0e0e0', borderRadius: 6, padding: '8px 12px', marginBottom: 6, fontSize: 13 }}>
                <span style={{ fontWeight: 600 }}>[{e.cite_key}]</span> {e.title} — {e.author} ({e.year}), {e.journal}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
