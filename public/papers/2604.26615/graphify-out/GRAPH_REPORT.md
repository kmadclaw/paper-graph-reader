# Graph Report - arxiv-2604.26615  (2026-05-07)

## Corpus Check
- 3 files · ~7,600 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 35 nodes · 71 edges · 5 communities
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 6 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Paper Thesis & Claims|Paper Thesis & Claims]]
- [[_COMMUNITY_TDD Principles Manifesto|TDD Principles Manifesto]]
- [[_COMMUNITY_Governance Architecture|Governance Architecture]]
- [[_COMMUNITY_Agent Workflow & Repair Control|Agent Workflow & Repair Control]]
- [[_COMMUNITY_Related Work Context|Related Work Context]]

## God Nodes (most connected - your core abstractions)
1. `Authoritative engine governance` - 8 edges
2. `Prompt distribution across roles` - 8 edges
3. `Contribution: AI-native TDD framework` - 7 edges
4. `Machine-readable TDD manifesto` - 7 edges
5. `LLM proposal layer` - 7 edges
6. `Test generation prompt/agent` - 6 edges
7. `Bounded repair loops` - 6 edges
8. `Deterministic test run` - 6 edges
9. `Runtime enforcement mechanisms` - 6 edges
10. `Gap: tests are auxiliary, not enforceable constraints` - 5 edges

## Surprising Connections (you probably didn't know these)
- `Problem: unconstrained LLM coding is unstable` --requires_governance--> `Bounded repair loops`  [INFERRED]
  paper_text.md → paper_text.md  _Bridges community 0 → community 3_
- `Problem: unconstrained LLM coding is unstable` --requires_authority--> `Authoritative engine governance`  [INFERRED]
  paper_text.md → paper_text.md  _Bridges community 0 → community 2_
- `TDFlow` --informs--> `Contribution: AI-native TDD framework`  [INFERRED]
  paper_text.md → paper_text.md  _Bridges community 0 → community 4_
- `TiCoder` --informs--> `Test generation prompt/agent`  [INFERRED]
  paper_text.md → paper_text.md  _Bridges community 3 → community 4_
- `Contribution: AI-native TDD framework` --operationalizes--> `Classical TDD`  [EXTRACTED]
  paper_text.md → paper_text.md  _Bridges community 0 → community 1_
- `Phase gating` --implements--> `Red-Green-Refactor phase ordering`  [EXTRACTED]
  paper_text.md → paper_text.md  _Bridges community 1 → community 2_
- `Implementation prompt/agent` --must_be_minimal--> `Granularity constraints`  [EXTRACTED]
  paper_text.md → paper_text.md  _Bridges community 1 → community 3_
- `Authoritative engine governance` --controls--> `Bounded repair loops`  [EXTRACTED]
  paper_text.md → paper_text.md  _Bridges community 2 → community 3_

## Hyperedges (group relationships)
- **TDD principles become governance constraints** — tdd, principle_categories, manifesto, runtime_enforcement [EXTRACTED]
- **Governed Red-Green-Refactor workflow** — planner, test_generation, implementation, validation_gates, deterministic_tests, bounded_repair, atomic_mutation [EXTRACTED]
- **Prompt constraints + deterministic engine** — prompt_distribution, proposal_layer, engine_governance, validation_gates, phase_gating [EXTRACTED]

## Communities (5 total, 0 thin omitted)

### Community 0 - "Paper Thesis & Claims"
Cohesion: 0.74
Nodes (7): TDD Governance for Multi-Agent Code Generation via Prompt Engineering, Problem: unconstrained LLM coding is unstable, Gap: tests are auxiliary, not enforceable constraints, Contribution: AI-native TDD framework, Benefits claimed, Limitations, Future work

### Community 1 - "TDD Principles Manifesto"
Cohesion: 0.86
Nodes (8): Classical TDD, Red-Green-Refactor phase ordering, TDD principle categories, Order constraints, Granularity constraints, Feedback-quality constraints, Design hygiene constraints, Machine-readable TDD manifesto

### Community 2 - "Governance Architecture"
Cohesion: 0.88
Nodes (8): Governance-centric layered architecture, LLM proposal layer, Authoritative engine governance, Validation gates, Phase gating, Deterministic test run, Atomic apply / rollback, Runtime enforcement mechanisms

### Community 3 - "Agent Workflow & Repair Control"
Cohesion: 0.82
Nodes (8): Planner prompt/agent, Test generation prompt/agent, Implementation prompt/agent, Failure repair prompt/agent, Review prompt/agent, Bounded repair loops, Failure signature S, Prompt distribution across roles

### Community 4 - "Related Work Context"
Cohesion: 0.64
Nodes (4): TDFlow, TiCoder, LLM4TDD best practices, Self-Refine / structured CoT prompting

## Knowledge Gaps
- **2 isolated node(s):** `Failure signature S`, `Future work`
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **How does the paper turn TDD principles into enforceable mechanisms?**
  _Traces TDD → manifesto → prompt distribution/runtime enforcement._
- **What path connects LLM instability to bounded repair?**
  _Shows why nondeterminism motivates loop control and engine authority._
- **Which agent roles participate in the governed workflow?**
  _Maps planner/test/code/repair/review roles to gates and phases._
- **What are the limitations of the framework?**
  _Separates claims from evidence and future work._