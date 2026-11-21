# 13 — Submission & Demo QA

**Created 2026-11-20 night.** The submission format is UNKNOWN until check-in (02,
question 2). Prepare everything below anyway; it covers any likely format.

## Pitch copy (paste-ready)
- **Title:** ChonkVid
- **Tagline:** Flatten the curve of prompt injection.
- **One-liner:** We release a harmless self-spreading prompt into a population of
  Ministral agents, measure how fast it spreads, and show that targeted vaccination
  stops it, with a vaccine prompt written by Le Chonk.
- **Problem:** Agents now read each other's output. One compromised agent can spread a
  payload across a fleet, and teams shipping fleets have no numbers for how fast or
  which defence works.
- **What we measured:** per-contact spread probability (with CI), R0, attack rate under
  no intervention vs random vs targeted vaccination at the same dose.
- **Built with:** Ministral (population), mistral-embed (infection detection, variant
  lineages), Le Chonk (WHO agent and vaccine prompt), Mistral Vibe (build tool).
- **Prior work:** extends Morris II (Cohen et al., 2024) and Agent Smith (Gu et al.,
  2024) from "spread happens" to "here is what stops it".
- **Safety:** harmless chain-letter payload, sim-local agents, no real users or
  platforms.

## Pre-pitch QA (run at 17:30)
- [ ] Backup recording plays offline, full screen, with sound off
- [ ] Live run starts from one command or button in under 10 seconds
- [ ] Numbers strip shows real values from today's runs (no placeholders)
- [ ] Each number has a sample size next to it
- [ ] No "provably" or "minimal" wording anywhere on screen
- [ ] API key not visible on screen or in the repo
- [ ] Laptop on power, notifications off, screen mirroring tested if possible
- [ ] Pitch timed at 90 seconds, twice
- [ ] Q&A answers from 07 rehearsed by whoever takes questions

## If submission needs a repo
- [ ] README: what it is, how to run (mock mode and live), measured results table
- [ ] Clear first commit after 08:30 on 21 Nov (shows code written at the event)
- [ ] `.env.example` without real keys
