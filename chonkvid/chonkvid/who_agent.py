"""The WHO as a Mistral Managed Agent (Le Chonk, Mistral Large 4).

Every WHO call (situation reports, vaccine synthesis, the prompt test's vaccine) goes
through `LiveLLM.chat` with the WHO system prompt; when WHO_VIA_AGENT is on (default),
`LiveLLM` hands those calls to this module instead of plain chat completions.

The agent is text-only: no sandbox (so no file or shell tools), built-ins off, and
tool permissions set to deny. If the SDK is missing or a run fails, the caller falls
back to chat completions and records that in `usage.who_fallbacks`.
"""

from __future__ import annotations

import os

_AGENTS: dict[tuple[str, str], object] = {}


def available() -> bool:
    try:
        from mistralai import agents  # noqa: F401
    except Exception:
        return False
    return True


def _agent(model: str, instructions: str, api_key: str):
    key = (model, instructions)
    if key not in _AGENTS:
        os.environ.setdefault("MISTRAL_API_KEY", api_key)
        from mistralai import agents
        from mistralai.vibe_agents.sdk.authoring.types import Builtins
        _AGENTS[key] = agents.Agent(
            model=model,
            name="chonkvid_who",
            description="WHO for an agent fleet: situation reports and vaccine prompts",
            instructions=instructions,
            builtins=Builtins(skills=False, subagents=False, programmatic_tool_calling=False,
                              background_processes=False),
            permission_mode="deny",
        )
    return _AGENTS[key]


async def run(model: str, instructions: str, prompt: str, api_key: str,
              timeout: float = 300) -> tuple[str, str]:
    """One WHO turn. Returns (answer text, session id). Raises on any failure."""
    result = await _agent(model, instructions, api_key).run(prompt, timeout=timeout)
    text = getattr(result, "text", None)
    if not text:
        raise RuntimeError(f"WHO agent returned no text ({type(result).__name__}, "
                           f"stop_reason={getattr(result, 'stop_reason', None)})")
    return str(text).strip(), str(getattr(result, "session_id", "") or "")
