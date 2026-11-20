# Final recommendation: Le Chonk in London - Mistral Vibe Hackathon

## Primary concept
**Working title:** Allocation Replay
**Internal id:** `mut-r1-04-allocation-replay`
**Primary user:** On-site team-formation coordinator
**Painful workflow:** A coordinator needs to verify that a proposed grouping still obeys the published team-size rule after attendees join or leave.
**Imported mechanism:** Reproducible constraint validation: replay a saved roster and proposed groups against explicit cardinality rules. _(from operations research)_
**Data sources:** Manually entered anonymous roster identifiers, Synthetic group allocations
**Core computation:** Validate that every roster identifier appears exactly once and every group contains three to five people; return deterministic failures tied to group identifiers and input version.
**Last-mile action:** Run a repeatable validation test on the proposed local allocation and save its inputs and result as a replayable report.
**Visible transformation:** A proposed grouping becomes a reproducible pass or a precise list of allocation defects.
**Killer demo:** Validate eleven synthetic attendees in groups of four, four and three; move one attendee to create groups of five, four and two, then replay the saved failing case.
**Hard-to-fake advantage:** The saved fixture and deterministic checks let anyone reproduce duplicate, missing and invalid-size failures from the same inputs.
**Sponsor dependency:** None required.

## Why this concept was selected
Pairwise wins={'B': 3, 'A': 2, 'D': 1}; votes={'B': 6}; official competition criteria and their parsed weights/priorities determine ordering; disagreements=0

## Judge disagreement (do not average away)
- None (inspect vote table anyway)

### Judge votes
- **technical** → B: B has a bounded, deterministic core result that is feasible for a four-person team and uses credible synthetic inputs. Its saved fixtures make duplicate, missing and invalid-size failures reproducible. Its stated collision risk is medium. Participant eligibility, host approval and in-person attendance remain unverified for every candidate; the supplied team size of four meets the stated size rule. The deadline is operator-supplied, while the official page identifies that time as the event end. No official judging criteria were supplied, so no criterion scores can be assigned.
- **product** → B: B delivers a focused, practical result against the stated team-size rule, using credible local inputs and reproducible checks. Its deterministic replay makes the result independently verifiable. A four-person team makes the scope plausible by the supplied deadline, although the available build window is unknown. The proposed demonstration has medium delivery risk: roster changes and saved reports must work consistently. Participant ages, host approval and London attendance remain unverified for all candidates; four participants satisfy the stated team-size range. The operator's deadline is supplied as a constraint, while the official page identifies that time as the event end.
- **sponsor** → B: No official judging criteria were supplied, so there is no basis for assigning criterion scores. B has a concrete, reproducible result using accessible synthetic data, a bounded implementation, and medium stated collision risk. Its saved inputs and deterministic validation are straightforward to verify. The team’s ages, host approval and in-person attendance remain unconfirmed across the candidates; a team of four meets the stated size range. The operator-supplied deadline should be observed, while its status as an official submission deadline remains unconfirmed.
- **domain** → B: B has a clear, reproducible core result and a feasible scope for a four-person team. Its synthetic data is sufficient for the proposed validation, and replayable inputs and results make the checks difficult to fake. No official judging criteria were supplied, so there is no basis for criterion scores. The proposed demonstration has medium failure risk. Eligibility and attendance remain unverified across the candidates: age, host approval and in-person participation must be confirmed. The operator-supplied deadline should be observed, although the official page identifies that time only as the event end.
- **demo-risk** → B: B has a small, deterministic core and a credible synthetic-data demonstration: its saved inputs and validation results can be replayed to verify the claimed behavior. Its scope is practical for a four-person team before the operator-supplied deadline, although the build window is unspecified. The team's ages, host approval and ability to attend in London remain unverified for every candidate. No official scoring criteria were supplied.
- **contrarian** → B: No official judging criteria were supplied, so a criteria-based ranking is not possible. B is the tentative preference: its bounded result is reproducible from manually supplied inputs, and its synthetic examples demonstrate both passing and failing allocations. Its saved cases are harder to fake than an unsupported assertion of validity. A is similarly feasible but addresses a narrower one-off decision; C and D have high stated collision risk. All candidates share unresolved participant eligibility, host approval, and in-person attendance; a four-person team fits the stated size range, but membership is not verified. The operator-supplied deadline is treated as a constraint even though the event page identifies that time only as the event end.

