# Pass 1: Sanitized Competition Brief (researcher output, facts only)

For isolated ideation runs. Contains constraints, criteria, and the crowded
blacklist. Contains no prior-winner project descriptions and no incumbent concept.

## Verified competition constraints

- One-day, in-person hackathon run by Mistral AI, Saturday 21 Nov 2026, London,
  08:30-20:30. Teams of 3-5 builders. Roughly 11 usable build hours.
- Stack: free-tier access to the sponsor's own model APIs: a flagship large model,
  a family of very cheap small models suited to high-volume parallel calls, a code
  model, an embeddings model, and function calling / agent scaffolding. Everything
  must be demonstrated live from one laptop.
- Judging: no published rubric for this edition. The organiser's published criteria
  for a sibling edition (the closest proxy): technical depth, creativity,
  usefulness, quality of demo, and alignment with event objectives, equally
  weighted. A judge from the prior edition wrote on the record that winning teams
  "thought hardest about the user problem and about safety".
- Panel: the sponsor's own AI engineers, software engineers, TPMs and AI
  scientists. Practitioners: scripted or fake demos are usually caught.
- Prizes: sponsor API credits. Applicant profiles are shared with the hiring team.

## Sponsor capabilities that appear strategically important

- Cheap parallel small-model calls at population scale (hundreds per minute).
- A flagship model for analysis, synthesis and explanation.
- Embeddings for similarity, lineage and clustering.
- Agent scaffolding with function calling.

## Crowded / forbidden archetypes (the room will be full of these)

1. Civilization or world simulators where agents build a society (a project of
   this shape won the organiser's previous global event; expect many clones).
2. Chat personas on the flagship model; voice assistants; RAG document Q&A.
3. "Agent startup" theater; stock and crypto predictors.
4. Single-agent red-team scanners and prompt-injection checkers in their standard
   shape: paste one prompt, receive a safety verdict, test one agent in isolation.
5. Generic dashboards, task managers, tutors, summarizers, wellness bots,
   navigators and recommender lists.

## Underrepresented, per the organiser's own record

- What happens BETWEEN agents once a fleet is deployed (not one agent's capability).
- Measured interventions that visibly work, with numbers and baselines.
- Real workflows of the teams who ship and maintain agent fleets.
- Verification-first demonstrations: deterministic evidence over model self-report.

## Feasibility constraints for every idea

- 3-5 builders, ~11 hours, free-tier rate limits, one laptop.
- No time for heavy infrastructure, authentication systems, payments, or data
  pipelines that take hours to license or clean.
- The demo must not depend on flaky external services; a 90-second live pitch.

## Uncertainties (flagged, unverified)

- This edition's exact rubric is unpublished; the sibling-edition criteria are a
  proxy.
- The flagship model's precise context and tooling limits on the free tier.
