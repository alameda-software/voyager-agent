# Thoughts on `todo.md`

## Short answer

The core idea is strong, but combining Voyager and a wedding-planning product into the same MVP would probably slow you down instead of accelerating you.

Using fake data in the first stages is the right move if the goal is to validate agent behavior, chat UX, recommendation flows, clarification questions, cards, and booking-preparation logic before depending on real partner APIs.

## What is good in the idea

Your instinct is correct that these products share the same interaction model:

- user expresses a complex goal in natural language
- agent extracts structured preferences
- agent asks only necessary follow-up questions
- agent compares options
- agent saves state and preferences
- agent helps the user move toward a decision

That means there is a reusable platform layer:

- conversation engine
- structured state extraction
- recommendation cards
- ranking/comparison logic
- memory and saved preferences
- confirmation gates
- booking-preparation workflows

This is the real asset. Not “travel” by itself, and not “weddings” by itself.

## What is risky

The dangerous part is product focus.

Travel and weddings may share an agent architecture, but they are not the same operational business:

- travel has external APIs, inventory, dates, routes, prices, and existing user expectations
- weddings require supply onboarding, vendor relationship management, availability capture, lead handling, and trust-building with local vendors

If you merge both into one MVP, you create two problems at once:

1. building the agent product
2. choosing and proving the vertical

That usually weakens the MVP. Users, UI, data model, language, and onboarding all become less clear.

## My recommendation

Build one shared agent platform, but present only one vertical in the MVP.

The cleanest approach is:

- keep the backend and agent architecture domain-oriented and reusable
- choose one visible user experience first
- use mock data heavily at the beginning
- prove that the assistant behavior is genuinely useful

In practice, that means:

- do not build “Voyager + Wedding Planner” as one public app yet
- do build a reusable concierge engine underneath
- choose travel or weddings as the first front-end story

## Which vertical should go first

If the main goal is speed of execution and agent-quality validation, weddings may actually be easier for an MVP with mock data because:

- you do not need live API approvals immediately
- vendor cards can be manually curated
- availability can be simulated
- the value proposition is easy to demonstrate visually

If the main goal is long-term scalability and easier structured search, travel is stronger because:

- the data model is more standardized
- users already understand the search flow
- real integrations eventually become more defensible

So the choice depends on what you are optimizing for:

- fastest demo of agent behavior: weddings
- stronger long-term systemized marketplace path: travel

## Fake data

I agree with using fake data first.

But it should be done deliberately, not as random placeholders.

The fake data should simulate a real system:

- realistic vendor/travel inventory
- realistic availability states
- realistic pricing ranges
- realistic tradeoffs
- realistic follow-up questions
- structured recommendation objects

If the fake data is good, you can validate:

- whether the assistant asks smart questions
- whether cards and trip/event summaries are understandable
- whether users trust the flow
- whether recommendation ranking feels useful
- whether booking-preparation UX makes sense

## Best framing

The strongest framing is not:

"Should we merge both apps?"

The stronger framing is:

"Should we build a reusable AI concierge platform and launch it first in one vertical?"

My answer to that is yes.

## Concrete recommendation

If I were steering this project, I would do this:

1. Build the shared concierge core:
   chat, memory, structured state, recommendation cards, confirmation gates.
2. Use high-quality mock inventory first.
3. Pick one vertical-facing MVP.
4. Keep the internal architecture generic enough to support a second vertical later.
5. Only after the core UX works, decide whether the first commercial wedge is travel or weddings.

## Bottom line

`todo.md` contains a real strategic insight: the valuable thing here is the agent-assisted decision workflow, not just the travel niche.

But the wrong conclusion would be to combine both products into one MVP right now.

The better conclusion is to build one strong concierge engine, use fake data early, and launch with one vertical at a time.
