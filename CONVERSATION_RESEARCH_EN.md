# Wedding Concierge - Conversation Research & Design (EN)

**Objective:** Understand how users interact with the AI agent for wedding planning, identify patterns, and optimize responses.

**Creation Date:** 2026-05-28  
**Status:** In Development

---

## 1. User Intents (What does the user want to accomplish?)

### 1.1 Information Gathering
- [ ] "Where do I start planning?"
- [ ] "How much does a wedding cost in Seville?"
- [ ] "How much time do I need to plan?"
- [ ] "What vendors are essential?"

### 1.2 Vendor Search
- [ ] "I need a photographer"
- [ ] "Search catering for 100 people"
- [ ] "Garden venue options?"
- [ ] "DJ or live band?"

### 1.3 Comparison & Filtering
- [ ] "Which is better, A or B?"
- [ ] "Cheaper options?"
- [ ] "Best rated options?"
- [ ] "Available next weekend?"

### 1.4 Planning & Timeline
- [ ] "Wedding in 6 months, 150 people"
- [ ] "Budget €5000, what's the plan?"
- [ ] "Recommended timeline?"

### 1.5 Confirmation & Booking
- [ ] "I like this one, how do I book?"
- [ ] "I want to confirm X vendor"
- [ ] "Can you save my selections?"

### 1.6 Clarification & Follow-up
- [ ] "What does that mean?"
- [ ] "Can you explain more about X?"
- [ ] "Any alternatives?"

---

## 2. Common Questions by Category

### Venues/Fincas
```
"I need a venue for 150 people in Seville"
"Options with a pool?"
"Which has best value for money?"
"Can I bring my own catering?"
"Which is most beautiful for photos?"
"Available July 2026?"
```

### Catering/Banquet
```
"Traditional Andalusian menu options?"
"Minimum budget per person?"
"Beverages included?"
"Vegetarian options?"
"Custom chef service?"
"Table decoration included?"
```

### Photography
```
"Modern photographer, documentary style"
"How many hours of coverage?"
"Does it include album?"
"Video as well?"
"Digital editing?"
"Fixed price or hourly?"
```

### Music/DJ
```
"DJ or live band?"
"What music style?"
"How many hours?"
"Sound equipment included?"
"Budget?"
```

### Florist
```
"Custom bridal bouquet"
"Full venue decoration?"
"Fresh or artificial flowers?"
"Home delivery?"
"Budget for X tables?"
```

### Pastry/Cake
```
"Custom wedding cake"
"How many guests?"
"Available flavors?"
"Fondant or buttercream?"
"Delivery included?"
```

### General Planning
```
"What's the first step?"
"We have X months, Y budget, Z guests"
"Which vendors are must-haves?"
"Typical timeline?"
"Planning checklist?"
```

---

## 3. Conversation Patterns (Typical Flows)

### Pattern A: Quick Search (2-3 messages)
```
User: "DJ for 100 people in Seville"
System: [Shows 3-4 options with prices]
User: "I like this one"
Duration: 2-3 messages
Success: ✓ Fast, direct, actionable
```

### Pattern B: Browse & Compare (4-6 messages)
```
User: "Show me photographers in Seville"
System: [Shows 4 options with details]
User: "What's the difference between A and B?"
System: [Compares A vs B]
User: "I want to go with A"
Duration: 4-6 messages
Success: ✓ Informed, high confidence
```

### Pattern C: Planning Mode (8+ messages)
```
User: "Wedding in 6 months, 150 people, Seville"
System: [Generates checklist + proposes workflow]
User: "Where do I start?"
System: [First step: venue/finca]
User: "Show me options"
System: [Venue search]
... (continues exploring each category)
Duration: 8+ messages
Success: ✓ Educated, structured, confident
```

### Pattern D: Lost User (Confused)
```
User: [Vague/out-of-context question]
System: [Generic response]
User: [Doesn't understand, repeats]
System: [Still doesn't understand]
❌ Failure: Likely abandonment
```

---

## 4. LLM Response Quality Metrics

### ✅ What Works Well
- Conversational responses, not robotic
- Context-specific (mentions location, budget)
- Clear actions ("I'll show you X options")
- Natural follow-up questions
- Presents vendors with relevant details (price, rating, promotion)

### ❌ What Fails
- Generic responses ("there are many options")
- Too much text, overwhelming
- Doesn't extract context (forgets city, budget)
- No next step suggestion
- Lists vendors without explaining why

### 🎯 GOOD vs BAD Response Examples

**BAD:**
```
"There are many photographer options available. 
Which do you prefer? You can search by price, 
reviews or experience. Let me know what you're looking for."
```

**GOOD:**
```
"For Seville I have 4 top photographers:

1. **Elena Rodríguez** - 4.9⭐ - Modern, 
   documentary style. From €800 + premium album.
2. **Luis Mora** - 4.8⭐ - Classic artistic, 
   highly sought. From €900.

Does one appeal to you? Or looking for something 
more specific (budget, style, hours)?"
```

