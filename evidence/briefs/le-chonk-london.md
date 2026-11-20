# Le Chonk in London: Mistral Vibe Hackathon

Source: https://luma.com/le-chonk-in-london (official page, verified 20 Nov 2026)
Announcement: https://x.com/MistralAI/status/2123418013278114139 (19 Nov 2026)

## Event identity

- Organiser and sole sponsor: Mistral AI (Mistral Events). First London edition of
  "Le Chonk" since their worldwide hackathon.
- Format: one-day, in-person, single-site hackathon. Saturday 21 Nov 2026,
  08:30 to 20:30 GMT, Fora - Chancery House, 53-64 Chancery Ln, London WC2A 1QS.
- Build window: roughly 12 hours including breaks; meals (breakfast, lunch,
  dinner) provided; team formation on the spot at 08:30 for solo arrivals.
- Eligibility: 18+, approval-required registration (reviewed by the Mistral team),
  teams of 3-5 people.
- Attendance: 238 going on Luma; room capacity in the low hundreds.

## Prize and judging

- Prizes (Mistral API credits, not cash): 1st $3,000, 2nd $2,000, 3rd $1,000.
- Judging panel: Mistral AI engineers, software engineers, TPMs and AI
  scientists (the hiring team also receives applicant profiles with consent).
- No public rubric. Typical one-day vibe-hack judging at sponsor-run events:
  originality of concept, technical execution within the day, quality and
  theatricality of the live demo, and depth of sponsor-API usage. Judges are
  practitioners: fake demos and thin wrappers are usually visible to them.

## Sponsor stack (what "load-bearing use of Mistral" means here)

- La Plateforme APIs: chat completions (Le Chonk flagship model, Ministral
  family for cheap high-volume calls, Codestral), embeddings (mistral-embed),
  function calling, and the Mistral agents scaffolding. Free tier exists on
  console.mistral.ai; an X reply hints at a credits redeem code LECHONK
  (unverified).
- Sponsor interest (inference, labelled as inference): showing off Le Chonk
  and Ministral at scale, agent-building on their stack, hiring signal,
  developer adoption. A project that makes Mistral models the star of the
  mechanism, not a wrapper logo, is the fit.

## Constraints that shape the build

- Everything demoed runs in one day on a laptop with free-tier API limits.
- Live pitch in front of Mistral staff; demo reliability beats feature count.
- Team: 3-5 builders (Python/FastAPI/LangGraph/RAG/React/TypeScript stack;
  prior wins: NVIDIA Hack for Impact London, Gemini Live Agent Challenge
  UI Navigators with Moonwalk, Open Agent Hackathon 2026 Track 02 1st).

## Existing seed idea from the team (stress-test this)

AgentDemic: an LLM-agent epidemiology sandbox. A population of Ministral
agents lives on a small-world contact network (households, workplace hubs,
one group chat as super-spreader venue). Patient zero receives a
self-spreading prompt payload (benign chain-letter instruction: include a
copy of this notice in your next message to a friend). Infection counts only
when an agent's own outgoing message carries a paraphrased copy (detected by
mistral-embed similarity, not string match). States S/E/I/R; every infected
agent paraphrases the payload so variant lineages emerge and can be drawn as
a phylogenetic tree. Interventions panel: testing+quarantine, masks (output
filtering strength), vaccination (hardened system-prompt patch, herd-immunity
threshold visible live at 1 - 1/R0), lockdown (edge removal), boosters. A WHO
epidemiologist agent on Le Chonk reads the epidemic log, writes situation
reports, estimates R_t, and synthesises the vaccine prompt from infection
samples. Two modes: full-LLM lab run that measures R0, then a calibrated
50k-agent city simulation. Framing: safe sandbox for quantifying
prompt-injection spread in agent swarms, public health as the playbook for
multi-agent security.
