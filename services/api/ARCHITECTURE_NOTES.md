# Backend Structure Notes

## Why this structure

This backend is being shaped for a pre-MVP with two test modes:

- `voyager`
- `wedding`

The code should support that now without making a future split painful when
each app moves into its own project or repo.

## Folder intent

- `app/concierge`
  Shared orchestration runtime, memory flow, tool contracts, and response assembly.
- `app/domains/voyager`
  Voyager-specific prompts, schemas, fake providers, ranking, and card mapping.
- `app/domains/wedding`
  Wedding-specific prompts, schemas, fake providers, ranking, and card mapping.
- `app/models`
  Shared persistence models only. Domain-specific payloads can live inside JSON
  fields first, then migrate outward later if needed.

## Persistence rule

The shared tables should stay generic:

- `conversations`
- `messages`
- `structured_states`
- `generated_documents`
- `saved_recommendations`
- `pending_confirmations`

The domain-specific shape belongs inside structured JSON payloads and domain
modules, not in hardcoded travel-only tables.

## Future split path

When separation happens later, the likely extraction path is:

1. keep `app/concierge` as a shared package or copyable base
2. move `app/domains/voyager` into the Voyager repo
3. move `app/domains/wedding` into the Wedding repo
4. keep or duplicate the generic persistence primitives depending on whether
   the products still share infrastructure

This is why the shared backend should depend on `domain` mode selection rather
than travel-specific assumptions baked into the core.
