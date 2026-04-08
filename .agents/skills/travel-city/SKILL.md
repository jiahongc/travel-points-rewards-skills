---
name: travel-city
version: 1.0.0
description: |
  Given a city name (+ optional season/month + optional origin city), return a
  comprehensive travel briefing. Use when asked to research a city for travel,
  plan a trip, or get destination info.
  Examples: "/travel-city Taipei", "/travel-city Tokyo in March",
  "/travel-city Barcelona from New York"
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - WebSearch
  - WebFetch
  - AskUserQuestion
metadata:
  openclaw:
    emoji: "🌍"
---

# /travel-city — City Travel Briefing

You are an expert travel researcher. Given a city, produce a comprehensive,
well-sourced travel briefing using live web research.

---

## Step 1: Parse Inputs

Extract these parameters from the user's message:

| Parameter       | Required | Pattern                                    |
|-----------------|----------|--------------------------------------------|
| `city`          | Yes      | City name (e.g., "Taipei", "Tokyo")        |
| `season_month`  | No       | "in summer", "in March", "in December"     |
| `travel_from`   | No       | "from New York", "from JFK", "from LA"     |
| `export_pdf`    | No       | "export to PDF", "save as PDF"             |

If `city` is missing or ambiguous, use AskUserQuestion to clarify.

---

## Step 2: Research via Brave Search

Use Brave Search API for all research. Target **~45 seconds total** for the research phase.
Run up to **8 queries** max. Prioritize the most impactful queries first.

```bash
# Template — replace variables before running
curl -s "https://api.search.brave.com/res/v1/web/search?q=QUERY" \
  -H "Accept: application/json" \
  -H "Accept-Encoding: gzip" \
  -H "X-Subscription-Token: $BRAVE_API_KEY" | gunzip 2>/dev/null || \
curl -s "https://api.search.brave.com/res/v1/web/search?q=QUERY" \
  -H "Accept: application/json" \
  -H "X-Subscription-Token: $BRAVE_API_KEY"
```

### Query Plan (run in priority order, skip lower-priority if budget exhausted)

1. `"{city}" travel guide overview` — city basics, intro
2. `"{city}" travel safety advisory {current_year}` — safety, advisories
3. `"{city}" weather climate best time to visit` — seasonal info
4. `"{city}" top attractions things to do` — sightseeing
5. `"{city}" food must try dishes cuisine` — food scene
6. `"{city}" festivals events {current_year}` — events calendar
7. `flights from {travel_from} to {city} price` — only if travel_from provided
8. `"{city}" points miles award flights from {travel_from}` — only if travel_from provided

### Source Priority

**Prefer these sources** (official, authoritative):
- travel.state.gov, gov.uk/foreign-travel-advice — travel advisories
- Official tourism board sites (visitjapan.jp, etc.)
- cdc.gov/travel — health advisories

**Secondary** (reputable travel content):
- lonelyplanet.com, thepointsguy.com, skyscanner.com, google.com/travel
- numbeo.com (cost of living), xe.com (currency), rome2rio.com (transit), grokipedia.com

**Tertiary** (use only when primary/secondary lack coverage):
- tripadvisor.com

**Never use**: Reddit, X/Twitter, Facebook, Instagram, TikTok, Quora, Medium, personal blogs

Use `grokipedia.com` as a secondary city-guide source for overview, history, neighborhoods, attractions, and general destination context. Do not use it for safety advisories, health guidance, flight pricing, points pricing, or official transportation details.

---

## Step 3: Compile Briefing

Write the briefing using **all** of the following sections in order.
If `travel_from` is NOT provided, skip section 10.
If `season_month` IS provided, tailor sections 3, 6, and 10 to that time window.
If `export_pdf` is requested and file writing is available, also save:

1. A markdown copy of the final briefing
2. A PDF generated from that markdown copy

Use clear filenames derived from the city and timing, such as:

- `outputs/sydney-august-briefing.md`
- `outputs/sydney-august-briefing.pdf`

When generating the PDF inside this repo, use:

```bash
python scripts/export_travel_brief_pdf.py outputs/sydney-august-briefing.md outputs/sydney-august-briefing.pdf --title "Sydney in August"
```

### PDF Export Behavior

When the user asks to export as PDF, treat that as an action request, not just a formatting preference.

If the environment supports writing files and running local commands:

1. Generate the final briefing text
2. Save the briefing as `outputs/<slug>.md`
3. Run the PDF exporter to create `outputs/<slug>.pdf`
4. In the final response, include the absolute or project-relative path to the PDF that was created

If the environment does **not** support writing files or running commands:

- Do **not** claim the PDF was created
- Say clearly that PDF export is unavailable in the current environment
- Still provide the full travel briefing in text
- Optionally mention the exporter command the user can run locally

---

### Output Format

Use these exact section headings with emojis. Use numbered lists for ranked/ordered
content. Use bullet lists for unordered content. Keep paragraphs to 2-3 sentences.

---

## 🌍 City Overview

- Population, country, language(s), currency, timezone
- Brief intro — what the city is known for, its character and vibe
- Format population as: `9.7 million` or `850,000`
- Format timezone as: `UTC+9 (JST)`

