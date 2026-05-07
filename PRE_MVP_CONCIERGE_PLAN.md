# Pre-MVP Concierge Plan

## Goal

For this pre-MVP, the goal is not live bookings or real integrations.

The goal is to make the user feel they are talking to a genuinely capable AI concierge that can:

- understand messy natural-language requests
- extract structured preferences
- ask only the necessary follow-up questions
- remember context over time
- compare options intelligently
- generate plans and useful documents
- prepare booking-style actions without actually executing risky operations

The benchmark is a KiloClaw-like feeling of capability, but implemented as a controlled product system inside Voyager.

## Product Direction

For testing, the app can start with two entry buttons:

- `Go to Voyager`
- `Go to Wedding`

This is acceptable for pre-MVP validation.

The important constraint is that this should not become one blurred product. It should be one shared concierge engine with two domain modes.

## Core Decision

Yes, the same AI core can power both Voyager and Wedding.

But only the core should be shared.

The domain layer should remain separate.

## Shared Concierge Core

The shared concierge core should be responsible for:

- conversation orchestration
- memory and context handling
- extracting structured facts from messages
- deciding what is missing
- asking follow-up questions
- generating plans and summaries
- comparing options
- confirmation gating
- response formatting
- document generation

This layer should be domain-agnostic.

## Domain Packs

Each domain should provide its own pack:

### Voyager pack

- trip schema
- travel-specific prompts
- tool definitions for flights, hotels, tours, cars, restaurants
- travel card components
- itinerary generation rules
- travel fake inventory

### Wedding pack

- wedding schema
- wedding-specific prompts
- tool definitions for venues, catering, bands, photographers, planners, transport
- vendor card components
- wedding planning rules
- wedding fake inventory

The engine should never hardcode travel-only assumptions if weddings are going to share it.

## Shared State Contract

Each conversation should have:

- `domain`: `voyager` or `wedding`
- `conversation_id`
- `user_id` or anonymous session id
- `structured_state`
- `messages`
- `generated_documents`
- `saved_recommendations`
- `pending_confirmations`

The engine should work against a generic envelope:

```json
{
  "domain": "voyager",
  "conversation_id": "conv_123",
  "structured_state": {},
  "messages": [],
  "saved_recommendations": [],
  "generated_documents": [],
  "pending_confirmations": []
}
```

Then each domain fills `structured_state` with its own schema.

## Domain State Examples

### Voyager state

```json
{
  "trip_type": "family_trip",
  "origin": "London",
  "destination": "Seville",
  "dates": {
    "start": null,
    "end": null,
    "flexibility": "weekend"
  },
  "travellers": {
    "total": 3,
    "adults": 2,
    "children": 1
  },
  "budget": null,
  "preferences": {
    "direct_flights": true,
    "family_friendly": true
  },
  "itinerary": [],
  "recommendations": []
}
```

### Wedding state

```json
{
  "event_type": "wedding",
  "location": "Seville",
  "date": null,
  "guest_count": 120,
  "budget": null,
  "style": null,
  "priorities": [
    "beautiful venue",
    "good food",
    "live music"
  ],
  "vendors_needed": [
    "venue",
    "catering",
    "band"
  ],
  "recommendations": []
}
```

## Tool Interface

Even when using fake data, tools should behave like real product tools.

The engine should call tools through a stable interface such as:

- `extract_state_from_message(domain, state, message)`
- `find_missing_fields(domain, state)`
- `search_options(domain, category, state)`
- `rank_options(domain, category, options, state)`
- `save_recommendation(domain, conversation_id, item)`
- `generate_plan(domain, state)`
- `generate_document(domain, type, state, recommendations)`
- `prepare_booking(domain, item_id)`
- `require_confirmation(action)`

This matters because later you can swap fake providers for real providers without rewriting the orchestration logic.

## Fake Data Strategy

Fake data should not be random demo filler.

