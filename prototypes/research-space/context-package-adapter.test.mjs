import assert from 'node:assert/strict';
import { contextPackageToResearchSpace } from './context-package-adapter.js';

const pkg = {
  id: 'example:synthetic:001',
  schema_version: '0.1.0',
  created_at: '2026-08-21T00:00:00Z',
  question: {
    original: '합성 예시 문헌은 무엇을 보여 주는가?',
    normalized: '합성 예시의 명시적 내용과 해석을 구분한다.',
    scope: { chronology: [], places: [], languages: ['Korean'], genres: ['synthetic example'], notes: [] },
  },
  evidence: [{
    id: 'ev:001',
    source: 'synthetic',
    source_record_id: 'synthetic:001',
    stable_url: 'https://example.com/source',
    locator: 'evidence[0]',
    layer: 'edition',
    excerpt: '합성 자료다.',
    attribution: 'contributors',
    license_manifest_id: 'project:apache-2.0',
  }],
  claims: [{
    id: 'claim:001',
    statement: '이 패키지는 합성 예시다.',
    status: 'attested',
    supporting_evidence_ids: ['ev:001'],
    challenging_evidence_ids: [],
    confidence: 'high',
    reasoning: '증거가 직접 명시한다.',
  }],
  debates: [],
  uncertainties: [{
    target: 'historical applicability',
    kind: 'coverage',
    description: '실제 역사 증거가 아니다.',
    evidence_ids: ['ev:001'],
  }],
  bibliography: [],
  retrieval: { run_at: '2026-08-21T00:00:00Z', source_manifest_ids: [], queries: [], software_version: '0.1.0', model: null, prompt_version: null },
  review: { status: 'source_checked', reviewers: ['maintainer'], notes: [] },
};

const graph = contextPackageToResearchSpace(pkg);

assert.equal(graph.packageId, pkg.id);
assert.equal(graph.meta.reviewStatus, 'source_checked');
assert.ok(graph.nodes.some((n) => n.id === 'question:root' && n.type === 'question'));
assert.ok(graph.nodes.some((n) => n.id === 'ev:001' && n.type === 'evidence'));
assert.ok(graph.nodes.some((n) => n.id === 'claim:001' && n.type === 'claim'));
assert.ok(graph.nodes.some((n) => n.type === 'uncertainty' && n.data.kind === 'coverage'));
assert.ok(graph.edges.some((e) => e.from === 'ev:001' && e.to === 'claim:001' && e.relation === 'supports'));
assert.ok(graph.edges.some((e) => e.relation === 'grounded_in'));

assert.throws(
  () => contextPackageToResearchSpace({ ...pkg, schema_version: '9.9.9' }),
  /Unsupported Context Package schema/
);

console.log(`ok - ${graph.nodes.length} nodes, ${graph.edges.length} edges`);
