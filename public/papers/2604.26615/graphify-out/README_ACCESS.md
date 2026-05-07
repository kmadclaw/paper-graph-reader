# Accessing this graphified paper

Workspace: /root/graphified-papers/arxiv-2604.26615

Key files:
- README.md: paper metadata and abstract
- paper.pdf: original PDF
- paper_text.md: extracted full text
- graphify-out/GRAPH_REPORT.md: human-readable summary of graph structure
- graphify-out/graph.html: interactive browser visualization
- graphify-out/wiki/index.md: Obsidian-style vault entry point
- graphify-out/graph.json: Graphify-compatible machine graph

Useful commands from this directory:
- graphify query "How does TDD become enforceable governance?" --graph graphify-out/graph.json
- graphify explain "Machine-readable TDD manifesto" --graph graphify-out/graph.json
- graphify path "Problem: unconstrained LLM coding is unstable" "Bounded repair loops" --graph graphify-out/graph.json
- python3 -m http.server 8765 then open http://localhost:8765/graphify-out/graph.html
