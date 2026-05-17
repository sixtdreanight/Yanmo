import React, { useState } from 'react';

interface ParsedTask {
  action: string;
  keywords: string[];
  priority: string;
}

interface PlannedTask {
  index: number;
  action: string;
  keywords: string[];
  phase: string;
  estimated_days_min: number;
  estimated_days_max: number;
  depends_on: number[];
  subtasks: string[];
  resources: string[];
  milestone: string;
}

interface ResearchPlan {
  title: string;
  total_days_min: number;
  total_days_max: number;
  tasks: PlannedTask[];
  timeline: { task_index: number; action: string; phase: string; start_day: number; end_day: number }[];
}

const phaseColors: Record<string, string> = {
  '调研阶段': 'var(--accent)',
  '设计阶段': '#8b5cf6',
  '实现阶段': 'var(--amber)',
  '实验阶段': 'var(--green)',
  '写作阶段': 'var(--red)',
};

export const TermAdvisorPanel: React.FC = () => {
  const [input, setInput] = useState('');
  const [tasks, setTasks] = useState<ParsedTask[]>([]);
  const [plan, setPlan] = useState<ResearchPlan | null>(null);
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState<'parse' | 'plan'>('plan');

  const doParse = async () => {
    if (!input.trim()) return;
    setLoading(true);
    setPlan(null);
    const res = await fetch('http://127.0.0.1:8000/api/term-advisor/parse', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: input }),
    });
    const data = await res.json();
    setTasks(data.tasks);
    setLoading(false);
  };

  const doPlan = async () => {
    if (!input.trim()) return;
    setLoading(true);
    setTasks([]);
    const res = await fetch('http://127.0.0.1:8000/api/term-advisor/plan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: input, title: '' }),
    });
    const data = await res.json();
    setPlan(data);
    setLoading(false);
  };

  const handleSubmit = () => {
    if (mode === 'plan') doPlan();
    else doParse();
  };

  return (
    <div style={{ maxWidth: 780 }}>
      <div style={{ background: 'var(--red-bg)', border: '1px solid #d93025', borderRadius: 8, padding: '12px 16px', marginBottom: 16, fontSize: 13, color: 'var(--red)' }}>
        Local model only. Advisor communications are classified as secret. Data never leaves your machine.
      </div>

      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder={"Paste the advisor's words...\n\ne.g. First do a literature review on Transformer attention mechanisms, then implement an improved sparse attention variant, finally run experiments on GLUE benchmark to compare with baseline"}
        rows={5}
        style={{ width: '100%', padding: 12, border: '1px solid #ddd', borderRadius: 8, fontSize: 14, resize: 'vertical', boxSizing: 'border-box', fontFamily: 'inherit' }}
      />

      <div style={{ display: 'flex', gap: 8, marginTop: 12, alignItems: 'center' }}>
        <select
          value={mode}
          onChange={(e) => setMode(e.target.value as 'parse' | 'plan')}
          style={{ padding: '8px 12px', border: '1px solid #ddd', borderRadius: 6, fontSize: 14, background: '#fff' }}
        >
          <option value="plan">Full Plan (Parse + Schedule)</option>
          <option value="parse">Parse Only</option>
        </select>
        <button onClick={handleSubmit} disabled={loading}
          style={{ padding: '8px 24px', background: 'var(--accent)', color: '#fff', border: 'none', borderRadius: 6, cursor: 'pointer', fontSize: 14 }}>
          {loading ? 'Working...' : mode === 'plan' ? 'Generate Plan' : 'Parse'}
        </button>
      </div>

      {/* Parse-only results */}
      {tasks.length > 0 && !plan && (
        <div style={{ marginTop: 20 }}>
          <h3 style={{ fontSize: 16, marginBottom: 12 }}>Parsed Tasks ({tasks.length})</h3>
          {tasks.map((t, i) => (
            <div key={i} style={{ border: '1px solid #e0e0e0', borderRadius: 8, padding: 12, marginBottom: 8 }}>
              <span style={{ fontWeight: 600 }}>{t.action}</span>
              {t.keywords.length > 0 && (
                <div style={{ marginTop: 6, display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                  {t.keywords.map((kw, j) => (
                    <span key={j} style={{ background: 'var(--accent-soft)', color: 'var(--accent)', padding: '2px 8px', borderRadius: 12, fontSize: 12 }}>
                      {kw}
                    </span>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Full plan results */}
      {plan && (
        <div style={{ marginTop: 20 }}>
          {/* Summary bar */}
          <div style={{ display: 'flex', gap: 16, marginBottom: 20 }}>
            <div style={{ flex: 1, background: 'var(--accent-soft)', borderRadius: 8, padding: '12px 16px', textAlign: 'center' }}>
              <div style={{ fontSize: 24, fontWeight: 700, color: 'var(--accent)' }}>{plan.tasks.length}</div>
              <div style={{ fontSize: 12, color: 'var(--text-secondary)' }}>Phases</div>
            </div>
            <div style={{ flex: 1, background: '#fef7e0', borderRadius: 8, padding: '12px 16px', textAlign: 'center' }}>
              <div style={{ fontSize: 24, fontWeight: 700, color: 'var(--amber)' }}>{plan.total_days_min}–{plan.total_days_max}</div>
              <div style={{ fontSize: 12, color: 'var(--text-secondary)' }}>Days (estimated)</div>
            </div>
            <div style={{ flex: 1, background: 'var(--green-bg)', borderRadius: 8, padding: '12px 16px', textAlign: 'center' }}>
              <div style={{ fontSize: 24, fontWeight: 700, color: 'var(--green)' }}>
                {plan.timeline.length > 0 ? plan.timeline[plan.timeline.length - 1].end_day : 0}
              </div>
              <div style={{ fontSize: 12, color: 'var(--text-secondary)' }}>Timeline (days)</div>
            </div>
          </div>

          {/* Timeline */}
          <h3 style={{ fontSize: 16, marginBottom: 12 }}>Timeline</h3>
          <div style={{ marginBottom: 4, position: 'relative', paddingLeft: 24 }}>
            <div style={{ position: 'absolute', left: 8, top: 0, bottom: 0, width: 2, background: 'var(--border)' }} />
            {plan.timeline.map((entry) => {
              const color = phaseColors[entry.phase] || 'var(--text-secondary)';
              return (
                <div key={entry.task_index} style={{ position: 'relative', marginBottom: 4, padding: '10px 14px', border: '1px solid #e8e8e8', borderRadius: 8, background: 'var(--bg-card)' }}>
                  <div style={{ position: 'absolute', left: -20, top: 14, width: 10, height: 10, borderRadius: '50%', background: color }} />
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                      <span style={{ fontWeight: 600, fontSize: 14 }}>{entry.action}</span>
                      <span style={{ fontSize: 11, color: '#fff', background: color, padding: '1px 6px', borderRadius: 8, marginLeft: 8 }}>{entry.phase}</span>
                    </div>
                    <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>
                      Day {entry.start_day} – {entry.end_day}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Detailed task cards */}
          <h3 style={{ fontSize: 16, marginBottom: 12, marginTop: 24 }}>Task Details</h3>
          {plan.tasks.map((task) => {
            const color = phaseColors[task.phase] || 'var(--text-secondary)';
            return (
              <div key={task.index} style={{ border: `1px solid ${color}20`, borderLeft: `3px solid ${color}`, borderRadius: 8, padding: 16, marginBottom: 12, background: 'var(--bg-card)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 10 }}>
                  <div>
                    <span style={{ fontWeight: 700, fontSize: 16 }}>{task.action}</span>
                    <span style={{ fontSize: 11, color: '#fff', background: color, padding: '2px 8px', borderRadius: 10, marginLeft: 8 }}>{task.phase}</span>
                    {task.depends_on.length > 0 && (
                      <span style={{ fontSize: 12, color: 'var(--text-muted)', marginLeft: 8 }}>
                        depends on: {task.depends_on.map((d) => `#${d}`).join(', ')}
                      </span>
                    )}
                  </div>
                  <span style={{ fontSize: 13, color: color, fontWeight: 600, whiteSpace: 'nowrap' }}>
                    {task.estimated_days_min}–{task.estimated_days_max} days
                  </span>
                </div>

                {task.keywords.length > 0 && (
                  <div style={{ marginBottom: 10, display: 'flex', gap: 4, flexWrap: 'wrap' }}>
                    {task.keywords.map((kw, j) => (
                      <span key={j} style={{ background: `${color}15`, color: color, padding: '1px 8px', borderRadius: 10, fontSize: 11 }}>
                        {kw}
                      </span>
                    ))}
                  </div>
                )}

                <details style={{ marginBottom: 6 }}>
                  <summary style={{ cursor: 'pointer', fontSize: 13, color: '#555', fontWeight: 500 }}>
                    Subtasks ({task.subtasks.length})
                  </summary>
                  <ul style={{ margin: '6px 0 0 0', paddingLeft: 20, fontSize: 13, color: '#444', lineHeight: 1.7 }}>
                    {task.subtasks.map((s, j) => <li key={j}>{s}</li>)}
                  </ul>
                </details>

                {task.resources.length > 0 && (
                  <details>
                    <summary style={{ cursor: 'pointer', fontSize: 13, color: '#555', fontWeight: 500 }}>
                      Resources ({task.resources.length})
                    </summary>
                    <ul style={{ margin: '6px 0 0 0', paddingLeft: 20, fontSize: 13, color: '#444', lineHeight: 1.7 }}>
                      {task.resources.map((r, j) => <li key={j}>{r}</li>)}
                    </ul>
                  </details>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
