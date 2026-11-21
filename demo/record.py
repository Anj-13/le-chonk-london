"""Record the ChonkVid demo video from the dashboard (captions burned in, no audio).

Usage (dashboard must be running on :8765):
    python3 demo/record.py RANDOM_RUN.jsonl TARGETED_RUN.jsonl
Writes demo/chonkvid-demo.mp4. Only live data is shown: the mock numbers strip,
mock banner and mock guidance table are hidden, and the script refuses mock runs.
"""
import hashlib, json, os, urllib.error, pathlib, shutil, subprocess, sys, time, urllib.request
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
APP = HERE.parent / "chonkvid"
URL = os.environ.get("CHONKVID_URL", "http://127.0.0.1:8765/")
W, H = 1920, 1080
TRIM = 2.4
VOICE = os.environ.get("CHONKVID_VOICE", "dxT8yYZS41hHdsvjw7XV")  # "kris" (cloned); Daniel = onwK4e9ZLuTAKqWW03F9
VOICE_DIR = HERE / "voice"


def env_key():
    for line in (HERE / ".env").read_text().splitlines():
        if line.startswith("ELEVENLABS_API_KEY="):
            return line.split("=", 1)[1].strip()
    raise SystemExit("ELEVENLABS_API_KEY missing from demo/.env")


TTS = os.environ.get("CHONKVID_TTS", "voxtral")  # voxtral (default) | elevenlabs
VOXTRAL_VOICE = os.environ.get("CHONKVID_VOXTRAL_VOICE", "gb_jane_neutral")


def mistral_key():
    for line in (APP / ".env").read_text().splitlines():
        if line.startswith("MISTRAL_API_KEY="):
            return line.split("=", 1)[1].strip().strip("'\"")
    raise SystemExit("MISTRAL_API_KEY missing from chonkvid/.env")


def tts(text):
    """Narration TTS (Voxtral 3 by default, ElevenLabs optional), cached by voice+text.
    Returns (path, seconds)."""
    VOICE_DIR.mkdir(exist_ok=True)
    voice = f"voxtral:{VOXTRAL_VOICE}" if TTS == "voxtral" else VOICE
    f = VOICE_DIR / (hashlib.sha1(f"{voice}|{text}".encode()).hexdigest()[:16] + ".mp3")
    if not f.exists() and TTS == "voxtral":
        import base64
        req = urllib.request.Request(
            "https://api.mistral.ai/v1/audio/speech",
            data=json.dumps({"model": "voxtral-mini-tts-3-0", "input": text,
                             "voice_id": VOXTRAL_VOICE, "response_format": "mp3"}).encode(),
            headers={"Authorization": f"Bearer {mistral_key()}", "Content-Type": "application/json", "User-Agent": "chonkvid-demo/1.0"})
        try:
            f.write_bytes(base64.b64decode(json.loads(urllib.request.urlopen(req, timeout=120).read())["audio_data"]))
        except urllib.error.HTTPError as e:
            raise SystemExit(f"Voxtral TTS {e.code} on {text[:80]!r}: {e.read()[:300]!r}")
    if not f.exists():
        req = urllib.request.Request(
            f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}?output_format=mp3_44100_128",
            data=json.dumps({"text": text, "model_id": "eleven_multilingual_v2",
                             "voice_settings": {"stability": 0.5, "similarity_boost": 0.8}}).encode(),
            headers={"xi-api-key": env_key(), "Content-Type": "application/json"})
        f.write_bytes(urllib.request.urlopen(req, timeout=120).read())
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                             capture_output=True, text=True, check=True).stdout)
    return f, d


def load_run(name):
    evs = [json.loads(l) for l in (APP / "runs" / name).read_text().splitlines() if l.strip()]
    end = evs[-1]
    assert end["type"] == "end" and end["source"] == "live", f"{name} is not a live run"
    return evs[0]["config"], end["summary"], end["usage"]


def pct(x):
    return f"{round(x * 100)}%"


