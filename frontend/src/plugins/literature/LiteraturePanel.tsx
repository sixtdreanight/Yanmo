import React, { useState, useEffect, useCallback } from 'react';

interface Paper {
  id?: string;
  arxiv_id?: string;
  title: string;
  authors: string;
  summary: string;
  published: string;
  link: string;
  venue?: string | { name?: string };
  citations?: number;
  year?: string;
  doi?: string;
}

const paperKey = (p: Paper): string => p.id || p.arxiv_id || p.title;
const paperLink = (p: Paper): string => p.link || (p.doi ? `https://doi.org/${p.doi}` : '#');
const venueName = (p: Paper): string => {
  if (!p.venue) return '';
  if (typeof p.venue === 'string') return p.venue;
  return p.venue.name || '';
};


const timeAgo = (dateStr: string): string => {
  if (!dateStr) return '';
  const pub = new Date(dateStr);
  const now = new Date();
  const days = Math.floor((now.getTime() - pub.getTime()) / (1000 * 60 * 60 * 24));
  if (days === 0) return 'Today';
  if (days === 1) return 'Yesterday';
  if (days < 7) return `${days}d ago`;
  if (days < 30) return `${Math.floor(days / 7)}w ago`;
  return pub.toLocaleDateString('zh-CN');
};

