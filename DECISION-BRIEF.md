# Le Chonk Decision Brief (self-contained, for cold analysis)

> **Event update (21 Nov, 01:45):** registration approved; agenda is hack 10:00–18:00, submission
> hard stop 18:00, pitches 19:00–21:00, theme announced at the 09:00 kick-off. Credits link on the day.
> Gates: command-centre/11. The "Tonight's checklist" below is superseded.

> **Scope note (21 Nov, 01:00):** the build scope was cut on 20 Nov night (no GAIA/AgentDojo,
> city mode, masks, lockdown or boosters; one-hop trials for measurement). The build spec is
> command-centre/10-project-architecture.md, which overrides this brief on scope.

Written Fri 20 Nov 2026, night before the event. This file is the whole picture in
one place: a fresh AI session (or teammate) can read just this and understand the
decision, the evidence, and what to challenge. Detailed docs are alongside in this
folder (see map at the end).

## The decision, in plain words

Tomorrow (Sat 21 Nov 2026) we go to Mistral's one-day London hackathon and build
**ChonkVid**: the "AI agents infected by covid" simulation. An epidemic of a
self-spreading prompt runs through a population of Mistral agents doing real tasks,
we measure its spread live (R0, curves, variant lineages), then beat it with the
public-health playbook and end on a computed "vaccine" result.

Event facts:
- Le Chonk in London: Mistral Vibe Hackathon. One day, in person, 08:30 to 20:30 GMT,
  Fora - Chancery House, 53-64 Chancery Ln, London WC2A 1QS.
- Teams of 3-5, free entry, meals provided, judged by Mistral's own AI engineers,
  SWEs, TPMs and AI scientists. Prizes: $3,000 / $2,000 / $1,000 in Mistral credits.
- Registration: submitted 17 Nov via 2383758@brunel.ac.uk (Luma tk=n0fIwx). It was
  still "Pending Approval" at the last check (20 Nov); no approval email in the
  Brunel inbox as of the 11:07 GMT scan. OPEN ITEM: confirm the ticket tonight,
  signed in, or contact the host if still pending.

## Why this idea, honestly (the evidence)

1. **The organiser's own record rewards exactly this shape.** Their previous global
   winner was Mistralverse, a population-scale autonomous agent civilization (London
   team). An NYC judge wrote that winners "thought hardest about the user problem
   and about safety". Iterate's own showcase of standout projects includes a safety
   fine-tune (Ministral-3B-Sec) and names prompt injection among the problems strong
   projects tackle. Every celebrated project had measured numbers, not vibes.
2. **A blind panel re-invented the lane.** Four isolated ideation sessions (100
   seeds, 12 assigned disciplines, none shown our idea or the winners) independently
   produced SIR contamination modeling, herd-immunity hardening targets, and ring
   vaccination from the epidemiology assignment alone. When a blind panel re-derives
   your mechanism family, that is external validation, not confirmation bias.
3. **The lane is open.** Across 980 live competitor analogues scraped that evening:
   epidemic simulation had 1 off-topic hit; canary/DLP had 86; guardrails had 69;
   failover/routing had 19. The crowded lanes are exactly the ones our second-tier
   candidates landed in.
4. **The fallback engine disagreed, and was wrong for an instructive reason.** The
   HackForge engine (given a compliance-heavy brief) picked a team-roster validator
   its own red team called "easy to reproduce with ChatGPT". Diagnosis: it mined
   event logistics because my brief led with them. Lesson recorded; the engine's
   collision corpus was still salvaged for the audit above.
5. **It survived a 10/10 winner-pattern validation** with two honest caveats (one of
   three data sources is self-generated, anchored by AgentDojo and GAIA; the sim is
   re-implementable but the measured numbers are not), both repaired by the same
   move: pre-register the measurement and lead the demo with the numbers.

## The build, in one paragraph

Population of Ministral agents on a contact network (households + one group chat as
the super-spreader venue) doing GAIA tool-use tasks. Patient zero receives a benign
self-spreading prompt (chain-letter style). Infection counts only when an agent's
own outgoing message carries a paraphrased copy, detected by mistral-embed
similarity, so the models genuinely decide whether to propagate. States S/E/I/R;
paraphrasing makes the payload mutate, so variant lineages emerge and can be drawn
as a phylogeny. Interventions panel: testing+quarantine, masks (output filtering),
lockdown, vaccination. A Le Chonk "WHO agent" reads the epidemic log, writes
situation reports, names variants, and synthesises the vaccine prompt. Two modes:
a full-LLM lab run that measures R0, and (timeboxed, cut by 16:00 if flaky) a
calibrated large-N city run.