## 📰 Recent History

- Notable events from the last ~10 years
- Political or economic changes that affect travelers
- Major infrastructure changes (new airports, transit lines, etc.)

## 🗓️ Best Time to Visit

- Climate by season with temperature ranges
- Peak vs. off-season timing and pricing impact
- Weather considerations and natural disaster risks
- If `season_month` provided: focus on that specific window
- Format temperatures as: `85°F (29°C)` (Fahrenheit first)

## 🏘️ Top Neighborhoods & Nearby Cities

- Notable neighborhoods/districts — **2-3 sentences each** covering vibe, key activities, and who it's best for
- Day-trip cities within 1-2 hours
- Where to stay for different traveler types (budget, luxury, nightlife, culture)

## 🎯 Things to Do

- Top 10-15 attractions, experiences, and landmarks (numbered list)
- Mix of iconic must-sees and lesser-known gems
- Include approximate visit duration and cost where known
- Format prices in both local currency and USD: `¥1,500 (~$10 USD)`

## 🎉 Popular Events

- Major festivals, holidays, and recurring events
- If `season_month` provided: highlight events in that window
- Include dates/months when events typically occur
- Note which events require advance booking

## 🍜 Food & Dining

- Must-try dishes (numbered list, 8-12 items)
- Food culture overview — meal times, dining customs
- Price ranges by category: street food, casual, mid-range, fine dining
- Tipping norms
- Format prices in both local currency and USD

## 🎌 Cultural Norms

- Essential etiquette and customs
- Dress codes (temples, restaurants, business)
- Do's and don'ts
- Communication tips (common phrases, language barriers)
- Religious or social sensitivities

## 🛡️ Safety & Security

- General crime overview and safety level
- Common scams and tourist traps to watch for
- Current travel advisories (cite travel.state.gov or equivalent)
- Health considerations (vaccines, water safety, air quality)
- Emergency numbers

## ✈️ Getting There

**Only include this section if `travel_from` is provided.**

- Direct flight routes and major airlines serving them
- Airport info (name, code, distance to city center)
- Flight duration
- Approximate cash pricing (economy, round trip): `$800–$1,200 RT`
- Points/miles estimates with program names: `60k–80k United MileagePlus miles RT`
- Transfer partner options: `transferable from Chase UR, Amex MR`
- Best booking strategies and when to book
- Airport-to-city transportation options

## 🚇 Getting Around

- Public transit overview (metro, bus, rail) with fare info
- Ride-hailing apps available (Uber, local alternatives)
- Walkability assessment
- Tourist passes or transit cards worth buying
- Intercity transportation if relevant

## 📋 Confidence Notes

Flag data freshness and uncertainty:

- **Confirmed**: Items verified from official/primary sources during this research
- **Unconfirmed**: Items from training data not verified by live search (mark with `(unconfirmed)`)
- **Conflicting**: Items where sources disagreed — note the discrepancy
- **Stale data flags**: Note any data that may change rapidly (prices, exchange rates, political situations)
- Include the date of research: `Research conducted: {today's date}`
- Include: `Brave Search API calls used: {count}/8`

## 🔗 Sources

List key sources used during research in terminal-safe format: `Name — URL`.
Do not rely on Markdown named hyperlinks because some terminals do not render them.
Group by category. Example:

- **Official:** GO TOKYO Official Travel Guide — https://www.gotokyo.org/en/, U.S. State Dept — Japan Advisory — https://travel.state.gov/...
- **Travel guides:** Lonely Planet Tokyo — https://www.lonelyplanet.com/..., The Points Guy — Japan Miles — https://thepointsguy.com/...
- **Reference:** Grokipedia Tokyo — https://grokipedia.com/...
- **Flights:** Expedia JFK→NRT — https://www.expedia.com/..., KAYAK JFK→NRT — https://www.kayak.com/...

Only include sources that were actually consulted. Keep to ~8-12 links max.

---

## Formatting Rules

- **Emoji section headings**: Every H2 uses a relevant emoji prefix
- **Numbered lists**: For ranked/ordered items (top attractions, must-try dishes)
- **Bullet lists**: For unordered items (cultural norms, safety tips)
- **Bold key terms** on first mention: **Shinkansen** (bullet train)
- **Italics for foreign words**: *izakaya* (casual bar)
- **Prices**: Always dual currency — `¥1,500 (~$10 USD)`
- **Temperatures**: Fahrenheit first — `85°F (29°C)`
- **Distances**: Miles first with km — `15 miles (24 km)`
- **Flight durations**: `14h 30m`
- **Flight prices**: Ranges with RT — `$800–$1,200 RT`
- **Points/miles**: Program name + amount — `60k–80k United MileagePlus miles RT`
- **Time-sensitive data**: Mark with `(as of Month YYYY)`
- **Paragraphs**: 2-3 sentences max
- **Google Maps URLs**: For every named location, include a plain Google Maps search URL in terminal-safe format: `Sensō-ji Temple — https://www.google.com/maps/search/Sensoji+Temple+Tokyo+Japan`. Use `+` for spaces in the URL.
- **No trailing summary**: End with Sources section, not a recap
