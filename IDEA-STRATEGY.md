# Le Chonk in London: Mistral Vibe Hackathon — Idea Strategy

Elite-strategist run, 20 Nov 2026. Idea quality only: no architecture, no code, no roadmap.
Competition inputs from the official Luma page plus this session's live winner research.

## Competition Decode

- **Event:** one-day, in-person hackathon by Mistral (Mistral Events). Sat 21 Nov 2026,
  08:30-20:30 GMT, Fora - Chancery House, London. Teams 3-5, free, meals provided,
  approval-gated crowd of ~238, self-selected strong builders.
- **Theme, literally:** none published. The de facto open track is "build with Mistral
  models and APIs". The "Vibe" in the name points at Mistral Vibe, their agentic coding
  product; the previous worldwide edition even had a "Best use of Mistral Vibe" award.
- **Sponsor goals (inference, labelled as inference):** show Le Chonk and Ministral
  doing things many cheap model calls can do, agent-building on their stack, hiring
  signal (profiles are shared with their hiring team, and hiring opportunity was part of
  the global prize last time), developer adoption.
- **Judging:** no published rubric. Closest published proxy from the same organisers
  (Sydney edition of their worldwide hackathon): technical depth, creativity,
  usefulness, quality of demo, alignment with objectives, equally weighted. An NYC judge
  wrote: "the teams that won had thought hardest about the user problem and about
  safety." The operator Iterate's own bar: a clearly defined problem, a defensible
  technical approach, measured evidence of improvement, and a demonstration anyone can
  understand.
- **Constraints that shape ideas:** ~11 hours of build time, free-tier API budget, live
  demo from a laptop, Mistral models as the star, practitioner judges who can smell a
  scripted demo.
- **What judges probably reward:** a measurable claim backed by numbers (their last
  winners reported 1.33x speedups, 60% acceptance rates, compiler-verified proofs), a
  phenomenon only a population of cheap LLM agents can produce, safety framing, and a
  demo that lands inside 60 seconds.
- **What will feel generic:** chat wrappers, RAG over documents, another agent
  observability dashboard, a "nicer ChatGPT for X", todo or trip-planner agents, demo
  theater with no measurement.
- **Under 60 seconds:** a live epidemic spreading through a visible agent population
  with a curve and a number (R0) judges can check themselves.
- **Wow moment:** the moment the intervention panel bends a live exponential curve.
- **Remembered after 20 demos:** "the team that gave AI agents covid and then cured it".
- **Commercially / technically valuable:** quantified spread dynamics and policy
  guidance for teams shipping agent fleets in 2026.
- **Rejected as toy:** an animated graph where infection is scripted; any version where
  the models are not actually deciding whether to propagate the pathogen.

## Winning Patterns From Research

Patterns extracted from this organiser's own events (worldwide edition, Feb 2026):
do not copy the winners, use the patterns.

1. **Population-scale agent systems can win outright.** The global winner, Mistralverse,
   was a London team's autonomous agent civilization in a metaverse. Rooms full of
   practitioners find "many agents, emergent dynamics, visible on a screen" inherently
   impressive.
2. **Winners thought hardest about user problem + safety** (NYC judge, on the record).
3. **Evidence beats confidence.** Hydra Ministral reported 1.33x faster generation and
   ~60% token acceptance. Lean Agent replaced model confidence with compiler verdicts.
   Poltergeist actively searched for failures. Iterate's own summary: generation and
   verification should remain separate.
4. **Attack-resistance is celebrated, not punished.** Ministral-3B-Sec (a safety
   fine-tune) is one of the seven projects Iterate showcases; prompt injection is named
   in their write-up among the concrete limitations strong projects tackled.
5. **Visible complexity.** Vibecraft ends in a Minecraft circuit; WingFox ends in a
   generated video. The last thing on screen must be understandable without narration.
6. **Execution test, not an ideas competition** (Sydney edition, on the record).
7. **Originality now decides.** The Tokyo winner's published lesson: as AI collapsed the
   implementation bar, idea distinctiveness became the separator.
