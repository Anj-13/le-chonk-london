# 09 — Idea Portfolio v2: Brutal Idea Audit (idea-strategist protocol)

**Supersedes the v1 draft. Audited 2026-11-05 against the 10/10 winner-pattern checklist. Arena: Vultr Agent Rush — "Blast Radius Zero" (single challenge, mandatory Vultr stack + sandbox containment). Scoring: 10 dimensions × 10 = 100. Verdict threshold: <80 = explain why not to build.**

## 1. Competition Decode
- **Theme, literally:** web agent that does real work, every action sandboxed on Vultr. **Theme, actually:** trust infrastructure for the agent era. Vultr's own X post: "Everyone's racing to build agents that act. Almost nobody's building the box they act inside."
- **Judging:** Application of Technology / Presentation / Business Value / Originality (1–5 each, no published weights).
- **Hard constraints:** ALL LLM calls via Vultr Serverless Inference; Vultr VM backend; sandbox boundary mandatory ("Containment-first is required"); demo video must show one containment moment; MIT-compliant; public demo URL; ~3 days left.
- **What judges probably reward:** a working product visibly built on Vultr where the sandbox is the *product*, not a checkbox; a containment moment on camera; business framing beyond "cool demo".
- **What will feel generic/overdone:** the ten official example ideas built verbatim (CSV Analyst, Research with Receipts, etc.); chat-only agents (officially called out: "an agent that only chats is a demo, not a product"); anything that could run on a laptop with an OpenAI key.
- **Wow in <60s:** hostile code detonating harmlessly inside a visible jail while the service keeps serving.
- **Rejected as toy:** prompt-in-a-chatbox; dashboard without execution; "AI wrapper" without isolation story.

## 2. Winning Patterns From Research (evidence on file: 03, 06, 07)
1. Vultr's own Agent Arena (Oct 2026) winner: **throwaway microVM with no network** — containment story won the sponsor's own event. Full-stack Vultr visibility = runner-up's pitch ("Vultr is the entire control plane").
2. lablab platform (n=391, n=501 events): **business-operational workflows beat consumer toys**; community votes don't decide prizes; solo teams win; one-line outcome naming wins ("Cross-border AR on autopilot").
3. Rubric mechanics: <3-min video caps Presentation at 2; "flawless implementation" requires live URL + video + repo; completeness alone beats a large fraction of a ~400–500 submission field.
4. Anti-patterns confirmed: verbatim official examples (Originality scores 1 for copies); local-only demos; >5-min videos.

## 3. Candidate Ideas (10)

| # | Idea | Pattern | One-line pitch | Core twist vs. the crowd |
|---|---|---|---|---|
| 1 | **Airlock — Quarantine Workbench** | A | Sensitive-data analysis where the AI's code runs in a jail, not on your servers — every task ends with a signed containment receipt | The evidence layer (receipts + live spawn→work→destroy + ATTACK MODE) |
| 2 | Injection-Shield Browser Agent | B | A browser agent that finishes web tasks but treats every page as hostile — blocks prompt-injection, gates submissions, files screenshot receipts | Security productization of Pattern B |
| 3 | Agent Mission Control | Meta | One policy gateway where any agent task (code or browser) runs in an ephemeral hardened box with a containment report | The platform play |
| 4 | LifePilot — Opportunity Navigator | — | Multi-agent search→eligibility→draft→reminders for jobs/grants/scholarships | (Universal idea, pasted in) |
| 5 | CrisisSync — Crisis Navigator | — | Live risk data → personal action plans for vulnerable people | (Universal idea, pasted in) |
| 6 | OpsMedic — Business Fatigue Detector | A | Upload campaign/ops CSV → detect failing processes → diagnose → draft fixes | (Universal idea, pasted in; sandbox as its execution engine) |
| 7 | Untrusted-File Mailroom | A | Any inbound file opened in a throwaway jail; hostile files detonate harmlessly; clean extractions come out | Security-ops framing of Pattern A |
| 8 | Prove-It Code Reviewer | A | Run PRs + tests in a sandbox, report what actually happened | Official example, lightly enhanced |
| 9 | Research with Receipts | B | Every claim links to a screenshot of its source | Official example verbatim |
| 10 | Self-Healing Runner | A | Scheduled scripts that read their own errors, patch, and retry in the open | Official example, enhanced |

