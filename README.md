# Travel Points & Rewards Skills

Travel Points & Rewards Skills turns your AI coding agent into a travel research assistant you can query on demand.

It currently includes one travel briefing skill for **Claude Code**, **Codex**, and **Open Claude**, with the repo structured to grow into a larger multi-skill suite over time. The current skill covers destination overview, timing, neighborhoods, food, safety, transportation, and flight/points context, and it can export the final result to a shareable PDF.

### Without Travel Points & Rewards Skills

- You ask for a city guide and get a generic answer based on stale model knowledge
- Flight and points guidance is vague or missing
- Seasonal advice is not tied to your actual month of travel
- Safety and transit details are inconsistent
- You end up manually turning a chat response into something printable

### With Travel Points & Rewards Skills

| Skill | What it does |
| --- | --- |
| `/travel-city` | Full city briefing with live research: overview, weather timing, neighborhoods, attractions, events, food, norms, safety, transport, and optional flight/points guidance |

## Demo

Start with the main skill:

```text
/travel-city Sydney in August from New York
```

Or ask for a shareable version:

```text
/travel-city Sydney in August from New York and export to PDF
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
- Confidence notes
- Getting there, when an origin city is provided

## Who This Is For

This repo is for travelers, points users, and trip planners who want better destination research than a generic chat answer.

It is not meant to be a casual “top 10 things to do” prompt. The skill is designed as a research workflow: it uses live search, prioritizes primary sources, separates confirmed from unconfirmed information, and produces output that is easier to save, review, and share.

* * *

## Install

Requirements: Git and any agent that supports skill-style prompts. The repo currently supports **Claude Code**, **Codex**, and **Open Claude** directly.

### Claude Code

```bash
mkdir -p ~/.claude/skills
cp -R .claude/skills/travel-city ~/.claude/skills/travel-city
```

### Codex

```bash
mkdir -p ~/.codex/skills
cp -R .agents/skills/travel-city ~/.codex/skills/travel-city
```

### Open Claude

```bash
mkdir -p ~/.agents/skills
cp -R .agents/skills/travel-city ~/.agents/skills/travel-city
```

If your client is already pointed at this repository, you can also use the checked-in skill directories directly instead of copying them elsewhere.

Repository layout:

```text
.claude/skills/travel-city/
  SKILL.md

.agents/skills/travel-city/
  SKILL.md
  agents/openai.yaml
```

Use:

- `.claude/skills/travel-city` for Claude Code
- `.agents/skills/travel-city` for Codex and Open Claude

Notes:

- `agents/openai.yaml` is only client metadata for Codex-style tools
- Claude Code does not need that file
- `.agents` is a tool convention used by Codex-style agent clients, not a universal standard

* * *

## Setup

For live research, set a Brave Search API key:

```bash
export BRAVE_API_KEY=your_key_here
```

Get a key at [brave.com/search/api](https://brave.com/search/api/).

Optional, for PDF export:

```bash
python3 -m pip install reportlab
```

You need:

- network access for Brave Search
- Python 3 for PDF export
- `reportlab` for PDF export

* * *

## PDF Export

This repo includes a styled PDF exporter at [scripts/export_travel_brief_pdf.py](/Users/jiahongchen/Desktop/Coding/travel-points-rewards/scripts/export_travel_brief_pdf.py).

It converts a saved briefing into a clean PDF with:

- a cover page
- strong section headers
- readable print-oriented typography
- numbered pages
- support for the skill's heading and list structure

Example:

```bash
mkdir -p outputs
python3 scripts/export_travel_brief_pdf.py outputs/sydney-august-briefing.md outputs/sydney-august-briefing.pdf --title "Sydney in August"
```

Recommended workflow:

1. Run `/travel-city ...`
2. Save the final briefing as `outputs/<slug>.md`
3. Export it to `outputs/<slug>.pdf`

* * *

## Terminal Compatibility

The skill is written to work in plain terminals, not just rich chat UIs.

- It prefers plain URLs over Markdown named hyperlinks
- This matters most in Claude Code in a normal terminal
- The same output still works fine in clients that do support rich links

* * *

## Source Policy

The skill prioritizes:

- **Primary:** official tourism boards, government travel advisories, CDC travel guidance
- **Secondary:** Lonely Planet, The Points Guy, Skyscanner, Google Flights, Numbeo, Grokipedia
- **Tertiary:** TripAdvisor

It explicitly avoids Reddit, X/Twitter, Facebook, Instagram, TikTok, Quora, Medium, and personal blogs.

Grokipedia is intended as a city-guide/reference source for destination context, but not for safety advisories, live pricing, or official transport details.

* * *

## Roadmap-Friendly Notes

This repo is intentionally laid out so more travel and points skills can be added later without changing the install story.

- Keep `.claude/skills/...` and `.agents/skills/...` in sync
- Keep each skill self-contained in its own directory
- Treat `SKILL.md` as the canonical behavior spec
- Use `agents/openai.yaml` for Codex-compatible metadata

## License

MIT
