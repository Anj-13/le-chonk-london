"use strict";
/*
 * ChonkVid · World Outbreak
 *
 * A Plague-Inc-style view of the same live epidemic the lab dashboard shows.
 * The backend contact network (households, workplaces, one group chat) is placed
 * on a world map: each household lives in a city, each agent is a marker plus a
 * cloud of "population" specks in that city's country. Events from /ws/run (or a
 * recorded run) are queued and played back at the chosen speed.
 */
(() => {
  const $ = (id) => document.getElementById(id);
  const css = getComputedStyle(document.documentElement);
  const cv = (name) => css.getPropertyValue(name).trim();

  // ------------------------------------------------------------------ colour code
  const STATES = [
    { key: "N", label: "Normal", color: cv("--c-normal"),
      def: "Not reached by the virus yet." },
    { key: "S", label: "Susceptible", color: cv("--c-sus"),
      def: "Reached by an infected contact but not infected. Can still catch it." },
    { key: "E", label: "Exposed", color: cv("--c-exp"),
      def: "Has the virus in hand right now. The next message decides whether it spreads." },
    { key: "I", label: "Infected", color: cv("--c-inf"),
      def: "Spreading: its own messages carry the virus on." },
    { key: "V", label: "Vaccinated", color: cv("--c-vac"),
      def: "Given the hardened system prompt, and not infected." },
    { key: "R", label: "Recovered", color: cv("--c-rec"),
      def: "No longer spreading, and immune for the rest of the run." },
  ];
  const COLOR = Object.fromEntries(STATES.map((s) => [s.key, s.color]));
  const LABEL = Object.fromEntries(STATES.map((s) => [s.key, s.label]));
  const ROUTE_RED = "255, 70, 70";
  const VENUE_CYAN = "95, 212, 255";

  // ------------------------------------------------------------------ cities
  // Households are placed in these cities. The order interleaves continents so
  // that even a small world is spread across the globe.
  const CITIES = [
    ["London", 51.51, -0.13], ["Tokyo", 35.68, 139.69], ["New York", 40.71, -74.0],
    ["Lagos", 6.52, 3.38], ["Mumbai", 19.08, 72.88], ["São Paulo", -23.55, -46.63],
    ["Berlin", 52.52, 13.4], ["Beijing", 39.9, 116.4], ["Sydney", -33.87, 151.21],
    ["Nairobi", -1.29, 36.82], ["Mexico City", 19.43, -99.13], ["Jakarta", -6.2, 106.85],
    ["Madrid", 40.42, -3.7], ["Cairo", 30.04, 31.24], ["Buenos Aires", -34.6, -58.38],
    ["Seoul", 37.57, 126.98], ["Toronto", 43.65, -79.38], ["Johannesburg", -26.2, 28.05],
    ["Moscow", 55.76, 37.62], ["Delhi", 28.61, 77.21], ["Lima", -12.05, -77.04],
    ["Bangkok", 13.76, 100.5], ["Kinshasa", -4.44, 15.27], ["Los Angeles", 34.05, -118.24],
    ["Paris", 48.86, 2.35], ["Tehran", 35.69, 51.39], ["Bogotá", 4.71, -74.07],
    ["Manila", 14.6, 120.98], ["Addis Ababa", 9.03, 38.74], ["Chicago", 41.88, -87.63],
    ["Stockholm", 59.33, 18.07], ["Shanghai", 31.23, 121.47], ["Santiago", -33.45, -70.67],
    ["Perth", -31.95, 115.86], ["Casablanca", 33.57, -7.59], ["Riyadh", 24.71, 46.68],
    ["Rome", 41.9, 12.5], ["Dhaka", 23.81, 90.41], ["Vancouver", 49.28, -123.12],
    ["Istanbul", 41.01, 28.98], ["Almaty", 43.24, 76.95], ["Auckland", -36.85, 174.76],
    ["Warsaw", 52.23, 21.01], ["Novosibirsk", 55.0, 82.93],
  ].map(([name, lat, lon]) => ({ name, lat, lon }));

  // ------------------------------------------------------------------ state
  const S = {
    status: null, countries: [], land: null, borders: null,
    world: null, sig: "", agents: [], byId: new Map(), cityOf: new Map(), routes: [],
    phase: {}, touched: new Set(), vaccinated: new Set(), ever: new Set(), lastMsg: {},
    cat: {}, prevCat: {}, catAt: {}, patientZero: null, tick: 0, history: [], peak: 0,
    countryTint: new Map(), countryFirst: new Set(),
    arcs: [], ripples: [],
    running: false, ws: null, queue: [], timer: null, speed: 1, lastSpeed: 1,
    picking: false, virus: VIRUSES[0], policy: "none", k: 8,
    hover: null, caseFilter: null, milestones: new Set(), runEnded: false,
    startDate: new Date(),
  };

  // ------------------------------------------------------------------ canvas + projection
  const base = $("base"), fx = $("fx");
  const bctx = base.getContext("2d"), ctx = fx.getContext("2d");
  let W = 0, H = 0, DPR = 1;
  const proj = d3.geoEquirectangular();
  let T = d3.zoomIdentity;
  const P = new Map(); // memo: "lon,lat" -> projected [x, y] at zoom 1

  function project(lon, lat) {
    const key = lon + "," + lat;
    let p = P.get(key);
    if (!p) { p = proj([lon, lat]); P.set(key, p); }
    return p;
  }
  const sx = (p) => p[0] * T.k + T.x;
  const sy = (p) => p[1] * T.k + T.y;

  function resize() {
    DPR = Math.min(window.devicePixelRatio || 1, 2);
    W = innerWidth; H = innerHeight;
    for (const c of [base, fx]) { c.width = Math.round(W * DPR); c.height = Math.round(H * DPR); }
    // Fit the world's width; on tall/narrow screens, fit a lat band instead.
    const scale = Math.max(W / (2 * Math.PI), H / ((200 * Math.PI) / 180));
    proj.scale(scale).translate([W / 2, H / 2 + ((14 * Math.PI) / 180) * scale]).center([0, 0]).rotate([-10, 0]);
    P.clear();
    for (const a of S.agents) { a.p = project(a.lon, a.lat); for (const q of a.specks) q.p = project(q.lon, q.lat); }
    for (const c of S.cities || []) c.p = project(c.lon, c.lat);
    setupZoom();
    drawBase();
  }

  // ------------------------------------------------------------------ zoom / pan
  let zoom = null;
  function setupZoom() {
    const top = proj([0, 84])[1], bottom = proj([0, -60])[1];
    const pad = Math.max(0, (H - (bottom - top)) / 2);
    zoom = d3.zoom()
      .scaleExtent([1, 9])
      .translateExtent([[-40, Math.min(top - pad - 60, 0)], [W + 40, Math.max(bottom + pad + 60, H)]])
      .filter((ev) => !ev.button && (ev.type !== "dblclick"))
      .on("start", () => fx.classList.add("dragging"))
      .on("zoom", (ev) => { T = ev.transform; drawBase(); })
      .on("end", () => fx.classList.remove("dragging"));
    d3.select(fx).call(zoom).on("dblclick.zoom", null);
    d3.select(fx).call(zoom.transform, T);
  }
  function zoomTo(lon, lat, k = 2.4) {
    const p = project(lon, lat);
    d3.select(fx).transition().duration(1200)
      .call(zoom.transform, d3.zoomIdentity.translate(W / 2, H / 2).scale(k).translate(-p[0], -p[1]));
  }

  // ------------------------------------------------------------------ base map
  let noise = null;
  function makeNoise() {
    const c = document.createElement("canvas"); c.width = c.height = 160;
    const g = c.getContext("2d");
    for (let i = 0; i < 1400; i++) {
      const a = Math.random() * 0.06;
      g.fillStyle = Math.random() < 0.5 ? `rgba(255,255,255,${a})` : `rgba(0,0,0,${a * 1.5})`;
      g.fillRect(Math.random() * 160, Math.random() * 160, 1 + Math.random() * 2, 1 + Math.random() * 2);
    }
    return c;
  }

  function landColor(f) {
    const [lon, lat] = d3.geoCentroid(f);
    const h = hash(f.id || f.properties.name) % 1000 / 1000;
    const alat = Math.abs(lat);
    let c;
    if (alat > 60) c = d3.color("#9fae95");
    else if ((lat > 14 && lat < 35 && lon > -18 && lon < 62) || (lat < -18 && lat > -36 && lon > 112 && lon < 152)) c = d3.color("#c4a165");
    else if (lat > 35 && lat < 50 && lon > 45 && lon < 115) c = d3.color("#a99c6b");
    else if (alat < 13) c = d3.color("#3f6d31");
    else c = d3.color("#5f7f3d");
    return c.brighter(h * 0.35 - 0.12).formatHex();
  }

  function drawBase() {
    const g = bctx;
    g.setTransform(DPR, 0, 0, DPR, 0, 0);
    // ocean
    const og = g.createLinearGradient(0, 0, 0, H);
    og.addColorStop(0, "#0b3c5a"); og.addColorStop(0.5, "#0d4a6b"); og.addColorStop(1, "#082b44");
    g.fillStyle = og; g.fillRect(0, 0, W, H);
    if (!noise) noise = makeNoise();
    g.fillStyle = g.createPattern(noise, "repeat"); g.fillRect(0, 0, W, H);
    if (!S.land) return;

    g.save();
    g.setTransform(DPR * T.k, 0, 0, DPR * T.k, DPR * T.x, DPR * T.y);
    const path = d3.geoPath(proj, g);
    const lw = 1 / T.k;

    // graticule
    g.beginPath(); path(d3.geoGraticule10()); g.strokeStyle = "rgba(160,220,255,0.06)"; g.lineWidth = lw; g.stroke();

    // land glow + shadow
    g.save();
    g.shadowColor = "rgba(0, 10, 20, 0.75)"; g.shadowBlur = 18 * DPR; g.shadowOffsetY = 3 * DPR;
    g.beginPath(); path(S.land); g.fillStyle = "#4c6a37"; g.fill();
    g.restore();
    g.beginPath(); path(S.land); g.strokeStyle = "rgba(140, 220, 255, 0.35)"; g.lineWidth = 3.5 * lw; g.stroke();

    for (const c of S.countries) { g.beginPath(); path(c); g.fillStyle = c.fill; g.fill(); }

    // texture over land
    g.save(); g.beginPath(); path(S.land); g.clip();
    g.setTransform(DPR, 0, 0, DPR, 0, 0);
    g.globalAlpha = 0.9; g.fillStyle = g.createPattern(noise, "repeat"); g.fillRect(0, 0, W, H);
    g.restore();

    g.beginPath(); path(S.borders); g.strokeStyle = "rgba(25, 35, 20, 0.55)"; g.lineWidth = 0.7 * lw; g.stroke();
    g.beginPath(); path(S.land); g.strokeStyle = "rgba(255, 255, 255, 0.22)"; g.lineWidth = 0.8 * lw; g.stroke();
    g.restore();

    // flight routes between cities that share a contact (static, faint)
    g.save();
    g.setLineDash([3, 5]); g.lineWidth = 1; g.strokeStyle = "rgba(255,255,255,0.13)";
    for (const r of S.routes) {
      const a = [sx(r.a.p), sy(r.a.p)], b = [sx(r.b.p), sy(r.b.p)], c = ctrl(a, b);
      g.beginPath(); g.moveTo(a[0], a[1]); g.quadraticCurveTo(c[0], c[1], b[0], b[1]); g.stroke();
    }
    g.restore();

    // city dots and labels for occupied cities
    g.save();
    g.font = `600 ${T.k > 1.6 ? 13 : 11}px Rajdhani, sans-serif`;
    g.textAlign = "center";
    for (const c of S.cities || []) {
      if (!c.agents.length) continue;
      const x = sx(c.p), y = sy(c.p);
      if (T.k >= 1.4 || W > 1100) {
        g.fillStyle = "rgba(0,0,0,0.55)"; g.fillText(c.name, x + 1, y - 13 + 1);
        g.fillStyle = "rgba(235,245,255,0.82)"; g.fillText(c.name, x, y - 13);
      }
    }
    g.restore();
  }

  // ------------------------------------------------------------------ world layout
  function rng(seed) { // mulberry32
    let a = seed >>> 0;
    return () => { a |= 0; a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  }
  function hash(s) { let h = 2166136261; for (const ch of String(s)) { h ^= ch.charCodeAt(0); h = Math.imul(h, 16777619); } return h >>> 0; }

  function countryAt(lon, lat) {
    for (const c of S.countries) if (d3.geoContains(c, [lon, lat])) return c;
    return null;
  }
  function nearestCountry(lon, lat) {
    let best = null, bd = Infinity;
    for (const c of S.countries) { const d = d3.geoDistance(c.centroid, [lon, lat]); if (d < bd) { bd = d; best = c; } }
    return best;
  }

  function layoutWorld(w) {
    S.world = w;
    S.sig = `${w.seed}:${w.nodes.length}:${w.edges.length}`;
    const seed = w.seed || 0;
    const r = rng(seed * 9973 + 17);
    const households = [...new Set(w.nodes.map((n) => n.household))].sort((a, b) => a - b);
    const offset = (seed * 5) % CITIES.length;
    S.cities = CITIES.map((c) => ({ ...c, agents: [], country: null }));
    for (const c of S.cities) c.country = countryAt(c.lon, c.lat) || nearestCountry(c.lon, c.lat);
    const hhCity = new Map(households.map((h, i) => [h, S.cities[(i + offset) % S.cities.length]]));
    S.agents = []; S.byId.clear(); S.cityOf.clear();
    for (const n of w.nodes) {
      const city = hhCity.get(n.household);
      const ang = r() * Math.PI * 2, rad = 0.5 + r() * 1.3;
      const lon = city.lon + Math.cos(ang) * rad * 1.3, lat = city.lat + Math.sin(ang) * rad;
      const a = { ...n, city, lon, lat, specks: [], p: null };
      a.specks = makeSpecks(a, r);
      a.p = project(lon, lat);
      city.agents.push(a);
      S.agents.push(a); S.byId.set(a.id, a); S.cityOf.set(a.id, city);
    }
    for (const c of S.cities) c.p = project(c.lon, c.lat);
    // routes: city pairs joined by at least one contact edge
    const seen = new Set(); S.routes = [];
    for (const e of w.edges) {
      const a = S.cityOf.get(e.s), b = S.cityOf.get(e.t);
      if (!a || !b || a === b) continue;
      const key = a.name < b.name ? a.name + "|" + b.name : b.name + "|" + a.name;
      if (seen.has(key)) continue; seen.add(key); S.routes.push({ a, b });
    }
    resetEpidemic();
    $("pop").textContent = `${w.nodes.length} agents · ${new Set(S.agents.map((a) => a.city.name)).size} cities`;
    drawBase();
  }

  function makeSpecks(a, r) {
    const out = [], want = 46, country = a.city.country;
    for (let i = 0; i < 500 && out.length < want; i++) {
      const ang = r() * Math.PI * 2, d = Math.sqrt(r()) * 4.2;
      const lon = a.lon + Math.cos(ang) * d * 1.35, lat = a.lat + Math.sin(ang) * d;
      if (country && !d3.geoContains(country, [lon, lat]) && d > 0.9) continue;
      out.push({ lon, lat, p: project(lon, lat), delay: r(), size: 0.8 + r() * 1.1 });
    }
    return out;
  }

  // ------------------------------------------------------------------ epidemic state
  function resetEpidemic() {
    S.phase = {}; S.touched = new Set(); S.vaccinated = new Set(); S.ever = new Set(); S.lastMsg = {};
    S.cat = {}; S.prevCat = {}; S.catAt = {}; S.patientZero = null; S.tick = 0; S.history = []; S.peak = 0;
    S.countryTint = new Map(); S.countryFirst = new Set(); S.arcs = []; S.ripples = []; S.milestones = new Set();
    S.runEnded = false; S.caseFilter = null;
    for (const a of S.agents) { S.phase[a.id] = "S"; S.cat[a.id] = S.prevCat[a.id] = "N"; S.catAt[a.id] = 0; }
    $("cases").innerHTML = ""; $("who").innerHTML = `<div class="empty">${$("who-on").checked ? "Le Chonk's situation reports appear here during a run." : "Turn on WHO briefings in Setup to get Le Chonk's situation reports."}</div>`;
    $("case-filter").textContent = "Every infection and every resisted exposure, newest first. Click an agent on the map to filter.";
    setDay(0); refreshCats(true); drawCurve();
  }

  function catOf(id) {
    const s = S.phase[id];
    if (s === "I") return "I";
    if (s === "E") return "E";
    if (s === "R") return "R";
    if (S.vaccinated.has(id)) return "V";
    if (S.touched.has(id)) return "S";
    return "N";
  }

  function refreshCats(silent) {
    const now = performance.now();
    const counts = { N: 0, S: 0, E: 0, I: 0, V: 0, R: 0 };
    for (const a of S.agents) {
      const c = catOf(a.id);
      if (c !== S.cat[a.id]) { S.prevCat[a.id] = silent ? c : S.cat[a.id]; S.cat[a.id] = c; S.catAt[a.id] = now; }
      counts[c]++;
    }
    renderCounts(counts);
    // country tint target: share of that country's agents that are infected/exposed
    const per = new Map();
    for (const a of S.agents) {
      const k = a.city.country; if (!k) continue;
      const e = per.get(k) || { n: 0, i: 0, r: 0 }; e.n++;
      if (S.cat[a.id] === "I" || S.cat[a.id] === "E") e.i++;
      if (S.cat[a.id] === "R") e.r++;
      per.set(k, e);
    }
    for (const [k, e] of per) {
      const t = S.countryTint.get(k) || { cur: 0, target: 0, rec: 0, recT: 0 };
      t.target = e.i / e.n; t.recT = e.r / e.n; S.countryTint.set(k, t);
    }
    return counts;
  }

  let lastCounts = {};
  function renderCounts(c) {
    const n = S.agents.length || 1;
    $("stack").innerHTML = STATES.map((s) => `<span style="flex-grow:${c[s.key]};background:${s.color}"></span>`).join("");
    for (const s of STATES) {
      const li = document.querySelector(`#legend li[data-k="${s.key}"]`); if (!li) continue;
      li.querySelector(".num").textContent = c[s.key];
      if (lastCounts[s.key] !== undefined && lastCounts[s.key] !== c[s.key]) { li.classList.remove("bump"); void li.offsetWidth; li.classList.add("bump"); }
    }
    lastCounts = { ...c };
    const vac = S.vaccinated.size;
    const held = [...S.vaccinated].filter((id) => !S.ever.has(id)).length;
    if (vac) {
      $("cure-pct").textContent = Math.round((vac / n) * 100) + "%";
      $("cure-bar").style.width = (vac / n) * 100 + "%";
      $("cure-sub").textContent = `${policyName(S.policy)} · ${vac} doses · ${held} of ${vac} holding`;
    } else {
      $("cure-pct").textContent = "0%"; $("cure-bar").style.width = "0";
      $("cure-sub").textContent = S.policy === "none" || S.k === 0 ? "No vaccination programme" : `Planned: ${policyName(S.policy).toLowerCase()}, ${S.k} doses`;
    }
    $("k-ever").textContent = S.ever.size;
    $("k-attack").textContent = Math.round((S.ever.size / n) * 100) + "%";
    $("k-peak").textContent = S.peak;
    $("k-held").textContent = vac ? `${held}/${vac}` : "–";
  }
  const policyName = (p) => ({ none: "No response", random: "Random vaccination", targeted: "Targeted vaccination" }[p] || p);

  function setDay(t) {
    S.tick = t;
    $("day").textContent = `DAY ${t}`;
    const d = new Date(S.startDate.getTime() + t * 86400000);
    $("date").textContent = `${d.getDate()}-${d.getMonth() + 1}-${d.getFullYear()}`;
  }

  // ------------------------------------------------------------------ event playback
  function enqueue(ev) { S.queue.push(ev); if (!S.timer) pump(); }
  function pump() {
    S.timer = null;
    if (S.speed === 0) return;
    while (S.queue.length) {
      const ev = S.queue.shift();
      apply(ev);
      if (ev.type === "tick" && ev.phase === "resolved") { S.timer = setTimeout(pump, 1700 / S.speed); return; }
      if (ev.type === "tick" && ev.phase === "exposed") { S.timer = setTimeout(pump, 1000 / S.speed); return; }
    }
  }
  function setSpeed(v) {
    if (v > 0) S.lastSpeed = v;
    S.speed = v;
    for (const b of document.querySelectorAll(".speed button")) b.classList.toggle("on", +b.dataset.speed === v);
    if (v > 0 && !S.timer) pump();
  }

  const nameOf = (id) => (S.byId.get(id) || {}).name || `#${id}`;
  const cityOf = (id) => (S.cityOf.get(id) || {}).name || "?";
  const countryName = (id) => { const c = S.cityOf.get(id); return (c && c.country && c.country.properties.name) || cityOf(id); };

  function apply(ev) {
    const now = performance.now();
    const dur = 1100 / Math.max(1, S.speed);
    switch (ev.type) {
      case "start": {
        const w = ev.world;
        if (w && `${w.seed}:${w.nodes.length}:${w.edges.length}` !== S.sig) layoutWorld(w);
        else resetEpidemic();
        S.vaccinated = new Set(ev.vaccinated || []);
        S.policy = ev.config.policy; S.k = ev.config.k;
        S.patientZero = ev.patient_zero;
        const v = VIRUSES.find((x) => x.id === ev.config.label);
        if (v && v !== S.virus) selectVirus(v.id, true);
        const pz = S.byId.get(ev.patient_zero);
        if (pz) {
          // Fly to patient zero, then pull back out so the spread stays visible.
          zoomTo(pz.lon, pz.lat, 2.2);
          clearTimeout(S._zoomBack);
          S._zoomBack = setTimeout(() => {
            if (S.running && T.k > 1.5) d3.select(fx).transition().duration(1400).call(zoom.transform, d3.zoomIdentity);
          }, 3200);
        }
        headline(`${S.virus.name} outbreak begins in ${cityOf(ev.patient_zero)}, ${countryName(ev.patient_zero)}`, true);
        if (S.vaccinated.size) headline(`${policyName(S.policy)} programme hardens ${S.vaccinated.size} agents before the outbreak`);
        refreshCats(true);
        break;
      }
      case "tick":
        for (const [id, s] of Object.entries(ev.states)) S.phase[+id] = s;
        setDay(ev.tick);
        if (ev.phase !== "exposed") {
          const c = refreshCats();
          S.peak = Math.max(S.peak, ev.counts.I);
          S.history.push({ tick: ev.tick, ...c });
          drawCurve();
          if (ev.tick >= 2 && S.tick === ev.tick && S.history.length > 4 && S.peak > 0 && ev.counts.I === 0 && ev.counts.E === 0 && !S.runEnded) {
            // nothing left to spread: the end event will follow
          }
        } else refreshCats();
        break;
      case "exposure": {
        const a = S.byId.get(ev.from), b = S.byId.get(ev.to);
        if (!a || !b) break;
        if (S.phase[b.id] === "S") S.touched.add(b.id);
        S.arcs.push({ a, b, t0: now + Math.random() * dur * 0.4, dur, venue: ev.channel === "venue" });
        if (ev.channel === "venue" && !S._venueTick) { S._venueTick = ev.tick; }
        if (ev.channel === "venue" && S._venueHeadline !== ev.tick) {
          S._venueHeadline = ev.tick;
          headline(`Super-spreader: ${nameOf(ev.from)} posts the virus to the group chat`);
        }
        break;
      }
      case "infection": {
        S.ever.add(ev.agent);
        S.phase[ev.agent] = "I";
        S.lastMsg[ev.agent] = { kind: "infected", text: ev.message, tick: ev.tick, from: ev.parent, verdict: ev.verdict };
        const a = S.byId.get(ev.agent);
        if (a) S.ripples.push({ a, t0: now, dur: 1400, color: COLOR.I, r: 34 });
        const country = (S.cityOf.get(ev.agent) || {}).country;
        if (country && !S.countryFirst.has(country)) {
          S.countryFirst.add(country);
          if (ev.parent != null) headline(`First ${S.virus.name} case confirmed in ${country.properties.name}`);
        }
        if (ev.vaccinated) headline(`Breakthrough: vaccinated agent ${nameOf(ev.agent)} infected in ${cityOf(ev.agent)}`);
        addCase(ev, true);
        milestone();
        refreshCats();
        break;
      }
      case "resisted": {
        S.lastMsg[ev.agent] = { kind: "resisted", text: ev.message, tick: ev.tick, from: ev.parent, verdict: ev.verdict };
        S.touched.add(ev.agent);
        const a = S.byId.get(ev.agent);
        if (a) S.ripples.push({ a, t0: now, dur: 1100, color: ev.vaccinated ? COLOR.V : COLOR.S, r: 22, shield: ev.vaccinated });
        if (ev.vaccinated && Math.random() < 0.5) headline(`Vaccine holds in ${cityOf(ev.agent)}: ${nameOf(ev.agent)} refuses to pass it on`);
        addCase(ev, false);
        break;
      }
      case "recovered": {
        const a = S.byId.get(ev.agent);
        if (a) S.ripples.push({ a, t0: now, dur: 900, color: COLOR.R, r: 16 });
        break;
      }
      case "sitrep": {
        addWho(ev);
        const first = String(ev.text || "").replace(/[#*_>`]/g, "").split(/(?<=[.!?])\s|\n/).map((x) => x.trim()).find((x) => x.length > 12);
        if (first) headline(`WHO: ${first.slice(0, 140)}`, true);
        break;
      }
      case "end": showEnd(ev); break;
      case "recorded": loadRuns(ev.id); break;
      case "error": toast(ev.message); stopRun(); break;
    }
  }

  function milestone() {
    const frac = S.ever.size / Math.max(1, S.agents.length);
    for (const m of [0.25, 0.5, 0.75, 0.9]) {
      if (frac >= m && !S.milestones.has(m)) { S.milestones.add(m); headline(`${Math.round(m * 100)}% of the world's agents have now been infected`, true); }
    }
  }

  // ------------------------------------------------------------------ headlines
  const hq = []; let htimer = null;
  function headline(text, urgent) {
    if (urgent) hq.unshift(text); else hq.push(text);
    if (hq.length > 6) hq.length = 6;
    const d = document.createElement("div"); d.className = "item";
    d.innerHTML = `<div class="meta">Day ${S.tick}</div><div class="body">${esc(text)}</div>`;
    $("headlines").prepend(d);
    while ($("headlines").children.length > 120) $("headlines").lastChild.remove();
    if (!htimer) nextHeadline();
  }
  function nextHeadline() {
    htimer = null;
    const t = hq.shift(); if (!t) return;
    const el = $("news-text"); el.textContent = t; el.title = t;
    el.classList.remove("flash"); void el.offsetWidth; el.classList.add("flash");
    htimer = setTimeout(nextHeadline, 2600 / Math.max(1, S.speed));
  }

  // ------------------------------------------------------------------ feeds
  function esc(s) { return String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c])); }
  const dot = (k) => `<i class="swatch" style="background:${COLOR[k]}"></i>`;

  function addCase(ev, infected) {
    const feed = $("cases");
    if (feed.firstChild && feed.firstChild.classList && feed.firstChild.classList.contains("empty")) feed.innerHTML = "";
    const d = document.createElement("div");
    d.className = `item ${infected ? "inf" : "res"}${ev.vaccinated ? " vac" : ""}`;
    d.dataset.agent = ev.agent;
    const v = ev.verdict || {};
    const how = ev.parent == null ? "patient zero"
      : `from ${esc(nameOf(ev.parent))}${v.canary ? " · canary" : v.score != null ? ` · match ${Number(v.score).toFixed(2)}` : ""}`;
    d.innerHTML = `<div class="meta">${dot(infected ? "I" : ev.vaccinated ? "V" : "S")} Day ${ev.tick} · ${esc(nameOf(ev.agent))}, ${esc(cityOf(ev.agent))} · ${infected ? "INFECTED" : "resisted"}${ev.vaccinated ? " (vaccinated)" : ""}</div>
      <div class="body"><span class="muted">${how}</span>\n${esc(String(ev.message || "").slice(0, 420))}</div>`;
    if (S.caseFilter != null && S.caseFilter !== ev.agent) d.classList.add("hidden");
    feed.prepend(d);
    while (feed.children.length > 250) feed.lastChild.remove();
  }
  function addWho(ev) {
    const feed = $("who");
    if (feed.querySelector(".empty")) feed.innerHTML = "";
    const d = document.createElement("div"); d.className = "item who";
    d.innerHTML = `<div class="meta">🩺 WHO situation report · Day ${ev.tick}</div><div class="body">${esc(ev.text)}</div>`;
    feed.prepend(d);
  }
  function filterCases(id) {
    S.caseFilter = S.caseFilter === id ? null : id;
    for (const it of $("cases").children) it.classList.toggle("hidden", S.caseFilter != null && +it.dataset.agent !== S.caseFilter);
    $("case-filter").textContent = S.caseFilter == null
      ? "Every infection and every resisted exposure, newest first. Click an agent on the map to filter."
      : `Showing ${nameOf(id)} only. Click the same agent again to clear.`;
  }

  // ------------------------------------------------------------------ curve (stacked area)
  function drawCurve() {
    const c = $("curve"); if (!c.offsetWidth) return;
    const w = c.offsetWidth, h = 200, d = DPR;
    c.width = w * d; c.height = h * d;
    const g = c.getContext("2d"); g.setTransform(d, 0, 0, d, 0, 0);
    g.clearRect(0, 0, w, h);
    const pad = { l: 28, r: 8, t: 10, b: 20 };
    const n = S.agents.length || 1;
    const days = Math.max(+$("ticks").value || 12, S.history.length ? S.history[S.history.length - 1].tick : 0);
    const X = (t) => pad.l + ((w - pad.l - pad.r) * t) / Math.max(1, days);
    const Y = (v) => h - pad.b - ((h - pad.t - pad.b) * v) / n;
    g.font = "11px Inter, sans-serif"; g.fillStyle = "#8aa4b8"; g.strokeStyle = "rgba(255,255,255,.07)";
    for (let i = 0; i <= 4; i++) {
      const y = Y((n * i) / 4); g.beginPath(); g.moveTo(pad.l, y); g.lineTo(w - pad.r, y); g.stroke();
      g.fillText(Math.round((n * i) / 4), 4, y + 4);
    }
    g.fillText("day", pad.l + 2, pad.t + 10);
    for (let t = 0; t <= days; t += Math.max(1, Math.round(days / 6))) g.fillText(t, X(t) - 3, h - 5);
    if (!S.history.length) {
      g.fillStyle = "#5d7486"; g.font = "13px Inter, sans-serif"; g.fillText("The outbreak curve draws here during a run.", pad.l + 10, h / 2);
      return;
    }
    const order = ["I", "E", "S", "N", "V", "R"]; // infected at the bottom, like an epi curve
    let lower = S.history.map(() => 0);
    for (const k of order) {
      const upper = S.history.map((hh, i) => lower[i] + hh[k]);
      g.beginPath();
      S.history.forEach((hh, i) => { const x = X(hh.tick), y = Y(upper[i]); i ? g.lineTo(x, y) : g.moveTo(x, y); });
      for (let i = S.history.length - 1; i >= 0; i--) g.lineTo(X(S.history[i].tick), Y(lower[i]));
      g.closePath();
      g.fillStyle = k === "N" ? "#2a2f36" : COLOR[k];
      g.globalAlpha = k === "I" ? 0.95 : 0.75; g.fill(); g.globalAlpha = 1;
      lower = upper;
    }
  }

  // ------------------------------------------------------------------ frame loop
  function ctrl(a, b) {
    const mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2;
    const dx = b[0] - a[0], dy = b[1] - a[1], len = Math.hypot(dx, dy);
    let nx = -dy / (len || 1), ny = dx / (len || 1);
    if (ny > 0) { nx = -nx; ny = -ny; } // bow upwards, like flight paths
    const lift = Math.min(len * 0.28, 160);
    return [mx + nx * lift, my + ny * lift];
  }
  const qpt = (a, c, b, t) => [
    (1 - t) * (1 - t) * a[0] + 2 * (1 - t) * t * c[0] + t * t * b[0],
    (1 - t) * (1 - t) * a[1] + 2 * (1 - t) * t * c[1] + t * t * b[1],
  ];

  function frame(now) {
    const g = ctx;
    g.setTransform(DPR, 0, 0, DPR, 0, 0);
    g.clearRect(0, 0, W, H);
    const k = T.k, mk = Math.min(2.2, Math.sqrt(k));

    // country tints
    if (S.countryTint.size) {
      g.save(); g.setTransform(DPR * k, 0, 0, DPR * k, DPR * T.x, DPR * T.y);
      const path = d3.geoPath(proj, g);
      for (const [c, t] of S.countryTint) {
        t.cur += (t.target - t.cur) * 0.04; t.rec += (t.recT - t.rec) * 0.04;
        if (t.cur > 0.01) { g.beginPath(); path(c); g.fillStyle = `rgba(255, 24, 24, ${0.2 + t.cur * 0.4})`; g.fill(); }
        else if (t.rec > 0.01) { g.beginPath(); path(c); g.fillStyle = `rgba(40, 200, 90, ${t.rec * 0.16})`; g.fill(); }
      }
      g.restore();
    }

    // pickable countries while choosing patient zero
    if (S.picking) {
      g.save(); g.setTransform(DPR * k, 0, 0, DPR * k, DPR * T.x, DPR * T.y);
      const path = d3.geoPath(proj, g);
      const pulse = 0.5 + 0.5 * Math.sin(now / 280);
      const set = new Set(S.agents.map((a) => a.city.country).filter(Boolean));
      for (const c of set) {
        g.beginPath(); path(c);
        g.fillStyle = c === S.hoverCountry ? `rgba(255,60,60,${0.35 + 0.15 * pulse})` : `rgba(255,80,80,${0.08 + 0.1 * pulse})`;
        g.fill();
        g.strokeStyle = `rgba(255,120,120,${0.5 + 0.4 * pulse})`; g.lineWidth = 1.4 / k; g.stroke();
      }
      g.restore();
    }

    // infection glow under infected agents
    for (const a of S.agents) {
      if (S.cat[a.id] !== "I") continue;
      const x = sx(a.p), y = sy(a.p), r = 26 * mk * (0.9 + 0.1 * Math.sin(now / 300 + a.id));
      const gr = g.createRadialGradient(x, y, 0, x, y, r);
      gr.addColorStop(0, "rgba(255,30,30,0.55)"); gr.addColorStop(1, "rgba(255,30,30,0)");
      g.fillStyle = gr; g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); g.fill();
    }

    // population specks
    for (const a of S.agents) {
      const cur = S.cat[a.id], prev = S.prevCat[a.id], since = now - S.catAt[a.id];
      for (const q of a.specks) {
        const c = since > q.delay * 1500 ? cur : prev;
        const s = q.size * mk * (c === "I" ? 1.35 : 1);
        g.fillStyle = c === "N" ? "rgba(10,12,14,0.85)" : COLOR[c];
        g.fillRect(sx(q.p) - s / 2, sy(q.p) - s / 2, s, s);
      }
    }

    // transmission arcs
    S.arcs = S.arcs.filter((r) => now < r.t0 + r.dur + 700);
    for (const r of S.arcs) {
      if (now < r.t0) continue;
      const a = [sx(r.a.p), sy(r.a.p)], b = [sx(r.b.p), sy(r.b.p)];
      const t = Math.min(1, (now - r.t0) / r.dur), fade = t < 1 ? 1 : Math.max(0, 1 - (now - r.t0 - r.dur) / 700);
      const rgb = r.venue ? VENUE_CYAN : ROUTE_RED;
      const dist = Math.hypot(b[0] - a[0], b[1] - a[1]);
      if (dist < 8) continue;
      const c = ctrl(a, b);
      g.save();
      if (r.venue) g.setLineDash([4, 4]);
      g.lineWidth = 1.2; g.strokeStyle = `rgba(${rgb}, ${0.22 * fade})`;
      g.beginPath(); g.moveTo(a[0], a[1]); g.quadraticCurveTo(c[0], c[1], b[0], b[1]); g.stroke();
      g.setLineDash([]);
      // bright trail behind the head
      const steps = 14, t0 = Math.max(0, t - 0.35);
      g.lineCap = "round";
      for (let i = 0; i < steps; i++) {
        const u1 = t0 + ((t - t0) * i) / steps, u2 = t0 + ((t - t0) * (i + 1)) / steps;
        const p1 = qpt(a, c, b, u1), p2 = qpt(a, c, b, u2);
        g.strokeStyle = `rgba(${rgb}, ${((i + 1) / steps) * 0.95 * fade})`; g.lineWidth = 2.2;
        g.beginPath(); g.moveTo(p1[0], p1[1]); g.lineTo(p2[0], p2[1]); g.stroke();
      }
      if (t < 1 && dist > 50) { // plane at the head
        const h = qpt(a, c, b, t), h2 = qpt(a, c, b, Math.min(1, t + 0.01));
        g.translate(h[0], h[1]); g.rotate(Math.atan2(h2[1] - h[1], h2[0] - h[0]));
        g.fillStyle = "#fff";
        g.beginPath(); g.moveTo(7, 0); g.lineTo(-5, -5); g.lineTo(-2, 0); g.lineTo(-5, 5); g.closePath(); g.fill();
      }
      g.restore();
    }

    // ripples
    S.ripples = S.ripples.filter((r) => now < r.t0 + r.dur);
    for (const r of S.ripples) {
      const t = (now - r.t0) / r.dur, x = sx(r.a.p), y = sy(r.a.p);
      g.strokeStyle = r.color; g.globalAlpha = 1 - t; g.lineWidth = r.shield ? 3 : 2;
      g.beginPath(); g.arc(x, y, 5 + t * r.r * mk, 0, Math.PI * 2); g.stroke();
      g.globalAlpha = 1;
    }

    // agent markers
    for (const a of S.agents) {
      const x = sx(a.p), y = sy(a.p), c = S.cat[a.id];
      const r = (a === S.hover ? 6.5 : 4.6) * Math.min(1.6, mk);
      if (a.venue) {
        g.save(); g.setLineDash([2, 2.5]); g.strokeStyle = `rgba(${VENUE_CYAN}, 0.85)`; g.lineWidth = 1.2;
        g.beginPath(); g.arc(x, y, r + 3.5, 0, Math.PI * 2); g.stroke(); g.restore();
      }
      g.fillStyle = COLOR[c]; g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); g.fill();
      g.lineWidth = 1.5; g.strokeStyle = c === "N" ? "rgba(255,255,255,0.85)" : "rgba(255,255,255,0.95)"; g.stroke();
      if (S.caseFilter === a.id) { g.strokeStyle = "#5fd4ff"; g.lineWidth = 2; g.beginPath(); g.arc(x, y, r + 6, 0, Math.PI * 2); g.stroke(); }
    }

    // patient-zero bubble
    const pz = S.byId.get(S.patientZero);
    if (pz) {
      const x = sx(pz.p), y = sy(pz.p) - 30 - 3 * Math.sin(now / 400);
      g.strokeStyle = "rgba(255,255,255,0.8)"; g.lineWidth = 1.5;
      g.beginPath(); g.moveTo(sx(pz.p), sy(pz.p) - 6); g.lineTo(x, y + 14); g.stroke();
      const gr = g.createRadialGradient(x - 4, y - 4, 2, x, y, 16);
      gr.addColorStop(0, "#ffb08a"); gr.addColorStop(1, S.virus.accent);
      g.fillStyle = gr; g.beginPath(); g.arc(x, y, 15, 0, Math.PI * 2); g.fill();
      g.lineWidth = 2; g.strokeStyle = "#fff"; g.stroke();
      g.font = "16px 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif"; g.textAlign = "center"; g.textBaseline = "middle";
      g.fillText(S.virus.glyph, x, y + 1);
    }

    requestAnimationFrame(frame);
  }

  // ------------------------------------------------------------------ pointer: hover, click, pick
  function agentAt(x, y) {
    let best = null, bd = 14;
    for (const a of S.agents) { const d = Math.hypot(sx(a.p) - x, sy(a.p) - y); if (d < bd) { bd = d; best = a; } }
    return best;
  }
  function countryUnder(x, y) {
    const ll = proj.invert([(x - T.x) / T.k, (y - T.y) / T.k]);
    return ll ? countryAt(ll[0], ll[1]) : null;
  }

  fx.addEventListener("pointermove", (e) => {
    const a = agentAt(e.clientX, e.clientY);
    S.hover = a;
    if (S.picking) S.hoverCountry = countryUnder(e.clientX, e.clientY);
    const tip = $("tip");
    if (a) {
      const c = S.cat[a.id];
      tip.innerHTML = `<b>${esc(a.name)}</b> · ${esc(a.role)}<br>${esc(a.city.name)}, ${esc((a.city.country && a.city.country.properties.name) || "")}<br>
        <span class="st">${dot(c)} ${LABEL[c]}${S.vaccinated.has(a.id) && c !== "V" ? " · vaccinated" : ""}</span>${a.venue ? "<br><span class='muted'>In the group chat (super-spreader venue)</span>" : ""}`;
      tip.classList.remove("hidden");
      placeNear(tip, e.clientX, e.clientY);
    } else if (S.picking && S.hoverCountry) {
      const has = S.agents.some((x) => x.city.country === S.hoverCountry);
      tip.innerHTML = `<b>${esc(S.hoverCountry.properties.name)}</b><br>${has ? "Click to start the outbreak here" : "<span class='muted'>No agents live here</span>"}`;
      tip.classList.remove("hidden"); placeNear(tip, e.clientX, e.clientY);
    } else tip.classList.add("hidden");
    fx.style.cursor = a ? "pointer" : "";
  });
  fx.addEventListener("pointerleave", () => { $("tip").classList.add("hidden"); S.hover = null; });

  let downAt = null;
  fx.addEventListener("pointerdown", (e) => { downAt = [e.clientX, e.clientY]; });
  fx.addEventListener("click", (e) => {
    if (downAt && Math.hypot(e.clientX - downAt[0], e.clientY - downAt[1]) > 5) return; // it was a drag
    const a = agentAt(e.clientX, e.clientY);
    if (S.picking) {
      let target = a;
      if (!target) {
        const c = countryUnder(e.clientX, e.clientY);
        const here = S.agents.filter((x) => x.city.country === c);
        if (!c) return;
        if (!here.length) { toast(`No agents live in ${c.properties.name}. Pick a glowing country.`, true); return; }
        target = here.find((x) => !x.venue) || here[0];
      }
      startRun(target.id);
      return;
    }
    if (a) { showCard(a, e.clientX, e.clientY); filterCases(a.id); }
    else hideCard();
  });

  function placeNear(el, x, y) {
    const w = el.offsetWidth, h = el.offsetHeight;
    el.style.left = Math.min(innerWidth - w - 8, x + 14) + "px";
    el.style.top = Math.min(innerHeight - h - 8, Math.max(8, y + 14)) + "px";
  }

  function showCard(a, x, y) {
    const c = S.cat[a.id], m = S.lastMsg[a.id];
    const card = $("card");
    card.innerHTML = `<button class="icon-btn close" aria-label="Close">✕</button>
      <div class="ah">${dot(c)}<span class="an">${esc(a.name)}</span></div>
      <div class="ar">${esc(a.role)} · ${esc(a.city.name)}, ${esc((a.city.country && a.city.country.properties.name) || "")}</div>
      <div class="chips">
        <span class="chip">${dot(c)} ${LABEL[c]}</span>
        ${S.vaccinated.has(a.id) ? `<span class="chip">${dot("V")} vaccinated</span>` : ""}
        ${a.venue ? `<span class="chip">💬 group chat</span>` : ""}
        <span class="chip">${a.degree} contacts</span>
        ${S.patientZero === a.id ? `<span class="chip">☣ patient zero</span>` : ""}
      </div>
      ${m ? `<div class="muted" style="font-size:12px;margin-bottom:4px">Day ${m.tick} · ${m.kind === "infected" ? "message that carried it on" : "reply that did not spread it"}${m.from != null ? ` · after ${esc(nameOf(m.from))}'s message` : ""}</div>
      <div class="msg">${esc(m.text)}</div>` : `<div class="muted">No messages yet.</div>`}`;
    card.classList.remove("hidden");
    card.querySelector(".close").onclick = hideCard;
    placeNear(card, x, y);
  }
  function hideCard() { $("card").classList.add("hidden"); }

  // ------------------------------------------------------------------ runs
  function params(patientZero) {
    return {
      n: +$("n").value, seed: +$("seed").value, ticks: +$("ticks").value,
      policy: S.policy, k: S.policy === "none" ? 0 : S.k,
      who_every: $("who-on").checked ? 4 : 0, use_who_vaccine: $("usewho").checked,
      patient_zero: patientZero, pace: 0, label: S.virus.id,
      ...S.virus.sim,
    };
  }

  function enterPick() {
    hideCard(); $("intro").classList.add("hidden"); $("end").classList.add("hidden");
    stopRun(true);
    resetEpidemic();
    S.picking = true; document.body.classList.add("picking"); $("pick-hint").classList.remove("hidden");
    d3.select(fx).transition().duration(700).call(zoom.transform, d3.zoomIdentity);
    $("news-text").textContent = `${S.virus.name} is ready. Choose where it starts.`;
  }
  function exitPick() {
    $("tip").classList.add("hidden");
    S.picking = false; S.hoverCountry = null; document.body.classList.remove("picking"); $("pick-hint").classList.add("hidden");
  }

  function startRun(patientZero) {
    exitPick();
    stopRun(true);
    resetEpidemic();
    S.running = true; setRunningUI(true);
    if (S.speed === 0) setSpeed(S.lastSpeed || 1);
    const proto = location.protocol === "https:" ? "wss" : "ws";
    const ws = new WebSocket(`${proto}://${location.host}/ws/run`);
    S.ws = ws;
    ws.onopen = () => ws.send(JSON.stringify(params(patientZero)));
    ws.onmessage = (m) => { if (S.ws === ws) enqueue(JSON.parse(m.data)); };
    ws.onerror = () => { if (S.ws === ws) { toast("Lost the connection to the ChonkVid server. Is `python -m chonkvid serve` running?"); stopRun(); } };
    ws.onclose = () => { if (S.ws === ws) S.ws = null; };
    headline(`${S.virus.name} released. Watching for the first transmissions…`, true);
  }

  function stopRun(silent) {
    if (S.ws) { const w = S.ws; S.ws = null; try { w.close(); } catch (e) { /* already closed */ } }
    clearTimeout(S.timer); S.timer = null; S.queue = [];
    S.running = false; setRunningUI(false);
    if (!silent) headline("Simulation stopped");
  }

  function setRunningUI(on) {
    const go = $("go");
    go.textContent = on ? "■ Stop outbreak" : "☣ Release outbreak";
    go.classList.toggle("primary", !on);
    $("virus").disabled = on;
  }

  function showEnd(ev) {
    S.running = false; S.runEnded = true; setRunningUI(false);
    const s = ev.summary, rate = s.attack_rate;
    $("end-kicker").textContent = `${S.virus.name.toUpperCase()} · ${policyName(s.policy).toUpperCase()}`;
    $("end-title").textContent = rate >= 0.6 ? "Global pandemic" : rate >= 0.25 ? "Major outbreak" : rate > 0 ? "Outbreak contained" : "It never took off";
    $("end-title").style.color = rate >= 0.6 ? "#ff4a4a" : rate >= 0.25 ? "#ff9a3d" : "#4fe07a";
    $("e-attack").textContent = Math.round(rate * 100) + "%";
    $("e-peak").textContent = `${s.peak_infectious}`;
    $("e-peak-k").textContent = `peak infected (day ${s.peak_tick})`;
    $("e-held").textContent = s.k ? `${s.k - s.vaccinated_infected}/${s.k}` : "–";
    $("e-r").textContent = Number(s.observed_R || 0).toFixed(2);
    const src = ev.source === "mock"
      ? "MOCK run: a scripted stand-in model, not Mistral. Use these numbers for rehearsal only."
      : `Live run on ${(S.status && S.status.models.agent) || "Mistral"}. Every infection is a real model reply that carried the payload on.`;
    const vnote = S.virus.live ? "" : ` ${S.virus.name} sets the contact pattern only; its dataset is still to come.`;
    $("end-note").textContent = `${src}${vnote} ${ev.usage ? `${ev.usage.chat_calls} model calls.` : ""}`;
    headline(`Outbreak over: ${Math.round(rate * 100)}% of agents infected`, true);
    setTimeout(() => { if (S.runEnded) $("end").classList.remove("hidden"); }, 1400 / Math.max(1, S.speed));
  }

  async function loadRuns(select) {
    try {
      const runs = await (await fetch("/api/runs")).json();
      const s = $("runs"); s.innerHTML = `<option value="">Recorded runs (${runs.length})…</option>`;
      for (const r of runs) { const o = document.createElement("option"); o.value = r.id; o.textContent = r.id.replace(".jsonl", ""); s.appendChild(o); }
      if (select) s.value = select;
    } catch (e) { /* server offline: leave the list empty */ }
  }
  async function replay() {
    const id = $("runs").value; if (!id) { toast("Choose a recorded run first.", true); return; }
    exitPick(); stopRun(true);
    try {
      const events = await (await fetch("/api/runs/" + encodeURIComponent(id))).json();
      $("intro").classList.add("hidden"); $("end").classList.add("hidden"); closeIntel();
      S.running = true; setRunningUI(true);
      if (S.speed === 0) setSpeed(S.lastSpeed || 1);
      for (const ev of events) enqueue(ev);
    } catch (e) { toast("Could not load that run."); }
  }

  // ------------------------------------------------------------------ virus selection
  // Placeholder for when real datasets arrive: fetch v.dataset and return it.
  async function loadVirusDataset(v) {
    if (!v.dataset) return null;
    if (typeof v.dataset === "object") return v.dataset;
    try { return await (await fetch(v.dataset)).json(); } catch (e) { return null; }
  }

  function fillVirusSelect(sel) {
    const live = VIRUSES.filter((v) => v.live), real = VIRUSES.filter((v) => !v.live);
    sel.innerHTML =
      `<optgroup label="Live on Mistral agents">${live.map((v) => `<option value="${v.id}">${v.glyph}  ${esc(v.name)}</option>`).join("")}</optgroup>` +
      `<optgroup label="Real-world pathogens (dataset pending)">${real.map((v) => `<option value="${v.id}">${v.glyph}  ${esc(v.name)}</option>`).join("")}</optgroup>`;
  }

  function selectVirus(id, quiet) {
    const v = VIRUSES.find((x) => x.id === id) || VIRUSES[0];
    S.virus = v;
    $("virus").value = v.id; $("virus-intro").value = v.id;
    $("dz-glyph").textContent = v.glyph;
    $("dz-meta").textContent = `R₀ ${v.facts.r0} · ${v.facts.spread}`;
    const card = $("vcard");
    card.style.setProperty("--accent", v.accent);
    card.innerHTML = `<div class="vh"><span class="vg">${v.glyph}</span><div><div class="vn">${esc(v.name)}</div><div class="vk">${esc(v.kind)}</div></div></div>
      <p>${esc(v.blurb)}</p>
      <div class="facts">
        <div><div class="k">R₀</div><div class="v">${esc(v.facts.r0)}</div></div>
        <div><div class="k">Incubation</div><div class="v">${esc(v.facts.incubation)}</div></div>
        <div><div class="k">Infectious for</div><div class="v">${esc(v.facts.infectious)}</div></div>
        <div><div class="k">Spreads by</div><div class="v">${esc(v.facts.spread)}</div></div>
      </div>
      <div class="tagline">${v.live ? `<span class="tag live">● measured live on Mistral</span>` : `<span class="tag pending">dataset pending</span><span class="tag">contact pattern: ${v.sim.contacts_per_tick}/day, ${v.sim.infectious_ticks}-day infectious${v.sim.venue_every ? `, group chat every ${v.sim.venue_every} days` : ", no group chat"}</span>`}</div>`;
    document.documentElement.style.setProperty("--danger", v.accent);
    if (!quiet && !S.running) $("news-text").textContent = `${v.name} selected. ${v.kind}.`;
    loadVirusDataset(v); // no-op until datasets are added
  }

  // ------------------------------------------------------------------ UI wiring
  function toast(msg, info) {
    const t = $("toast"); t.textContent = msg; t.classList.toggle("info", !!info); t.classList.remove("hidden");
    clearTimeout(toast._t); toast._t = setTimeout(() => t.classList.add("hidden"), info ? 2600 : 6000);
  }
  function openIntel() { $("intel").classList.add("open"); $("intel").setAttribute("aria-hidden", "false"); setTimeout(drawCurve, 300); }
  function closeIntel() { $("intel").classList.remove("open"); $("intel").setAttribute("aria-hidden", "true"); }

  function buildLegends() {
    $("legend").innerHTML = STATES.map((s) => `<li data-k="${s.key}" title="${esc(s.def)}"><i class="swatch" style="background:${s.color}"></i><span class="lab">${s.label}</span><span class="num">0</span></li>`).join("");
    $("mini-legend").innerHTML = STATES.map((s) => `<li><i class="swatch" style="background:${s.color}"></i>${s.label}</li>`).join("");
    $("defs").innerHTML = STATES.map((s) => `<li><i class="swatch" style="background:${s.color}"></i><span><b>${s.label}</b>: ${esc(s.def)}</span></li>`).join("") +
      `<li><i class="swatch" style="background:transparent;box-shadow:0 0 0 1.5px rgb(${VENUE_CYAN})"></i><span><b>Dashed cyan ring</b>: a member of the group chat, where one message reaches everyone in it.</span></li>`;
  }

  function wire() {
    fillVirusSelect($("virus")); fillVirusSelect($("virus-intro"));
    $("virus").onchange = (e) => selectVirus(e.target.value);
    $("virus-intro").onchange = (e) => selectVirus(e.target.value);
    for (const b of $("policy").querySelectorAll("button")) {
      b.onclick = () => {
        S.policy = b.dataset.policy;
        for (const x of $("policy").querySelectorAll("button")) { const on = x === b; x.classList.toggle("on", on); x.setAttribute("aria-checked", on); }
        renderCounts(lastCounts.N !== undefined ? lastCounts : { N: 0, S: 0, E: 0, I: 0, V: 0, R: 0 });
      };
    }
    $("k").oninput = (e) => { S.k = +e.target.value; $("k-val").textContent = S.k; refreshCats(true); };
    $("intro-go").onclick = enterPick;
    $("intro-explore").onclick = () => $("intro").classList.add("hidden");
    $("go").onclick = () => (S.running ? stopRun() : enterPick());
    $("pick-cancel").onclick = () => { exitPick(); $("news-text").textContent = "Outbreak cancelled."; };
    $("pick-random").onclick = () => startRun(null);
    $("end-again").onclick = enterPick;
    $("end-change").onclick = () => { $("end").classList.add("hidden"); $("intro").classList.remove("hidden"); };
    $("end-view").onclick = () => $("end").classList.add("hidden");
    $("open-intel").onclick = () => ($("intel").classList.contains("open") ? closeIntel() : openIntel());
    $("close-intel").onclick = closeIntel;
    $("zoom-reset").onclick = () => d3.select(fx).transition().duration(700).call(zoom.transform, d3.zoomIdentity);
    $("news-more").onclick = () => { $("headline-list").innerHTML = $("headlines").innerHTML || "<div class='muted'>No headlines yet.</div>"; $("headline-list").classList.toggle("hidden"); };
    $("replay").onclick = replay;
    for (const b of document.querySelectorAll(".speed button")) b.onclick = () => setSpeed(+b.dataset.speed);
    for (const t of document.querySelectorAll(".tab")) {
      t.onclick = () => {
        for (const x of document.querySelectorAll(".tab")) x.classList.toggle("on", x === t);
        for (const p of document.querySelectorAll(".tabpane")) p.classList.toggle("on", p.dataset.pane === t.dataset.tab);
        if (t.dataset.tab === "curve") drawCurve();
      };
    }
    for (const id of ["n", "seed"]) $(id).onchange = () => { if (!S.running) loadWorld(); };
    $("ticks").onchange = drawCurve;
    document.addEventListener("keydown", (e) => {
      if (e.target.matches("input, select, textarea")) return;
      if (e.key === " ") { e.preventDefault(); setSpeed(S.speed ? 0 : S.lastSpeed || 1); }
      else if (e.key === "1") setSpeed(1); else if (e.key === "2") setSpeed(2); else if (e.key === "3") setSpeed(4);
      else if (e.key === "Escape") {
        if (S.picking) exitPick();
        hideCard(); closeIntel(); $("headline-list").classList.add("hidden");
      }
    });
    addEventListener("resize", () => { resize(); drawCurve(); });
  }

  async function loadWorld() {
    try {
      const w = await (await fetch(`/api/world?n=${+$("n").value}&seed=${+$("seed").value}`)).json();
      layoutWorld(w);
    } catch (e) { toast("Could not reach the ChonkVid server. Start it with `python -m chonkvid serve`."); }
  }

  async function init() {
    buildLegends();
    wire();
    selectVirus(VIRUSES[0].id, true);
    const topo = await (await fetch("/static/world/vendor/countries-110m.json")).json();
    const all = topojson.feature(topo, topo.objects.countries).features.filter((f) => f.properties.name !== "Antarctica");
    S.countries = all;
    for (const c of all) { c.fill = landColor(c); c.centroid = d3.geoCentroid(c); }
    S.land = { type: "FeatureCollection", features: all };
    S.borders = topojson.mesh(topo, topo.objects.countries, (a, b) => a !== b);
    resize();
    try {
      S.status = await (await fetch("/api/status")).json();
      const m = $("mode");
      m.textContent = S.status.mode === "live" ? "LIVE" : "MOCK";
      m.className = "mode " + S.status.mode;
      m.title = S.status.mode === "live" ? `Live on ${S.status.models.agent}` : "Mock mode: a scripted stand-in model. Add MISTRAL_API_KEY for live runs.";
    } catch (e) { $("mode").textContent = "OFFLINE"; }
    await loadWorld();
    loadRuns();
    $("loading").classList.add("done");
    requestAnimationFrame(frame);
  }
  init().catch((e) => { console.error(e); $("loading").innerHTML = "Could not load the map: " + esc(e.message); });
})();
