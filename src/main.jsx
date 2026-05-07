import React, { useEffect, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { BookOpen, Boxes, Brain, ExternalLink, FileText, GitBranch, Network, Search, Sparkles, Workflow, Download, Layers, ArrowRight } from 'lucide-react';
import './styles.css';

const tabs = [
  { id: 'overview', label: 'Overview', icon: Sparkles },
  { id: 'read', label: 'Read', icon: BookOpen },
  { id: 'graph', label: 'Graph', icon: Network },
  { id: 'tree', label: 'Tree', icon: Workflow },
  { id: 'report', label: 'Report', icon: FileText },
  { id: 'wiki', label: 'Wiki', icon: Boxes },
  { id: 'files', label: 'Files', icon: Download },
];

function cleanMarkdown(md = '') {
  return md
    .replace(/```[\s\S]*?```/g, (m) => m.replace(/</g, '&lt;'))
    .replace(/^# (.*)$/gm, '<h1>$1</h1>')
    .replace(/^## (.*)$/gm, '<h2>$1</h2>')
    .replace(/^### (.*)$/gm, '<h3>$1</h3>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/^\- (.*)$/gm, '<li>$1</li>')
    .replace(/\n\n/g, '</p><p>')
    .replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>')
    .replace(/^/, '<p>')
    .replace(/$/, '</p>')
    .replace(/<p><h/g, '<h')
    .replace(/<\/h([123])><\/p>/g, '</h$1>')
    .replace(/<p><ul>/g, '<ul>')
    .replace(/<\/ul><\/p>/g, '</ul>');
}

function useText(url) {
  const [text, setText] = useState('');
  useEffect(() => {
    if (!url) return;
    fetch(url).then((r) => r.text()).then(setText).catch(() => setText('Unable to load.'));
  }, [url]);
  return text;
}

function useJson(url, fallback) {
  const [data, setData] = useState(fallback);
  useEffect(() => {
    if (!url) return;
    fetch(url).then((r) => r.json()).then(setData).catch(() => setData(fallback));
  }, [url]);
  return data;
}

function App() {
  const [paperIndex, setPaperIndex] = useState({ papers: [] });
  const [activePaperId, setActivePaperId] = useState('2604.26615');
  const [activeTab, setActiveTab] = useState('overview');
  const [query, setQuery] = useState('');

  useEffect(() => {
    fetch('/papers/index.json').then((r) => r.json()).then(setPaperIndex);
  }, []);

  const paper = paperIndex.papers.find((p) => p.id === activePaperId) || paperIndex.papers[0];
  const pages = useJson(paper ? `/papers/${paper.slug}/pages.json` : null, []);
  const graph = useJson(paper?.assets?.graphJson, { nodes: [], links: [] });
  const report = useText(paper?.assets?.report);
  const wikiIndex = useText(paper?.assets?.wikiIndex);

  const filteredPages = useMemo(() => {
    if (!query.trim()) return pages;
    const q = query.toLowerCase();
    return pages.filter((p) => p.text.toLowerCase().includes(q));
  }, [pages, query]);

  const topNodes = useMemo(() => {
    const links = graph.links || graph.edges || [];
    const degree = new Map();
    links.forEach((e) => {
      degree.set(e.source, (degree.get(e.source) || 0) + 1);
      degree.set(e.target, (degree.get(e.target) || 0) + 1);
    });
    return (graph.nodes || [])
      .map((n) => ({ ...n, degree: degree.get(n.id) || 0 }))
      .sort((a, b) => b.degree - a.degree)
      .slice(0, 10);
  }, [graph]);

  if (!paper) return <div className="boot">Loading paper graph reader...</div>;

  return (
    <div className="shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark"><Brain size={22} /></div>
          <div>
            <div className="eyebrow">Neuroweave paper graph</div>
            <h1>Paper Reader</h1>
          </div>
        </div>

        <div className="paper-list">
          <div className="eyebrow">Library</div>
          {paperIndex.papers.map((p) => (
            <button key={p.id} className={`paper-card ${p.id === paper.id ? 'active' : ''}`} onClick={() => setActivePaperId(p.id)}>
              <span>{p.kind} {p.id}</span>
              <strong>{p.title}</strong>
              <small>{p.stats.nodes} nodes · {p.stats.edges} edges · {p.stats.pages} pages</small>
            </button>
          ))}
        </div>

        <div className="sidebar-note">
          <Layers size={16} />
          Add future papers by dropping a graphified folder into public/papers and updating index.json.
        </div>
      </aside>

      <main className="main">
        <header className="hero">
          <div>
            <div className="kicker">{paper.kind} · {paper.id} · {paper.category}</div>
            <h2>{paper.title}</h2>
            <p>{paper.authors}</p>
          </div>
          <div className="hero-actions">
            <a href={paper.assets.pdf} target="_blank">PDF <ExternalLink size={14} /></a>
            <a href={paper.assets.graphHtml} target="_blank">Graph <ExternalLink size={14} /></a>
          </div>
        </header>

        <nav className="tabs">
          {tabs.map(({ id, label, icon: Icon }) => (
            <button key={id} onClick={() => setActiveTab(id)} className={activeTab === id ? 'active' : ''}>
              <Icon size={16} /> {label}
            </button>
          ))}
        </nav>

        {activeTab === 'overview' && <Overview paper={paper} topNodes={topNodes} />}
        {activeTab === 'read' && <Read pages={filteredPages} query={query} setQuery={setQuery} />}
        {activeTab === 'graph' && <Frame title="Interactive graph" url={paper.assets.graphHtml} />}
        {activeTab === 'tree' && <Frame title="Tree browser" url={paper.assets.treeHtml} />}
        {activeTab === 'report' && <Markdown title="Graph report" text={report} />}
        {activeTab === 'wiki' && <Markdown title="Wiki index" text={wikiIndex} />}
        {activeTab === 'files' && <Files paper={paper} />}
      </main>
    </div>
  );
}

function Overview({ paper, topNodes }) {
  return <section className="grid overview">
    <article className="panel span-2">
      <div className="eyebrow">One sentence</div>
      <h3>Tests become governance, not just evaluation.</h3>
      <p>{paper.abstract}</p>
    </article>
    <article className="panel stats">
      <div><strong>{paper.stats.nodes}</strong><span>Nodes</span></div>
      <div><strong>{paper.stats.edges}</strong><span>Edges</span></div>
      <div><strong>{paper.stats.pages}</strong><span>Pages</span></div>
    </article>
    <article className="panel">
      <div className="eyebrow">Communities</div>
      <div className="chips">{paper.communities.map((c) => <span key={c}>{c}</span>)}</div>
    </article>
    <article className="panel">
      <div className="eyebrow">Ask the graph</div>
      {paper.featuredQuestions.map((q) => <div className="question" key={q}><ArrowRight size={14} />{q}</div>)}
    </article>
    <article className="panel span-2">
      <div className="eyebrow">Core abstractions</div>
      <div className="node-list">{topNodes.map((n) => <div key={n.id}><strong>{n.label}</strong><span>{n.degree} links</span></div>)}</div>
    </article>
  </section>;
}

function Read({ pages, query, setQuery }) {
  return <section className="reader-wrap">
    <div className="searchbar"><Search size={17} /><input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search inside the paper..." /></div>
    <div className="reader">
      {pages.map((p) => <article className="page" key={p.page}><div className="page-num">Page {p.page}</div><pre>{p.text}</pre></article>)}
    </div>
  </section>;
}

function Frame({ title, url }) {
  return <section className="frame-panel">
    <div className="frame-head">
      <div>
        <h3>{title}</h3>
        <p>Pinch/drag inside the frame, or open full screen for the best mobile graph view.</p>
      </div>
      <a href={url} target="_blank">Open full screen <ExternalLink size={14} /></a>
    </div>
    <iframe src={url} title={title} />
  </section>;
}

function Markdown({ title, text }) {
  return <section className="markdown panel"><h3>{title}</h3><div dangerouslySetInnerHTML={{ __html: cleanMarkdown(text) }} /></section>;
}

function Files({ paper }) {
  const entries = Object.entries(paper.assets);
  return <section className="grid files">{entries.map(([name, url]) => <a className="file-card" href={url} target="_blank" key={name}><FileText size={18} /><strong>{name}</strong><span>{url}</span></a>)}</section>;
}

createRoot(document.getElementById('root')).render(<App />);
