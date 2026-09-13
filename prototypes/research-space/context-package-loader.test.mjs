import assert from 'node:assert/strict';
import { loadContextPackage, buildCanvasLayout } from './context-package-loader.mjs';

const fixture = {
  id: 'fixture:001',
  schema_version: '0.1.0',
  created_at: '2026-09-13T00:00:00Z',
  question: { original: '무엇을 보여 주는가?', normalized: '무엇을 보여 주는지 검토한다.', scope: { chronology: [], places: [], languages: [], genres: [], notes: [] } },
  evidence: [{ id: 'ev:1', source: 'fixture', source_record_id: '1', stable_url: 'https://example.com/1', locator: '1', layer: 'edition', excerpt: '근거', attribution: 'tester', license_manifest_id: 'fixture' }],
  claims: [{ id: 'claim:1', statement: '주장', status: 'attested', supporting_evidence_ids: ['ev:1'], challenging_evidence_ids: [], confidence: 'high', reasoning: '직접 근거' }],
  debates: [],
  uncertainties: [{ target: 'claim:1', kind: 'coverage', description: '범위가 제한적이다.', evidence_ids: ['ev:1'] }],
  bibliography: [],
  retrieval: { run_at: '2026-09-13T00:00:00Z', source_manifest_ids: [], queries: [], software_version: '0.1.0', model: null, prompt_version: null },
  review: { status: 'source_checked', reviewers: ['tester'], notes: [] },
};

const okFetch = async () => ({ ok: true, status: 200, json: async () => fixture });
const loaded = await loadContextPackage('/fixture.json', okFetch);
assert.equal(loaded.package.id, 'fixture:001');
assert.ok(loaded.graph.nodes.some((node) => node.id === 'claim:1'));
assert.ok(loaded.graph.edges.some((edge) => edge.from === 'ev:1' && edge.to === 'claim:1' && edge.relation === 'supports'));

const layout = buildCanvasLayout(loaded.graph);
assert.equal(layout.length, loaded.graph.nodes.length);
assert.ok(layout.every((node) => Number.isFinite(node.x) && Number.isFinite(node.y)));
assert.equal(layout.find((node) => node.type === 'question').x, 36);
assert.equal(layout.find((node) => node.type === 'claim').x, 266);

await assert.rejects(
  () => loadContextPackage('/missing.json', async () => ({ ok: false, status: 404 })),
  /Failed to load Context Package: 404/
);

console.log(`ok - loaded ${loaded.graph.nodes.length} nodes and laid out ${layout.length}`);
