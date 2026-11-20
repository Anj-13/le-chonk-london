# 10 — Project Architecture & Execution Plan: "Airlock" (primary concept)

**Created 2026-11-05 evening, day 3 of 5.** Build window remaining: ~3 days. Solo-first plan.

## One-liner
**Airlock — sensitive-data analysis where the AI's code runs in a jail, not on your servers.**
Upload a spreadsheet → agent writes Python → executed in a network-isolated, resource-capped, destroyed-after-every-task sandbox on Vultr → answer + chart + code + a signed **containment receipt**.

## Scope
- **Must-have:** CSV/JSON upload → plain-English analysis → executed code + chart; per-task sandbox (Docker+gVisor, no network, CPU/mem caps, timeout); containment receipt (actions, blocked events, lifecycle); live lifecycle UI; ATTACK MODE page (rm -rf / fork bomb / exfil → absorbed).
- **Winning feature:** the receipt + live spawn→execute→destroy visual (nobody else will productize the evidence layer).
- **Stretch (only if MVP done by Nov 7 morning gate):** vision QA of rendered chart (nemotron-omni); Vultr API throwaway-instance garnish in demo; Object Storage for artifacts.
- **Explicitly excluded:** multi-user auth/teams, payments, browser-use pattern, dataset persistence, more than one polished journey.

## Architecture (all on one Vultr VM, e.g. High Frequency 2 vCPU/4 GB ≈ $12/mo; $200 credits cover it)
```
Browser (React/Vite or plain HTMX) ──HTTP──▶ FastAPI (app on VM, port 443 via Caddy)
   │                                            │  never shares a process/netns with sandboxes
   │                                            ├─▶ Vultr Serverless Inference (api.vultrinference.com/v1)
   │                                            │     brain: glm-5.3-flash or qwen3.8-flash-next (tools[])
   │                                            │     vision: nemotron-3-nano-omni-30b-a3b-reasoning (stretch)
   │                                            ├─▶ Sandbox Manager: per task →
   │                                            │     docker run --runtime=runsc --network none \
   │                                            │       --memory 256m --cpus 0.5 --pids-limit 64 \
   │                                            │       -v /srv/tasks/<id>:/work:ro? (results via /out) \
   │                                            │       timeout 60s → capture stdout/artifacts → docker rm -f
   │                                            └─▶ Receipt Store (SQLite/JSON per task) + optional Object Storage
```
- API key lives only in the app's env; **never** enters the sandbox (secret hygiene box ticked and shown in receipt).
- All LLM calls from the app process → Serverless Inference (never from inside sandbox → also a containment talking point).
- Tool loop: `tools[]` = run_python, list_files, save_artifact; follow-ups re-send `tools[]`; retry/backoff on 429/504.
- Fallback sandbox if gVisor setup drags: plain Docker with the same caps (rules' letter satisfied); gVisor is the upgrade.

## Schedule (UK time; submission ~Nov 8, exact hour TBC → treat as Nov 8 12:00 UTC worst case)
| When (Nov 5) | Gate | Output |
|---|---|---|
| Tonight | Credits + VM up; `curl` Serverless Inference: models list, tool-call round-trip, vision ping | Environment proven; model IDs pinned |
| Tonight | Repo init (MIT LICENSE), FastAPI skeleton + docker run/destroy manager | Hello-sandbox: echo script runs in isolated container |
| Nov 6 AM | Tool loop + CSV analysis journey end-to-end locally | Upload→question→executed answer |
| Nov 6 PM | Deploy to VM + demo URL (Caddy+HTTPS); receipts + lifecycle UI | Production-style URL live |
| Nov 7 AM | **GATE: kill features, freeze scope** | MVP works from a cold browser session |
| Nov 7 PM | ATTACK MODE + gVisor upgrade; video (3–4 min) + slides + README | Submission package 90% |
| Nov 8 AM | Submit on lablab **before deadline**; verify links from incognito; buffer | Submitted with hours to spare |

## Risks
| Risk | L | I | Mitigation |
|---|---|---|---|
| Tool-calling flaky on chosen flash model | M | H | Test 3 models tonight; fallback hand-rolled JSON-tool loop; nemotron-omni known to support tools |
| gVisor install issues on Vultr VM | M | M | Plain-Docker fallback ready; gVisor is upgrade not blocker |
| 429/504 under demo load | M | M | Backoff; one user at a time in demo; multiple model fallbacks |
| Deadline hour TBA | M | H | Confirm in Discord tonight; submit Nov 8 AM regardless |
| rm -rf demo actually harms VM | L | H | gVisor/no-capabilities container; test attack scripts on VM before recording; never demo from host |
| Browser upload size edge cases | M | L | Cap 10 MB, validate, friendly error |

## Demo-day checklist inherits 02-rules checklist items 6–10.
