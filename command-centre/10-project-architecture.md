# 10 — Project Architecture & Execution Plan: "ChonkVid" (primary concept)

**Created 2026-11-20 night, before the one-day build (Sat 21 Nov, 08:30-20:30 GMT,
Fora - Chancery House, London). Design only: no code written before the event
(Mistral published no pre-built-code rules; code happens at the venue).**
**Revised 2026-11-21 01:00:** the night's corrections are folded into the body below;
this page is the build spec and overrides HACKATHON.md and DECISION-BRIEF.md on scope.

## One-liner

**ChonkVid: release a harmless self-spreading prompt into a population of Ministral
agents, measure its spread probability and R0 live, then show that targeted hardening
beats random hardening at the same dose, ending on a Le Chonk-synthesised vaccine patch.**

## Why the scope looks like this (corrections, 20 Nov night)

1. **Scope cut.** Core only: contact network + real Ministral transmission + SEIR
   curve + targeted-vs-random vaccination at equal dose + Le Chonk WHO vaccine
   prompt. **Cut:** GAIA tasks, AgentDojo, city mode, masks, lockdown, boosters.
   Phylogeny only if everything else is done by 16:00.
2. **Measure with one-hop trials, not repeated epidemics.** Give an agent the payload
   and check whether its next message carries it; repeat n times. That gives a
   binomial spread probability with CI; R0 = probability × mean contacts. Cheap, and
   it makes the "dynamics roulette" the measurement itself.
3. **Detect infection against the parent message**, not patient zero's payload, so
   mutated variants are not miscounted as recovered.
4. **No "provably minimal hardening set".** Optimal immunisation is NP-hard in
   general. Use greedy targeting (degree / betweenness / ring) and show it beats
   random vaccination at the same dose.
5. **Budget first.** Read the real rate limits on the console before sizing N.

## Scope

- **Must-have:** contact-network world (N=30-60 Ministral agents, sized from the real
  rate limits: household cliques + a few workplace hubs + 1 group-chat venue as the
  super-spreader); message loop through real Mistral calls; infection detected by
  mistral-embed similarity of each outgoing message against its parent message
  (paraphrase-resistant, threshold exposed and logged); S/E/I/R state machine per
  agent; append-only epidemic log (JSONL); live dashboard (network graph, S/E/I/R
  curves, conversation ticker); one-hop trial harness (spread probability with
  binomial CI, R0); vaccination = a hardened system prompt on chosen agents, compared
  at equal dose: random vs greedy targeted (degree / betweenness); numbers strip as a
  first-class output.
- **Winning feature:** the WHO agent on Le Chonk: reads the epidemic log every K
  ticks, publishes situation reports, and synthesises the vaccine system-prompt patch
  from collected infection samples; its patch is then re-measured with one-hop trials.
  Final frame: the vaccine diff plus the guidance table.
- **Stretch (only after the 16:00 gate passes):** variant phylogeny from embedding
  lineages; quarantine of detected positives as a second intervention.
- **Explicitly excluded:** GAIA/AgentDojo task layers, city mode, masks, lockdown,
  boosters, auth, settings pages, persistence, multiple venues, fine-tuning, any
  real-money or real-platform integration.

## Architecture (one laptop, Mistral APIs)

```
Dashboard (React or plain HTML + canvas/SVG, WebSocket-fed)
   │ live: world graph (node color = state), S/E/I/R curves,
   │ conversation ticker, WHO feed, numbers strip
   ▼
FastAPI sim core (Python, asyncio)
   ├─▶ World: NetworkX graph; per tick, sample contacts along edges;
   │     venue ticks reach many agents at once (super-spreader moment)
   ├─▶ Agent runtime: persona + short memory; brain: Ministral (batched,
   │     parallel, backoff); infection = payload instructions carried in
   │     its own outgoing message (models decide to propagate; no scripted coloring)
   ├─▶ Detection: mistral-embed similarity vs the parent message,
   │     threshold as a tuning knob; every verdict logged
   ├─▶ Trials: one-hop harness → spread probability ± CI, R0
   ├─▶ Vaccination: hardened system prompt on k agents;
   │     random vs greedy targeted (degree / betweenness) at equal k
   ├─▶ WHO agent (Le Chonk): situation reports, vaccine prompt synthesis
   └─▶ Epidemic log: append-only JSONL (contacts, messages, verdicts,
         interventions, transitions) = WHO input + eval data + audit trail

Mock mode: identical loop on a scripted stub "model" (deterministic, tunable
infectivity) behind one flag — develop with zero API burn and tune dynamics
before spending a single real call.
```

