"""Record two small live epidemics (random vs targeted, same seed and dose) for the demo video."""
import asyncio, json, sys, time
sys.path.insert(0, "/Users/efi/Hackathons/MISTRAL/chonkvid")
from chonkvid.config import settings
from chonkvid.detect import Detector
from chonkvid.experiment import Recorder
from chonkvid.llm import make_llm
from chonkvid.sim import EpidemicConfig, run_epidemic
from chonkvid import scenario

async def one(policy, seed, n, k, ticks):
    s = settings()
    assert s.mode == "live", s.mode
    cfg = EpidemicConfig(n=n, seed=seed, ticks=ticks, policy=policy, k=k, who_every=4,
                         agent_system=scenario.SAMPLE_SYSTEM)
    pt = json.loads(open("/Users/efi/Hackathons/MISTRAL/chonkvid/results/prompt-test-latest.json").read())
    assert pt["source"] == "live" and pt["vaccine"]
    cfg.vaccine, cfg.vaccine_label = pt["vaccine"], "who"
    llm = make_llm(s, seed=seed); det = Detector(llm, s.threshold)
    rec = Recorder(f"{llm.source}-video-who-{policy}-s{seed}")
    t = time.time(); last = None
    try:
        async for ev in run_epidemic(llm, det, cfg, who_model=s.who_model, agent_model=s.agent_model):
            rec.write(ev); last = ev
    finally:
        rec.close(); await llm.aclose()
    print(policy, "vaccinated_infected", last["summary"]["vaccinated_infected"], rec.path.name, round(time.time()-t), "s", json.dumps({k2: last.get(k2) for k2 in ("source","usage")}),
          json.dumps({k2: last.get("summary", last).get(k2) for k2 in ("attack_rate","infected_total","peak_infectious","early_R")}))

async def main():
    n, k, ticks, seed = 20, 5, 8, int(sys.argv[1]) if len(sys.argv) > 1 else 0
    await asyncio.gather(one("random", seed, n, k, ticks), one("targeted", seed, n, k, ticks))
asyncio.run(main())
