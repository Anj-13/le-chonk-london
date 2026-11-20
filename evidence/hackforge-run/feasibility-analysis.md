# Feasibility analysis

## mut-r1-02-next-check-scheduler
- Delivery risk: **medium**
- Kill?: False
- Non-fakeable core: Generate a valid local calendar reminder at the user-confirmed time, before the decision point, with accurate conditional follow-up and no claim of approval.
- Minimum completion/proof loop: Enter an unknown status and feasible decision point, confirm a check time, export and inspect the calendar file, then change the status and verify the follow-up changes.
- Dependencies: Host approval, four eligible team members, and attendance in London remain unconfirmed., A valid user-supplied decision point and a feasible check time before it., Confirmation of the actual submission process and cutoff; 20:30 UTC is supplied as an operator deadline but identified on the event page as the event end.
- Notes: The local implementation has few dependencies, but the asserted delivery-feasibility pass does not establish available build time or participation eligibility. The event is already covered by the Le Chonk London registration task and the 2026-11-20 owner record; no duplicate queue item is needed.

## mut-r1-03-team-change-gate
- Delivery risk: **medium**
- Kill?: False
- Non-fakeable core: Apply the three-to-five count and three-valued individual checks correctly, block unresolved or invalid cases, and label a pass as based on supplied records rather than host certification.
- Minimum completion/proof loop: Test a six-person roster, a three-person roster with unknown approval, and a fully supported synthetic roster; verify distinct block reasons and the local pass.
- Dependencies: Host approval, four eligible team members, and attendance in London remain unconfirmed., Accurate, current user-supplied age and approval records for any real use., Confirmation of the actual submission process and cutoff.
- Notes: Synthetic evidence proves rule handling, not actual eligibility or evidence authenticity. The supplied timebox claim does not prove delivery by the operator cutoff.

## mut-r1-04-allocation-replay
- Delivery risk: **medium**
- Kill?: False
- Non-fakeable core: Deterministically detect missing, duplicate, and unrecognized identifiers and groups outside three to five, then replay the saved input to the same result.
- Minimum completion/proof loop: Validate a synthetic four-four-three allocation, introduce an invalid two-person group and a duplicate or missing identifier, save the inputs and result, and replay them.
- Dependencies: Host approval, four eligible team members, and attendance in London remain unconfirmed., A complete and accurately entered roster and allocation for real coordinator use., Confirmation of the actual submission process and cutoff.
- Notes: A synthetic replay establishes validator behavior, not coordinator access or real-world usefulness. A passing allocation does not verify individual eligibility. The available build window is unspecified.

## mut-r1-01-evidence-patch
- Delivery risk: **high**
- Kill?: False
- Non-fakeable core: Distinguish supported corrections from unresolved claims beyond the scripted example, preserve the original and source, and apply or reverse a patch only after confirmation.
- Minimum completion/proof loop: Use direct, conflicting, and ambiguous excerpt cases; apply and reverse a supported correction, and verify that an ambiguous deadline claim remains unchanged.
- Dependencies: Host approval, four eligible team members, and attendance in London remain unconfirmed., Reliable interpretation of arbitrary claims and excerpts, including ambiguous or conflicting evidence., Confirmation of the actual submission process and cutoff.
- Notes: General semantic support classification is the main delivery risk: a human-confirmed or narrowly constrained workflow is more credible than an unsupported automated verification claim. Preserve the operator-supplied cutoff as a separate operational constraint while noting that the official page identifies 20:30 UTC as event end.
