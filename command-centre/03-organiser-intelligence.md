# 03 — Organiser Intelligence (Mistral AI)

**Assembled 2026-11-20.** Labels: **Verified** (official page or on-record quote),
**Inference** (our reading, not stated by Mistral).

## Who runs it
- **Mistral AI / Mistral Events** host and are the sole sponsor (Verified).
- Iterate operated the Feb 2026 worldwide hackathon and published its standout
  projects (Verified). Whether Iterate runs this London one-day is UNKNOWN.

## What Mistral wants from the day
| Goal | Label | What it means for us |
|---|---|---|
| Show Le Chonk and Ministral doing something only their models make practical | Inference | Make Mistral models the experiment itself, not a logo on a wrapper |
| Hiring signal | Verified (profiles go to their hiring team) | Clean engineering, honest measurement and a sharp Q&A matter as much as the prize |
| Agent-building on their stack | Inference | Real multi-agent calls through La Plateforme |
| Developer adoption of Mistral Vibe | Inference (it is in the event name) | Build with the Vibe CLI and say so in the pitch |

## What their judges have rewarded (worldwide edition, Feb 2026)
- Population-scale agent systems (Mistralverse, global winner, London team).
- Safety made explicit and measured (Ministral-3B-Sec showcased; prompt injection
  named among the limitations strong projects tackled).
- Numbers with baselines (Hydra Ministral: 1.33x speed-up, ~60% token acceptance).
- Verification separated from generation (Lean Agent: a compiler as judge).
- Execution over ideas (Sydney edition, on record); originality as the separator
  once AI lowered the build bar (Tokyo winner's lesson).

## What the judges will know (prepare for it)
AI scientists in the room may know the prior work on self-spreading LLM payloads:
- **Morris II / "ComPromptMized"** (Cohen, Bitton, Nassi, 2024): a self-replicating
  prompt worm through GenAI email assistants.
- **"Agent Smith"** (Gu et al., ICML 2024): one adversarial image spreads an infectious
  jailbreak through up to a million multimodal agents exponentially fast.

- **Prompt Infection** (Lee & Tiwari, arXiv 2410.07283, Oct 2024; verified 21 Nov): self-replicating prompts across interconnected agents, plus an "LLM Tagging" defence. https://arxiv.org/abs/2410.07283 **This is the closest prior art**: same attack, multi-agent setting, a defence.

Our answer: they showed that spread happens. We measure transmissibility on Mistral
models and show which interventions work, including targeted versus random hardening
at the same dose. Cite both papers ourselves before a judge does. (Morris II and Agent Smith
citations are from memory: check before putting them on a slide. Prompt Infection is verified.)
