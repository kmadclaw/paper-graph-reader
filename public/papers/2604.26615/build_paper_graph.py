from pathlib import Path
import json, re, shutil, subprocess

from graphify.build import build_from_json
from graphify.export import to_json, to_html, to_obsidian, to_canvas, to_graphml, to_svg, to_cypher
from graphify.report import generate as generate_report
from graphify.analyze import god_nodes, surprising_connections

ROOT = Path('/root/graphified-papers/arxiv-2604.26615')
OUT = ROOT / 'graphify-out'
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True)

source = 'paper_text.md'

def node(id, label, file_type='paper', desc='', community=None):
    d = {'id': id, 'label': label, 'file_type': file_type, 'source_file': source}
    if desc: d['description'] = desc
    if community is not None: d['community_hint'] = community
    return d

def edge(s, t, rel, conf='EXTRACTED', note=''):
    d = {'source': s, 'target': t, 'relation': rel, 'confidence': conf, 'source_file': source}
    if note: d['note'] = note
    return d

nodes = [
    node('paper', 'TDD Governance for Multi-Agent Code Generation via Prompt Engineering', desc='EASE 2026 arXiv paper proposing AI-native TDD governance for multi-agent code generation.'),
    node('problem', 'Problem: unconstrained LLM coding is unstable', desc='LLMs show non-determinism, hallucinations, reproducibility gaps, and weak process discipline.'),
    node('gap', 'Gap: tests are auxiliary, not enforceable constraints', desc='Existing LLM approaches use tests as prompts/evaluation but do not enforce full TDD discipline.'),
    node('contribution', 'Contribution: AI-native TDD framework', desc='Turns classical TDD principles into prompt-level and workflow-level governance mechanisms.'),
    node('tdd', 'Classical TDD', desc='Red-Green-Refactor micro-cycle where tests specify behavior before implementation.'),
    node('red_green_refactor', 'Red-Green-Refactor phase ordering', desc='A disciplined cycle: failing test first, minimal code to pass, then behavior-preserving refactor.'),
    node('principle_categories', 'TDD principle categories', desc='Order, granularity, feedback quality, and design hygiene.'),
    node('order_constraints', 'Order constraints', desc='Test-first and Red→Green→Refactor sequencing.'),
    node('granularity_constraints', 'Granularity constraints', desc='Minimal failing test, minimal passing code, one failing test at a time.'),
    node('feedback_quality', 'Feedback-quality constraints', desc='FAST, independent, repeatable, self-validating, timely tests with meaningful assertions.'),
    node('design_hygiene', 'Design hygiene constraints', desc='Remove duplication and refactor continuously while green.'),
    node('manifesto', 'Machine-readable TDD manifesto', desc='JSON-style structured governance object with principle id, title, intent, AI-native interpretation, constraints, and anti-patterns.'),
    node('architecture', 'Governance-centric layered architecture', desc='Separates non-authoritative LLM proposal generation from authoritative engine-controlled mutation.'),
    node('proposal_layer', 'LLM proposal layer', desc='Planner, test, code, repair, and review agents propose structured outputs but cannot mutate workspace directly.'),
    node('engine_governance', 'Authoritative engine governance', desc='Engine owns validation, phase transitions, test runs, atomic apply, rollback, and state mutation.'),
    node('planner', 'Planner prompt/agent', desc='Decomposes requirements into ordered steps with expected test outcomes.'),
    node('test_generation', 'Test generation prompt/agent', desc='RED-phase prompt restricted to tests with meaningful assertions aligned to the spec.'),
    node('implementation', 'Implementation prompt/agent', desc='GREEN-phase prompt restricted to minimal code changes needed to satisfy failing tests.'),
    node('failure_repair', 'Failure repair prompt/agent', desc='Uses structured failure context for minimal localized corrections.'),
    node('review', 'Review prompt/agent', desc='Quality gate preventing over-specification, invented requirements, and phase pollution.'),
    node('validation_gates', 'Validation gates', desc='Schema/content checks, policy enforcement, phase consistency checks, and optional approval.'),
    node('phase_gating', 'Phase gating', desc='Code generation is not allowed until a failing test state exists; refactor is only allowed while green.'),
    node('bounded_repair', 'Bounded repair loops', desc='At most N=3 repair attempts, with early termination for repeated failure signature, no effective change, or semantically equivalent proposals.'),
    node('failure_signature', 'Failure signature S', desc='Exception type, failing tests, normalized message; used to detect repeated failures.'),
    node('deterministic_tests', 'Deterministic test run', desc='Engine executes tests as an authoritative verifier after approved proposals.'),
    node('atomic_mutation', 'Atomic apply / rollback', desc='All file mutations are performed atomically by the engine after validation; rollback protects refactoring.'),
    node('runtime_enforcement', 'Runtime enforcement mechanisms', desc='Planner-ordered FAIL gating, scope restrictions, no-op/unrelated-change rejection, post-apply tests, rollback.'),
    node('prompt_distribution', 'Prompt distribution across roles', desc='Governance invariants are distributed across system, planner, test generation, implementation, failure repair, and review prompts.'),
    node('benefit', 'Benefits claimed', desc='Reduced uncontrolled iteration, improved stability/reproducibility, less speculative code expansion, auditable AI-assisted development.'),
    node('limitations', 'Limitations', desc='Prompt-level enforcement only partial; empirical validation preliminary; cross-model/repository-scale evaluation needed; strict governance may limit exploration.'),
    node('future_work', 'Future work', desc='Repository-scale industrial settings, CI/CD integration, configurable governance levels, regulated-domain auditability.'),
    node('related_tdflow', 'TDFlow', desc='Related agentic TDD workflow; this paper emphasizes governed execution under non-determinism.'),
    node('related_ticoder', 'TiCoder', desc='Related interactive TDD-style test refinement and code generation.'),
    node('related_llm4tdd', 'LLM4TDD best practices', desc='Related practical guidance for TDD-style LLM use.'),
    node('related_self_refine', 'Self-Refine / structured CoT prompting', desc='Related prompt engineering loops that improve code generation quality but do not enforce full process discipline.'),
]

