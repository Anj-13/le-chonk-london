# 11 — Execution Tracker (ChonkVid, Sat 21 Nov 2026)

**Created 2026-11-20 night; re-timed 2026-11-21 01:45 to the official agenda** (hack
10:00–18:00, submission hard stop 18:00, pitches 19:00). App: `chonkvid/` (own git repo,
scaffold built 21 Nov 01:00–03:00, mock mode verified: 13 tests pass, dashboard runs).
Disclose the scaffold at check-in. **Live path untested until the credits key arrives.**
Update this file at every gate.

## Before doors (Sat 21 Nov morning)
- [x] Luma ticket approved (acceptance email, 20 Nov)
- [ ] Discord: join, react in #hackathon-access
- [ ] Luma QR on phone, **ID card**, laptop charged, charger packed
- [ ] Teammates confirmed (3–5), or form at 09:40
- [ ] Mistral Vibe CLI installed; Python env with fastapi, networkx, mistralai ready
- [ ] Leave in time to be at Chancery Lane by 08:20 (spot can be released after 08:45)
- Credits: access link shared on the day (no key needed tonight; LECHONK not needed)

## Build day gates
| Time | Gate | Done? | Notes |
|---|---|---|---|
| 08:30–09:00 | in by 08:30 with QR + ID; redeem credits; key into `chonkvid/.env`; `python -m chonkvid check` then `probe` | [ ] | limits: ____ · probe p: ____ |
| 09:00–09:20 | kick-off: write **theme + judging criteria** into 02 | [ ] | |
| 09:20–09:40 | **theme-fit check** (09): ChonkVid fits / reframe / Plan B; check-in questions to mentors | [ ] | |
| 09:40–10:00 | team formation; roles (10); pitch the plan in 60 s | [ ] | |
| 10:00–11:00 | tune payload wording + threshold from the probe; set RPS/concurrency to the limits; live dashboard run at N=20 | [ ] | |
| 11:00–12:00 | `python -m chonkvid experiment` (live) → results/latest.md; record a live run | [ ] | spread prob: ____ |
| 12:00–12:30 | lunch; **pivot check at 12:30** (09) | [ ] | stay / pivot |
| 12:30–14:00 | vaccination: targeted vs random at equal dose | [ ] | |
| 14:00–15:30 | WHO agent (Le Chonk) + vaccine prompt, re-measured | [ ] | |
| 15:30 | **scope freeze**; record the full backup run | [ ] | |
| 15:30–17:15 | polish, numbers strip, guidance table, README with results | [ ] | |
| 17:15–17:45 | **submit** (target 17:45; hard stop 18:00) + screenshot of the confirmation | [ ] | |
| 18:00–19:00 | apéro: rehearse the 90-second demo twice, run 13 QA | [ ] | |
| 19:00–21:00 | pitches to the judges and finals | [ ] | |

## Measured numbers (fill in on the day)
| Metric | Value | n | CI |
|---|---|---|---|
| Per-contact spread probability | | | |
| R0 (prob × mean contacts) | | | |
| Attack rate, no intervention | | | |
| Attack rate, random vaccination (X%) | | | |
| Attack rate, targeted vaccination (X%) | | | |
| Attack rate, after the WHO vaccine prompt | | | |
