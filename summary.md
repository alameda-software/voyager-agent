# Voyager Project Context

Voyager is an AI-first travel concierge app. The product experience is similar to a chat-based travel agency, inspired by messaging apps like Telegram or WhatsApp. Users can describe a trip naturally, for example:

> “I’m from London, family of 3, and want to go to Feria de Abril in Seville.”

Voyager should understand the request, extract structured trip information, ask only essential missing questions, create a trip plan, compare options, save relevant documents, and help the user prepare bookings.

## Core Product Vision

Voyager helps users plan and manage trips through an intelligent AI travel assistant.

The app should support:

- Conversational trip planning
- Persistent trip memory
- Itinerary generation
- Flight, hotel, restaurant, car, tour, and event-ticket search
- Booking preparation
- Saved documents and travel details
- Family/group travel preferences
- Budget-aware recommendations
- Confirmation before risky or paid actions
- A clean chat-first experience with trip dashboards/cards

Voyager should feel like a personal travel agent, not just a chatbot.

## Key Architecture Decision

KiloClaw/OpenClaw should not replace the Voyager backend.

Voyager remains the actual product and system of record. The backend owns user accounts, trip data, bookings, permissions, documents, payments, and integrations.

KiloClaw/OpenClaw should act as the agent/operator layer behind Voyager. It can coordinate workflows, call approved tools, assist with planning, and support internal operations, but it should not have unrestricted access to production systems.

Kilo Code is used to build and improve the Voyager codebase.

KiloClaw/OpenClaw is used to create the intelligent travel-agent experience and internal operator workflows.

## Recommended Architecture

```text
Voyager web/mobile app
   ↓
Voyager backend API
   ↓
Voyager agent orchestration layer
   ↓
LLM router / model gateway
   ↓
Models:
   - Claude Sonnet for complex reasoning, planning, and difficult workflows
   - Cheaper/faster models for simple Q&A, summaries, formatting, and routine tasks

External services/tools:
   - Flights
   - Hotels
   - Restaurants
   - Tours
   - Maps
   - Event tickets
   - Cars
   - Calendar
   - Documents
   - Payments
   - Notifications

Internal operator:
   KiloClaw/OpenClaw
   ↓
GitHub, support workflows, admin tasks, marketing, monitoring, release notes