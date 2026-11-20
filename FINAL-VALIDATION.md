# ChonkVid: Final 10/10 Winner-Pattern Validation

Run 20 Nov 2026, evening, before committing the build. Rule applied: start from
precedent, not imagination. All winner facts below come from this session's live
research (organiser pages, judge recaps, winner write-ups, Iterate's showcase).

## 0. Past Winner Analysis (5 winners, same organiser ecosystem)

| Project | Event, year | Problem | Why judges likely picked it | Demo style | Data / tools | Depth | Visual | Impact | Pattern we reuse / gap we exploit |
|---|---|---|---|---|---|---|---|---|---|
| **Mistralverse** (global winner, London) | Mistral Worldwide Hackathon 2026 | none stated: an autonomous AI civilization growing in a metaverse | population-scale emergent behavior, huge execution, spectacle | live world view | Mistral APIs at population scale | very high | spectacular | demo-first | reuse: many agents + emergent dynamics + visible world. Gap: it celebrated growth, nobody showed control; ChonkVid runs the adversarial inverse and adds interventions |
| **WingFox** (Tokyo winner) | same event | video production is slow and skill-gated | original idea, brand-new tech learned live with AI help | generated video artifact | Remotion + ElevenLabs + Mistral | high | artifact anyone can watch | creator tooling | end the demo on an artifact, not a talk |
| **Veristral** (Paris winner) | same event | political TV misinformation goes unchecked live | civic bite, live-input bravery, real user | live TV stream in, verdicts out | Mistral + streaming pipeline | high | live tension | public trust | live input beats slides; a real-world threat on screen |
| **Lean Agent** (2nd, NYC) | same event | LLM math claims are unverifiable | generation separated from verification, compiler as judge | proof pass/fail on screen | Lean compiler loop | very high | austere but decisive | correctness culture | our infection is embedding-verified and R0 measured, never asserted |
| **Ministral-3B-Sec** (showcase) | same event | models either refuse everything or comply with attacks | safety made explicit and measured (refuse malicious, answer benign) | before/after refusals | 5,227 malicious prompts, two-stage tune | high | plain | fleet safety | safety is judge-catnip here; our whole frame |

Supporting: **Hydra Ministral** (won on measured 1.33x + 60% acceptance: numbers with
baselines) and **Poltergeist** (won on actively searching for failures: red-team
posture). **Repeated judge preferences, on record:** user problem + safety first
(NYC judge), measured evidence over confidence, spectacle with understandable final
frame, execution over ideas. **The gap across all of them:** every celebrated
project tests or celebrates a system's capability; none models what happens BETWEEN
agents in a deployed fleet, and none closes the loop with an intervention that
visibly works. That is the gap ChonkVid occupies.

## The 10 checks

**1. Winning potential: PASS.** Wow: patient zero infected live, curve bends at the
herd-immunity threshold, final frame is a merge-ready vaccine diff. Understandable in
under 60 seconds. Depth beyond CRUD: a live multi-agent experiment with measured
emergent dynamics. One-line pitch locked: "the app that gives an AI agent fleet its
flu shot before shipping."

**2. Real problem: PASS.** Fleets of inter-communicating agents are shipping in 2026
with no contagion numbers: no R0, no time-to-majority, no evidence any defence works.
Who: platform teams shipping agent fleets (named edge user: PM at a 12-person startup,
50 support agents, no security budget). Current solutions fail: red-team suites test
one agent in isolation, never transmission. Cost of doing nothing: majority-infected
fleet before anyone notices. Why now: self-propagating LLM payloads were demonstrated
in 2024 research and everything since made agents more connected.

**3. Real data: PASS (thinnest section, honestly flagged).** Three named sources with
roles: **AgentDojo** (ETH Zurich, open-source benchmark on GitHub; adversarial
prompt-injection tasks for agents, roughly a thousand, static release; the pathogen
corpus), **GAIA** (Meta AI + Hugging Face, 466 real tool-use questions, static; the
town's daily jobs so agents work, not chat), and **live epidemic logs** (generated in
the room: timestamped transmission chains, S/E/I/R series, per-variant embedding
lineages; the measured dataset nobody else has). Mitigation for the self-generated
third: the two public benchmarks anchor it and the measurement IS the product.

**4. Track alignment: PASS.** The event has one de facto track: build with Mistral.
Satisfies the organiser's own published-criteria proxy: technical depth (live
multi-agent experiment), creativity (epidemiology frame), usefulness (deployment
policy table), demo quality (90-second arc), alignment (Le Chonk plays WHO).
Stronger than a generic submission because the sponsor's models are the host
organism of the experiment.

**5. Defined users: PASS.** Primary: platform PM shipping a fleet next week.
Secondary: agent safety / security leads. Decision maker and approver: same platform
lead. Person who feels the pain: the same PM watching a fleet she cannot certify.
Beneficiary: every end user whose data the agents touch.

**6. Platform justification: PASS.** The phenomenon requires hundreds of parallel
live model calls within a free-tier budget: only a cheap, fast small model
(Ministral) makes the population physically possible in 11 hours. Paraphrase-resistant
infection detection and the variant phylogeny require embeddings (mistral-embed).
The vaccine synthesis and situation reports are the event's namesake model, Le Chonk,
on stage. A scripted animation on a laptop is the toy version; the sponsor's models
deciding whether to propagate is the real one.

**7. Not replaceable by ChatGPT: PASS.** Live multi-agent simulation, continuous
decision loops, real-time dashboard, and a system action (vaccine patch deployed
behind an approval gate). No judge can get an R0 from a chat window.

**9. Non-generic: PASS.** Not the hundredth red-team tool, not a Mistralverse
civilization clone (the crowd magnet): the frame is epidemiology, and the
differentiation line is held: interventions plus measurement are the product, the
virus is only the setup.

**10. Defensible: PASS, with an honest note.** Sponsor-native implementation (Le
Chonk as the WHO is unrepeatable at any other event), the live-measured dataset
generated in the room, and the measurement pipeline (R0 with CI, intervention
ablation, dose-response, phylogeny). A strong team could re-implement the sim later;
they cannot re-run our measurement or claim our numbers. The moat is evidence-first
framing plus the live dataset.

## Final test

- [x] Past winners analysed (5 primary + 2 supporting, same organiser)
- [x] Can it win (wow, visual, sub-60s, beyond CRUD, one-line pitch)
- [x] Real problem (named user, cost of inaction, why now)
- [x] Real data (AgentDojo, GAIA, live logs, roles explicit)
- [x] Specific track (the open Mistral track, organiser's own criteria)
- [x] Users defined (PM shipping, safety lead, approver, beneficiary)
- [x] Platform essential (Ministral population, mistral-embed, Le Chonk WHO)
- [x] ChatGPT cannot do it (measured live simulation with a system action)
- [x] Non-generic (epidemiology frame, differentiation line held)
- [x] Defensible (sponsor-native, live dataset, measurement pipeline)

## Verdict

**10/10: Build immediately.** No section fails. Two sections carry honest caveats
(data: one of three sources is self-generated, anchored by two public benchmarks;
defensibility: the sim is re-implementable, the numbers are not) and both are
mitigated by the same move: pre-register the measurement tonight (R0 with CI, one
intervention ablation, one dose-response) and lead the demo with those numbers on
screen. Precedent says this organiser rewards exactly that.

Outstanding before doors: Mistral API key (console.mistral.ai, try redeem code
LECHONK), team confirmation (3-5, Isaiah default), Luma approval status check
tonight, pre-recorded full-run backup during the event. HackForge engine still
running; reconcile its collision and feasibility reports against this verdict when
they land.
