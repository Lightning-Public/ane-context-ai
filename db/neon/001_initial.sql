-- ANE Context AI — Neon/PostgreSQL initial schema
-- Safe for public source control: contains no credentials or environment-specific values.

create extension if not exists vector;

create table if not exists sources (
  id text primary key,
  name text not null,
  stable_url text not null,
  source_type text not null,
  license_manifest_id text,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists artifacts (
  id text primary key,
  source_id text not null references sources(id) on delete restrict,
  source_record_id text not null,
  stable_url text not null,
  period text,
  provenience text,
  genre text,
  language text,
  script_stage text,
  status text not null default 'candidate' check (status in ('candidate','resolved','metadata_checked','needs_revision','verified')),
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (source_id, source_record_id)
);

create table if not exists context_packages (
  id text primary key,
  schema_version text not null,
  question_original text not null,
  question_normalized text not null,
  review_status text not null default 'unreviewed' check (review_status in ('unreviewed','needs_revision','source_checked','expert_reviewed')),
  payload jsonb not null,
  created_at timestamptz not null,
  retrieved_at timestamptz,
  updated_at timestamptz not null default now()
);

create table if not exists evidence (
  id text primary key,
  context_package_id text not null references context_packages(id) on delete cascade,
  artifact_id text references artifacts(id) on delete restrict,
  source_id text not null references sources(id) on delete restrict,
  source_record_id text not null,
  stable_url text not null,
  locator text not null,
  layer text not null check (layer in ('artifact','image','transliteration','translation','edition','secondary')),
  excerpt text not null default '',
  attribution text not null,
  license_manifest_id text not null,
  created_at timestamptz not null default now()
);

create table if not exists claims (
  id text primary key,
  context_package_id text not null references context_packages(id) on delete cascade,
  statement text not null,
  claim_status text not null check (claim_status in ('attested','derived','scholarly_interpretation','model_inference')),
  confidence text not null check (confidence in ('high','medium','low','unknown')),
  reasoning text not null,
  supporting_evidence_ids text[] not null default '{}',
  challenging_evidence_ids text[] not null default '{}',
  created_at timestamptz not null default now()
);

create table if not exists reviews (
  id text primary key,
  target_type text not null check (target_type in ('context_package','artifact')),
  target_ids text[] not null,
  reviewer_identity_type text not null check (reviewer_identity_type in ('human','ai_assistant')),
  reviewer_name text not null,
  reviewer_identifier text,
  reviewer_role text,
  reviewer_expertise text[] not null default '{}',
  reviewed_at timestamptz not null,
  decision text not null check (decision in ('approve','needs_revision','reject')),
  is_promotion_authority boolean generated always as (reviewer_identity_type = 'human' and decision = 'approve') stored,
  record jsonb not null,
  created_at timestamptz not null default now()
);

create table if not exists embeddings (
  id bigserial primary key,
  entity_type text not null check (entity_type in ('artifact','evidence','claim','context_package','source')),
  entity_id text not null,
  model text not null,
  dimensions integer not null,
  embedding vector,
  content_hash text not null,
  created_at timestamptz not null default now(),
  unique (entity_type, entity_id, model, content_hash)
);

create index if not exists idx_artifacts_source on artifacts(source_id);
create index if not exists idx_artifacts_period on artifacts(period);
create index if not exists idx_artifacts_provenience on artifacts(provenience);
create index if not exists idx_evidence_package on evidence(context_package_id);
create index if not exists idx_evidence_artifact on evidence(artifact_id);
create index if not exists idx_claims_package on claims(context_package_id);
create index if not exists idx_reviews_target_type on reviews(target_type);

comment on table embeddings is 'Vector data is optional. Add an HNSW/IVFFlat index only after a concrete embedding model and dimensions are fixed.';
