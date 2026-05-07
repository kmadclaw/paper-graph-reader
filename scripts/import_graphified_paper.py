#!/usr/bin/env python3
"""Import a graphified paper folder into the Vercel Paper Graph Reader app.

Usage:
  python scripts/import_graphified_paper.py /root/graphified-papers/arxiv-2604.26615 --id 2604.26615

Expected source folder files:
  README.md, paper.pdf, paper_text.md, graphify-out/graph.json, graphify-out/GRAPH_REPORT.md,
  graphify-out/graph.html, graphify-out/GRAPH_TREE.html, graphify-out/wiki/index.md
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]
PAPERS_DIR = APP_ROOT / "public" / "papers"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def parse_pages(text: str) -> list[dict]:
    parts = re.split(r"\n# Page (\d+)\n\n", text)
    if parts and not parts[0].strip():
        parts = parts[1:]
    pages = []
    for i in range(0, len(parts), 2):
        try:
            pages.append({"page": int(parts[i]), "text": parts[i + 1].strip()})
        except Exception:
            continue
    return pages or [{"page": 1, "text": text.strip()}]


def parse_meta(dst: Path, paper_id: str, slug: str) -> dict:
    readme = read(dst / "README.md")
    graph_path = dst / "graphify-out" / "graph.json"
    graph = json.loads(read(graph_path)) if graph_path.exists() else {"nodes": [], "links": []}
    text = read(dst / "paper_text.md")
    pages = parse_pages(text)
    (dst / "pages.json").write_text(json.dumps(pages, indent=2), encoding="utf-8")

    title_match = re.search(r"^#\s+(.+)", readme, re.M)
    authors_match = re.search(r"^- Authors:\s*(.+)", readme, re.M)
    abstract_match = re.search(r"## Abstract\s+(.+)", readme, re.S)
    category_match = re.search(r"^- (?:Subjects|Categories):\s*(.+)", readme, re.M)

    title = title_match.group(1).strip() if title_match else f"Paper {paper_id}"
    authors = authors_match.group(1).strip() if authors_match else "Unknown authors"
    abstract = re.sub(r"\s+", " ", abstract_match.group(1)).strip() if abstract_match else ""
    category = category_match.group(1).strip() if category_match else "paper"
    links = graph.get("links", graph.get("edges", []))

    return {
        "id": paper_id,
        "slug": slug,
        "kind": "arXiv" if re.match(r"^\d{4}\.\d+", paper_id) else "Paper",
        "title": title,
        "authors": authors,
        "published": "",
        "category": category,
        "abstract": abstract,
        "assets": {
            "pdf": f"/papers/{slug}/paper.pdf",
            "text": f"/papers/{slug}/paper_text.md",
            "report": f"/papers/{slug}/graphify-out/GRAPH_REPORT.md",
            "graphJson": f"/papers/{slug}/graphify-out/graph.json",
            "graphHtml": f"/papers/{slug}/graphify-out/graph.html",
            "treeHtml": f"/papers/{slug}/graphify-out/GRAPH_TREE.html",
            "wikiIndex": f"/papers/{slug}/graphify-out/wiki/index.md",
            "canvas": f"/papers/{slug}/graphify-out/graph.canvas",
            "cypher": f"/papers/{slug}/graphify-out/graph.cypher",
            "graphml": f"/papers/{slug}/graphify-out/graph.graphml",
        },
        "stats": {"nodes": len(graph.get("nodes", [])), "edges": len(links), "pages": len(pages)},
        "communities": [],
        "featuredQuestions": [
            "What is the central thesis?",
            "What are the core abstractions?",
            "Which connections are surprising?",
            "What are the limitations?",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--id", required=True, help="Stable paper id, e.g. 2604.26615")
    parser.add_argument("--slug", help="URL slug. Defaults to --id")
    args = parser.parse_args()

    slug = args.slug or args.id
    dst = PAPERS_DIR / slug
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(args.source, dst, ignore=shutil.ignore_patterns("abs.html", ".git", "node_modules"))

    meta = parse_meta(dst, args.id, slug)
    (dst / "paper.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    index_path = PAPERS_DIR / "index.json"
    index = json.loads(read(index_path)) if index_path.exists() else {"papers": []}
    papers = [p for p in index.get("papers", []) if p.get("id") != args.id]
    papers.append(meta)
    papers.sort(key=lambda p: p.get("id", ""), reverse=True)
    index_path.write_text(json.dumps({"papers": papers}, indent=2), encoding="utf-8")
    print(f"Imported {args.id} -> {dst}")


if __name__ == "__main__":
    main()
