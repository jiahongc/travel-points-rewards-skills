# Travel Points & Rewards Skills

Travel Points & Rewards Skills turns your AI coding agent into a travel research assistant you can query on demand.

It currently includes two destination-briefing skills for **Claude Code**, **Codex**, **Open Claude**, and **OpenClaw / ClawHub**:

- `/travel-city` for English output
- `/travel-city-chinese` for Simplified Chinese output with paired Chinese + English place and food names

Both skills cover destination overview, timing, neighborhoods, food, safety, transportation, and optional flight / points context.

### Without Travel Points & Rewards Skills

- You ask for a city guide and get a generic answer based on stale model knowledge
- Flight and points guidance is vague or missing
- Seasonal advice is not tied to your actual month of travel
- Safety and transit details are inconsistent
- You end up manually turning a chat response into something printable

### With Travel Points & Rewards Skills

| Skill | Language | What it does |
| --- | --- | --- |
| `/travel-city` | English | Full city briefing with live research: overview, weather timing, neighborhoods, attractions, events, food, norms, safety, transport, and optional flight / points guidance |
| `/travel-city-chinese` | Simplified Chinese | Chinese-first city briefing for Chinese readers, with paired Chinese + English names for places, foods, and transit terms, plus both U.S. and Chinese passport visa guidance by default |

## Demo

English:

```text
/travel-city Sydney in August from New York
```

Chinese:

```text
/travel-city-chinese Bergen in May from New York
```

Typical output includes:

- City overview
- Recent history
- Best time to visit
- Top neighborhoods and nearby cities
- Things to do
- Popular events
- Food and dining
- Cultural norms
- Safety and security
- Getting around
- First-time traveler tips
- Confidence notes
- Getting there, when an origin city is provided

## Who This Is For

This repo is for travelers, points users, and trip planners who want better destination research than a generic chat answer.

It is not meant to be a casual “top 10 things to do” prompt. The skills are designed as research workflows: they use live search, prioritize primary sources, separate confirmed from unconfirmed information, and produce output that is easier to save, review, and share.

* * *

## Install

Requirements: Git and any agent that supports skill-style prompts. The repo currently supports **Claude Code**, **Codex**, **Open Claude**, and **OpenClaw / ClawHub**.

### Claude Code

```bash
mkdir -p ~/.claude/skills
cp -R .claude/skills/travel-city ~/.claude/skills/travel-city
cp -R .claude/skills/travel-city-chinese ~/.claude/skills/travel-city-chinese
```

### Codex

```bash
mkdir -p ~/.codex/skills
cp -R .agents/skills/travel-city ~/.codex/skills/travel-city
cp -R .agents/skills/travel-city-chinese ~/.codex/skills/travel-city-chinese
```

### Open Claude

```bash
mkdir -p ~/.agents/skills
cp -R .agents/skills/travel-city ~/.agents/skills/travel-city
cp -R .agents/skills/travel-city-chinese ~/.agents/skills/travel-city-chinese
```

### OpenClaw / ClawHub

If your client is already pointed at this repository, you can use the checked-in skill directories directly:

- `clawhub/travel-city`
- `clawhub/travel-city-chinese`

Repository layout:

```text
.claude/skills/travel-city/
  SKILL.md

.claude/skills/travel-city-chinese/
  SKILL.md

.agents/skills/travel-city/
  SKILL.md

.agents/skills/travel-city-chinese/
  SKILL.md

clawhub/travel-city/
  SKILL.md

clawhub/travel-city-chinese/
  SKILL.md
```

Use:

- `.claude/skills/...` for Claude Code
- `.agents/skills/...` for Codex and Open Claude
- `clawhub/...` for OpenClaw / ClawHub packaging

Notes:

- `.agents` is a tool convention used by Codex-style agent clients, not a universal standard
- Claude Code does not use `agents/openai.yaml` in this repo

* * *

## Setup

For live research, set a Brave Search API key:

```bash
export BRAVE_API_KEY=your_key_here
```

Get a key at [brave.com/search/api](https://brave.com/search/api/).

You need:

- network access for Brave Search
- Python 3 if your client or workflow needs it for other tooling

* * *

## Output Style Differences

### `/travel-city`

- English output
- U.S.-passport-first framing unless the user specifies another nationality
- Standard English travel-guide naming

### `/travel-city-chinese`

- Simplified Chinese output
- Default visa guidance for both U.S. and Chinese passports when relevant
- Chinese-first naming with paired English / local names on first mention, such as `卑尔根（Bergen）`
- Better fit for Chinese travel-planning tone and Chinese-platform source supplementation

* * *

## Source Policy

Both skills prioritize:

- **Primary:** official tourism boards, government travel advisories, immigration / visa pages, CDC travel guidance
- **Secondary:** Lonely Planet, The Points Guy, Skyscanner, Google Flights, Trip.com / 携程, 马蜂窝, 穷游, 飞猪, 航旅纵横, Numbeo, Rome2Rio, XE, Grokipedia
- **Tertiary:** TripAdvisor, Wikipedia

Both skills explicitly avoid Reddit, X/Twitter, Facebook, Instagram, TikTok, Quora, Medium, and personal blogs.

Grokipedia is intended as a city-guide / reference source for destination context, but not for safety advisories, live pricing, or official transport details.

When platform summaries conflict with official immigration or safety guidance, official sources win.

* * *

## Roadmap-Friendly Notes

This repo is intentionally laid out so more travel and points skills can be added later without changing the install story.

- Keep `.claude/skills/...`, `.agents/skills/...`, and `clawhub/...` aligned by capability
- Keep each skill self-contained in its own directory
- Treat `SKILL.md` as the canonical behavior spec
- Keep examples and install commands in the README in sync with the actual shipped directories

## License

MIT
