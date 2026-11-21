# 07 — Winning Playbook (one-day, live-pitch, Mistral judges)

**Assembled 2026-11-20.** Ranked by how much each tactic moves the score.

## Honest odds
About 50–70 teams, so any team's top-3 base rate is about 5%. A clean, distinctive,
measured ChonkVid is roughly **15–25% for top 3 and about 10% for 1st** (rough). The
two things that move it most: a real measured result on screen by the 15:30 freeze, and
surviving the first hard technical question.

## Tactics, ranked
1. **Numbers before animation.** First screen: spread probability per contact with a
   confidence interval, R0, and targeted-vs-random vaccination at the same dose. Then
   the live network.
2. **Safety frame in sentence one.** "A safe sandbox: a harmless chain-letter payload,
   sim-local agents, the goal is measuring defences."
3. **Name the prior work yourself** (Morris II, Agent Smith; see 03) and state the
   difference: interventions and measured transmissibility on Mistral models.
4. **Claims you can defend.** Say "targeted hardening beats random at equal dose", not
   "provably minimal set". Optimal immunisation is NP-hard in general; a scientist
   will catch the overclaim.
5. **Live but safe.** Run a small live epidemic on stage; keep the full recorded run
   one click away.
6. **Named user.** A platform PM at a 12-person startup shipping 50 support agents next
   week with no security budget.
7. **Mistral is the experiment.** Ministral population, mistral-embed detection, Le
   Chonk WHO; built with Mistral Vibe.
8. **End on an artefact.** The vaccine system-prompt diff plus the guidance table
   (time to majority infection under each policy).

Rehearse during the 18:00–19:00 apéro: the app is already submitted by then, so the
live demo must run from the submitted version.

## 90-second demo arc
1. (0–10s) "Agents are a population now, and populations get epidemics. This is a safe
   sandbox." Numbers strip on screen.
2. (10–25s) Infect patient zero live; network lights up.
3. (25–45s) Curve rises; the WHO agent posts a situation report.
4. (45–70s) Vaccinate: random 30% versus targeted 30%. Targeted bends the curve; show
   the attack-rate difference.
5. (70–90s) Final frame: the vaccine prompt diff and guidance table. "Public health
   has a century of maths for this. We gave agent security the same playbook."

## Q&A prep (likely questions)
- "Isn't this Agent Smith?" See tactic 3.
- "Isn't this Prompt Infection (Lee & Tiwari 2024)?" "They showed prompts self-replicate across agents and proposed tagging. We put a number on it: per-contact spread probability with a CI for *your* system prompt on Mistral models, and we verify the vaccine with the same measurement."
- "Targeted beating random is textbook network epidemiology." "Yes, and that's the point: the textbook transfers. What's new is the measured transmissibility per prompt, which is the input the textbook needs."
- "How do you know an agent is infected and not just chatting?" Embedding similarity
  to the parent message, with the threshold shown and every verdict logged.
- "What is your sample size?" State the number of one-hop trials and the CI.
- "Would this happen in a real fleet?" Agents that read each other's output are the
  default in 2026; the per-contact rate is the number a team can measure on its own
  fleet with this harness.
- "Why Mistral?" Population cost: Ministral makes 1,000+ calls per run affordable.