8. **Demo-first mechanics.** Recurring judge advice across events: something working
   within 60-90 seconds, one "now this is possible" moment, mock everything that can
   stall, rehearse against the clock.

## Candidate Ideas (9)

**1. ChonkVid (AgentDemic).** One-line: release a self-spreading prompt "virus" into a
town of Mistral agents doing real work, measure its R0 live, then beat it with the
public-health playbook. Primary user: teams shipping agent fleets. Problem: one
compromised agent can propagate through a fleet; nobody knows how fast, or which
defence works. Pain: deployment decisions are currently vibes. Current solutions fail:
static red-teaming tests one agent, not spread; security scanners do not model
 contagion. Real data: AgentDojo (ETH Zurich's public prompt-injection benchmark for
agents) as the pathogen corpus, GAIA (public, 466 real tool-use tasks) as the agents'
daily jobs, plus the live epidemic logs the event itself generates. Fit: needs hundreds
of cheap model calls and embeddings, which is exactly Ministral + mistral-embed, with Le
Chonk as the WHO epidemiologist. Non-generic: epidemiology, not another red-team tool.
Wow: infect patient zero on stage, watch the network light up and the curve bend when
vaccination hits the herd-immunity threshold. Memorable because: "flatten the curve of
prompt injection." Weakness: reads as a toy if the dynamics are not rigorously measured.

**2. PromptPharma.** One-line: run randomised clinical trials for system prompts across
a population of agents and issue FDA-style approval labels with dose-response curves
and side effects (refusal rates). User: prompt engineers and platform teams. Problem:
prompts ship untested at scale. Data: IFEval (public instruction-following benchmark)
plus live trial logs. Fit: any strong LLM works, Mistral fine. Non-generic: the clinical
framing is fresh. Wow: "this prompt failed its trial, here is the label." Weakness: eval
tooling exists (promptfoo, HELM), and the RCT machinery is heavy for one day.

**3. AgentLloyd's.** One-line: actuarial tables for agent failures; run standard agent
tasks, tabulate failure modes, and issue a live insurance quote for an AI agent fleet.
User: risk managers, CFOs, platform PMs. Problem: enterprises cannot underwrite agent
deployments; no failure statistics exist. Data: GAIA and SWE-bench (public) plus live
runs. Non-generic: nobody prices agent risk. Wow: an underwriting decision made on
stage. Weakness: credible tables need far more task runs than 11 hours allows, and the
idea does not need Mistral specifically: sponsor-necessity is weak in this arena.

**4. Vibe Black Box.** One-line: a flight recorder for vibe-coding sessions that
detects the moment a build diverges (scope creep, hallucinated APIs, unread diffs) and
replays the session at speed with the divergence annotated. User: agentic coding teams.
Problem: vibe coding sessions fail silently. Fit: on-product for Mistral Vibe. Wow: a
replayed session with the "moment it went wrong" flagged. Weakness: agent tracing is
2026's most crowded devtools category (LangSmith, Langfuse, Braintrust), and wiring
real session capture plus replay in one day is heavy.

**5. AgentCon.** One-line: a con-artist agent loose in a town of agents; watch who
falls for social-engineering attacks and build the scam-resistance profile of a
population. User: agentic-commerce platforms. Problem: agent-to-agent fraud is arriving
with agent commerce. Data: scam-baiting corpora (thin). Wow: the room watches an agent
get talked out of its wallet. Weakness: same engine as #1 with a weaker evidence layer;
a demo laughing-stock risk if the scam flops.

**6. The Digital Civil Service.** One-line: simulate a benefits-appeals office as an
agent bureaucracy on GOV.UK appeal statistics; find where agents help and where they jam
the queue. User: caseworkers, councils. Problem: appeals take months. Data: GOV.UK
tribunal statistics (real, named). Weakness: solemn, low wow, and zero Mistral
necessity: wrong arena (this could win a civic hackathon instead).

**7. DemoGuard.** One-line: stress-test your own live demo before you present it
(kill the network, throttle the API, poison the cache) and grade its survivability.
User: every hackathon team. Problem: demos break. Weakness: meta-cute, thin product,
nobody in the room is the buyer; toy.