edges = [
    edge('paper','problem','motivated_by'), edge('paper','gap','addresses'), edge('paper','contribution','proposes'),
    edge('contribution','tdd','operationalizes'), edge('tdd','red_green_refactor','contains'), edge('tdd','principle_categories','abstracted_into'),
    edge('principle_categories','order_constraints','includes'), edge('principle_categories','granularity_constraints','includes'), edge('principle_categories','feedback_quality','includes'), edge('principle_categories','design_hygiene','includes'),
    edge('order_constraints','red_green_refactor','enforces'), edge('granularity_constraints','implementation','constrains'), edge('feedback_quality','deterministic_tests','requires'), edge('design_hygiene','atomic_mutation','protected_by'),
    edge('manifesto','order_constraints','encodes'), edge('manifesto','granularity_constraints','encodes'), edge('manifesto','feedback_quality','encodes'), edge('manifesto','design_hygiene','encodes'),
    edge('contribution','manifesto','uses'), edge('contribution','architecture','implemented_as'),
    edge('architecture','proposal_layer','separates'), edge('architecture','engine_governance','separates'), edge('proposal_layer','engine_governance','submits_to'),
    edge('proposal_layer','planner','contains'), edge('proposal_layer','test_generation','contains'), edge('proposal_layer','implementation','contains'), edge('proposal_layer','failure_repair','contains'), edge('proposal_layer','review','contains'),
    edge('engine_governance','validation_gates','performs'), edge('engine_governance','phase_gating','performs'), edge('engine_governance','deterministic_tests','executes'), edge('engine_governance','atomic_mutation','owns'), edge('engine_governance','bounded_repair','controls'),
    edge('planner','phase_gating','establishes_order'), edge('planner','test_generation','routes_to_red'), edge('test_generation','deterministic_tests','expects_initial_fail'), edge('test_generation','phase_gating','precedes_code'),
    edge('implementation','deterministic_tests','validated_by'), edge('implementation','granularity_constraints','must_be_minimal'), edge('review','validation_gates','acts_as'),
    edge('failure_repair','bounded_repair','governed_by'), edge('bounded_repair','failure_signature','uses'), edge('bounded_repair','deterministic_tests','retries_until_pass_or_cap'),
    edge('validation_gates','atomic_mutation','precedes'), edge('atomic_mutation','deterministic_tests','followed_by'), edge('phase_gating','red_green_refactor','implements'),
    edge('runtime_enforcement','phase_gating','includes'), edge('runtime_enforcement','validation_gates','includes'), edge('runtime_enforcement','bounded_repair','includes'), edge('runtime_enforcement','atomic_mutation','includes'),
    edge('prompt_distribution','planner','constrains'), edge('prompt_distribution','test_generation','constrains'), edge('prompt_distribution','implementation','constrains'), edge('prompt_distribution','failure_repair','constrains'), edge('prompt_distribution','review','constrains'),
    edge('manifesto','prompt_distribution','informs'), edge('manifesto','runtime_enforcement','maps_to'), edge('prompt_distribution','runtime_enforcement','complemented_by'),
    edge('contribution','benefit','claims'), edge('benefit','problem','mitigates'), edge('limitations','contribution','qualifies'), edge('future_work','limitations','responds_to'),
    edge('related_tdflow','gap','contrasted_with'), edge('related_ticoder','gap','contrasted_with'), edge('related_llm4tdd','gap','contrasted_with'), edge('related_self_refine','gap','contrasted_with'),
    edge('related_tdflow','contribution','informs', 'INFERRED'), edge('related_ticoder','test_generation','informs', 'INFERRED'), edge('related_llm4tdd','prompt_distribution','informs', 'INFERRED'), edge('related_self_refine','failure_repair','informs', 'INFERRED'),
    edge('problem','bounded_repair','requires_governance', 'INFERRED'), edge('problem','engine_governance','requires_authority', 'INFERRED'),
]

