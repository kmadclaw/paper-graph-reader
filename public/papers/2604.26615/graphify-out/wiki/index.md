# arXiv 2604.26615 Graphified Paper

Paper: [[TDD Governance for Multi-Agent Code Generation via Prompt Engineering]]

## Start here

- [[_COMMUNITY_Paper Thesis & Claims|Paper Thesis & Claims]]
- [[_COMMUNITY_TDD Principles Manifesto|TDD Principles Manifesto]]
- [[_COMMUNITY_Governance Architecture|Governance Architecture]]
- [[_COMMUNITY_Agent Workflow & Repair Control|Agent Workflow & Repair Control]]
- [[_COMMUNITY_Related Work Context|Related Work Context]]

## Core nodes

- [[Machine-readable TDD manifesto]]
- [[Authoritative engine governance]]
- [[Prompt distribution across roles]]
- [[Bounded repair loops]]
- [[Validation gates]]
- [[Phase gating]]

## CLI examples

From `/root/graphified-papers/arxiv-2604.26615`:

```bash
graphify query "How does TDD become enforceable governance?" --graph graphify-out/graph.json
graphify explain "Machine-readable TDD manifesto" --graph graphify-out/graph.json
graphify path "Problem: unconstrained LLM coding is unstable" "Bounded repair loops" --graph graphify-out/graph.json
```