export const LiteraturePanel: React.FC = () => {
  const [papers, setPapers] = useState<Paper[]>([]);
  const [interests, setInterests] = useState<string[]>([]);
  const [newInterest, setNewInterest] = useState('');
  const [loading, setLoading] = useState(false);
  const [summaries, setSummaries] = useState<Record<string, string>>({});
  const [searchQuery, setSearchQuery] = useState('');
  const [showSearch, setShowSearch] = useState(false);

  const loadFeed = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch('http://127.0.0.1:8000/api/literature/feed', { method: 'POST' });
      const data = await res.json();
      setPapers(data.papers ?? []);
      if (data.interests?.length) setInterests(data.interests);
    } catch (e) {
      setPapers([]);
    } finally {
      setLoading(false);
    }
  }, []);

  const loadInterests = async () => {
    const res = await fetch('http://127.0.0.1:8000/api/literature/interests');
    const data = await res.json();
    if (data.keywords?.length) setInterests(data.keywords);
  };

  useEffect(() => {
    loadInterests();
    loadFeed();
  }, [loadFeed]);

  const [gaps, setGaps] = useState<{ direction: string; confidence: string; reason: string }[]>([]);
  const [showGaps, setShowGaps] = useState(false);

  const findGaps = async () => {
    if (papers.length === 0) return;
    const res = await fetch('http://127.0.0.1:8000/api/evaluator/gap-analysis', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ papers: papers.slice(0, 10) }),
    });
    const data = await res.json();
    setGaps(data.gaps || []);
    setShowGaps(true);
  };

  const [graph, setGraph] = useState<{ nodes: { id: string; name: string; symbolSize: number }[]; edges: { source: string; target: string; weight: number; shared_keywords: string[] }[]; total_nodes: number; total_edges: number } | null>(null);

  const buildGraph = async () => {
    if (papers.length < 2) return;
    const res = await fetch('http://127.0.0.1:8000/api/literature/citation-graph', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ papers: papers.slice(0, 20) }),
    });
    const data = await res.json();
    setGraph(data);
  };

  const saveInterests = async (updated: string[]) => {
    setInterests(updated);
    await fetch('http://127.0.0.1:8000/api/literature/interests', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ keywords: updated }),
    });
  };

  const addInterest = () => {
    const kw = newInterest.trim();
    if (!kw || interests.includes(kw)) return;
    const updated = [...interests, kw];
    saveInterests(updated);
    setNewInterest('');
  };

  const removeInterest = (kw: string) => {
    saveInterests(interests.filter((k) => k !== kw));
  };

  const doSearch = async () => {
    if (!searchQuery.trim()) return;
    setLoading(true);
    const res = await fetch('http://127.0.0.1:8000/api/literature/fetch', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: searchQuery, max_results: 10 }),
    });
    const data = await res.json();
    setPapers(data.papers);
    setLoading(false);
  };

  const summarizePaper = async (paper: Paper) => {
    if (summaries[paperKey(paper)]) return;
    const res = await fetch('http://127.0.0.1:8000/api/literature/summarize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(paper),
    });
    const data = await res.json();
    setSummaries((prev) => ({ ...prev, [paperKey(paper)]: data.summary }));
  };

  return (
    <div style={{ maxWidth: 780 }}>
      {/* Interests bar */}
      <div style={{ marginBottom: 16 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8, flexWrap: 'wrap' }}>
          <span style={{ fontSize: 13, color: '#888', whiteSpace: 'nowrap' }}>Your fields:</span>
          {interests.map((kw) => (
            <span key={kw}
              onClick={() => removeInterest(kw)}
              title="Click to remove"
              style={{ background: '#e8f0fe', color: 'var(--accent)', padding: '3px 10px', borderRadius: 14, fontSize: 12, cursor: 'pointer', userSelect: 'none' }}>
              {kw} ×
            </span>
          ))}
          <input
            value={newInterest}
            onChange={(e) => setNewInterest(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && addInterest()}
            placeholder="+ add keyword"
            style={{ width: 120, padding: '4px 8px', border: '1px dashed #ccc', borderRadius: 14, fontSize: 12, outline: 'none' }}
          />
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button onClick={loadFeed} disabled={loading}
            style={{ padding: '6px 16px', background: 'var(--accent)', color: '#fff', border: 'none', borderRadius: 6, cursor: 'pointer', fontSize: 13, fontWeight: 500 }}>
            {loading ? 'Loading...' : 'Refresh Feed'}
          </button>
          <button onClick={() => setShowSearch(!showSearch)}
            style={{ padding: '6px 16px', background: 'transparent', color: '#888', border: '1px solid #ddd', borderRadius: 6, cursor: 'pointer', fontSize: 13 }}>
            {showSearch ? 'Hide Search' : 'Search...'}
          </button>
          <button onClick={findGaps} disabled={papers.length === 0}
            style={{ padding: '6px 16px', background: 'transparent', color: 'var(--accent)', border: '1px solid var(--accent-border)', borderRadius: 6, cursor: 'pointer', fontSize: 13 }}>
            找思路
          </button>
          <button onClick={buildGraph} disabled={papers.length < 2}
            style={{ padding: '6px 16px', background: 'transparent', color: 'var(--accent)', border: '1px solid var(--accent-border)', borderRadius: 6, cursor: 'pointer', fontSize: 13 }}>
            引用图
          </button>
          {papers.length > 0 && (
            <span style={{ fontSize: 12, color: '#aaa', alignSelf: 'center' }}>
              {papers.length} papers
            </span>
          )}
        </div>
      </div>

      {/* Collapsible search */}
      {showSearch && (
        <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
          <input value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && doSearch()}
            placeholder="Search ArXiv..."
            style={{ flex: 1, padding: '8px 12px', border: '1px solid #ddd', borderRadius: 6, fontSize: 14 }} />
          <button onClick={doSearch}
            style={{ padding: '8px 16px', background: '#333', color: '#fff', border: 'none', borderRadius: 6, cursor: 'pointer', fontSize: 13 }}>
            Search
          </button>
        </div>
      )}

      {/* Empty state */}
      {!loading && papers.length === 0 && (
        <div style={{ textAlign: 'center', padding: 48, color: '#aaa' }}>
          <div style={{ fontSize: 40, marginBottom: 12 }}>—</div>
          <div style={{ fontSize: 15, marginBottom: 8 }}>No papers yet</div>
          <div style={{ fontSize: 13 }}>
            Add your research interests above and click "Refresh Feed"
          </div>
        </div>
      )}

      {/* Citation graph */}
      {graph && (
        <div style={{ marginBottom: 20, border: '1px solid var(--border)', borderRadius: 10, padding: 16, background: 'var(--bg-card)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
            <span style={{ fontWeight: 600, fontSize: 15 }}>Citation Graph ({graph.total_nodes} papers, {graph.total_edges} connections)</span>
            <button onClick={() => setGraph(null)} style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text-muted)', fontSize: 18 }}>×</button>
          </div>
          <div style={{ maxHeight: 400, overflow: 'auto' }}>
            {graph.edges.length === 0 ? (
              <div style={{ textAlign: 'center', padding: 32, color: 'var(--text-muted)' }}>No shared keywords between papers. Try adding more papers.</div>
            ) : (
              <div>
                {graph.edges.slice(0, 20).map((edge, i) => {
                  const src = graph.nodes.find((n: { id: string }) => n.id === edge.source);
                  const tgt = graph.nodes.find((n: { id: string }) => n.id === edge.target);
                  return (
                    <div key={i} style={{
                      display: 'flex', alignItems: 'center', gap: 12, padding: '8px 0',
                      borderBottom: '1px solid var(--border-light)', fontSize: 12,
                    }}>
                      <span style={{ fontWeight: 500, flex: 1, textAlign: 'right', color: 'var(--accent)' }}>{src?.name || edge.source}</span>
                      <span style={{
                        flexShrink: 0, padding: '2px 8px', borderRadius: 10, fontSize: 10,
                        background: `color-mix(in srgb, var(--accent) ${edge.weight * 20}%, transparent)`,
                        color: 'var(--accent)', fontWeight: 600,
                      }}>{edge.weight} shared</span>
                      <span style={{ fontWeight: 500, flex: 1, color: 'var(--text-primary)' }}>{tgt?.name || edge.target}</span>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Gap analysis results */}
      {showGaps && gaps.length > 0 && (
        <div style={{ marginBottom: 20, border: '1px solid var(--accent-border)', borderRadius: 10, padding: 16, background: 'var(--accent-soft)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
            <span style={{ fontWeight: 600, fontSize: 15, color: 'var(--accent)' }}>Research Gaps</span>
            <button onClick={() => setShowGaps(false)}
              style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text-muted)', fontSize: 18 }}>×</button>
          </div>
          {gaps.map((g, i) => (
            <div key={i} style={{ marginBottom: 8, fontSize: 13, lineHeight: 1.6 }}>
              <span style={{ fontWeight: 600 }}>{g.direction}</span>
              <span style={{
                marginLeft: 8, fontSize: 10, padding: '1px 6px', borderRadius: 8,
                background: g.confidence === 'high' ? 'var(--red-bg)' : 'var(--amber-bg)',
                color: g.confidence === 'high' ? 'var(--red)' : 'var(--amber)',
              }}>{g.confidence === 'high' ? 'high confidence' : 'medium'}</span>
              <div style={{ color: 'var(--text-secondary)', marginTop: 2 }}>{g.reason}</div>
            </div>
          ))}
        </div>
      )}

      {/* News feed */}
      <div>
        {papers.map((paper) => {
          const isNew = paper.published && new Date(paper.published).getTime() > Date.now() - 7 * 24 * 60 * 60 * 1000;

          return (
            <div key={paperKey(paper)}
              style={{
                border: '1px solid var(--border)',
                borderRadius: 10,
                padding: 20,
                marginBottom: 12,
                background: 'var(--bg-card)',
                position: 'relative',
              }}>
              {/* New badge */}
              {isNew && (
                <span style={{
                  position: 'absolute', top: -1, right: -1,
                  background: '#d93025', color: '#fff',
                  padding: '2px 8px', borderRadius: '0 10px 0 8px',
                  fontSize: 11, fontWeight: 600,
                }}>
                  NEW
                </span>
              )}

              {/* Title */}
              <h4 style={{ margin: '0 0 8px 0', fontSize: 16, lineHeight: 1.4, paddingRight: isNew ? 40 : 0 }}>
                <a href={paperLink(paper)} target="_blank" rel="noopener noreferrer"
                  style={{ color: 'var(--accent)', textDecoration: 'none' }}>
                  {paper.title}
                </a>
                {paper.doi && (
                  <span style={{ fontSize: 10, color: 'var(--text-muted)', marginLeft: 6 }}>DOI</span>
                )}
              </h4>

              {/* Meta line */}
              <div style={{ fontSize: 12, color: 'var(--text-muted)', marginBottom: 10, display: 'flex', gap: 10, alignItems: 'center', flexWrap: 'wrap' }}>
                <span>{paper.authors.split(',').slice(0, 3).join(', ')}{paper.authors.split(',').length > 3 ? ' et al.' : ''}</span>
                {paper.year && <span style={{ fontWeight: 500 }}>{paper.year}</span>}
                {paper.citations !== undefined && paper.citations > 0 && (
                  <span style={{ color: 'var(--green)', fontWeight: 500 }}>{paper.citations} cites</span>
                )}
                {venueName(paper) && (
                  <span style={{ fontStyle: 'italic' }}>{venueName(paper)}</span>
                )}
                <span>{timeAgo(paper.published)}</span>
              </div>

              {/* Abstract preview */}
              <div style={{ fontSize: 13, lineHeight: 1.65, color: '#555', marginBottom: 10 }}>
                {paper.summary.slice(0, 280)}{paper.summary.length > 280 ? '...' : ''}
              </div>

              {/* Summarize button / result */}
              {summaries[paperKey(paper)] ? (
                <div style={{
                  background: '#f0f7ff', borderLeft: '2px solid #1a73e8',
                  borderRadius: 4, padding: '8px 12px', fontSize: 13, lineHeight: 1.55, color: '#333',
                }}>
                  {summaries[paperKey(paper)]}
                </div>
              ) : (
                <button onClick={() => summarizePaper(paper)}
                  style={{
                    padding: '3px 10px', background: 'transparent', color: 'var(--accent)',
                    border: '1px solid #1a73e840', borderRadius: 4, cursor: 'pointer', fontSize: 12,
                  }}>
                  AI Summarize
                </button>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
