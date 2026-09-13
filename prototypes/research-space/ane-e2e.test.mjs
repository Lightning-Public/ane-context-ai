import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import { contextPackageToResearchSpace } from './context-package-adapter.mjs';

const raw = await fs.readFile(new URL('../../examples/context-package.uruk-writing.json', import.meta.url), 'utf8');
const pkg = JSON.parse(raw);
const graph = contextPackageToResearchSpace(pkg);

assert.equal(pkg.schema_version, '0.1.0');
assert.equal(pkg.review.status, 'source_checked');
assert.ok(pkg.debates.length >= 1);
assert.ok(pkg.uncertainties.length >= 2);

assert.ok(graph.nodes.some((node) => node.type === 'debate'));
assert.ok(graph.nodes.filter((node) => node.type === 'position').length >= 2);
assert.ok(graph.nodes.filter((node) => node.type === 'uncertainty').length >= 2);
assert.ok(graph.nodes.some((node) => node.id === 'claim:administrative-core'));
assert.ok(graph.nodes.some((node) => node.id === 'ev:met-origins:admin'));

assert.ok(graph.edges.some((edge) => edge.relation === 'supports'));
assert.ok(graph.edges.some((edge) => edge.relation === 'has_position'));
assert.ok(graph.edges.some((edge) => edge.relation === 'supported_by'));
assert.ok(graph.edges.some((edge) => edge.relation === 'opens'));
assert.ok(graph.edges.some((edge) => edge.relation === 'grounded_in'));

const adminClaim = pkg.claims.find((claim) => claim.id === 'claim:administrative-core');
assert.equal(adminClaim.status, 'scholarly_interpretation');
assert.equal(adminClaim.confidence, 'high');

console.log(`ok - ANE E2E graph: ${graph.nodes.length} nodes, ${graph.edges.length} edges`);
