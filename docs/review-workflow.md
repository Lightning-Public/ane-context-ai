# Human review and promotion workflow

ANE Context AI separates **machine resolution**, **AI-assisted audit**, and **human scholarly approval**. A record that resolves in an API is not thereby verified, and an AI audit cannot assign a human-reviewed state.

## State model

```text
candidate
  → resolved
  → metadata_checked / needs_revision
  → human source review
  → verified artifact

unreviewed Context Package
  → AI-assisted audit
  → needs_revision
  → human source review
  → source_checked
  → optional broader expert review
  → expert_reviewed
```

## Review record

Every review is stored as an immutable, machine-readable record conforming to [`schemas/review-record.schema.json`](../schemas/review-record.schema.json). The record identifies:

- the reviewer and whether the reviewer is human or an AI assistant;
- a stable identity or signature;
- the reviewed artifact, Context Package, evidence IDs, lines, plates, and editions;
- corrections, disagreements, limitations, and where unresolved issues remain visible;
- attribution and reuse checks;
- the decision: `approve`, `needs_revision`, or `reject`.

AI-assisted records are useful for finding problems and may issue `needs_revision` or `reject`. They may not issue a promotion-valid `approve`.

## Context Package promotion

A Context Package may use `source_checked` or `expert_reviewed` only when:

1. `review.reviewers`, `review.review_record_ids`, and `review.reviewed_at` are present;
2. at least one referenced review record is a human `approve` decision targeting the package;
3. the approving record covers every evidence ID in the package;
4. at least one edition or primary source with an exact locator was consulted;
5. attribution and reuse conditions were checked;
6. no blocking finding remains;
7. non-blocking disagreements name the package location where they remain visible;
8. the package review timestamp is not earlier than the approving review.

Run:

```bash
ane-context validate-promotion path/to/package.json \
  --review-record path/to/human-review.json
```

## Artifact promotion

A source-pack artifact may use `status: verified` only when it also records:

```json
{
  "object_id": "P000000",
  "status": "verified",
  "verified_at": "2026-08-21T00:00:00Z",
  "review_record_ids": ["review:artifact:..."]
}
```

At least one referenced human `approve` review must target that artifact.

Run:

```bash
ane-context validate-source-pack data/manifests/source-pack.json \
  --review-record path/to/artifact-review.json
```

## Review levels

- **resolved**: the external identifier currently returns a record.
- **metadata_checked**: identifiers and current catalogue fields were compared.
- **needs_revision**: blocking ambiguity, missing edition collation, unsupported claim, or rights issue remains.
- **verified artifact**: a human reviewer approved the artifact identity, cited edition/lines, and rights/attribution record.
- **source_checked package**: a human reviewer approved every evidence item and its use in the package.
- **expert_reviewed package**: source checking is complete and the broader interpretation has received attributable domain review.

## Git and community use

Review records are committed beside the research object. Corrections create new review records rather than overwriting the history. A community discussion, reaction count, or AI-generated summary is not itself a promotion record.

Use [`docs/reviews/REVIEW-TEMPLATE.md`](reviews/REVIEW-TEMPLATE.md) for the human-readable checklist and `templates/review-record.template.json` for the machine-readable starting point.
