# travel-city

AI-powered city travel briefing skill for Claude Code, OpenAI Codex, and OpenClaw.

Given a city name (+ optional season/month + optional origin city), generates a comprehensive travel briefing with live web research via Brave Search.

## Usage

```
/travel-city Taipei                       # City travel briefing
/travel-city Tokyo in March               # Seasonal travel briefing
/travel-city Barcelona from New York      # With flight info + points/miles
```

## What You Get

| Section | Always | Conditional |
|---------|--------|-------------|
| City Overview | Yes | |
| Recent History | Yes | |
| Best Time to Visit | Yes | Tailored if season/month provided |
| Top Neighborhoods & Nearby Cities | Yes | |
| Things to Do | Yes | |
| Popular Events | Yes | Tailored if season/month provided |
| Food & Dining | Yes | |
| Cultural Norms | Yes | |
| Safety & Security | Yes | |
| Getting There | | Only if origin city provided |
| Getting Around | Yes | |
| Confidence Notes | Yes | |

The **Getting There** section includes direct flights, airlines, approximate cash pricing, and points/miles redemption estimates (e.g., "60k United miles RT from JFK").

## Installation

### Claude Code

Copy the skill into your Claude Code skills directory:

```bash
# Global install (available in all projects)
cp -r .claude/skills/travel-city ~/.claude/skills/

# Project-local install (available in this project only)
# Already in place if you cloned this repo
```

### OpenAI Codex

The `agents/openai.yaml` metadata file is included. Copy to your Codex agents directory:

```bash
cp -r .claude/skills/travel-city ~/.agents/skills/travel-city
```

### OpenClaw / ClawHub

Install from ClawHub:

```bash
clawhub install travel-city
```

Or copy manually — the SKILL.md includes OpenClaw metadata in the frontmatter.

## Requirements

- **Brave Search API key**: Set `BRAVE_API_KEY` environment variable
  - Get a key at [brave.com/search/api](https://brave.com/search/api/)
- An AI coding assistant that supports skills (Claude Code, Codex, or OpenClaw)

## Structure

```
.claude/skills/travel-city/
  SKILL.md              # Self-contained skill (all rules, formatting, sources inline)
  agents/
    openai.yaml         # Codex interface metadata
```

## Source Policy

Research is conducted via Brave Search API with the following source priority:

- **Primary**: Official tourism boards, government travel advisories (travel.state.gov)
- **Secondary**: Lonely Planet, The Points Guy, Skyscanner, Google Flights, Numbeo
- **Tertiary**: TripAdvisor, Wikipedia (background facts only)
- **Disallowed**: Reddit, X/Twitter, Facebook, Instagram, TikTok, Quora, personal blogs

## License

MIT
