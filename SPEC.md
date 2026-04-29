# VoyagerAgent (VA) — Spec

## Vision
A mobile-first app with a chat-centric interface (Telegram-like) where an AI agent handles travel research, comparison, and booking across multiple APIs.

## Core Concept
- **Main screen = Chat** — similar to Telegram: a list of conversations, with the agent as the primary "contact"
- **Agent capabilities** — search, compare, and book travel services via integrated APIs
- **Cards inside chat** — rich results (flight cards, hotel cards, car rental options) rendered inline within the conversation

## Features (Phase 1)

### Chat UI
- Telegram-style conversation list
- Real-time messaging interface with the VA agent
- Message types: text, rich cards (flights, hotels, cars, tours), quick-reply buttons
- Conversation history persisted per user

### Travel Agent
- Natural language travel queries ("Find me a flight from Seville to London next weekend")
- Multi-step search (agent can ask clarifying questions)
- Results as rich interactive cards within chat
- Ability to book/hold selected options

### Travel Data Sources
- **Flights**: LetsFG (Python SDK, 400+ airlines, no API key, free) ✅ MVP
- **Hotels**: Phase 2 — Google Maps API (user has key)
- **Restaurants**: Phase 2 — Google Maps API

Note: Traditional APIs (Amadeus, Kiwi, Duffel) require commercial agreements or are shutting down developer access.

## Features (Phase 2 — stretch)
- Multi-agent: specialized agents for flights, hotels, activities
- Group travel: shared trip planning conversations
- Price alerts & tracking
- Calendar integration
- Booking management dashboard

## Tech Stack (Decided)

| Layer | Technology |
|---|---|
| **Frontend** | Expo (React Native) — iOS + Android |
| **Backend** | Python + FastAPI |
| **Testing/Staging** | Dokploy |
| **Production** | AWS |
| **Dev machine** | macOS |

## Technical Decisions (Decided)
3. **Agent framework**: LangChain (tool-calling for API integrations)
4. **Database**: PostgreSQL (users, bookings, conversations) + Redis (search caching)
5. **API strategy**: LetsFG for flights + swoop for hotels (no signup, no MAU, works immediately)
6. **Auth**: Email/phone + optional social login (Google/Apple)

## Open Questions
- Budget for travel API access (many require commercial agreements)
- Do we handle actual booking/payment, or just search + redirect?
- White-label vs own brand?
