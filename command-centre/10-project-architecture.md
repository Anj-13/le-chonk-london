# 10 — Project Architecture & Execution Plan: "ChonkVid" (primary concept)

**Created 2026-11-20 night, before the one-day build (Sat 21 Nov, 08:30-20:30 GMT,
Fora - Chancery House, London). Design only: no code written before the event
(Mistral published no pre-built-code rules; code happens at the venue).**

## One-liner

**ChonkVid: release a self-spreading prompt virus into a town of Mistral agents
doing real work, measure its R0 live, then beat it with the public-health playbook,
ending on the computed minimal hardening set and a Le Chonk-synthesised vaccine patch.**

## Scope

- **Must-have:** contact-network world (N=40-80 Ministral agents: 8-12 household
  cliques + 3-4 workplace hubs + 1 group-chat venue as the super-spreader); message
  loop through real Mistral calls; infection detected by mistral-embed similarity of
  outgoing messages against the payload reference set (paraphrase-resistant); S/E/I/R
  state machine per agent; append-only epidemic log (JSONL); live dashboard (network
  graph, S/E/I/R curves, R_t line, conversation ticker); intervention panel (masks =
  output-filter probability, quarantine positives, lockdown = cut inter-household
  edges, vaccination coverage); herd-immunity targeting (computed minimal hardening
  set); numbers strip as a first-class output (R0 with bootstrap CI over transmission
  chains, one intervention ablation, one vaccination dose-response sweep).
- **Winning feature:** the WHO agent on Le Chonk: reads the epidemic log each K
  ticks, publishes situation reports, names variants, synthesises the vaccine
  system-prompt patch from collected infection samples; final frame is the
  merge-ready vaccine diff deployed behind a human approval click.
- **Stretch (only after the 16:00 gate passes):** calibrated 50k-agent city mode
  (pure computation, no API); scam payload as a second attack mode.
- **Explicitly excluded:** auth, settings pages, persistence, multiple venues,
  fine-tuning, any real-money or real-platform integration.

## Architecture (one laptop, free-tier Mistral APIs)

```
Dashboard (React + canvas/SVG, WebSocket-fed)
   │ live: world graph (node color = state), curves + R_t + herd-immunity
   │ marker, conversation ticker, variant phylogeny, WHO feed, numbers strip
   ▼
FastAPI sim core (Python, asyncio)
   ├─▶ World: NetworkX graph; per tick, sample contacts along edges;
   │     venue ticks reach many agents at once (super-spreader moment)
   ├─▶ Agent runtime: persona + GAIA task assignment + short memory;
   │     brain: Ministral 8B (batched, parallel);
   │     infection = payload instructions carried in its own outgoing message
   │     (models genuinely decide to propagate; no scripted coloring)
   ├─▶ Detection: mistral-embed similarity vs payload reference set,
   │     threshold exposed as a tuning knob; every verdict logged
   ├─▶ WHO agent (Le Chonk): situation reports, R_t estimate, variant naming
   │     (embed lineage clustering = phylogeny), vaccine synthesis
   ├─▶ Interventions: masks / quarantine / lockdown / vaccination;
   │     herd-immunity targeting = high-betweenness separator hardening set
   └─▶ Epidemic log: append-only JSONL (contacts, messages, infection verdicts,
         lineages, interventions, transitions) = WHO input + eval data + audit trail

Mock mode: identical loop on a scripted stub "model" (deterministic, tunable
infectivity) behind one flag — develop with zero API burn and tune dynamics
before spending a single real call.
```

- **API budget:** lab run ≈ 1-2k chat calls + embeddings (N=40 × ~10 ticks); mock
  mode costs zero; city mode is pure local computation; the full demo gets
  pre-recorded once as the live-stage safety copy.
- **Measurement is the product:** R0 via branching-process estimate over
  transmission chains with bootstrap CI; ablation = each intervention off/on;
  dose-response = coverage sweep 0→100% attack-rate curve. Numbers on screen
  before the animation.

## Schedule (Sat 21 Nov, UK time; pitches from ~18:00)

| When | Gate | Output |
|---|---|---|
| 08:30-09:15 | doors, team, repo, API keys, topology + mock-loop skeleton | stub agents talking on mock mode |
| 09:15-10:30 | mock-mode full loop: states, transmission, log, curves | dashboard skeleton fed by mocked events (frontend person parallel) |
| 10:30-12:00 | flip to real Ministral calls + embed detection; tune infectivity at N=40 | real infection spreads at a usable rate |
| 12:00-13:00 | lunch (provided); keep a lab run cooking in background | first measured R0 draft |
| 13:00-14:30 | interventions + herd-immunity targeting | sliders bend the curve; hardening set computed |
| 14:30-16:00 | WHO agent + variant phylogeny + vaccine synthesis | live situation reports; diff generated |
| 16:00-17:30 | **GATE: city mode timeboxed — if flaky, CUT.** Pre-record the full backup run; freeze scope | recorded backup + frozen demo |
| 17:30-18:00 | rehearse the 90-second demo twice; polish the final frame | pitch-ready |
| 18:00-20:30 | pitches + Q&A | done |

**Team split (4):** A) sim core, world, log; B) LLM layer, detection, variants;
C) dashboard; D) WHO agent, intervention math, demo script + recording. With 3:
A+B merge, C+D merge.

**Pivot rule (pre-decided):** if the epidemic dynamics are unstable by ~13:00,
pivot to Plan B (functional-redundancy failover: the flagship "dies" mid-demo and
the fleet degrades to pre-qualified small-model cover with measured fidelity
floors). Reused unchanged: population, probe streams, dashboard, log. Plan B is
the safer, more deterministic build; the case for it is recorded in
FUNNEL-FINAL-VERDICT.md, not buried.

## Risks

| Risk | L | I | Mitigation |
|---|---|---|---|
| Infection dynamics too hot or too cold | M | H | tune payload wording + susceptibility in mock mode first; seed multiple patient zeros; recorded backup |
| API latency / rate limits at N=40+ | M | M | batch + parallel + backoff; small N on stage; pre-recorded full run as safety copy |
| Toy-risk verdict from judges | M | H | lead with measured numbers (R0 ± CI, ablation, dose-response) before the animation |
| Embed threshold misfires (false infections) | M | M | threshold knob + visible confirmation in the ticker; everything logged |
| WHO agent latency mid-demo | M | M | pre-generate one situation report; live-generate only the vaccine |
| Registration still pending at doors | L | H | check ticket tonight; if pending, talk to hosts at check-in citing the NVIDIA Hack for Impact win |