It should be structured, realistic, and intentionally designed to create meaningful tradeoffs.

### Fake Voyager inventory should include

- flights with dates, durations, stops, fares, baggage, cabin, refundability
- hotels with neighborhood, amenities, cancellation terms, family fit, pricing
- restaurants, tours, cars, and event options with realistic metadata

### Fake Wedding inventory should include

- venues with capacity, style, location, availability, pricing band
- caterers with cuisine type, service style, dietary support, price per guest
- bands and photographers with style, region, package types, availability

If the data is shallow, the assistant will feel shallow.

## Document Generation Layer

To get the “real concierge” feeling, the assistant should generate useful artifacts, not only chat replies.

The first pre-MVP document types should be:

- trip summary
- itinerary draft
- recommendation comparison
- budget outline
- wedding shortlist
- vendor comparison sheet
- next-step checklist
- draft inquiry message or email

These can initially be rendered as structured markdown blocks or saved text artifacts.

## UX Flow

### Entry

The first screen shows:

- `Voyager`
- `Wedding`

### Conversation flow

1. User chooses a domain.
2. App creates a conversation with that domain.
3. Assistant starts with a domain-specific opening.
4. User sends natural-language request.
5. Engine updates structured state.
6. Engine asks one or more focused follow-up questions if needed.
7. Engine returns cards, plans, and suggested next steps.
8. Engine saves recommendations and generated documents.

## How this maps to the current repo

The current repo already has the right rough split:

- Expo mobile app
- FastAPI backend
- early agent/service layer

But it needs to be reorganized around a reusable concierge engine.

## Suggested Next Steps

### Step 1: Define shared backend models

Add backend concepts for:

- `Conversation`
- `Message`
- `DomainSession` or `ConciergeSession`
- `StructuredState`
- `GeneratedDocument`
- `SavedRecommendation`
- `PendingConfirmation`

You may keep separate domain-specific payloads inside JSON fields at first.

### Step 2: Introduce domain mode at conversation creation

When a conversation is created, it should store:

- `domain = voyager`
- or `domain = wedding`

That single field should drive prompt selection, tool selection, state schema, and UI behavior.

### Step 3: Build a real concierge orchestration service

Create one service that does:

- load conversation and structured state
- pick domain pack
- extract new facts from user message
- detect missing info
- decide whether to ask or recommend
- run fake search tools
- save results
- generate response plus UI metadata

### Step 4: Create domain packs

Create:

- `domains/voyager`
- `domains/wedding`

Each should contain:

- prompts
- schemas
- fake data adapters
- ranking logic
- card mappers
- document templates

### Step 5: Replace hardcoded mobile chat demo state

The mobile app should stop seeding fake messages in component state and instead:

- choose a domain from the first screen
- create a conversation through the backend
- fetch/send messages through the API
- render cards returned by the backend
- render saved documents/plans as part of the conversation

### Step 6: Add realistic fake inventory sources

Do not mix fake rows directly inside screens.

Store them as structured backend data fixtures so the assistant can search and rank them consistently.

### Step 7: Add document generation endpoints

The backend should expose generated artifacts so the app can show:

- planning summaries
- shortlist comparisons
- itinerary or wedding plan drafts
- inquiry drafts

## Recommended Build Order

1. Add domain selection and conversation creation.
2. Add shared structured state storage.
3. Add one concierge orchestration path.
4. Implement Voyager fake-search flow.
5. Implement Wedding fake-search flow.
6. Add generated documents.
7. Improve ranking, memory, and follow-up quality.

## Bottom Line

The pre-MVP should be built as a dual-domain concierge testbed, not as a fully integrated marketplace.

That means:

- same AI concierge core
- separate domain packs
- fake but realistic data
- strong memory
- strong plan/document generation
- travel and wedding both testable from the first screen

If done well, this will let you evaluate the real thing you care about: whether the concierge experience feels genuinely powerful before you invest in live integrations.
