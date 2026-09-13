export function contextPackageToResearchSpace(pkg) {
  if (!pkg || pkg.schema_version !== '0.1.0') throw new Error('Unsupported Context Package schema');
  const nodes = [], edges = [];
  const addNode = (node) => nodes.push(node);
  const addEdge = (from, to, relation, suffix = '') => edges.push({ id:`edge:${from}:${relation}:${to}${suffix?`:${suffix}`:''}`, from, to, relation });
  const questionId = 'question:root';
  addNode({ id:questionId, type:'question', label:pkg.question.original, data:{ normalized:pkg.question.normalized, scope:pkg.question.scope } });
  for (const ev of pkg.evidence || []) addNode({ id:ev.id, type:'evidence', label:ev.excerpt || `${ev.source} ${ev.locator}`.trim(), data:{...ev} });
  for (const claim of pkg.claims || []) {
    addNode({ id:claim.id, type:'claim', label:claim.statement, data:{...claim} });
    addEdge(questionId, claim.id, 'answered_by');
    for (const id of claim.supporting_evidence_ids || []) addEdge(id, claim.id, 'supports');
    for (const id of claim.challenging_evidence_ids || []) addEdge(id, claim.id, 'challenges');
  }
  (pkg.debates || []).forEach((debate, i) => {
    const debateId=`debate:${i+1}`; addNode({id:debateId,type:'debate',label:debate.issue,data:{issue:debate.issue}});
    debate.positions.forEach((position,j)=>{ const positionId=`${debateId}:position:${j+1}`; addNode({id:positionId,type:'position',label:position.summary,data:{...position}}); addEdge(debateId,positionId,'has_position'); for(const id of position.evidence_ids||[]) addEdge(positionId,id,'supported_by'); });
    debate.open_questions.forEach((text,j)=>{ const id=`${debateId}:question:${j+1}`; addNode({id,type:'question',label:text,data:{open:true}}); addEdge(debateId,id,'opens'); });
  });
  (pkg.uncertainties || []).forEach((u,i)=>{ const id=`uncertainty:${i+1}`; addNode({id,type:'uncertainty',label:u.description,data:{...u}}); for(const evidenceId of u.evidence_ids||[]) addEdge(id,evidenceId,'grounded_in'); });
  for (const source of pkg.bibliography || []) addNode({id:source.id,type:'source',label:source.citation,data:{...source}});
  addNode({id:'provenance:retrieval',type:'provenance',label:`Retrieval ${pkg.retrieval.run_at}`,data:{...pkg.retrieval}}); addEdge('provenance:retrieval',questionId,'provenance_of');
  addNode({id:'review:package',type:'review',label:pkg.review.status,data:{...pkg.review}}); addEdge('review:package',questionId,'review_of');
  return { packageId:pkg.id, schemaVersion:pkg.schema_version, nodes, edges, meta:{createdAt:pkg.created_at,reviewStatus:pkg.review.status} };
}
