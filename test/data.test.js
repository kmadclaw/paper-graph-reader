import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

test('paper index exposes graphified TDD paper and required assets', async () => {
  const index = JSON.parse(await readFile('public/papers/index.json', 'utf8'));
  assert.equal(index.papers.length, 1);
  const paper = index.papers[0];
  assert.equal(paper.id, '2604.26615');
  assert.match(paper.title, /TDD Governance/);
  assert.ok(paper.assets.graphHtml);
  assert.ok(paper.assets.report);
  assert.ok(paper.stats.nodes >= 30);
});