- **API budget:** compute from the console limits first (see 04). Rough guide:
  one-hop trials ≈ 3 conditions × n=50 ≈ 150 chat calls + embeddings; one live
  epidemic ≈ N × ~10 ticks; the full demo gets pre-recorded once as the stage copy.
- **Measurement is the product:** spread probability with binomial CI from one-hop
  trials; R0 = probability × mean contacts; attack rate under no intervention vs
  random vs targeted at the same dose; the WHO vaccine re-measured the same way.
  Numbers on screen before the animation.

## Schedule (Sat 21 Nov, UK time; pitches from ~18:00)

Matches the gates in 11.

| When | Gate | Output |
|---|---|---|
| 08:30-09:15 | doors, team, repo, API keys, check-in questions (02) | fresh repo; stub agents talking on mock mode |
| 09:15-10:30 | mock-mode full loop: network, states, log, curve | dashboard skeleton fed by mocked events (frontend person parallel) |
| 10:30-12:00 | real Ministral calls + embed detection; one-hop trials running | first measured spread probability |
| 12:00-13:00 | lunch (provided); **pivot check** | stay or pivot (rule below) |
| 13:00-14:30 | vaccination: targeted vs random at equal dose | attack-rate comparison with n |
| 14:30-16:00 | WHO agent (Le Chonk) + vaccine prompt, re-measured | live situation reports; vaccine diff + its measured effect |
| 16:00 | **scope freeze**; record the full backup run | recorded backup + frozen demo |
| 16:00-17:30 | polish, numbers strip, guidance table; stretch only if green | final frame ready |
| 17:30-18:00 | rehearse the 90-second demo twice (see 07, 13) | pitch-ready |
| 18:00-20:30 | pitches + Q&A | done |

**Team split (4):** A) sim core, world, log; B) LLM layer, detection, trials;
C) dashboard; D) WHO agent, vaccination comparison, demo script + recording. With 3:
A+B merge, C+D merge.

**Pivot rule (pre-decided):** if by ~13:00 the one-hop trials show spread probability
near 0 or near 1 and tuning the payload wording does not fix it, pivot to Plan B
(functional-redundancy failover: the flagship "dies" mid-demo and the fleet degrades
to pre-qualified small-model cover with measured fidelity floors). Reused unchanged:
population, logging, dashboard. The case for Plan B is recorded in
FUNNEL-FINAL-VERDICT.md.

## Risks

| Risk | L | I | Mitigation |
|---|---|---|---|
| Ministral never (or always) copies the payload | M | H | ~20-call probe before building; tune payload wording in the first real hour; pivot rule at 13:00 |
| API latency / rate limits | M | M | size N from console limits; batch + parallel + backoff; small N on stage; pre-recorded run |
| Toy-risk verdict from judges | M | H | lead with measured numbers (probability ± CI, R0, equal-dose comparison) before the animation |
| Embed threshold misfires (false infections) | M | M | threshold knob + visible confirmation in the ticker; everything logged |
| Overclaim caught in Q&A | M | H | say "targeted beats random at equal dose"; never "provably" or "minimal" (see 07, 13) |
| WHO agent latency mid-demo | M | M | pre-generate one situation report; live-generate only the vaccine |
| Registration still pending at doors | L | H | check ticket before leaving; if pending, talk to hosts at check-in citing the NVIDIA Hack for Impact win |
