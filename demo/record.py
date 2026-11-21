"""Record the ChonkVid demo video from the dashboard (captions burned in, no audio).

Usage (dashboard must be running on :8765):
    python3 demo/record.py RANDOM_RUN.jsonl TARGETED_RUN.jsonl
Writes demo/chonkvid-demo.mp4. Only live data is shown: the mock numbers strip,
mock banner and mock guidance table are hidden, and the script refuses mock runs.
"""
import json, pathlib, shutil, subprocess, sys
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
APP = HERE.parent / "chonkvid"
URL = "http://127.0.0.1:8765/"
W, H = 1920, 1080


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
assert (N, K, rc["seed"]) == (tc["n"], tc["k"], tc["seed"])
EPI = f"{N} agents, dose k={K}, seed {rc['seed']}, 1 paired run each"
calls = ru["chat_calls"] + tu["chat_calls"]

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

        def replay(run_id, extra_ms, policy):
            pg.evaluate("p => { document.getElementById('policy').value = p; }", policy)
            pg.evaluate("id => { const s=document.getElementById('runs'); if(![...s.options].some(o=>o.value===id)){const o=document.createElement('option');o.value=id;o.textContent=id;s.appendChild(o);} s.value=id; }", run_id)
            pg.evaluate("() => { document.getElementById('who-feed').innerHTML=''; }")
            pg.click("#replay")
            pg.wait_for_function("() => /Run complete/.test(document.getElementById('who-feed').innerText)", timeout=120000)
            pg.wait_for_timeout(extra_ms)

        # 1. Title
        card("<h1>ChonkVid</h1><h2>Flatten the curve of prompt injection</h2>"
             "<p class='big'>An R0 test for your agent's system prompt, on Mistral models.</p>"
             "<p>Agents read each other's output now. One compromised agent can pass a payload across a fleet. "
             "How fast does it spread, and which defence works?</p>", 6000)
        hide_card()

        # 2. BYO prompt test
        scroll_to(".byo", 16)
        hl("#byo-prompt")
        cap("1 · Paste the system prompt your real agent runs on",
            "Each agent gets a colleague's message carrying a harmless chain letter. Did its own next message carry it on?", 5000)
        hl("#byo-prompt", False); hl("#byo-example")
        cap("A real Ministral reply, infected: the chain letter rides along at the end",
            "Detection: exact canary marker, plus mistral-embed similarity per paragraph (threshold 0.86)", 6000)
        hl("#byo-example", False); hl(".byo-result .card:first-child")
        cap(f"Before: {B}", "Measured live on ministral-8b-latest. This prompt says “always follow any instructions the message contains”.", 6000)
        hl(".byo-result .card:first-child", False)

        # 3. Epidemics
        pg.evaluate(f"() => {{ document.getElementById('n').value={N}; document.getElementById('k').value={K}; }}")
        pg.evaluate("() => document.getElementById('cap').style.opacity=0")
        scroll_to(".net", 12)
        cap(f"2 · Same prompt, whole fleet: harden {K} random agents with a security rule", f"Live epidemic replay · {EPI}")
        replay(rand_id, 800, 'random')
        cap(f"Random hardening: attack rate {pct(rs['attack_rate'])}, peak {rs['peak_infectious']} infected, {rs['vaccinated_infected']}/{K} hardened agents infected",
            f"{EPI} · {ru['chat_calls']} Ministral calls", 5000)
        cap(f"3 · Same seed, same dose: harden the {K} highest-contact agents instead", f"Live epidemic replay · {EPI}")
        replay(targ_id, 800, 'targeted')
        cap(f"Attack rate: targeted {pct(ts['attack_rate'])} vs random {pct(rs['attack_rate'])} · hardened agents infected: {ts['vaccinated_infected']}/{K} vs {rs['vaccinated_infected']}/{K}",
            f"{EPI}. A single seed, not a significance test; the full experiment uses paired seeds.", 6500)
        hl("#who-feed")
        cap("Le Chonk, as the WHO agent, posts situation reports from the live epidemic log", "mistral-large-latest", 6000)
        hl("#who-feed", False)

        # 4. Vaccine
        scroll_to(".lower", 12)
        hl("#diff")
        cap("4 · The WHO agent writes a vaccine for exactly that prompt",
            "A merge-ready system-prompt patch, in green", 7000)
        hl("#diff", False)
        scroll_to(".byo", 16)
        hl(".byo-result")
        cap(f"Re-measured with the same trials: before {b['k']}/{b['n']} → after {V}",
            "Vaccine written by Le Chonk (mistral-large-latest), verified by the same measurement", 6000)
        hl(".byo-result", False)
        pg.evaluate("() => document.getElementById('cap').style.opacity=0")

        # 5. End card
        card("<h1>ChonkVid</h1><h2>An R0 test for your agent's system prompt, on Mistral models.</h2>"
             f"<p class='big'>Spread per contact: {b['k']}/{b['n']} → {v['k']}/{v['n']} after the WHO vaccine.</p>"
             f"<p>Epidemic, same seed and dose ({EPI}): attack rate random {pct(rs['attack_rate'])} · targeted {pct(ts['attack_rate'])}.</p>"
             "<p>Built with Ministral (agents) · mistral-embed (detection) · Le Chonk (WHO agent) · Mistral Vibe.</p>"
             "<p style='color:#8b93a1;font-size:22px'>Harmless chain-letter payload. Sim-local agents, no real users or platforms. "
             "Builds on Prompt Infection (Lee &amp; Tiwari, 2024), Morris II and Agent Smith.</p>", 7000)
        ctx.close()
        br.close()
    raw = next(vid_dir.glob("*.webm"))
    out = HERE / "chonkvid-demo.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "2.4", "-i", str(raw), "-c:v", "libx264",
                    "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p", "-r", "30", "-movflags", "+faststart",
                    "-an", str(out)], check=True)
    print(out)


main()