## The demo arc (90 seconds)

Infect patient zero live in the first 15 seconds. Curve goes exponential, network
lights up, WHO agent names variant one. Apply interventions: the curve bends at the
computed herd-immunity threshold. Final frame: the variant phylogeny ("40 mutations,
3 surviving lineages, here is the R0 we measured") and the merge-ready vaccine
system-prompt diff, deployed behind an approval click.

## The two upgrades that matter

1. **Herd-immunity targeting** (from the blind panel, seed D-17): the vaccination
   beat is not a slider; it is a greedy targeted hardening set (degree /
   betweenness) chosen from the live contact topology, shown to beat random
   hardening at the same dose. (Revised 20 Nov night: the earlier "provably minimal
   set" claim was dropped; optimal immunisation is NP-hard in general.) Toy becomes result.
2. **Workflow-collapse framing:** "fleets get red-teamed one prompt at a time in a
   spreadsheet; ChonkVid runs your whole fleet as a live epidemic and returns R0,
   the variant tree, the hardening set, and a merge-ready vaccine patch in one
   command." Named user: a platform PM shipping a 50-agent fleet next week with no
   security budget.

## Plan B (decided in advance, no guilt)

If the epidemic dynamics are unstable by early afternoon: pivot to
**functional-redundancy failover** (blind-panel seed D-23): the flagship model
"dies" mid-demo and the fleet degrades to pre-qualified small-model cover with
measured per-task fidelity floors, with the monoculture correlated-failure audit
(D-22) folded in as one slide. It reuses most of the same population, probe and
dashboard infrastructure and is the safer, more deterministic build. Dissent kept
on record: if you value delivery certainty over live emergence, the case for Plan B
is real.

## Known risks (do not hide these)

- Dynamics roulette: the infection may fizzle or explode on stage. Mitigations:
  tunable susceptibility, seeded patient zeros, pre-recorded full-run backup.
- Toy risk: pretty animation without measurement loses. Mitigation: pre-register
  R0 with confidence interval, one intervention ablation, one dose-response; numbers
  on screen before the animation.
- Safety optics: frame it in the first sentence: safe sandbox, benign chain-letter
  payload, sim-local, goal is quantifying defence.
- Approval status unresolved until the ticket is checked.
- Collision-audit tooling fault: agents/collision.py returned identical canned
  Devpost matches for unrelated queries tonight; its HIGH flags were noise. The
  980-analogue corpus distribution is the trustworthy signal.

## Tonight's checklist

1. Confirm the Luma ticket (signed in as 2383758@brunel.ac.uk); if still pending,
   use Contact the Host and cite the NVIDIA Hack for Impact win.
2. Create the Mistral API key on console.mistral.ai; try redeem code LECHONK
   (unverified hint from X replies).
3. Confirm teammates (3-5 required; Isaiah Paul is the default on record).

## What a fresh analyst should challenge

If you are reading this cold: attack the decision. Is the "measured epidemic"
demo actually achievable in ~11 hours on a free tier? Is the primary user (fleet PM)
real or a convenient fiction? Does the herd-immunity upgrade hold up as a mechanism
or is it decoration? Is the epidemiology frame a strength with Mistral judges or a
gimmick that reads as a game? Is Plan B actually reachable from Plan A's code by
mid-afternoon? The evidence says yes to each, but the point of this brief is to be
re-checked, not admired.

## Folder map (deeper reading, same folder)

- HACKATHON.md: the build brief (event, plan, stack, demo script, risks).
- IDEA-STRATEGY.md: nine scored candidates, the layer-2 stress test, and why the
  other eight were killed.
- FINAL-VALIDATION.md: the 10/10 winner-pattern validation with the winner table.
- FUNNEL-FINAL-VERDICT.md: the 100-seed blind funnel, gates, collision corpus
  numbers, pairwise judging, and the preserved dissent.
- PASS1-SANITIZED-BRIEF.md: the sanitized brief the blind ideators received.
- ENGINE-RUN-RECONCILIATION.md: why the HackForge engine's own pick was rejected.
- evidence/: raw HackForge run outputs, the engine brief, the 980-analogue
  collision corpus (JSON), and the original event research brief.
- command-centre/: the 10-file execution centre for the build day (rewritten for
  this event on 20 Nov night; earlier copies were from Vultr Agent Rush).