**8. TubeStrikeTown.** One-line: 10,000 agent commuters on TfL open data during a
strike; watch the network re-route. Data: TfL open data (real, excellent). Weakness:
civic agent sims are common, and TfL has nothing to do with the sponsor; fails the
sponsor-necessity test in this arena.

**9. Context ICU.** One-line: triage for overloaded agent contexts; decide what an
agent forgets, measured against task performance. User: agent builders. Problem:
context bloat degrades agents. Weakness: memory tooling is crowded (mem0 and friends),
build is heavy for one day, wow is low.

## Brutal Scoring Table

| Idea | Win Pot | Real Prob | Real Data | Track Fit | Users | Sponsor Tech | ≠ChatGPT | Build 12h | Non-Generic | Defensible | Total | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 ChonkVid | 9 | 8 | 7 | 9 | 7 | 9 | 9 | 7 | 9 | 7 | **82** | **Build immediately** |
| 3 AgentLloyd's | 8 | 9 | 8 | 7 | 9 | 6 | 9 | 6 | 9 | 7 | **78** | Needs work: not enough hours for credible tables, weak sponsor necessity |
| 2 PromptPharma | 8 | 8 | 7 | 8 | 7 | 8 | 9 | 6 | 8 | 6 | **75** | Needs work: fold its dose-response evidence layer into #1 |
| 5 AgentCon | 8 | 8 | 6 | 8 | 7 | 8 | 9 | 7 | 8 | 6 | **75** | Needs work: fold its scam payload into #1 as attack mode |
| 4 Vibe Black Box | 7 | 8 | 6 | 8 | 7 | 8 | 8 | 5 | 7 | 5 | **69** | Kill: crowded devtools lane, heavy capture build |
| 6 Digital Civil Service | 5 | 8 | 9 | 4 | 8 | 5 | 7 | 6 | 6 | 6 | **64** | Kill for this arena: no Mistral necessity, low wow |
| 9 Context ICU | 6 | 7 | 6 | 7 | 6 | 7 | 7 | 5 | 7 | 5 | **63** | Kill: crowded memory lane, heavy build |
| 7 DemoGuard | 6 | 7 | 5 | 5 | 6 | 5 | 7 | 6 | 7 | 4 | **58** | Kill: toy, no buyer in the room |
| 8 TubeStrikeTown | 6 | 6 | 9 | 3 | 6 | 4 | 7 | 6 | 5 | 5 | **57** | Kill: wrong arena, zero sponsor fit |

## Ideas to Kill and Why

- **AgentLloyd's (78):** the sharpest commercial brain in the list, but two hard fails
  here: credible actuarial tables need thousands of runs (11 hours cannot produce
  them, and judges will ask for the sample size), and it does not need Mistral
  specifically, so it wastes the sponsor-necessity criterion. Park it for an insurance
  or fintech arena.
- **PromptPharma (75):** its genuinely strong piece is the evidence aesthetic
  (dose-response, side effects, trial labels). Fold that into ChonkVid's measurement
  layer rather than shipping a second eval framework nobody asked for.
- **AgentCon (75):** same contagion engine as ChonkVid with a weaker data story. Fold
  its con-artist payload in as a second attack mode.
- **Vibe Black Box (69):** right pain, wrong decade of crowd: agent observability is
  the most funded lane in devtools and judges know Langfuse exists.
- **Digital Civil Service, Context ICU, DemoGuard, TubeStrikeTown:** wrong arena (no
  sponsor necessity, low wow, or crowded lanes). Each could live at a different
  hackathon; here they waste the one thing Mistral judges are guaranteed to reward,
  which is Mistral models doing something only a population of Mistral models can do.

## Best Winning Idea

**Name:** **ChonkVid** (keep AgentDemic as the internal repo name).

**One-line pitch:** "ChonkVid: we release a self-spreading prompt virus into a town of
Mistral agents doing real work, measure its R0 live, then beat it with the public-health
playbook: testing, masks, quarantine, and a vaccine prompt synthesised by a Le Chonk
WHO agent."

