export function contextPackageToResearchSpace(pkg) {
  if (!pkg || pkg.schema_version !== '0.1.0') {
    throw new Error('Unsupported Context Package schema');
  }

  const nodes = [];
  const edges = [];
  const addNode = (node) => nodes.push(node);
  const addEdge = (from, to, relation, suffix = '') => edges.push({
    id: `edge:${from}:${relation}:${to}${suffix ? `:${suffix}` : ''}`,
    from,
    to,
    relation,
  });

  const questionId = 'question:root';
  addNode({
    id: questionId,
    type: 'question',
    label: pkg.question.original,
    data: {
      normalized: pkg.question.normalized,
      scope: pkg.question.scope,
    },
  });

  for (const ev of pkg.evidence || []) {
    addNode({
      id: ev.id,
      type: 'evidence',
      label: ev.excerpt || `${ev.source} ${ev.locator}`.trim(),
      data: { ...ev },
    });
  }

  for (const claim of pkg.claims || []) {
    addNode({
      id: claim.id,
      type: 'claim',
      label: claim.statement,
      data: { ...claim },
    });
    addEdge(questionId, claim.id, 'answered_by');
    for (const evidenceId of claim.supporting_evidence_ids || []) {
      addEdge(evidenceId, claim.id, 'supports');
    }
    for (const evidenceId of claim.challenging_evidence_ids || []) {
      addEdge(evidenceId, claim.id, 'challenges');
    }
  }

  (pkg.debates || []).forEach((debate, debateIndex) => {
    const debateId = `debate:${debateIndex + 1}`;
    addNode({
      id: debateId,
      type: 'debate',
      label: debate.issue,
      data: { issue: debate.issue },
    });
    debate.positions.forEach((position, positionIndex) => {
      const positionId = `${debateId}:position:${positionIndex + 1}`;
      addNode({
        id: positionId,
        type: 'position',
        label: position.summary,
        data: { ...position },
      });
      addEdge(debateId, positionId, 'has_position');
      for (const evidenceId of position.evidence_ids || []) {
        addEdge(positionId, evidenceId, 'supported_by');
      }
    });
    debate.open_questions.forEach((text, questionIndex) => {
      const openQuestionId = `${debateId}:question:${questionIndex + 1}`;
      addNode({
        id: openQuestionId,
        type: 'question',
        label: text,
        data: { open: true },
      });
      addEdge(debateId, openQuestionId, 'opens');
    });
  });

  (pkg.uncertainties || []).forEach((uncertainty, index) => {
    const uncertaintyId = `uncertainty:${index + 1}`;
    addNode({
      id: uncertaintyId,
      type: 'uncertainty',
      label: uncertainty.description,
      data: { ...uncertainty },
    });
    for (const evidenceId of uncertainty.evidence_ids || []) {
      addEdge(uncertaintyId, evidenceId, 'grounded_in');
    }
  });

  for (const source of pkg.bibliography || []) {
    addNode({
      id: source.id,
      type: 'source',
      label: source.citation,
      data: { ...source },
    });
  }

  const provenanceId = 'provenance:retrieval';
  addNode({
    id: provenanceId,
    type: 'provenance',
    label: `Retrieval ${pkg.retrieval.run_at}`,
    data: { ...pkg.retrieval },
  });
  addEdge(provenanceId, questionId, 'provenance_of');

  const reviewId = 'review:package';
  addNode({
    id: reviewId,
    type: 'review',
    label: pkg.review.status,
    data: { ...pkg.review },
  });
  addEdge(reviewId, questionId, 'review_of');

  return {
    packageId: pkg.id,
    schemaVersion: pkg.schema_version,
    nodes,
    edges,
    meta: {
      createdAt: pkg.created_at,
      reviewStatus: pkg.review.status,
    },
  };
}
