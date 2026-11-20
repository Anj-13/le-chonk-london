# 13 — Submission Package & Final QA

**Updated 2026-11-05.** All text below is paste-ready for the lablab submission form.

## Submission form copy (paste-ready)

**Project title:** Airlock — sandboxed AI data analysis with containment receipts

**Short description (≤ 200 chars):**
> Sensitive-data analysis where the AI's code runs in a jail, not on your servers. Every task ends with a tamper-evident containment receipt.

**Long description:**
> Companies want AI-analyst productivity but cannot risk AI-analyst behaviour: model-generated code can delete files, fork-bomb, or quietly exfiltrate the dataset it was asked to analyse. Sandboxes alone don't fix trust — E2B and the commercial interpreters isolate, but none *prove* what happened. **Airlock's product is the proof: verifiable containment.**
>
> Upload a CSV, ask a question in plain English. An LLM (via Vultr Serverless Inference) writes pandas code, and that code executes inside a sealed per-task sandbox on a Vultr VM: no network, 256 MB memory cap, 0.5 CPU, 64-process cap, read-only rootfs, all Linux capabilities dropped, gVisor userspace kernel. The container is force-removed after every single run.
>
> Every task ends with a **containment receipt** — a SHA-256-chained event log of what the model decided, what code executed, what was blocked, and proof the sandbox was destroyed. Edit one event and on-screen verification fails. For the compliance team, that's an audit trail, not a promise.
>
> **Attack Mode** runs `rm -rf /`, fork bombs, memory bombs, exfiltration attempts and a 2 GB zip bomb through the exact same jailed pipeline (nothing is special-cased). All five are absorbed, logged, and the service health-checks green on camera.
>
> **Who this is for:** engineering and security leads at regulated organisations — fintech/health analytics teams, MSPs — who want agent productivity without agent risk, self-hosted on their own Vultr VM with a cryptographic audit trail.
>
> Stack: one Vultr VM (FastAPI + Docker + gVisor), all LLM calls via Vultr Serverless Inference (OpenAI-compatible `tools[]`, fallback model chain, 429/504 backoff), a second vision model QA-checks every chart. MIT licensed.

**Technology tags:** `vultr`, `serverless-inference`, `docker`, `gvisor`, `fastapi`, `python`, `sandbox`, `ai-agents`, `security`, `pandas`

**Category tags:** AI Agents · Developer Tools · Security

## Required attachments checklist
| # | Item | Status | Location |
|---|---|---|---|
| 1 | Cover image | ✅ BANKED | `airlock/demo/cover.png` (1280×720) |
| 2 | Slide presentation (PDF) | ✅ BANKED | `airlock/demo/airlock-slides.pptx` → **export to PDF before upload** |
| 3 | Video presentation | ⬜ Record Nov 7 PM (script ready: `airlock/demo/VIDEO_SCRIPT.md`) — must include containment moment, 3–5 min, MP4 |
| 4 | Public GitHub repo | ✅ code complete — push to public GitHub before submission |
| 5 | Application URL | ⬜ after VM deployment (RUNBOOK ready) |
| 6 | Demo platform field | fill: "Vultr VM (self-hosted)" |
| 7 | README with Vultr usage | ✅ BANKED (`airlock/README.md`) |
| 8 | MIT LICENSE | ✅ BANKED |

## Final pre-submission audit (run Nov 8 AM, ~15 min)
- [ ] `/health` shows `docker:true`, `sandbox_runtime:runsc`, `inference_configured:true`
- [ ] Public URL loads in incognito (no VPN), workbench + attack pages render
- [ ] One real analysis on the demo CSV through the **public URL**; answer + chart present
- [ ] All 5 attack payloads re-run on the VM: verdict ABSORBED each time
- [ ] Receipts page: chains verified (no INVALID)
- [ ] `docker ps` shows no airlock-* containers between runs
- [ ] Video: 3–5 min, contains ≥1 containment moment, URL bar visible, captions readable, MP4 ≤ limits
- [ ] Slides PDF opens; cover image uploads; tags set
- [ ] Repo public, MIT LICENSE visible, README renders (architecture + Vultr usage sections)
- [ ] Submitted on lablab **before the confirmed deadline**; screenshot proof of submission
- [ ] All links re-clicked from a judge's perspective (fresh incognito profile)

## Test evidence (as of 2026-11-05)
- `backend/tests/gate_sandbox.py` — **11/11** containment checks pass
- `backend/tests/gate_inference.py` — **8/8** client-logic checks pass (mocked HTTP)
- Attack mode E2E over HTTP — **5/5 ABSORBED** (rm-rf, fork bomb, memory bomb, exfil, zip bomb), receipts chain-verified
- Task flow E2E over HTTP — SSE timeline streams, result + receipt 200s