- **Exact problem:** prompt injection stops being a single-agent bug the moment agents
  talk to each other. Nobody has deployment-grade numbers for how fast a contagious
  payload spreads through an agent fleet, or which intervention actually bends the
  curve.
- **Primary user:** engineers and PMs shipping fleets of LLM agents into production.
  **Secondary:** AI safety and platform-security leads. **Decision maker:** the
  platform lead who signs off fleet deployment. **Beneficiary:** everyone downstream of
  an agent mesh (customers whose data the agents touch).
- **Why the problem matters:** 2024 research already demonstrated self-propagating
  LLM worms through email assistants (ComPromptMized). 2026 ships agents that talk to
  each other by default. The attack surface is now a population, and populations are
  an epidemiology problem.
- **Cost of doing nothing:** an unpatched fleet gets majority-infected in hours and
  nobody knows their R0 until it already happened.
- **Why existing solutions fail:** static red-team suites test one agent in isolation
  and never model transmission; guardrail scanners judge a single message, not a
  contagion process; "don't let agents talk" is not a strategy.
- **Why non-obvious:** everyone builds defences for the patient; nobody brings a
  century of public-health mathematics (R0, herd immunity, contact tracing, variant
  fitness) to the population.
- **Why it fits this hackathon:** it needs hundreds of cheap parallel model calls
  (Ministral), embedding similarity to detect paraphrased infection (mistral-embed),
  and one big model reading the epidemic log and synthesising the vaccine (Le Chonk,
  the eponymous chonk, as the WHO). Remove Mistral and the experiment cannot run at
  this scale in a day.
- **Why it can win:** it stacks every extracted pattern at once: population-scale
  agents (the global winner's archetype), safety-first framing (the judge's stated
  criterion), measured evidence (R0, ablation of each intervention, dose-response for
  vaccination rate), and a demo whose final frame (curve bending under a slider) is
  understandable without narration.
