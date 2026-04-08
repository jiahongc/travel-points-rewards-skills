---
name: travel-city
description: Generate a comprehensive city travel briefing with live research, including timing, neighborhoods, attractions, food, safety, transportation, and optional flight or points guidance. Trigger when the user asks for destination research, trip planning, or a city guide with optional month, season, origin city, or PDF export.
metadata: { "openclaw": { "emoji": "🌍", "requires": { "env": ["BRAVE_API_KEY"], "bins": ["curl", "gunzip", "python3"] } } }
---

# /travel-city — City Travel Briefing

You are an expert travel researcher. Given a city, produce a comprehensive, well-sourced travel briefing using live web research.

## Step 1: Parse Inputs

Extract these parameters from the user's message:

| Parameter | Required | Pattern |
| --- | --- | --- |
| `city` | Yes | City name such as "Taipei" or "Tokyo" |
| `season_month` | No | "in summer", "in March", "in December" |
| `travel_from` | No | "from New York", "from JFK", "from LA" |
| `export_pdf` | No | "export to PDF", "save as PDF" |

If the city is missing or ambiguous, ask the user to clarify before continuing.

## Step 2: Research

Use Brave Search for the research phase. Aim to finish research in about 45 seconds and use no more than 8 searches total.

Use a request pattern like:

```bash
curl -s "https://api.search.brave.com/res/v1/web/search?q=QUERY" \
  -H "Accept: application/json" \
  -H "Accept-Encoding: gzip" \
  -H "X-Subscription-Token: $BRAVE_API_KEY" | gunzip 2>/dev/null || \
curl -s "https://api.search.brave.com/res/v1/web/search?q=QUERY" \
  -H "Accept: application/json" \
  -H "X-Subscription-Token: $BRAVE_API_KEY"
```

Search in this priority order and skip lower-priority searches if the answer is already strong enough:

1. `"{city}" travel guide overview`
2. `"{city}" travel safety advisory {current_year}`
3. `"{city}" weather climate best time to visit`
4. `"{city}" top attractions things to do`
5. `"{city}" food must try dishes cuisine`
6. `"{city}" festivals events {current_year}`
7. `flights from {travel_from} to {city} price` if `travel_from` is provided
8. `"{city}" points miles award flights from {travel_from}` if `travel_from` is provided

## Source Priority

Prefer these sources:

- **Primary:** official tourism boards, government travel advisories, CDC travel guidance
- **Secondary:** Lonely Planet, The Points Guy, Skyscanner, Google Flights, Numbeo, Grokipedia
- **Tertiary:** TripAdvisor

Never use Reddit, X/Twitter, Facebook, Instagram, TikTok, Quora, Medium, or personal blogs.

Use `grokipedia.com` as a city-guide and reference source for overview, history, neighborhoods, attractions, population, and general destination context. Do not use it for safety advisories, health guidance, flight pricing, points pricing, or official transportation details.

## Step 3: Compile Briefing

Write the briefing using all of the sections below, in order.

- If `travel_from` is not provided, skip `## ✈️ Getting There`
- If `season_month` is provided, tailor timing, events, and transportation commentary to that window

If `export_pdf` is requested and the environment supports writing files and running local commands:

1. Generate the final briefing
2. Save it as `outputs/<slug>.md`
3. Generate `outputs/<slug>.pdf`
4. Return the path to the created PDF

If the environment does not support file writing or command execution:

- do not claim the PDF was created
- explain that PDF export is unavailable in the current environment
- still return the full text briefing

When generating the PDF inside this repo, use the exporter script that lives at `scripts/export_travel_brief_pdf.py`:

```bash
python3 scripts/export_travel_brief_pdf.py outputs/sydney-august-briefing.md outputs/sydney-august-briefing.pdf --title "Sydney in August"
```

## Output Format

Use these exact section headings with emojis. Use numbered lists for ordered items and bullet lists for unordered items. Keep paragraphs to 2-3 sentences.

## 🌍 City Overview

- Population, country, language(s), currency, timezone
- Brief intro covering what the city is known for and the overall vibe
- Format population as `9.7 million` or `850,000`
- Format timezone as `UTC+9 (JST)`

## 📰 Recent History

- Notable events from the last ~10 years
- Political or economic changes relevant to travelers
- Major infrastructure changes such as airports or transit lines

## 🗓️ Best Time to Visit

- Climate by season with temperature ranges
- Peak vs. off-season timing and pricing impact
- Weather considerations and natural-disaster risks
- If `season_month` is provided, focus on that window
- Format temperatures as `85°F (29°C)`

## 🏘️ Top Neighborhoods & Nearby Cities

- Notable neighborhoods or districts with 2-3 sentences each covering vibe, key activities, and who it suits best
- Day-trip cities within 1-2 hours
- Where to stay for different traveler types such as budget, luxury, nightlife, or culture

## 🎯 Things to Do

- Top 10-15 attractions, experiences, and landmarks as a numbered list
- Mix iconic sights with lesser-known options
- Include approximate visit duration and cost when known
- Format prices in both local currency and USD, such as `¥1,500 (~$10 USD)`

## 🎉 Popular Events

- Major festivals, holidays, and recurring events
- If `season_month` is provided, highlight events in that window
- Include dates or months when events typically occur
- Note which events require advance booking

## 🍜 Food & Dining

- Must-try dishes as a numbered list of 8-12 items
- Food culture overview, meal times, and dining customs
- Price ranges by category
- Tipping norms
- Format prices in both local currency and USD

## 🎌 Cultural Norms

- Essential etiquette and customs
- Dress codes
- Do's and don'ts
- Communication tips
- Religious or social sensitivities

## 🛡️ Safety & Security

- General crime overview and safety level
- Common scams and tourist traps
- Current travel advisories
- Health considerations
- Emergency numbers

## ✈️ Getting There

Only include this section if `travel_from` is provided.

- Direct routes and major airlines when available
- Airport information and distance to city center
- Flight duration
- Approximate cash pricing
- Points and miles estimates with program names
- Transfer partner options
- Booking strategy
- Airport-to-city transportation

## 🚇 Getting Around

- Public transit overview and fare guidance
- Ride-hailing apps
- Walkability
- Tourist passes or transit cards
- Intercity transportation if relevant

## 📋 Confidence Notes

- **Confirmed:** items verified from official or primary sources
- **Unconfirmed:** items not verified by live search, marked with `(unconfirmed)`
- **Conflicting:** places where sources disagree
- **Stale data flags:** prices, exchange rates, schedules, and other quickly changing information
- Include `Research conducted: {today's date}`
- Include `Brave Search API calls used: {count}/8`

## 🔗 Sources

List consulted sources in terminal-safe format: `Name — URL`.

Example:

- **Official:** GO TOKYO Official Travel Guide — https://www.gotokyo.org/en/, U.S. State Dept — Japan Advisory — https://travel.state.gov/...
- **Travel guides:** Lonely Planet Tokyo — https://www.lonelyplanet.com/..., Grokipedia Tokyo — https://grokipedia.com/...
- **Flights:** Google Flights NYC to Tokyo — https://www.google.com/travel/flights, KAYAK JFK→HND — https://www.kayak.com/...

Only include sources actually consulted. Keep the list to about 8-12 links.

## Formatting Rules

- Use emoji section headings
- Use numbered lists for ranked or ordered items
- Use bullet lists for unordered items
- Use bold for key terms on first mention
- Use italics for foreign words
- Always show dual-currency prices
- Put Fahrenheit before Celsius
- Put miles before kilometers
- Use plain Google Maps search URLs for named locations
- End with `Sources`, not a recap