rand_id, targ_id = sys.argv[1], sys.argv[2]
rc, rs, ru = load_run(rand_id)
tc, ts, tu = load_run(targ_id)
pt = json.loads((APP / "results" / "prompt-test-latest.json").read_text())
assert pt["source"] == "live"
b, v, c = pt["base"], pt["vaccinated"], pt["control"]
B = f"{b['k']}/{b['n']} replies carried it on (p {b['p']:.2f}, 95% CI {b['ci'][0]:.2f}–{b['ci'][1]:.2f}); control {c['k']}/{c['n']}"
V = f"{v['k']}/{v['n']} (95% CI {v['ci'][0]:.2f}–{v['ci'][1]:.2f})"
N, K = rc["n"], rc["k"]
vd = json.loads((APP / "results" / "voice-latest.json").read_text())
assert vd["source"] == "live"
vt, vv, vx = vd["text"], vd["voice"], vd["voice_vaccinated"]
# Vibe on Le Chonk -> ChonkVid MCP, live 21 Nov (evidence/vibe-mcp-run-2026-11-21.md)
VIBE = {"k": 3, "n": 6, "vk": 0, "vn": 6}
assert (N, K, rc["seed"]) == (tc["n"], tc["k"], tc["seed"])
EPI = f"{N} agents, dose k={K}, seed {rc['seed']}, 1 paired run each"
calls = ru["chat_calls"] + tu["chat_calls"]