- **Named datasets:** AgentDojo (ETH Zurich's public prompt-injection benchmark for
  agents, the pathogen corpus; verify task count at build), GAIA (public benchmark,
  466 real tool-use tasks, the agents' daily jobs), and the live epidemic logs the
  event itself generates (transmission chains, S/E/I/R time series, variant embeddings).
- **Emotional hook:** everyone in that room lived through covid. Watching an
  exponential curve of hijacked agents feels viscerally dangerous, and "flatten the
  curve" needs zero explanation.
- **Practical value:** the output is a deployment guidance table: time-to-majority
  infection at the measured R0 under each policy (none, masks, quarantine, vaccination
  at the herd-immunity threshold). That table is the product.
- **Long-term potential:** the same harness runs any contagion: scams (AgentCon folded
  in as attack mode), data-poison memes, brand-safe content drift. It becomes the
  "flu lab" every agent platform needs before shipping a fleet.
- **Weakest part:** the toy risk. If the dynamics are pretty but unmeasured, judges
  file it under visualization. **Fix:** pre-register the numbers before the event
  (R0 with confidence interval, one ablation table, one dose-response curve), and lead
  the demo with the measurement, not the animation.

## Why This Can Win

- Only idea in the portfolio that maxes sponsor necessity (Mistral models are the host
  organism of the experiment, not a badge).
- Aligns with two on-record judge signals from this exact organiser: safety thinking
  and user-problem clarity.
- Produces evidence in the exact format their previous winners used: a measured number
  with a baseline and an ablation, not a claim.
- The demo has a built-in arc (infection, panic, intervention, cure) that compresses
  into 90 seconds and survives being the twentieth demo of the day.
- The build splits naturally across 3-5 people with no single point of failure, and
  has a mock mode so the team can develop without burning API budget.

## Real Data Sources

1. **AgentDojo** (ETH Zurich, open source): adversarial prompt-injection tasks for LLM
   agents; the pathogen corpus. Verify the exact task count when building; it is
   roughly a thousand tasks across agent scenarios.
2. **GAIA** (Meta AI + Hugging Face, public, 466 questions, three difficulty levels):
   real tool-use tasks the agents perform while the epidemic runs, so the town has an
   economy instead of idle chat.
3. **Live epidemic logs** (generated by the event run, timestamped): transmission
   chains, S/E/I/R time series, per-variant embedding lineages, intervention ablation
   runs. This is the dataset nobody else can have: measured today, in the room.

## Sponsor-Tech Fit

Sponsor tech is the experiment, not the logo: Ministral powers the population (hundreds
of cheap parallel calls are physically impossible on a single big-model budget),
mistral-embed detects paraphrased infection and builds the variant phylogeny, Le Chonk
(the event's namesake model) plays the WHO epidemiologist that reads the log, names the
variant, and synthesises the vaccine prompt that demonstrably bends the curve. The
prize (Mistral credits) literally funds the next, larger epidemic runs: a closing line
judges can retell. Without Mistral the project does not exist at hackathon scale; that
is the sponsor-necessity test passed in one sentence.

## Demo Wow Moment

Infect patient zero live, on stage, in the first 15 seconds. Network lights up, curve
goes exponential, the WHO agent publishes a situation report naming the first variant.
Then the intervention panel: masks, quarantine, lockdown, then vaccinate 70% and watch
the herd-immunity threshold bend the curve in real time. Final frame: the variant
phylogeny, "40 mutations, 3 surviving lineages, and here is the R0 we measured", over
the guidance table for fleets. Ninety seconds, one story.

## 30-Second Judge Explanation

"Agents are a population now, and populations get epidemics. ChonkVid releases a
self-spreading prompt into a town of Ministral agents doing real GAIA tasks, measures
the virus's R0 live, and then beats it with the public-health playbook, ending with a
Le Chonk WHO agent that synthesises the vaccine prompt from infection samples. It is a
safe sandbox that turns agent security from vibes into epidemiology: curves,
thresholds, and a deployment table you can act on."

## Weaknesses and Fixes

1. **Toy risk (the big one).** Animation without measurement loses to a simpler
   project with a table. Fix: pre-register three numbers (R0 with CI, one intervention
   ablation, one dose-response) and put them on screen before the animation.
2. **Dynamics roulette.** The infection may fizzle or explode too fast on stage. Fix:
   tunable susceptibility, seeded patient zeros, and a pre-recorded full run as the
   fallback the rules of live demos demand.
3. **Abstract user.** "Agent security" can drift into research-demo tone. Fix: open
   with the fleet-deployment table ("at this R0, your unpatched 10k-agent fleet is
   majority-infected in 40 minutes") so the user and the decision are concrete.
4. **Saturation flag.** The collision auditor flagged HIGH; its listed analogues
   looked off-topic (invoice and fraud fixes), so it is probably semantic noise, but
   the team should hold one line of differentiation: the intervention layer and the
   measurement are the product, the spreading virus is only the setup.
5. **Safety optics.** A room of Mistral staff watching a "worm" needs the frame set in
   the first sentence: safe sandbox, benign chain-letter payload, sim-local agents,
   goal is quantifying defence. Fix: say it before the demo, not after.

## Final 10/10 Checklist

| # | Test | Pass |
|---|---|---|
| 1 | Could it place top 3 (wow, visual, under 60s, beyond CRUD, one-line pitch) | Yes |
| 2 | Real problem (named users, cost of doing nothing) | Yes |
| 3 | Real data (AgentDojo, GAIA, live logs) | Yes |
| 4 | Track fit (the open Mistral track, Sydney-style criteria) | Yes |
| 5 | Defined users (fleet PMs, safety leads, decision maker named) | Yes |
| 6 | Sponsor tech essential (Ministral population, mistral-embed, Le Chonk WHO) | Yes |
| 7 | ChatGPT cannot do it (multi-agent live simulation, measured R0) | Yes |
| 8 | Buildable in 11 hours (mock mode, 4-person split, recorded backup) | Yes, with tuning risk |
| 9 | Non-generic (epidemiology framing, not the tenth red-team tool) | Yes, with the differentiation line held |
| 10 | Defensible (measurement pipeline, live dataset nobody else has) | Yes |

## Final Verdict

**Build immediately.** ChonkVid at 82/100, with the evidence layer from PromptPharma
and the attack modes from AgentCon folded in. It is the only candidate where the
sponsor's models are the experiment itself, the only one with a demo that needs no
narration, and it speaks the exact language (safety, user problem, measured evidence)
this organiser's judges have already rewarded on the record. The 2 points it leaves on
the table are build risk and user-abstraction, both fixed by pre-registering the
numbers and leading with the fleet-deployment table.

---

# Layer 2: Advanced Strategy Stress Test (20 Nov 2026, evening)

## What the room will build tomorrow (anti-obvious decode)

The crowd magnets at a Mistral one-day: Mistralverse clones (the last global winner
was a civilization sim, expect copies), Le Chonk chat personas, vibe-coding toys on
Mistral Vibe, voice agents, RAG assistants, "agent startup" theater, predictor bots.
The anti-obvious move is to treat agents as a population to be studied, not a product
to be demoed. ChonkVid already occupies that space, and it inverts the archetype the
crowd will copy: their sim grows a civilization, ours runs an epidemic and then
controls it.

## Where the boring-pain doctrine is consciously waived

The advanced layer pushes toward boring workflow tools (grants, bookings, forms). This
organiser's own record argues against it here: across the worldwide edition, every
celebrated project was a phenomenon or experiment (attention surgery, speculative
decoding, safety fine-tune, formal verification, adversarial VLM testing, civilization
sim, generated video, live TV debunk). Zero devtools placed. Spirit kept, letter
waived: the pain stays real and grounded in deployment, but the artifact is a
measured experiment, not a form-filler.

## Advanced-layer challengers (generated and killed honestly)

- **SwitchDoctor (74):** the prompt passport; migrate a prompt suite to Le Chonk,
  red-to-green regression, merge-ready diffs. Real boring pain, very buildable (9/10),
  sponsors would love the adoption story. Killed for this arena: the eval/migration
  lane is occupied (promptfoo and friends), and this room has never rewarded a devtool.
  Park it for an enterprise or devtools arena.
- **ShipGate (68):** ship / no-ship verdict with receipts for vibe-coded apps.
  On-product for Mistral Vibe, strong trust layer, but robust arbitrary-codebase
  analysis in 11 hours is a build risk and the test-generation lane is crowded.
- **EvalBill (60):** runaway-cost circuit breaker for agent loops. Thin product.

## Mandatory upgrades ChonkVid absorbs from this layer

1. **Edge user, named:** a platform PM at a 12-person startup shipping 50 support
   agents next week with no security budget; her current red-team process is pasting
   one suspicious email into one test agent and praying.
2. **Workflow-collapse pitch:** "Fleets are red-teamed one prompt at a time in a
   spreadsheet. ChonkVid runs your whole fleet as a live epidemic and returns the R0,
   the variant tree, the policy table, and a merge-ready vaccine patch in one command."
3. **Last-mile artifact:** the demo's final frame is the vaccine system-prompt diff
   plus the deployment policy table, deployed by a human approval click on stage.
4. **Trust layer:** pre-registered R0 with confidence interval, the transmission-chain
   log as the citation ("why this number" is one click away), approval gate before
   the patch goes live in the population.
5. **Cut discipline:** one user, one virus, one town, one cure. No auth, no settings
  pages, scam payload only if time remains. The 50k-agent city mode is timeboxed: if
   it is not working by 16:00, cut it and close on the measured lab numbers.
6. **Judge-memory sentence:** "the app that gives an AI agent fleet its flu shot
   before shipping."
7. **Expansion vision, one line:** demo is one virus in one town; the vision is the
   CDC for AI agents (scams, memes, poisoned data, any contagion a fleet can carry).

## Layer-2 verdict

ChonkVid survives the stress test and comes out sharper: it was already anti-obvious
for this room, and the layer's packaging upgrades (edge user, collapsed workflow,
vaccine diff as last mile, trust layer, cut discipline) fix its two real weaknesses
(user abstraction and toy risk). The boring-pain doctrine is the one rule consciously
waived, with the organiser's own winner record as evidence.