---

## 5. Testing Checklist

### 5.1 Extraction Test (Does it understand context?)
- [ ] Extracts city correctly
- [ ] Identifies vendor category
- [ ] Captures numbers (guests, budget, date)
- [ ] Understands intent (search vs plan)

### 5.2 Response Quality Test
- [ ] Response is conversational
- [ ] Includes specific details (ratings, prices)
- [ ] Suggests next step
- [ ] Maintains context in follow-up

### 5.3 Vendor Search Test
- [ ] Returns correct results
- [ ] Orders by featured/rating
- [ ] Filters by city correctly
- [ ] Includes images in payload

### 5.4 Edge Cases Test
- [ ] User asks about other city (Madrid, Barcelona)
- [ ] Very low budget
- [ ] Very near or far date
- [ ] Question outside domain (travel, hotels)

---

## 6. Conversation Examples to Test

### Test Case 1: Quick Vendor Search
```
User: "Photographer for wedding in Seville"
Expected: 
  - Shows 3-4 photographers
  - Includes ratings, price, style
  - Offers comparison or next step
```

### Test Case 2: With Context
```
User: "I need catering for 150 people in Seville, budget €3000"
Expected:
  - Filters by budget (~€20/person)
  - Shows options within range
  - Mentions budget ("showing options up to €20/person")
```

### Test Case 3: Comparison Request
```
User: "Which is better, Delicias Gourmet or Chef Eventos?"
Expected:
  - Compares directly
  - Mentions advantages of each
  - Suggests which based on wedding type
```

### Test Case 4: Planning Mode
```
User: "We're getting married in 8 months, 120 people in Seville, €6000 budget"
Expected:
  - Generates checklist
  - Proposes vendor order
  - Suggests budget by category
```

### Test Case 5: Clarification
```
User: "What does fondant mean?"
Expected:
  - Explains clearly
  - Gives context (wedding cakes)
  - Returns to main topic
```

---

## 7. System Prompts - Current & To Test

### Current (gpt-4o)
```
You are a warm, experienced wedding planning concierge for Spain.
You help couples plan their perfect wedding step by step.
...
```

**Identified Problems:**
- [ ] Sometimes too formal
- [ ] Doesn't always extract context well
- [ ] Responses sometimes too long

**To Improve:**
- [ ] More conversational, less robotic
- [ ] ALWAYS extract city/budget/date
- [ ] Concise responses, max 2-3 paragraphs
- [ ] Always suggest next step

---

## 8. Data to Collect & Track

### Per Conversation
- Duration (# messages)
- Categories searched
- Cities mentioned
- Budget declared
- Confirmed vendor?

### Per Response
- LLM response time
- Relevance (1-5 scale)
- Context extraction accuracy
- User satisfaction signals (follow-up questions vs drop-off)

### Aggregated
- % conversations reaching confirmation
- Intent distribution (search 50%, planning 30%, etc)
- Most searched categories
- Drop-off points (where users get lost)

---

## 9. Planned Iterations

### Iteration 1: Validate Current (Week 1)
- [ ] Test all test cases above
- [ ] Document what works, what doesn't
- [ ] Collect real examples

### Iteration 2: Quick Wins (Week 2)
- [ ] Improve context extraction
- [ ] Shorten responses
- [ ] Improve vendor presentation

### Iteration 3: LLM Tuning (Week 3)
- [ ] A/B test system prompts
- [ ] Adjust function definitions
- [ ] Response formatting optimizations

### Iteration 4: Edge Cases (Week 4)
- [ ] Handle cities without vendors
- [ ] Extreme budgets
- [ ] Out-of-domain questions

---

## 10. Success Metrics

### 🎯 Target
- 80%+ conversation completion (user reaches confirmation)
- <2 sec average LLM response
- 4.5/5 average response relevance
- 70%+ context extraction accuracy

### 📊 How to Measure
- Analytics on each conversation
- Manual response scoring
- User feedback (emojis, comments)
- Conversion: search → confirmation

---

## Notes & Observations

### Initial Observations
- LLM understands vendor categories well
- Location extraction works well
- Needs improvement: follow-ups and clear actions

### Hypotheses to Validate
- Users prefer short searches + quick actions
- Checklists only useful in planning mode (not simple search)
- Vendor images critical for decision

### Known Issues
- [ ] When <4 vendors exist, should show all
- [ ] Doesn't handle "next weekend" well
- [ ] Vendor confirmation doesn't save state well

---

## Next Steps

1. **Now:** Test all questions above, document results
2. **Then:** Identify top 5 highest-impact improvements
3. **After:** Implement + A/B test
4. **Final:** Launch with clear success metrics

---

**Questions/Doubts?** Add them to this doc to iterate.
