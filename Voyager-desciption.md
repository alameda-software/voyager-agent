Here is a clean summary you can paste into your Codex/Kilo Code project context:

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

Agent Role in Voyager

The AI agent should not simply answer with generic travel text. It should manage a structured trip object.

Example user request:

I’m from London, family of 3, and want to go to Feria de Abril in Seville.

The agent should:

1. Detect the intent: plan a trip.
2. Extract known details:
    * Origin: London
    * Destination: Seville
    * Travellers: family of 3
    * Event: Feria de Abril
3. Ask only missing critical questions:
    * Dates or date flexibility
    * Traveller composition/ages
    * Budget
    * Hotel preferences
4. Create or update a trip record.
5. Generate a draft itinerary.
6. Search or prepare options for flights, hotels, restaurants, tours, and event tickets.
7. Save recommendations to the trip.
8. Prepare booking actions.
9. Require user confirmation before purchases, cancellations, document sharing, or payments.

Trip State / Persistent Memory

Voyager should not rely only on chat history. It should persist structured trip state in the database.

A trip record should include fields such as:

{
  "trip_id": "trip_123",
  "origin": "London",
  "destination": "Seville",
  "event": "Feria de Abril",
  "travellers": {
    "total": 3,
    "adults": null,
    "children": null
  },
  "dates": {
    "fixed": false,
    "start": null,
    "end": null,
    "flexibility": null
  },
  "budget": null,
  "preferences": {
    "family_friendly": true,
    "central_location": true,
    "direct_flights": true
  },
  "itinerary": [],
  "recommendations": [],
  "documents": [],
  "booking_status": "planning"
}

Persistent trip memory is one of the most important MVP features because it makes the assistant feel useful and reliable.

Backend Tools the Agent Should Use

The agent should interact with Voyager through controlled backend tools/functions, not direct database or payment access.

Possible tools:

create_trip()
get_trip_summary()
update_trip_preferences()
extract_trip_details_from_message()
create_itinerary()
search_flights()
search_hotels()
search_restaurants()
search_event_tickets()
search_tours()
search_cars()
save_recommendation()
save_document_metadata()
prepare_booking()
confirm_booking()
cancel_booking()
send_notification()
create_support_case()

Dangerous operations should be gated behind explicit confirmation.

Confirmation Rules

The AI can prepare actions, but the user must confirm anything involving money, identity, cancellation risk, or irreversible changes.

The agent may automatically:

* Suggest itineraries
* Search flights/hotels/restaurants/tours
* Compare options
* Save trip preferences
* Draft booking plans
* Prepare recommendations

The agent must ask for confirmation before:

* Buying tickets
* Paying for hotels/flights/tours
* Cancelling bookings
* Sharing documents
* Sending passport or identity data
* Making irreversible changes
* Storing sensitive documents
* Charging a card

MVP Scope

Voyager MVP should focus on:

1. Chat-first trip planning
2. Persistent trip memory
3. Structured trip state extraction
4. Itinerary generation
5. Flight/hotel/restaurant/tour recommendations
6. Trip dashboard/cards
7. Booking preparation, not full automatic booking
8. Human confirmation gates
9. Basic document vault placeholder
10. Clear safety/privacy rules

The first MVP does not need to directly purchase everything. It can start with recommendations, deep links, affiliate links, or booking handoff flows.

Future Scope

Later versions can add:

* Real booking APIs
* Restaurant reservations
* Event ticket purchasing
* Calendar sync
* Document vault
* Payment processing
* Travel disruption alerts
* Cancellation/change workflows
* Vendor/partner integrations
* Multi-user group trip collaboration

Security and Privacy Principles

Voyager will handle sensitive travel data such as locations, family details, documents, passports, bookings, and payments. Security must be designed from the start.

Rules:

* Do not give agents unrestricted database access.
* Do not give agents unrestricted shell access.
* Do not store raw passport/payment data in plain text.
* Do not expose production secrets to prompts or tools.
* Use scoped API keys.
* Log agent tool calls.
* Require confirmation for payments, bookings, cancellations, and document sharing.
* Keep user-facing agents separate from internal operator agents.
* KiloClaw/OpenClaw should be used with approved tools only.

Development Workflow

Kilo Code is used for building the Voyager application.

KiloClaw/OpenClaw is used as an operator/agent layer for:

* Coordinating development tasks
* Creating GitHub issues
* Summarising PRs
* Running controlled workflows
* Supporting travel planning logic
* Preparing marketing and launch materials
* Monitoring support/admin tasks

Development should use:

Telegram or KiloClaw chat
   ↓
KiloClaw as coordinator
   ↓
GitHub issues and branches
   ↓
Kilo Code as coding executor
   ↓
Pull request
   ↓
Human review and merge

Rules:

* Never push directly to main.
* Always use feature branches.
* Always open pull requests.
* Ask before database schema changes.
* Ask before adding dependencies.
* Ask before touching auth, payments, bookings, or document storage.
* Run tests/lint/typecheck before completing tasks.
* Keep tasks small and scoped.

Product Experience Goal

Voyager should feel like this:

User:
I want to go to Seville for Feria de Abril with my wife and son.
Voyager:
Great — I’ll plan this as a family trip. Are you travelling from London, and do you want a 3-night or 4-night stay?
User:
London, 4 nights, not crazy expensive.
Voyager:
Perfect. I’ll optimize for direct flights, a family-friendly hotel, and easy access to the Feria area. I’ll create your trip plan now.

Then Voyager creates:

* A trip card
* A draft itinerary
* Flight options
* Hotel options
* Restaurant shortlist
* Event/ticket notes
* Next actions

The goal is to create a reliable AI travel concierge, not a generic chatbot.