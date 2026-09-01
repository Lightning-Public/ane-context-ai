# Neon PostgreSQL setup

ANE Context AI uses Neon as an optional managed PostgreSQL backend while keeping the current static learning screen deployable without a database.

## Architecture

```text
Browser
  -> Vercel static UI
  -> future Vercel server-side API/functions
  -> Neon PostgreSQL
```

The browser must never receive a raw PostgreSQL connection string. `DATABASE_URL` is a server-side secret only.

## Project setup

Recommended Neon project name:

```text
ane-context-ai
```

Recommended region: choose the region closest to the primary Vercel deployment and expected users. Do not hard-code credentials or region-specific hostnames in Git.

After Neon creates the database, store the connection string only in Vercel environment variables:

```text
DATABASE_URL=postgresql://...
```

For local development, use a local `.env` file. `.env` and `.env.*` are ignored by Git.

## Initial migration

Apply:

```text
db/neon/001_initial.sql
```

The migration creates:

- `sources`
- `artifacts`
- `context_packages`
- `evidence`
- `claims`
- `reviews`
- `embeddings`

It also enables `vector` for future RAG/embedding use.

## Security baseline

1. Never expose `DATABASE_URL` through browser JavaScript or `VITE_*`/`NEXT_PUBLIC_*` variables.
2. Do not commit `.env`, Neon connection strings, passwords, tokens, or `.vercel/project.json` credentials.
3. Access Neon only from Vercel server-side functions/API routes or controlled migration tooling.
4. Keep the current static learning page DB-independent until an API layer is actually required.
5. Do not copy restricted CDLI images or line art into Neon Storage or PostgreSQL.
6. Store source identifiers, provenance, review records, and permitted excerpts; preserve external stable URLs.
7. Separate Preview and Production databases/branches when schema-changing PRs begin.

## Preview strategy

Preferred future flow:

```text
GitHub PR
  -> Vercel Preview
  -> Neon preview branch/database

main
  -> Vercel Production
  -> Neon production branch/database
```

Do not let Preview deployments write to the Production database.

## Current phase

The database is not required for the current R002 static prototype. The schema is prepared now so the next API/data persistence unit can start without redesigning provenance and human-review contracts.
