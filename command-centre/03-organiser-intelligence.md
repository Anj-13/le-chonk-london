# 03 — Organiser & Sponsor Intelligence

**Verified 2026-11-05** via research agent (30 sources fetched). Labels: Verified / Strong inference / Hypothesis.

## Vultr — what they want from this event
- **Positioning:** "enterprise agentic AI infrastructure" — Vultr Cloud Alliance + VAST Data partnership; **VX1 Cloud Compute** (launched Oct 21, 2025) promoted as "foundation for agentic AI infrastructure". [Verified: businesswire, blogs.vultr.com/vx1-cloud-compute]
- **They already ran the dress rehearsal:** **Agent Arena Hackathon, Cerebral Valley SF, Oct 2026** (Vultr's own). Winners — [Verified: blogs.vultr.com/agent-arena-hackathon-cerebral-valley-2026]:
  1. **Nusa** — rewrites inference kernels, runs in **"a throwaway microVM with no network"**, used Serverless Inference + VX1 → **the containment story won Vultr's own event**
  2. **Skeleton Key** — websites→APIs for agents; "Vultr is the entire control plane" (Cloud Compute, VPC, Serverless Inference, Container Registry, Object Storage)
  3. **RL Forge** — papers→RL environments, sandbox execution + reward verification
- Vultr's own takeaway: they value **"the agents themselves, and the infrastructure supporting them."** [Verified quote]
- **Strong inference:** Agent Rush = scaled-down, public-facing repeat of Agent Arena. Build what wins Agent Arena: infra-deep, real utility, *visible full-stack Vultr usage*, containment as a first-class feature.
- **Hypothesis:** no official Vultr MCP server exists (community requested one; none found) — an MCP-style surface is novel but unsupported by Vultr.

## lablab.ai — what they want
- Platform business: they want complete, presentable submissions on their platform (video, slides, repo, URL), active Discord, smooth events. [Verified: submission checklist + rules]
- Judging defaults to 4×1–5 criteria; events can override; community votes exist but **don't decide prizes** (Band of Agents: 147-vote favourite didn't win). [Verified]

## Strategic implications
1. **Make Vultr infrastructure the hero of the demo** — VM as control plane, Serverless Inference for all reasoning, Vultr API spawning/destroying throwaway instances on camera, optionally Object Storage for artifacts. Past Vultr winners showcased the full stack. [Strong inference]
2. **Containment is the theme Vultr chose** — the winning Agent Arena project was literally "sandbox with no network". Our Airlock receipt/lifecycle concept is squarely on-thesis; the differentiator must be *product polish + business framing* (Nusa was deep-infra; Agent Rush asks for a web product).
3. **The $200 credits + $5 VM** are enough: one VM hosts per-task containers; a throwaway instance via Vultr API is a demo garnish (60–120 s provisioning → too slow per tool call). [Strong inference, vpsbenchmarks]
