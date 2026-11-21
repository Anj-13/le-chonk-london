"use strict";
/*
 * Pathogen catalogue for the World Outbreak view.
 *
 * Each entry has two parts:
 *   - `facts`: what the card in the UI shows. Figures are commonly cited ranges,
 *     for flavour, not measurements from this app.
 *   - `sim`:   the EpidemicConfig fields sent to the backend (/ws/run). These shape
 *     the contact pattern (how many contacts per day, how long a case stays
 *     infectious, how often the group-chat "super-spreader venue" fires).
 *
 * In this version, whether an agent actually gets infected is still decided by
 * the agent model copying the ChonkVid payload (or the scripted model in MOCK
 * mode). The real-virus entries change the contact pattern only.
 *
 * Datasets: set `dataset` to a URL (or an object) when real data is added.
 * The UI already shows "dataset: pending" for entries where it is null. A loader
 * can read it in loadVirusDataset() in world.js.
 */
window.VIRUSES = [
  {
    id: "chonkvid",
    name: "ChonkVid-26",
    kind: "Prompt worm",
    glyph: "🐈",
    accent: "#ff3b5c",
    blurb:
      "A self-spreading chain-letter prompt. It jumps between Mistral agents when an agent copies it into its own next message. This is the one the app measures live.",
    facts: { r0: "measured live", incubation: "1 message", infectious: "3 days", spread: "Agent-to-agent messages" },
    sim: { contacts_per_tick: 2, infectious_ticks: 3, venue_every: 3 },
    live: true,
    dataset: null,
  },
  {
    id: "covid19",
    name: "SARS-CoV-2",
    kind: "Coronavirus · COVID-19",
    glyph: "🦠",
    accent: "#ff6a3d",
    blurb:
      "Respiratory virus spread by droplets and aerosols. Many cases spread it before they show symptoms, and crowded indoor events drive big clusters.",
    facts: { r0: "2.5 – 3.5", incubation: "2 – 14 days", infectious: "~8 days", spread: "Airborne, droplets" },
    sim: { contacts_per_tick: 2, infectious_ticks: 4, venue_every: 3 },
    dataset: null,
  },
  {
    id: "influenza",
    name: "Influenza A (H1N1)",
    kind: "Orthomyxovirus · flu",
    glyph: "🤧",
    accent: "#ffb020",
    blurb:
      "Seasonal and pandemic flu. Short incubation and a short infectious window, so it moves fast and burns out fast.",
    facts: { r0: "1.3 – 1.8", incubation: "1 – 4 days", infectious: "~5 days", spread: "Droplets, surfaces" },
    sim: { contacts_per_tick: 2, infectious_ticks: 2, venue_every: 4 },
    dataset: null,
  },
  {
    id: "measles",
    name: "Measles",
    kind: "Morbillivirus",
    glyph: "🔴",
    accent: "#ff2d55",
    blurb:
      "One of the most contagious viruses known. It hangs in the air for hours after an infected person leaves, so herd immunity needs about 95% coverage.",
    facts: { r0: "12 – 18", incubation: "10 – 14 days", infectious: "~8 days", spread: "Airborne" },
    sim: { contacts_per_tick: 4, infectious_ticks: 3, venue_every: 2 },
    dataset: null,
  },
  {
    id: "ebola",
    name: "Ebola",
    kind: "Filovirus · EVD",
    glyph: "🩸",
    accent: "#c3002f",
    blurb:
      "Spread by direct contact with body fluids, mostly in households and care settings. Low R0, but deadly, and no airborne spread.",
    facts: { r0: "1.5 – 2.5", incubation: "2 – 21 days", infectious: "~10 days", spread: "Direct contact" },
    sim: { contacts_per_tick: 1, infectious_ticks: 4, venue_every: 0 },
    dataset: null,
  },
  {
    id: "smallpox",
    name: "Smallpox",
    kind: "Orthopoxvirus · variola",
    glyph: "☣️",
    accent: "#a855f7",
    blurb:
      "Eradicated in 1980 after a global ring-vaccination campaign, which is the strategy behind targeted hardening here.",
    facts: { r0: "3.5 – 6", incubation: "7 – 17 days", infectious: "~14 days", spread: "Droplets, close contact" },
    sim: { contacts_per_tick: 3, infectious_ticks: 4, venue_every: 4 },
    dataset: null,
  },
];