## Closest competing projects
- Devpost for Teams (public product)
- Team Change Gate (current candidate: mut-r1-03-team-change-gate)
- Collision risk: medium
- Observable differentiator: A saved whole-roster allocation replays identical duplicate, missing and invalid-size failures.
- Differentiator substantive?: True

## Critical assumptions
- Data exists and is accessible: Manually entered anonymous roster identifiers, Synthetic group allocations
- Delivery risk: medium
- Technical risk note: A valid grouping does not establish individual age eligibility or host approval; report these separately as unverified.

## Technical proof sketch (not an architecture)
- Critical computation: Validate that every roster identifier appears exactly once and every group contains three to five people; return deterministic failures tied to group identifiers and input version.
- Required data: Manually entered anonymous roster identifiers, Synthetic group allocations
- Most dangerous dependency: Host approval, four eligible team members, and attendance in London remain unconfirmed.
- Minimum demonstrable loop: Validate a synthetic four-four-three allocation, introduce an invalid two-person group and a duplicate or missing identifier, save the inputs and result, and replay them.

## Build-window scope (due 2026-11-21 20:30 UTC)
- One user: On-site team-formation coordinator
- One workflow: A coordinator needs to verify that a proposed grouping still obeys the published team-size rule after attendees join or leave.
- One demo moment: Validate eleven synthetic attendees in groups of four, four and three; move one attendee to create groups of five, four and two, then replay the saved failing case.
- Cut anything that does not improve the killer demo.

## Primary failure risk
A synthetic replay establishes validator behavior, not coordinator access or real-world usefulness. A passing allocation does not verify individual eligibility. The available build window is unspecified.

## Red team
- Conditional acceptance: None
- Prefer backup instead: False
- Fatal flaws: ['The core is a basic roster validator, a crowded spreadsheet and form-validation archetype; it does not perform allocation or meaningful constraint solving.', 'The checks and replay report are easy to reproduce with a short script or ChatGPT. Determinism makes the result verifiable but is not a hard-to-fake advantage.', 'The synthetic eleven-person demo proves the code runs, not that coordinators face enough changes or errors to need a dedicated tool.', 'The cited source is not provided, so the three-to-five rule, coordinator need, and event-specific applicability cannot be independently assessed from the supplied material. A retrieved source does not establish all of these claims.', 'The compliance pass overstates the evidence: age eligibility, host approval, in-person participation, and submission proof remain unverified.']
- Survive if: ['Confirm the actual team-size rule and demonstrate a real coordinator workflow with representative roster changes and error frequency.', 'Show measurable value over a spreadsheet or short script, such as reliable audit and reconciliation across multiple versions with independently reproducible edge cases.', 'Clearly scope the report to roster and group-size checks, and verify participation and submission requirements separately.']

## Backup concept
**Next Check Scheduler** (`mut-r1-02-next-check-scheduler`)
- User: Applicant awaiting host approval
- Mechanism: Counterfactual testing: choose a bounded action that remains useful across explicitly modelled approval outcomes.
- Demo: Set approval to unknown and provide a decision point; export a reminder, then switch to approved and show that the suggested follow-up changes.

## Rejected / not advanced
- `concept-01` — Approval Ledger: outcompeted / clustered
- `concept-02` — Team Feasibility Desk: outcompeted / clustered
- `concept-03` — What Would Make Me Eligible?: outcompeted / clustered
- `concept-04` — Preference Tradeoff Board: outcompeted / clustered
- `concept-05` — Room-to-Team Planner: outcompeted / clustered
- `concept-06` — Deadline Evidence Lab: outcompeted / clustered
- `concept-07` — Deadline Ledger: outcompeted / clustered
- `concept-08` — Feasibility Switchboard: outcompeted / clustered
- `mut-r1-03-team-change-gate` — Team Change Gate: outcompeted / clustered

## Structurally different backup 2
**Evidence Patch** (`mut-r1-01-evidence-patch`)
- Stakeholder: Team member maintaining the shared event checklist
- Mechanism: Provenance verification: link each proposed edit to a direct source statement and retain the prior value.
- Proof/demo: Replace a fixture that incorrectly calls 20:30 the confirmed submission deadline with the supported statement that it is the event end; inspect the before-and-after checklist and provenance.
