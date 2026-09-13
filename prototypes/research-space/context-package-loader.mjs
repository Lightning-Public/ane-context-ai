import { contextPackageToResearchSpace } from './context-package-adapter.mjs';

export async function loadContextPackage(url, fetchImpl = globalThis.fetch) {
  if (typeof fetchImpl !== 'function') throw new Error('fetch implementation is required');
  const response = await fetchImpl(url);
  if (!response || !response.ok) {
    const status = response?.status ?? 'unknown';
    throw new Error(`Failed to load Context Package: ${status}`);
  }
  const pkg = await response.json();
  return {
    package: pkg,
    graph: contextPackageToResearchSpace(pkg),
  };
}

export function buildCanvasLayout(graph) {
  const columns = {
    question: 0,
    claim: 1,
    evidence: 2,
    debate: 1,
    position: 2,
    uncertainty: 3,
    source: 3,
    provenance: 4,
    review: 4,
  };
  const rowCounts = new Map();
  return graph.nodes.map((node) => {
    const column = columns[node.type] ?? 2;
    const row = rowCounts.get(column) ?? 0;
    rowCounts.set(column, row + 1);
    return {
      ...node,
      x: 36 + column * 230,
      y: 36 + row * 135,
    };
  });
}
