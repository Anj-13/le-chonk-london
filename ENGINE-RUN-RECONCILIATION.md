# HackForge Engine Run: Reconciliation (20 Nov 2026, evening)

Run: Master hackathon/runs/2026-11-20-le-chonk-london/2026-11-20-le-chonk-london/
(final-recommendation.md, collision-analysis.md, feasibility-analysis.md)

## Verdict of the engine

"Allocation Replay": a deterministic roster validator for the on-site
team-formation coordinator (checks 3-5 per group, replays saved failing cases).
All nine of its candidates were administrative meta-tools about the event itself
(approval ledgers, deadline ledgers, eligibility desks), not builds for the event.

## Status: REJECTED as a build recommendation

Not rejected out of dislike; rejected on the funnel's hard gates, confirmed by the
engine's own red-team section:
- Fails "ChatGPT cannot do it": "easy to reproduce with a short script or ChatGPT".
- Fails "real computation or action": "does not perform allocation or meaningful
  constraint solving".
- Fails non-generic: "a crowded spreadsheet and form-validation archetype".
- Its own survival conditions required value over a spreadsheet, which the concept
  did not demonstrate.

## Root cause (mine, not the engine's)

The brief was compliance-first: registration status, approval uncertainty, team
rules and deadline led the document, with the actual build problem compressed at the
end. HackForge mines the richest structured data in a brief; here that was event
logistics, so it ideated meta-tools about attendance. Also: the engine was given no
judging criteria (its judges note "no official judging criteria were supplied"), so
its ranking had no competition-specific weights to anchor on. The sanitized ideator
brief (PASS1-SANITIZED-BRIEF.md) fixed both problems for the panel runs.

Lesson banked in the Daily Log (2026-11-20): HackForge briefs must be build-first.

## Salvage (what the run is still worth)

1. The 980-analogue live competitor corpus
   (corpora/live-competitors/le-chonk-london.json) feeds the Pass 4 collision audit
   on the panel's semifinalists.
2. The collision report's structural comparison format (user / problem / mechanism /
   data / action / demo booleans, "substantive differentiator" question) is adopted
   for the panel's audit.
3. Independent confirmation of the attendance uncertainty: host approval remains
   unverified for the team (already tracked: Luma ticket check tonight stays an
   owner step).
4. Negative evidence for the meta-lane: the engine, given a free hand, drifted to
   admin tools about the event; that lane is confirmed dead for a room of Mistral
   practitioners.

## Consequence for the funnel

The live candidates are the four isolated ideator panels' seeds plus the incumbent
concept (ChonkVid), all to be judged blind with hard gates, the organiser's own
published-criteria weights, and pairwise comparison. The engine adds the corpus and
the audit format, not a candidate.
