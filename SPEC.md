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

### API Integrations (TBD — research phase)
- **Flights**: Amadeus, Duffel, Skyscanner, or Kiwi
- **Hotels**: Amadeus, Booking.com, Hotelbeds
- **Car Rentals**: Amadeus, Rentalcars.com
- **Tours/Activities**: Viator, GetYourGuide, Peek

## Features (Phase 2 — stretch)
- Multi-agent: specialized agents for flights, hotels, activities
- Group travel: shared trip planning conversations
- Price alerts & tracking
- Calendar integration
- Booking management dashboard

## Technical Decisions Needed
1. **Mobile framework**: React Native / Flutter / Native (iOS + Android)
2. **Backend**: Node.js / Python / Go
3. **Agent framework**: Custom LLM orchestration vs existing (LangChain, CrewAI, etc.)
4. **Database**: PostgreSQL + Redis (cache) / MongoDB
5. **API strategy**: Which travel APIs to prioritize first
6. **Auth**: Email/phone + optional social login

## Open Questions
- Target platforms: iOS, Android, or both first?
- Budget for travel API access (many require commercial agreements)
- Do we handle actual booking/payment, or just search + redirect?
- White-label vs own brand?
