# 02 — Rules & Compliance Matrix

**Last verified: 2026-11-05.** Sources: Vultr Community event page, lablab.build event page, lablab.build/hackathon-rules.

## Judging rubric (lablab default; event page repeats same 4 criteria, no published weights)
Scored 1–5 per criterion unless event overrides (Vultr page shows none → assume default):

| # | Criterion | What top score (5) means | Our evidence plan |
|---|---|---|---|
| 1 | **Application of Technology** | Requires **working demo link + demo video + GitHub code**; "flawless implementation". Judges "how effectively the chosen model(s) are integrated" | Live demo URL on Vultr VM + all LLM calls via Vultr Serverless Inference, shown in video + README |
| 2 | **Presentation** | Pitch communicated "in less than 5 min" (score 2 if video < 3 min — aim 3–5 min) | Tight 3–4 min video, product-first, containment moment shown live |
| 3 | **Business Value** | "Exceptional business value" with disruption potential | Real workflow + quantified impact framing |
| 4 | **Originality** | "Transformative idea or approach"; exact copies score 1 | Not a chatbot wrapper; containment-first architecture as the differentiator |

⚠️ No official weights published → all four matter roughly equally. The Band of Agents results (391 submissions) show **community votes ≠ judging**; business-viable + polished presentation won.

## Submission requirements (verbatim-backed)
Submit **on the lablab platform** — "Important: Submit on LabLab for judging."
- Project title, short + long description, technology & category tags
- Cover image, **video presentation**, slide presentation (PDF)
- **Public GitHub repository** (Vultr usage documented in the README)
- Demo application platform + **Application URL** (public demo URL, "production-style, not local-only")
- **"One containment moment" shown in the video** (e.g., sandbox absorbing `rm -rf`, infinite loop, or a hostile web page)
- Projects "must be original and MIT-compliant" → **add MIT LICENSE to repo**

## Hard rules & disqualifiers
- Submissions close at event deadline + "a short grace period of five minutes". For failures, "contact the organizers before the deadline: only they can extend it for a team"
- Plagiarism, gaming votes, tampering, unauthorized automation → "immediate disqualification"
- Rule non-compliance → lower score or exclusion
- Organisers may participate but are prize-ineligible; participating mentors can't judge

## Compliance checklist
| # | Requirement | Status | Owner | Risk if missed |
|---|---|---|---|---|
| 1 | Registered on lablab.ai | NOT YET VERIFIED (user action) | You | Cannot submit |
| 2 | Joined lablab Discord (both required) | NOT YET VERIFIED (user action) | You | Cannot submit |
| 3 | Vultr VM as backend/orchestration | PLANNED | Build | Fails sponsor-requirement test |
| 4 | ALL LLM calls via Vultr Serverless Inference (api.vultrinference.com/v1) | PLANNED | Build | Fails sponsor-requirement test |
| 5 | Sandboxed execution (Docker recommended; never in app process) | PLANNED | Build | Fails challenge core ("Containment-first is required") |
| 6 | Public demo URL (production-style) | PLANNED | Build | Loses most of Application-of-Tech score |
| 7 | Demo video 3–5 min incl. containment moment | PLANNED | Demo | Score 2 cap on Presentation if <3 min; missing containment moment = misses stated deliverable |
| 8 | Vultr usage documented in public GitHub README | PLANNED | Docs | Sponsor-usage doubt |
| 9 | MIT LICENSE file in repo | PLANNED | Docs | "MIT-compliant" requirement |
| 10 | Slides (PDF) + cover image + tags | PLANNED | Demo | Incomplete submission |
| 11 | Exact submission time confirmed (page says "To be announced") | **OPEN — check Discord today** | You | Missed deadline |
| 12 | On-site approval criteria (unpublished) | OPEN — non-blocking (online judging decides prizes) | — | Only affects SLC showcase |

## Unknowns / conflicts
- Submission deadline hour + timezone: lablab event page schedule "To be announced"; Vultr page daily window 16:00–03:00 UTC. → Verify in Discord.
- On-site (SLC) selection criteria: unpublished. → Treat online submission as the real competition.
- Whether event overrides default 1–5 scoring: no override seen on event pages → assume default.
