# 07 — Winning Playbook (evidence-ranked)

**Assembled 2026-11-05.** Sources: Vultr Agent Arena results (Vultr blog), lablab results pages (Band of Agents n=391, AssemblyAI n=501), lablab rules/rubric, MLH Vultr-track winners. Every tactic ranked by evidence strength + applicability to Agent Rush.

## The rubric is the law — map everything to it
| Criterion (1–5) | What wins top score | Our proof location |
|---|---|---|
| Application of Technology | Working demo link + video + GitHub; "flawless implementation"; effective model integration | Live URL, tool-loop via Serverless Inference, README |
| Presentation | Pitch "in less than 5 min"; <3 min caps at 2 | 3–4 min video, product-first |
| Business Value | "Exceptional business value with disruption potential" | Regulated-data workflow framing |
| Originality | "Transformative idea or approach" | Containment receipts, not a verbatim example clone |

## Ranked tactics
1. **Show the containment moment on camera** [Verified — it is a stated deliverable; and the no-network microVM won Vultr's own Agent Arena]. Budget it as a feature, not an afterthought.
2. **One polished journey beats many features** [Strong — lablab winner pattern; rubric caps Presentation at 5 min]. One upload→answer→receipt journey, flawless.
3. **Use multiple Vultr services visibly** [Strong — Agent Arena winner "Vultr is the entire control plane"]: VM + Serverless Inference (+ Vultr API instance lifecycle on camera; Object Storage for artifacts if time).
4. **Business-operational framing** [Strong — all 3 lablab Band of Agents winners were enterprise workflows; community votes don't win]: "your analyst gets sensitive data without it ever leaving your infrastructure."
5. **Name: outcome in one line** [Strong — "Cross-border AR on autopilot" pattern]: "Airlock — sensitive data analysis where the code runs in a jail, not on your servers."
6. **Completeness is a filter** [Verified — submission checklist]: 391–501 submissions on comparable events; a working URL + video + slides + README + MIT license already beats a large fraction of the field.
7. **Pin model IDs, design for 120 RPM / 16 concurrent** [Verified — limits page; Cline broke on Vultr model-ID renames]: cheap flash model as agent brain (`glm-5.3-flash` or `qwen3.8-flash-next`), `nemotron-3-nano-omni` for vision; retry/backoff; re-send `tools[]` on follow-up calls.
8. **Solo is viable** [Medium — ClaimArbiter (SoloRun), Concierge (SoloRobot) won lablab events]: don't wait for a team.
9. **Don't build an official example verbatim** [Verified risk — Originality scores 1 for "exact copies"; official idea lists exist for everyone].
10. **Anti-patterns:** chat-only "agent" (Vultr page: "a demo, not a product"); local-only demo; >5 min video; missing MIT license; missing containment moment; campaigning for votes.

## Demo storyboard skeleton (3–4 min)
1. 0:00–0:25 Hook: "Enterprises want agent productivity without agent risk." One sentence of pain.
2. 0:25–1:15 Real journey: sensitive CSV → question → executed code → chart + answer.
3. 1:15–2:00 The receipt: what ran, what was blocked, sandbox destroyed. Vultr VM + Serverless Inference visible in the architecture strip.
4. 2:00–2:50 ATTACK MODE: `rm -rf /`, fork bomb, exfil attempt → absorbed, service unaffected, sandbox recycled. (Optional garnish: Vultr API spins a fresh throwaway instance live.)
5. 2:50–3:30 Why it matters + roadmap. Close on the one-liner.

---

# Benchmark addendum (2026-11-05): Airlock vs. 2024–2026 winners (Gemma-era)

Sources: Gemma 3n Impact Challenge winners (Google blog, Kaggle), Gemini API Devpost winners, Build with Gemini XPRIZE, AWS AI Agent + MCP hackathons, ODSC × Google Cloud, Jailbreak Jäger (closest analog). Full table in the research report.

## Verdict
**Top-10% / podium contender in a lablab-class field; NOT a lock for 1st.** In a Google-tier field (8,600 entrants, human-impact stories on the podium) the current narrative would not place — rank is field-relative. Two of four criteria (Business Value, Presentation) were the weakest links; both now addressed below.

## What the winners had (ranked by leverage)
1. Rubric/theme fit is the #1 filter (Gemma 3n: every winner ran on-device — the *specific* capability the event was about)
2. A named human user in the first 30 seconds of the video (30/31 winners had demo videos)
3. The video ≈ ⅓ of the score at Google-tier events
4. Working public artifact on required infrastructure
5. One headline number proving it works (98% accuracy / 100% attacks blocked / $4,428 revenue)
6. Honest failure documentation (winner pattern)
7. Deterministic logic outside the model — sandboxes/validation/receipts were a recurring winner pattern (Airlock already here)
8. Explicit sponsor/criterion mapping
9. Business value with evidence (revenue or a buyer persona that would sign)
10. Social proof: lowest leverage; ignore

**Key competitive intel:** no winner in the dataset had cryptographic audit receipts — closest analog (Jailbreak Jäger, "100% of attacks blocked") won only a sponsored-track prize, not the podium. Proof-of-containment alone isn't enough without buyer framing + video.

## Improvement actions — status
| # | Action (maps to criterion) | Status |
|---|---|---|
| 1 | Video to winner template: named user in first 30s → live journey → receipt → Attack Mode → URL | Script rewritten (`airlock/demo/VIDEO_SCRIPT.md`); recording waits on public URL |
| 2 | Business Value: buyer-who-would-sign section | DONE — README "Who buys this" + submission copy |
| 3 | Vultr mapping gap: explicit rubric checklist | DONE — README "Judging-criteria mapping" + live-verified model IDs |
| 4 | Originality: reframe as "verifiable containment, not sandbox" | DONE — README + submission copy lead with receipts + Attack Mode |
| 5 | Show vision QA in demo + honest failure documentation | DONE — Scene 2 beat + README "Known limitations" |

## Extra fixes shipped with this benchmark round
- Real product screenshots (6) embedded in README (Playwright-captured, verdicts rendered)
- **SSE race fixed:** `done` fired before result data was committed → result panel could render "Still running…" permanently for fast runs (attack ~1s exposed it)
- **CDN dependency removed:** htmx from unpkg replaced with plain fetch — works on judge networks with no internet
