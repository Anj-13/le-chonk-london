# 04 — Sponsor Stack & Tracks

**Last verified: 2026-11-20.** One open track: build with Mistral. No separate tracks
are published. A Vibe side award is possible (see 02, check-in question 5).

## Mistral stack: what we use and why
| Product | Role in ChonkVid | Why it is load-bearing |
|---|---|---|
| **Ministral** (small, cheap, fast) | the agent population (30–60 agents) | hundreds of parallel calls in one day is only affordable on a small model |
| **mistral-embed** | infection detection (paraphrase-resistant) and variant lineages | string matching misses paraphrased copies; embeddings catch them |
| **Le Chonk** (flagship) | the "WHO" agent: situation reports, variant naming, vaccine prompt synthesis | the event's namesake model on stage doing the reasoning step |
| **Mistral Vibe** (agentic coding CLI) | our build tool for the day | costs nothing, on-brand, worth one line in the pitch |
| La Plateforme console | API keys, rate limits, credits | event credits via a link on the day; real limits unknown until checked |

Model IDs and the exact Le Chonk API name: confirm on console.mistral.ai at 08:30. Do
not hard-code from memory.

## Budget reality (the real feasibility gate)
- Event-credit rate limits may not support 30–60 live agents. Check the console at 08:30.
- Estimate before the event: agents × ticks × runs = calls. Example: 40 agents × 10
  ticks × 3 runs ≈ 1,200 chat calls + the same number of embeddings.
- Measure transmission with cheap one-hop trials (see 10) rather than many full
  epidemics.
- **Every attendee gets free API credits**; the access link is shared on the day
  (acceptance email). Ask the mentors about the rate limits on those credits.

## Crowd lanes to avoid (expected at a Mistral one-day)
Mistralverse clones (civilisation sims), Le Chonk chat personas, vibe-coding toys,
voice agents, RAG assistants, "agent startup" theatre, guardrail scanners, canary/DLP
tools. In a 980-analogue competitor scrape, epidemic simulation had 1 off-topic hit,
guardrails 69, canary/DLP 86.
