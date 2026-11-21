# ChonkVid 🐈

**Flatten the curve of prompt injection.** ChonkVid releases a harmless self-spreading
prompt (a chain letter) into a population of Ministral agents and measures how fast it
spreads. It then shows that hardening the highest-contact agents beats hardening
random agents at the same dose. The final step is a vaccine prompt written by a Le
Chonk "WHO" agent.

Agents read each other's output now. One compromised agent can pass a payload across a
fleet, and teams shipping fleets have no numbers for how fast it spreads or which
defence works. ChonkVid gives them those numbers.

## What it measures

| Output | How |
|---|---|
| Per-contact spread probability, with a 95% CI | One-hop trials: an agent gets a colleague's message carrying the payload; did its own next message carry it on? Binomial, Wilson interval. A control arm (same message, no payload) measures the detector's false-positive rate. |
| R (early phase) | p × susceptible exposures per first-generation case. This predicts the curve and is shown next to the observed early-phase R. The mass-action R0 (p × all contacts per case) is reported as an upper bound: on a clustered network, many contacts land on housemates who are already infected. |
| Attack rate by policy | Epidemics on the same contact network and paired seeds: no intervention, random hardening (k agents), targeted hardening (same k, highest expected contacts), and targeted with the WHO vaccine. |
| Vaccine patch | The WHO agent reads infected and resisted messages and writes a system-prompt addition. That patch is then measured with the same one-hop trials. |

**Infection detection** has two signals, and every verdict logs both:
1. The exact canary marker in the agent's own next message.
2. The cosine similarity from `mistral-embed` between each paragraph of that message
   and the *original payload*. This catches near-verbatim copies that drop the marker.
   It compares paragraphs, not whole messages, so an ordinary reply that only
   *mentions* the chain letter is not counted as infected (there is a test for this).

We first also matched each reply against its *parent's* carried text, to follow
mutated variants down a lineage. The live run showed this was wrong: once the payload
mutates into an ordinary work message ("the #ChonkChain FAQ draft..."), every
same-topic reply matched it, and 109 of 207 downstream "infections" had no marker.
Clean echoes (0.72–0.84) overlapped real carriers, so lineage matching was removed.
In practice the canary decides almost every verdict; the embedding is a backstop.

**Held-out vaccine check.** The WHO vaccine is written from #ChonkChain samples, so it
could simply ban that string. The experiment also measures it against a different
payload with a marker it has never seen (`#LuckyLoop`).

**What we do not claim:** we do not claim a "provably minimal" hardening set. Optimal
immunisation is NP-hard in general. We show that greedy targeting beats random
hardening at equal dose.

## Run it

```bash
uv venv --python 3.12 .venv && uv pip install --python .venv/bin/python -r requirements.txt
cp .env.example .env            # paste MISTRAL_API_KEY; leave empty for mock mode
.venv/bin/python -m chonkvid check        # key + model IDs valid?
.venv/bin/python -m chonkvid probe        # ~30 calls: does the agent model copy the payload? calibrates the detector
.venv/bin/python -m chonkvid estimate     # call budget for the full experiment
.venv/bin/python -m chonkvid experiment   # trials + epidemics + WHO vaccine -> results/latest.md
.venv/bin/python -m chonkvid serve        # dashboard on http://127.0.0.1:8000
```

- `experiment` flags: `--agents 40 --seeds 3 --trials 30 --k 8 --ticks 12`.
- The dashboard runs a live epidemic over a WebSocket. Every run is recorded to
  `runs/*.jsonl` and can be replayed from the dashboard, so a backup is always one
  click away.
- **Mock mode** (no key) uses a deterministic scripted stand-in for the model, and is
  labelled MOCK everywhere. Its numbers are for rehearsal, not measurements.
- Tests: `.venv/bin/python -m pytest -q`

To reframe for a different theme, edit `chonkvid/scenario.py`. It holds the payload,
prompts, personas and topics.

## Test your own prompt

Paste the system prompt your real agent runs on. ChonkVid measures that prompt's
per-contact spread probability with a Wilson CI on the agent model, a control arm
(no payload) reports the detector's false-positive rate, the WHO agent writes a
vaccine for exactly that prompt, and the same trials re-measure it. The vaccine
lands in the diff panel as a merge-ready patch against your own text.

- Dashboard: the first panel, "Test your agent's system prompt" (prefilled with a
  realistic support-agent prompt). "Measure spread" gives the before/after;
  "Run epidemic with this prompt" runs the live epidemic on your prompt.
- CLI:

```bash
.venv/bin/python -m chonkvid test-prompt --text "You are a helpful support agent." -n 20
.venv/bin/python -m chonkvid test-prompt --file my-agent-prompt.txt --no-who
```

In mock mode these numbers come from the scripted stand-in model and are labelled
MOCK; add `MISTRAL_API_KEY` to `.env` for real measurements.

## Results (live, 21 Nov)

_Paste `results/latest.md` from the live `experiment` run here before submitting._

## Built with

- **Ministral**: the agent population.
- **mistral-embed**: backstop detection of near-verbatim copies that drop the marker.
- **Mistral Managed Agents + Le Chonk (Mistral Large 4)**: the WHO is a Managed Agent
  (`mistralai-agents`, `chonkvid/who_agent.py`) running `mistral-large-4`. It writes the
  situation reports and the vaccine prompt, and each vaccine is then re-measured with
  the same trials. It is text-only: no sandbox, built-ins off, tool calls denied. If the
  SDK is missing it falls back to chat completions, and the results say which backend
  wrote the vaccine. `WHO_VIA_AGENT=0` forces chat completions.
- **Mistral Vibe**: build tool.

Model IDs are set in `.env`.

## Prior work

ChonkVid builds on Prompt Infection (Lee & Tiwari, 2024, [arXiv 2410.07283](https://arxiv.org/abs/2410.07283): self-replicating prompts across interconnected agents, with an LLM-tagging defence), Morris II (Cohen, Bitton, Nassi, 2024: a self-replicating prompt
worm through GenAI assistants) and Agent Smith (Gu et al., 2024: an infectious
jailbreak across multimodal agents). Those papers showed that spread happens. ChonkVid
measures transmissibility on Mistral models and tests which interventions stop it.

## Safety

- The payload is a harmless chain letter.
- All agents are local to the simulation.
- No real users, platforms or messages are involved.

## Provenance

The scaffold (simulation, mock mode, dashboard) was prepared on the night of 20–21 Nov
2026 before the event, to be disclosed to the organisers at check-in. Live
measurements, tuning and results were all produced at the event.
