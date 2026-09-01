-- ANE Context AI — Neon/PostgreSQL verification queries
-- Safe read-only checks to run after 001_initial.sql.

select extname
from pg_extension
where extname = 'vector';

select table_name
from information_schema.tables
where table_schema = 'public'
  and table_name in (
    'sources',
    'artifacts',
    'context_packages',
    'evidence',
    'claims',
    'reviews',
    'embeddings'
  )
order by table_name;

select indexname, tablename
from pg_indexes
where schemaname = 'public'
  and tablename in ('artifacts', 'evidence', 'claims', 'reviews')
order by tablename, indexname;

select
  (select count(*) from sources) as sources,
  (select count(*) from artifacts) as artifacts,
  (select count(*) from context_packages) as context_packages,
  (select count(*) from evidence) as evidence,
  (select count(*) from claims) as claims,
  (select count(*) from reviews) as reviews,
  (select count(*) from embeddings) as embeddings;
