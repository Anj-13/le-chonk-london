# 04 — Sponsor & Track Map ("Blast Radius Zero")

**Last verified: 2026-11-05.** Single main challenge, two sanctioned agent patterns. No separate tracks/prizes beyond 1st/2nd/3rd.

## The challenge, distilled
> Web-based agent that does real work, "every action contained in a sandbox on Vultr." "Containment-first is required." An agent that only chats is a demo; one that executes safely is a product.

## Required stack (all mandatory unless marked)
| Layer | Requirement | Notes |
|---|---|---|
| Compute/control | **Vultr VM** as "central control and orchestration system" | Backend runs here; app + sandbox orchestrator |
| LLM | **Vultr Serverless Inference for ALL LLM calls** | OpenAI-compatible, base URL `api.vultrinference.com/v1`, vision-capable models available. No other LLM API for agent reasoning. No Vultr GPUs in this event |
| Sandbox | Containers or throwaway Vultr instances — "never inside the app process" | **Docker strongly recommended**; OpenSandbox, gVisor, E2B suggested |
| Vultr API | Optional: spin up + destroy a throwaway instance per task | Strong differentiator if used (lifecycle discipline) |

## Pattern A — Sandboxed code execution (official example ideas)
1. **CSV Analyst** — upload spreadsheet, plain-English questions, executed chart + code
2. **Prove-It Code Reviewer** — run snippet/PR + tests in sandbox, report what happened
3. **Chart Anything** — NL in, executed matplotlib/plotly image out
4. **File Fixer** — messy CSV/JSON in, cleaned file out, executed before/after diff
5. **Self-Healing Runner** — run code, read errors, patch & retry, retry loop visible on screen

## Pattern B — Sandboxed browser use (official example ideas)
1. **Comparison Shopper** — product URLs in, screenshot-backed comparison table out
2. **Form Filler** — multi-step web form filled, screenshot trail, approve-before-submit gate
3. **Site QA Sweep** — find broken flows/links, screenshots + repro steps
4. **Research with Receipts** — every claim links to a screenshot of its source
5. **Page Watcher** — monitor listing/pricing pages, structured data, day-over-day diff

⚠️ These are *organiser-suggested ideas* — expect many teams to build them verbatim. Originality criterion punishes copies. Strategy: keep the sanctioned pattern's bones, add a differentiated product angle + a killer containment story.

## Containment focus areas (judges will probe these)
1. **Process isolation** — execution never touches host or app runtime
2. **Secret hygiene** — no keys/credentials inside the sandbox
3. **Resource limits** — time + memory caps per run
4. **Lifecycle discipline** — reset/destroy environments after each task

## Demo video must include
- **"One containment moment"** — e.g., sandbox absorbing `rm -rf`, an infinite loop, or a hostile web page

## Sponsor opportunity assessment
| Angle | Verified? | Strategic value |
|---|---|---|
| Vultr wants a public showcase of its full agent stack (VM + Serverless Inference + API-driven lifecycle) | Strong inference (X post: "Almost nobody's building the box they act inside") | HIGH — make Vultr infrastructure the hero of the demo |
| Vultr wants developer-adoption content (README, architecture docs) | Verified (README documentation required) | MEDIUM — clean docs double as marketing |
| lablab wants smooth, complete submissions (video+slides+URL+repo) | Verified (submission checklist) | MEDIUM — completeness is a scored gate, not an extra |
