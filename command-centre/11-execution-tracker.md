# 11 — Execution Tracker (Airlock build)

**Updated: 2026-11-05, ~23:55 UK.** Repo: `airlock/` — 7 commits, **public at https://github.com/shahaman098/airlock**.

## Verified state (post-bottleneck-removal)
- ✅ **PUBLIC REPO LIVE** (graded requirement; secrets-audited before push)
- ✅ **All 4 chain model IDs verified against the LIVE Vultr catalog** (35 models listed: glm-5.3-flash, qwen3.8-flash-next, mimo-v2.6-flash, nemotron-3-nano-omni-30b-a3b-reasoning) — model-ID-churn risk eliminated at the catalog layer; only per-model tool support waits on the key
- ✅ Sandbox gate **11/11** · inference client gate **8/8** · **agent-loop integration gate 11/11** (real production code path, LLM mocked at HTTP only, incl. vision QA + unknown-tool handling)
- ✅ Attack mode **5/5 ABSORBED E2E over HTTP** (rm-rf, fork bomb, mem bomb, exfil, 2 GB zip bomb)
- ✅ **One-command deploy:** `./deploy/deploy.sh root@VM_IP` — installs Docker+gVisor, builds image, writes key from `backend/.env`, starts services, verifies health, prints the public URL. (`/opt/airlock` path bug and service-ownership bug found and fixed; shellcheck clean.)
- ✅ **Key onboarding is zero-thought:** paste key into `backend/.env` → `scripts/live_model_test.py` → per-model verdict table + proven chain written out. `.env` auto-loads into the app and every script.
- ✅ Submission package banked: slides (6/6 visual pass), cover.png, paste-ready form copy + final audit checklist (`13-submission-qa.md`), video script, README with Vultr usage, MIT license

## The ONLY remaining user actions (~10 minutes of user time)
1. **vultr.com signup** → claim $200 credits → create Inference API key → paste into `airlock/backend/.env`
2. **Provision VM** (High Frequency, 2 vCPU/4 GB, Ubuntu 24.04; firewall allow 22/80/443) → hand ZCode the IP (or the Vultr API key and ZCode provisions too)
3. **lablab registration + join Discord** → confirm the exact submission hour (event page schedule still "TBA" as of Nov 5 23:50 UK)

## The moment 1+2 land (Nov 6 plan, ~15 min of compute)
`live_model_test.py` (2 min) → tune system prompt on 2–3 real runs → `deploy.sh root@IP` (8 min) → public URL verified from incognito → real analysis + attack runs through the URL

## Nov 7
Freeze gate 12:00 → record video per `airlock/demo/VIDEO_SCRIPT.md` on the public URL (containment moment + URL bar visible) → slides → PDF → final audit per `13-submission-qa.md`

## Nov 8
Submit on lablab **before the confirmed deadline** → incognito re-check of every link → screenshot proof of submission

## Risk register (residual)
| Risk | Status |
|---|---|
| Model-ID churn | ELIMINATED at catalog layer (verified live tonight); runtime chain + pinning remains |
| Per-model tool support | Scripted one-liner on key arrival; fallback chain already in code |
| gVisor on VM | Auto-select with runc fallback built into install.sh + runtime detection |
| Deadline hour TBA | User action #3; worst case plan submits Nov 8 12:00 UTC |
| VM not provisioned in time | Demo-mode app + local recordings exist as fallback, but public URL is graded — VM is the priority |