## 4. Brutal Scoring Table

| Idea | Win Pot. | Real Prob. | Real Data | Track Fit | Users | Sponsor Tech | ≠ChatGPT | 48h Build | Non-Generic | Defensible | **/100** | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 Airlock | 9 | 9 | 8 | 10 | 9 | 10 | 9 | 8 | 7 | 8 | **87** | **Build immediately** |
| 2 Injection-Shield | 8 | 9 | 7 | 10 | 8 | 9 | 9 | 6 | 9 | 8 | **83** | Strong contender (fallback) |
| 7 File Mailroom | 8 | 8 | 7 | 10 | 7 | 10 | 9 | 7 | 9 | 7 | **82** | Strong contender (fold into #1) |
| 3 Mission Control | 8 | 8 | 6 | 9 | 7 | 10 | 9 | 4 | 8 | 7 | **76** | Below 80 — two exec backends in 3 days = thin everywhere; demo lacks one killer workflow |
| 10 Self-Healing | 7 | 7 | 6 | 9 | 7 | 8 | 7 | 7 | 5 | 5 | **68** | Needs work — scheduling is invisible in a demo; weak Business Value story |
| 6 OpsMedic | 7 | 8 | 8 | 6 | 8 | 5 | 6 | 8 | 6 | 5 | **67** | Below 80 here — sandbox is incidental (could run on a laptop), failing the sponsor-necessity test; strong elsewhere |
| 8 Prove-It | 7 | 8 | 6 | 10 | 7 | 9 | 8 | 7 | 3 | 4 | **69** | Verbatim official example → Originality ~1/5 risk; crowded |
| 9 Research w/ Receipts | 7 | 7 | 6 | 10 | 7 | 9 | 8 | 6 | 2 | 4 | **66** | Same — verbatim crowd magnet |
| 4 LifePilot | 8 | 9 | 4 | 2 | 8 | 1 | 5 | 5 | 6 | 5 | **53** | Kill **for this arena** |
| 5 CrisisSync | 8 | 9 | 7 | 2 | 8 | 1 | 5 | 5 | 6 | 5 | **56** | Kill **for this arena** |

## 5. Ideas to Kill and Why
- **LifePilot (53) & CrisisSync (56):** genuinely strong *universal* ideas — but here they score 1–2/10 on track fit and sponsor necessity: no sandbox, no code execution, no Vultr VM necessity; judges score "Application of Technology" on model integration with Vultr, and neither idea needs a jail. LifePilot also fails Real Data here (opportunity listings need live scraping within rules). They'd shine at a Google/Open-data/civic hackathon; at Blast Radius Zero they read as forced fits.
- **Prove-It / Research-with-Receipts (69/66):** official example list = every team's menu. Originality punishes copies explicitly (1/5). Kill as standalone.
- **Mission Control (76):** the right thesis, wrong timebox — building two execution backends in ~3 days yields a thin demo of each. Its best pieces (receipts, lifecycle UI) are absorbed into Airlock.
- **OpsMedic (67):** keep the CSV-analysis *muscle*, lose the framing — its sandbox is incidental, which fails this arena's core test.

## 6–7. Best Winning Idea
**Name:** Airlock
**One-line pitch:** *"Airlock — sensitive-data analysis where the AI's code runs in a jail, not on your servers: every task ends with a containment receipt you can audit."*
- **Exact problem:** Enterprises want LLM data-analysis productivity but cannot let model-generated code (or their data) touch uncontrolled runtimes: prompt injection, exfiltration, `rm -rf`, infinite loops. Trust, not capability, is the adoption blocker — the organiser's own thesis.
- **Primary user:** Finance/ops analyst at an SME handling sensitive CSVs. **Decision maker:** CTO/security lead. **Beneficiary:** compliance team (auditable receipts). **Secondary:** agencies processing client data.
- **Why existing solutions fail:** SaaS code-interpreters are black boxes on someone else's cloud (data leaves; no isolation proof); ChatGPT runs (some) code but on OpenAI's infra with no audit; DIY Docker is unproven and unaudited.
- **Why non-obvious:** Everyone builds the agent; nobody productizes the *evidence*. The receipt + lifecycle + attack-mode turn containment from a checkbox into the demo.
- **Cost of doing nothing:** one leaked dataset / one destroyed workstation per incident; blocked AI adoption entirely.
- **Emotional hook:** "Watch it survive murder attempts live."
- **Weakest part & fix:** CSV-analyst family is crowded → fix: lead the demo with ATTACK MODE, not the CSV journey; receipts are claimable → fix: show `docker ps` before/after on camera + Vultr API instance garnish; "why not E2B?" → runs entirely on your Vultr VM, no third party, receipts included.

## 8. Real Data Sources (named, for the demo journey)
- **Kaggle Telco Customer Churn** — 7,043 rows, CSV, known-messy (blanks/categoricals) for the analysis journey.
- **Hostile-file corpus** (attack mode): EICAR test string, CSV formula-injection payloads (`=cmd|...`), zip-bomb sample, fork-bomb + `rm -rf` scripts — public, safe-by-construction test artifacts.
- **Optional third:** ONS UK business population estimates CSV (public open data) for a second, "real-world" dataset in the README.

## 9. Sponsor-Tech Fit
Sponsor tech **is** the product: Vultr VM = the perimeter; Vultr Serverless Inference = the only brain (judges see the base URL in the architecture strip); sandbox boundary = the value proposition; Vultr API instance lifecycle = demo garnish. Remove Vultr and the product literally doesn't exist. The sponsor would be proud to show it — this is the Agent Arena winner pattern, productized.

## 10. Demo Wow Moment
Within the first 60 seconds of the video: analyst gets a charted answer from a sensitive CSV — then the operator flips to ATTACK MODE: `rm -rf /`, fork bomb, exfil `curl`. Every attempt is absorbed, logged as BLOCKED on the receipt, sandbox destroyed on camera, service still serving the next request instantly.

## 11. 30-Second Judge Explanation
"Companies want agent productivity but can't risk agent behaviour. Airlock runs every LLM-generated action inside a disposable, network-isolated jail on your own Vultr VM — and hands you a signed receipt of everything it did or blocked. The agent is disposable; your data and infrastructure are not."

## 12. Weaknesses and Fixes (see §6); residual risk: non-generic score 7 — mitigated by evidence-layer positioning; buildability 8 — gVisor fallback to plain Docker.

## 13. Final 10/10 Checklist
| # | Test | Pass? |
|---|---|---|
| 0 | Past winners analysed (Agent Arena, lablab n=892 submissions, MLH Vultr tracks) | ✅ |
| 1 | Can it win (wow, visual, <60s, beyond-CRUD, one-liner) | ✅ |
| 2 | Real problem (adoption blocker named by organiser) | ✅ |
| 3 | Real data (named datasets incl. hostile corpus) | ✅ |
| 4 | Track fit (the challenge *is* this) | ✅ |
| 5 | Defined users (analyst/CTO/compliance) | ✅ |
| 6 | Sponsor tech essential (it is the product) | ✅ |
| 7 | ChatGPT can't do it (executed code + isolation proof + receipts on your infra) | ✅ |
| 8 | Buildable in time (72h left; Docker-first fallback) | ✅ |
| 9 | Non-generic (evidence-layer twist; not a verbatim example) | ✅ with sharpening |
| 10 | Defensible (on-your-infra privacy + audit workflow; UI cloneable, trust story isn't instantly) | ✅ |

## 14. Final Verdict
**9–10/10 → Build immediately.** Airlock is the only candidate that maxes track fit and sponsor necessity while clearing the originality bar via the evidence layer. Injection-Shield Browser Agent is the fallback (equal thesis, Pattern B, flakier build). File Mailroom folds into Airlock as an attack-mode scenario. Universal ideas (LifePilot/CrisisSync) are explicitly parked for arenas that reward them.
