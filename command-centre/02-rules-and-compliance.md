# 02 — Rules & Compliance

**Last verified: 2026-11-21 09:00** (official kick-off page, pasted at the venue). Source: https://luma.com/le-chonk-in-london. Mistral
published very little in the way of rules. Anything not on the page is marked UNKNOWN
and goes on the check-in question list below.

## Kick-off page (official, 21 Nov 09:00)
| Item | Detail |
|---|---|
| Submission | **project + demo video by 18:00** |
| Judging | submissions split into groups; **5-minute live presentation to a jury**, any format |
| Finals | jury picks finalists, who present to everyone (5 min); winners ~20:30 |
| Jury | Mistral engineers, SWEs, TPMs, AI scientists |
| Schedule | 09:00 breakfast & kickoff · 12:00 lunch · 16:00 snacks · 18:00 submissions due · 18:15 drinks · ~20:30 winners |
| Team | 3–5 required |
| Credits | 3 months Pro + extra API credit via redeem codes (on the kick-off page; not stored here). Credits work in Vibe CLI only with an API key from console.mistral.ai |

**Prizes and tracks**
| Track | Brief | Prize |
|---|---|---|
| Overall | Track_01 "Anything goes": build around Mistral Vibe and **Le Chonk (= Mistral Large 4)**: agents, skills, MCPs, scheduled tasks. Ambitious, creative, impactful | £3,000 / £2,000 / £1,000 credits |
| Bonus_02 | **Use Mistral Agents and/or Workflows, and tell the judges where and how** | +£500 credits for event winners who do |
| Special_03 | Best use of Voxtral | £250 credits |

**What this changes for ChonkVid**
- Record the demo video before submitting (target recorded by 17:15, submit 17:45).
- The pitch is 5 minutes, not 90 seconds: the 90-second arc becomes the demo
  segment inside a 5-minute talk (problem, live demo, measured numbers, honest limits).
- Le Chonk is Mistral Large 4: the WHO agent runs on `mistral-large-4` explicitly.
- Bonus_02: run the WHO agent through Mistral Agents so it qualifies, and name it in the pitch.
- Voxtral: not a fit for the core build; skip unless time is left.

## Judging
- Rubric: no scored rubric was published at kick-off; the track brief asks for
  "ambitious, creative and impactful". Judges are Mistral engineers, SWEs, TPMs and AI scientists.
- **Best proxy (same organiser, Sydney edition of the worldwide hackathon):**
  technical depth, creativity, usefulness, quality of demo, alignment with objectives,
  equally weighted. Treat these five as the rubric until told otherwise.
- **On-record judge signals:** "the teams that won had thought hardest about the user
  problem and about safety" (NYC judge). Iterate (the operator) wants a clear problem,
  a defensible technical approach, measured evidence of improvement, and a demo anyone
  can understand.

## Known rules (from the official page)
| Rule | Detail |
|---|---|
| Age | 18+ |
| Team size | 3–5 people |
| Entry | free, approval required |
| Build window | hack time 10:00–18:00; **submission hard stop 18:00** |
| Deliverable | a working app, not slides (email) |
| Attendance | in person only; arrive by 08:30, spot may be released after 08:45 |
| Bring | laptop, charger, Luma QR, ID |

## UNKNOWN: ask at check-in (first thing, before writing code)
1. Can code prepared beforehand be used? **We have a scaffold** (`chonkvid/`, built the
   night before). Disclose it first thing and follow the answer.
2. ~~Submission format~~ ANSWERED: project + demo video by 18:00 (exact form/link: ask).
3. ~~Pitch length~~ ANSWERED: 5 min live to a jury group; finalists 5 min to everyone.
4. ~~Required models~~ ANSWERED: build around Vibe and Le Chonk (Mistral Large 4).
5. ~~Side awards~~ ANSWERED: Agents/Workflows bonus £500, Voxtral £250.
6. Rate limits on the event credits (credits themselves are confirmed).
7. Must the repo be public, and is there a licence requirement?

## Compliance checklist
| # | Item | Status | Owner |
|---|---|---|---|
| 1 | Luma ticket approved | **DONE** (acceptance email) | — |
| 2 | Team of 3–5 confirmed | OPEN | You / on the spot |
| 3 | Event credits redeemed + real rate limits checked | at check-in (link shared on the day) | You |
| 4 | Check-in questions 1–7 answered | at doors | Pitch lead |
| 5 | **Scaffold prepared 20–21 Nov night** (sim, mock mode, dashboard in `chonkvid/`); disclose to mentors at check-in and ask if it's OK; if not, rebuild live from the design | at check-in | You |
| 8 | Project submitted before 18:00 hard stop | planned (submit by 17:45) | Pitch lead |
| 9 | Joined Discord (discord.gg/mistralai) | OPEN | You |
| 10 | Demo video recorded and attached to the submission | OPEN (by 17:15) | Pitch lead |
| 11 | Mistral Agents used and named in the pitch (Bonus_02) | planned: WHO agent | Team |
| 6 | Mistral models load-bearing in the build | planned (Ministral, mistral-embed, Le Chonk) | Team |
| 7 | Safety framing stated in the first sentence of the pitch | planned | Pitch lead |
