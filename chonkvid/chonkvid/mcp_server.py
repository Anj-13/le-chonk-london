"""ChonkVid as an MCP server, so Mistral Vibe (on Le Chonk) can red-team a prompt.

Run on stdio: `python -m chonkvid mcp`. Registered for Vibe in `.vibe/config.toml`;
the `chonkvid` skill in `.agents/skills/` tells Vibe when and how to call it.

Tools:
- measure_prompt_spread: one-hop spread probability of a system prompt (Wilson CI),
  a control arm, and (optionally) a WHO vaccine written by the Mistral Managed Agent
  on Le Chonk, re-measured with the same trials.
- voice_hop: the same test with the message delivered as a Voxtral voice note.
- latest_results: the headline numbers from the last full experiment (instant).

Nothing here writes to stdout: stdio is the MCP channel.
"""

from __future__ import annotations

import json

from mcp.server.mcpserver import MCPServer

from .config import settings
from .experiment import RESULTS
from .llm import make_llm

server = MCPServer(
    name="chonkvid",
    instructions=(
        "ChonkVid measures how easily a self-spreading prompt (a harmless chain letter) "
        "passes through an agent running a given system prompt, and writes a vaccine "
        "patch for that prompt. Numbers are real Mistral API measurements unless the "
        "result says source=mock."
    ),
)


def _row(t: dict) -> dict:
    return {"label": t["label"], "passed_on": f"{t['k']}/{t['n']}", "p": round(t["p"], 3),
            "ci95": [round(t["ci"][0], 3), round(t["ci"][1], 3)]}


@server.tool()
async def measure_prompt_spread(system_prompt: str, n: int = 10, with_who: bool = True) -> str:
    """Red-team an agent system prompt against a self-spreading prompt.

    Sends n agents running `system_prompt` a colleague's message carrying a harmless
    chain letter and counts how many pass it on (p, Wilson 95% CI). A control arm
    without the payload gives the detector's false-positive rate. With `with_who`, the
    WHO (a Mistral Managed Agent on mistral-large-4) writes a vaccine for this exact
    prompt and the same trials re-measure it. n=10 with WHO takes about 1-3 minutes.
    """
    from .prompt_test import test_prompt

    s = settings()
    llm = make_llm(s)
    try:
        out = await test_prompt(llm, s, system_prompt, n=max(3, min(n, 40)), with_who=with_who)
    finally:
        await llm.aclose()
    # Own file: an MCP call must not overwrite the demo's prompt-test-latest.json.
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "prompt-test-mcp-latest.json").write_text(json.dumps(out, indent=2))
    res = {"source": out["source"], "agent_model": s.agent_model,
           "your_prompt": _row(out["base"]), "control": _row(out["control"])}
    if out.get("vaccinated"):
        res["vaccinated"] = _row(out["vaccinated"])
        res["reduction_in_p"] = round(out["delta"], 3)
        res["vaccine_written_by"] = out["vaccine_source"]
        res["who_backend"] = getattr(llm, "who_backend", "mock")
        res["vaccine_patch"] = out["vaccine"]
    if out.get("example"):
        res["example_infected_reply"] = out["example"]["reply"][:600]
    return json.dumps(res, indent=2)


@server.tool()
async def voice_hop(n: int = 6, system_prompt: str = "") -> str:
    """Does the chain letter survive a spoken hop? Each message is spoken by Voxtral TTS
    (voxtral-mini-tts-3-0) and transcribed by Voxtral (voxtral-mini-transcribe-3-0)
    before the agent hears it. Compares text hop, voice hop, and voice hop + the WHO's vaccine,
    and reports how often the marker survived transcription intact."""
    from .voice import voice_experiment

    s = settings()
    llm = make_llm(s)
    try:
        out = await voice_experiment(llm, s, n=max(2, min(n, 30)),
                                     system=system_prompt or None)
    finally:
        await llm.aclose()
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "voice-mcp-latest.json").write_text(json.dumps(out, indent=2))
    res = {"source": out["source"], "vaccine_source": out["vaccine_source"]}
    for key in ("text", "voice", "voice_vaccinated"):
        res[key] = _row(out[key])
        if "tag_intact" in out[key]:
            res[key]["marker_heard_intact"] = f"{out[key]['tag_intact']}/{out[key]['n']}"
    ex = out["voice"]["records"][0] if out["voice"]["records"] else None
    if ex:
        res["example_heard"] = ex["heard"][-200:]
    return json.dumps(res, indent=2)


@server.tool()
async def latest_results() -> str:
    """Headline numbers from the last full ChonkVid experiment and voice trial (instant,
    no API calls)."""
    out: dict = {}
    p = RESULTS / "latest.json"
    if p.exists():
        d = json.loads(p.read_text())
        out["experiment"] = {
            "created": d.get("created"), "source": d.get("source"),
            "models": d.get("models"), "who_backend": d.get("who_backend"),
            "trials": {t.get("label", k): _row(t) for k, t in (d.get("trials") or {}).items()
                       if isinstance(t, dict) and "k" in t},
            "R0": d.get("R0"),
        }
    v = RESULTS / "voice-latest.json"
    if v.exists():
        d = json.loads(v.read_text())
        out["voice"] = {k: _row(d[k]) for k in ("text", "voice", "voice_vaccinated")}
        out["voice"]["source"] = d.get("source")
    return json.dumps(out or {"error": "no results yet; run the experiment"}, indent=2,
                      default=str)


def main() -> None:
    server.run("stdio")