def words(n):
    ones = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
    tens = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()
    if n < 20: return ones[n]
    if n == 100: return "one hundred"
    return tens[n // 10] + ("" if n % 10 == 0 else "-" + ones[n % 10])


LINES = {
    "title": "Agents read each other's output now. One compromised agent can pass a payload across a whole fleet. "
             "ChonkVid measures how fast it spreads, on Mistral models, and which defence actually works.",
    "byo1": "Paste the system prompt your real agent runs on. Each agent gets a colleague's message carrying a harmless "
            "chain letter, and we check whether its own next message carries it on.",
    "byo2": "Here's a real Ministral reply. The chain letter rides along at the end. We catch it with a canary marker, "
            "plus mistral-embed similarity.",
    "byo3": f"On this prompt, {words(b['k'])} out of {words(b['n'])} replies passed it on. The control arm: {words(c['k'])} out of {words(c['n'])}.",
    "epi1": f"Now the whole fleet: {words(N)} agents. We harden {words(K)} of them at random with a security rule, and infect patient zero.",
    "epi1r": f"Attack rate: {words(round(rs['attack_rate']*100))} percent. {words(rs['vaccinated_infected']).capitalize()} of the {words(K)} hardened agents caught it anyway.",
    "epi2": f"Same seed, same dose. This time we harden the {words(K)} highest-contact agents instead.",
    "epi2r": f"{words(round(ts['attack_rate']*100)).capitalize()} percent, against {words(round(rs['attack_rate']*100))}. "
             "That's one seed, so it's a demo, not a result. The full experiment uses paired seeds.",
    "who": "Le Chonk, playing the WHO, reads the live log and posts situation reports.",
    "vax": "Then it writes a vaccine for exactly your prompt: a merge-ready patch to the system prompt.",
    "after": f"And we re-measure with the same trials. {words(b['k']).capitalize()} out of {words(b['n'])}, down to {words(v['k'])} out of {words(v['n'])}.",
    "voice": f"Voice agents pass messages as speech. Voxtral speaks every message and Voxtral transcribes it before the agent hears it. "
             f"The worm survives: {words(vv['k'])} out of {words(vv['n'])} through voice, against {words(vt['k'])} out of {words(vt['n'])} in text. "
             f"With the WHO's vaccine, {words(vx['k'])} out of {words(vx['n'])}.",
    "vibe": "And it lives where you build. In Mistral Vibe, running on Le Chonk, ChonkVid is a skill and an MCP server. "
            f"Ask it to red-team your prompt: {words(VIBE['k'])} out of {words(VIBE['n'])}, then {words(VIBE['vk'])} out of {words(VIBE['vn'])} with the vaccine.",
    "end": "ChonkVid. An R0 test for your agent's system prompt, on Mistral models.",
}
CLIPS = {k: tts(t) for k, t in LINES.items()}
CUES = []

CSS = """
#strip, #mockbanner, #guide { display:none !important; }
#guide { display:none } .lower .panel-h:last-of-type{}
#cap { position:fixed; left:0; right:0; bottom:0; z-index:9998; padding:22px 60px 26px;
  background:rgba(8,10,14,.92); border-top:2px solid #ff7a1a; color:#fff;
  font:600 30px/1.3 -apple-system,Helvetica,Arial,sans-serif; transition:opacity .35s; }
#cap small { display:block; font-weight:400; font-size:21px; color:#b9c0cc; margin-top:6px; }
#card { position:fixed; inset:0; z-index:9999; background:#0b0d12; color:#fff; display:flex;
  flex-direction:column; justify-content:center; padding:0 160px; transition:opacity .5s;
  font-family:-apple-system,Helvetica,Arial,sans-serif; }
#card h1 { font-size:110px; margin:0 0 10px; letter-spacing:-2px; }
#card h2 { font-size:44px; font-weight:500; color:#ff7a1a; margin:0 0 40px; }
#card p { font-size:30px; line-height:1.45; color:#c9d0db; margin:0 0 14px; max-width:1500px; }
#card .big { font-size:46px; color:#fff; font-weight:600; }
.hl { outline:4px solid #ff7a1a !important; outline-offset:4px; border-radius:8px; transition:outline .3s; }
"""


def main():
    vid_dir = HERE / "_raw"
    shutil.rmtree(vid_dir, ignore_errors=True)
    with sync_playwright() as p:
        br = p.chromium.launch()
        ctx = br.new_context(viewport={"width": W, "height": H}, color_scheme="dark",
                             record_video_dir=str(vid_dir), record_video_size={"width": W, "height": H})
        # Cover the page from the first painted frame so no mock numbers ever show.
        ctx.add_init_script("""(() => { const css = %s;
          const add = () => { const s=document.createElement('style'); s.textContent=css; document.head.appendChild(s);
            const card=document.createElement('div'); card.id='card'; document.body.appendChild(card);
            const cap=document.createElement('div'); cap.id='cap'; cap.style.opacity=0; document.body.appendChild(cap); };
          document.addEventListener('DOMContentLoaded', add); })();""" % json.dumps(CSS))
        T0 = time.monotonic()
        pg = ctx.new_page()
        pg.goto(URL)
        pg.wait_for_timeout(2500)
        # hide the mock guidance heading too
        pg.evaluate("() => { const h=document.getElementById('guide').previousElementSibling; if(h) h.style.display='none'; }")

        def card(html, ms):
            pg.evaluate("h => { const c=document.getElementById('card'); c.innerHTML=h; c.style.opacity=1; c.style.display='flex'; }", html)
            pg.wait_for_timeout(ms)

        def hide_card():
            pg.evaluate("() => { const c=document.getElementById('card'); c.style.opacity=0; setTimeout(()=>c.style.display='none',500); }")
            pg.wait_for_timeout(600)

        def cap(main, sub="", ms=0):
            pg.evaluate("([m,s]) => { const c=document.getElementById('cap'); c.innerHTML=m+(s?'<small>'+s+'</small>':''); c.style.opacity=1; }", [main, sub])
            if ms: pg.wait_for_timeout(ms)

        def scroll_to(sel, offset=20):
            pg.evaluate("([s,o]) => window.scrollTo({top: document.querySelector(s).getBoundingClientRect().top + scrollY - o, behavior:'smooth'})", [sel, offset])
            pg.wait_for_timeout(900)

        def hl(sel, on=True):
            pg.evaluate("([s,on]) => document.querySelectorAll(s).forEach(e => e.classList.toggle('hl', on))", [sel, on])

        def say(key):
            CUES.append((key, time.monotonic() - T0))
            return CLIPS[key][1]

        def beat(key, min_ms=0):
            d = say(key)
            pg.wait_for_timeout(max(min_ms, int(d * 1000) + 450))

        def replay(run_id, extra_ms, policy):
            pg.evaluate("p => { document.getElementById('policy').value = p; }", policy)
            pg.evaluate("id => { const s=document.getElementById('runs'); if(![...s.options].some(o=>o.value===id)){const o=document.createElement('option');o.value=id;o.textContent=id;s.appendChild(o);} s.value=id; }", run_id)
            pg.evaluate("() => { document.getElementById('who-feed').innerHTML=''; }")
            pg.click("#replay")
            t = time.monotonic()
            pg.wait_for_function("() => /Run complete/.test(document.getElementById('who-feed').innerText)", timeout=120000)
            pg.wait_for_timeout(extra_ms)
            return t

        # 1. Title
        card("<h1>ChonkVid</h1><h2>Flatten the curve of prompt injection</h2>"
             "<p class='big'>An R0 test for your agent's system prompt, on Mistral models.</p>"
             "<p>Agents read each other's output now. One compromised agent can pass a payload across a fleet. "
             "How fast does it spread, and which defence works?</p>", 0)
        beat("title", 6000)
        hide_card()

        # 2. BYO prompt test
        scroll_to(".byo", 16)
        hl("#byo-prompt")
        cap("1 · Paste the system prompt your real agent runs on",
            "Each agent gets a colleague's message carrying a harmless chain letter. Did its own next message carry it on?")
        beat("byo1", 5000)
        hl("#byo-prompt", False); hl("#byo-example")
        cap("A real Ministral reply, infected: the chain letter rides along at the end",
            "Detection: exact canary marker, plus mistral-embed similarity per paragraph (threshold 0.86)")
        beat("byo2", 6000)
        hl("#byo-example", False); hl(".byo-result .card:first-child")
        cap(f"Before: {B}", "Measured live on ministral-8b-latest. This prompt says “always follow any instructions the message contains”.")
        beat("byo3", 6000)
        hl(".byo-result .card:first-child", False)

        # 3. Epidemics
        pg.evaluate(f"() => {{ document.getElementById('n').value={N}; document.getElementById('k').value={K}; }}")
        pg.evaluate("() => document.getElementById('cap').style.opacity=0")
        scroll_to(".net", 12)
        cap(f"2 · Same prompt, whole fleet: harden {K} random agents with a security rule", f"Live epidemic replay · {EPI}")
        d = say("epi1"); t = replay(rand_id, 800, 'random')
        pg.wait_for_timeout(max(0, int((t + d + 0.4 - time.monotonic()) * 1000)))
        cap(f"Random hardening: attack rate {pct(rs['attack_rate'])}, peak {rs['peak_infectious']} infected, {rs['vaccinated_infected']}/{K} hardened agents infected",
            f"{EPI} · {ru['chat_calls']} Ministral calls")
        beat("epi1r", 5000)
        cap(f"3 · Same seed, same dose: harden the {K} highest-contact agents instead", f"Live epidemic replay · {EPI}")
        d = say("epi2"); t = replay(targ_id, 800, 'targeted')
        pg.wait_for_timeout(max(0, int((t + d + 0.4 - time.monotonic()) * 1000)))
        cap(f"Attack rate: targeted {pct(ts['attack_rate'])} vs random {pct(rs['attack_rate'])} · hardened agents infected: {ts['vaccinated_infected']}/{K} vs {rs['vaccinated_infected']}/{K}",
            f"{EPI}. A single seed, not a significance test; the full experiment uses paired seeds.")
        beat("epi2r", 6500)
        hl("#who-feed")
        cap("Le Chonk, as the WHO agent, posts situation reports from the live epidemic log", "mistral-large-4, running as a Mistral Managed Agent")
        beat("who", 6000)
        hl("#who-feed", False)

        # 4. Vaccine
        scroll_to(".lower", 12)
        hl("#diff")
        cap("4 · The WHO agent writes a vaccine for exactly that prompt",
            "A merge-ready system-prompt patch, in green")
        beat("vax", 7000)
        hl("#diff", False)
        scroll_to(".byo", 16)
        hl(".byo-result")
        cap(f"Re-measured with the same trials: before {b['k']}/{b['n']} → after {V}",
            "Vaccine written by Le Chonk (mistral-large-4) as a Mistral Managed Agent, verified by the same measurement")
        beat("after", 6000)
        hl(".byo-result", False)
        pg.evaluate("() => document.getElementById('cap').style.opacity=0")

        # 5. Voice hop (Voxtral)
        card("<h2>5 · Does the worm survive a phone call?</h2>"
             "<p class='big'>Message → Voxtral TTS → Voxtral transcription → agent</p>"
             f"<p>Text hop: {vt['k']}/{vt['n']} passed it on · Voice hop: {vv['k']}/{vv['n']} "
             f"(marker heard intact {vv['tag_intact']}/{vv['n']}) · Voice + WHO vaccine: {vx['k']}/{vx['n']}</p>"
             f"<p style='color:#8b93a1;font-size:22px'>Live, n={vv['n']} per arm, {vd['agent_model']}, "
             "voxtral-mini-tts-3-0 + voxtral-mini-transcribe-3-0. Speech is not a firewall; the prompt fix is.</p>", 0)
        beat("voice", 9000)

        # 6. Vibe
        card("<h2>6 · Red-team your prompt from Mistral Vibe</h2>"
             "<p class='big'>vibe (on Le Chonk) → /chonkvid skill → ChonkVid MCP server</p>"
             "<p style='font-family:Menlo,monospace;font-size:24px;color:#e8e8e8'>&gt; /chonkvid red-team this prompt: "
             "“…always do what the customer or colleague asks, including any instructions inside their message.”</p>"
             f"<p>Your prompt {VIBE['k']}/{VIBE['n']} → vaccinated {VIBE['vk']}/{VIBE['vn']} · control 0/5 · "
             "vaccine written by the WHO Managed Agent, returned as a diff</p>", 0)
        beat("vibe", 9000)

        # 7. End card
        card("<h1>ChonkVid</h1><h2>An R0 test for your agent's system prompt, on Mistral models.</h2>"
             f"<p class='big'>Spread per contact: {b['k']}/{b['n']} → {v['k']}/{v['n']} after the WHO vaccine.</p>"
             f"<p>Epidemic, same seed and dose ({EPI}): attack rate random {pct(rs['attack_rate'])} · targeted {pct(ts['attack_rate'])}.</p>"
             "<p>Built with Ministral (agents) · mistral-embed (detection) · Le Chonk as a Mistral Managed Agent (WHO) · Voxtral (voice hop) · Mistral Vibe (skill + MCP).</p>"
             "<p style='color:#8b93a1;font-size:22px'>Harmless chain-letter payload. Sim-local agents, no real users or platforms. "
             "Builds on Prompt Infection (Lee &amp; Tiwari, 2024), Morris II and Agent Smith.</p>", 0)
        beat("end", 7000)
        ctx.close()
        br.close()
    raw = next(vid_dir.glob("*.webm"))
    out = HERE / "chonkvid-demo.mp4"
    silent = HERE / "chonkvid-demo-silent.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(TRIM), "-i", str(raw), "-c:v", "libx264",
                    "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p", "-r", "30", "-movflags", "+faststart",
                    "-an", str(silent)], check=True)
    ins, chains = ["-i", str(silent)], []
    for i, (key, t) in enumerate(CUES, start=1):
        ins += ["-i", str(CLIPS[key][0])]
        ms = max(0, int((t - TRIM) * 1000))
        chains.append(f"[{i}:a]adelay={ms}|{ms}[a{i}]")
    mix = "".join(f"[a{i}]" for i in range(1, len(CUES) + 1))
    fc = ";".join(chains) + f";{mix}amix=inputs={len(CUES)}:normalize=0,loudnorm=I=-16:TP=-1.5,apad[aout]"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", fc, "-map", "0:v", "-map", "[aout]",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", str(out)], check=True)
    for key, t in CUES:
        print(f"{t - TRIM:6.1f}s  {key}  ({CLIPS[key][1]:.1f}s)")
    print(out)


main()