hyperedges = [
    {'id': 'h_tdd_principles', 'label': 'TDD principles become governance constraints', 'nodes': ['tdd','principle_categories','manifesto','runtime_enforcement'], 'confidence': 'EXTRACTED'},
    {'id': 'h_governed_workflow', 'label': 'Governed Red-Green-Refactor workflow', 'nodes': ['planner','test_generation','implementation','validation_gates','deterministic_tests','bounded_repair','atomic_mutation'], 'confidence': 'EXTRACTED'},
    {'id': 'h_prompt_engine_split', 'label': 'Prompt constraints + deterministic engine', 'nodes': ['prompt_distribution','proposal_layer','engine_governance','validation_gates','phase_gating'], 'confidence': 'EXTRACTED'},
]

extraction = {'nodes': nodes, 'edges': edges, 'hyperedges': hyperedges, 'input_tokens': 0, 'output_tokens': 0}
(ROOT/'paper_graph_extraction.json').write_text(json.dumps(extraction, indent=2))
G = build_from_json(extraction, directed=False)

communities = {
    0: ['paper','problem','gap','contribution','benefit','limitations','future_work'],
    1: ['tdd','red_green_refactor','principle_categories','order_constraints','granularity_constraints','feedback_quality','design_hygiene','manifesto'],
    2: ['architecture','proposal_layer','engine_governance','validation_gates','phase_gating','deterministic_tests','atomic_mutation','runtime_enforcement'],
    3: ['planner','test_generation','implementation','failure_repair','review','bounded_repair','failure_signature','prompt_distribution'],
    4: ['related_tdflow','related_ticoder','related_llm4tdd','related_self_refine'],
}
labels = {0:'Paper Thesis & Claims',1:'TDD Principles Manifesto',2:'Governance Architecture',3:'Agent Workflow & Repair Control',4:'Related Work Context'}
cohesion = {0:0.74,1:0.86,2:0.88,3:0.82,4:0.64}

# Write graphify outputs
for p in [OUT/'wiki']:
    p.mkdir(exist_ok=True)
to_json(G, communities, str(OUT/'graph.json'), force=True)
to_html(G, communities, str(OUT/'graph.html'), community_labels=labels)
to_obsidian(G, communities, str(OUT/'wiki'), community_labels=labels, cohesion=cohesion)
to_canvas(G, communities, str(OUT/'graph.canvas'), community_labels=labels)
try:
    # GraphML cannot serialize list-valued graph metadata like hyperedges in this Graphify build.
    G_graphml = G.copy()
    G_graphml.graph.clear()
    to_graphml(G_graphml, communities, str(OUT/'graph.graphml'))
except Exception as e:
    (OUT/'graphml_error.txt').write_text(str(e))
try:
    to_svg(G, communities, str(OUT/'graph.svg'), community_labels=labels)
except Exception as e:
    (OUT/'svg_error.txt').write_text(str(e))
to_cypher(G, str(OUT/'graph.cypher'))

report = generate_report(
    G, communities, cohesion, labels, god_nodes(G, 10), surprising_connections(G, communities, 8),
    {'total_files': 3, 'total_words': 7600}, {'input':0,'output':0}, 'arxiv-2604.26615',
    suggested_questions=[
        {'question':'How does the paper turn TDD principles into enforceable mechanisms?', 'why':'Traces TDD → manifesto → prompt distribution/runtime enforcement.'},
        {'question':'What path connects LLM instability to bounded repair?', 'why':'Shows why nondeterminism motivates loop control and engine authority.'},
        {'question':'Which agent roles participate in the governed workflow?', 'why':'Maps planner/test/code/repair/review roles to gates and phases.'},
        {'question':'What are the limitations of the framework?', 'why':'Separates claims from evidence and future work.'},
    ],
)
(OUT/'GRAPH_REPORT.md').write_text(report)
(OUT/'README_ACCESS.md').write_text('''# Accessing this graphified paper\n\nWorkspace: /root/graphified-papers/arxiv-2604.26615\n\nKey files:\n- README.md: paper metadata and abstract\n- paper.pdf: original PDF\n- paper_text.md: extracted full text\n- graphify-out/GRAPH_REPORT.md: human-readable summary of graph structure\n- graphify-out/graph.html: interactive browser visualization\n- graphify-out/wiki/index.md: Obsidian-style vault entry point\n- graphify-out/graph.json: Graphify-compatible machine graph\n\nUseful commands from this directory:\n- graphify query "How does TDD become enforceable governance?" --graph graphify-out/graph.json\n- graphify explain "Machine-readable TDD manifesto" --graph graphify-out/graph.json\n- graphify path "Problem: unconstrained LLM coding is unstable" "Bounded repair loops" --graph graphify-out/graph.json\n- python3 -m http.server 8765 then open http://localhost:8765/graphify-out/graph.html\n''')

print(f'Wrote {G.number_of_nodes()} nodes and {G.number_of_edges()} edges to {OUT}')
