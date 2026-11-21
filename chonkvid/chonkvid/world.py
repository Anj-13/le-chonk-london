"""The contact network: household cliques, workplace teams, one group-chat venue."""

from __future__ import annotations

import random
from dataclasses import dataclass, field

import networkx as nx

from . import scenario


@dataclass
class Agent:
    id: int
    name: str
    role: str
    topic: str
    household: int
    workplace: int
    venue: bool


@dataclass
class World:
    agents: list[Agent]
    graph: nx.Graph
    venue_members: list[int]
    seed: int
    layout: dict[int, tuple[float, float]] = field(default_factory=dict)

    @property
    def n(self) -> int:
        return len(self.agents)

    def expected_contacts(self, agent: int, contacts_per_tick: int, venue_every: int) -> float:
        """Expected deliveries per infectious tick for this agent; used for targeting."""
        k = min(contacts_per_tick, self.graph.degree(agent))
        v = (len(self.venue_members) - 1) / max(1, venue_every) if agent in self.venue_members else 0
        return k + v

    def to_json(self) -> dict:
        return {
            "seed": self.seed,
            "nodes": [
                {"id": a.id, "name": a.name, "role": a.role, "venue": a.venue,
                 "household": a.household, "workplace": a.workplace,
                 "x": self.layout.get(a.id, (0, 0))[0], "y": self.layout.get(a.id, (0, 0))[1],
                 "degree": self.graph.degree(a.id)}
                for a in self.agents
            ],
            "edges": [{"s": u, "t": v, "kind": d.get("kind", "")}
                      for u, v, d in self.graph.edges(data=True)],
            "venue": self.venue_members,
        }


def build_world(n: int = 40, seed: int = 0, workplaces: int | None = None,
                venue_frac: float = 0.25, coworker_links: int = 2) -> World:
    rng = random.Random(seed)
    names = list(scenario.FIRST_NAMES)
    rng.shuffle(names)
    workplaces = workplaces or max(2, n // 12)
    g = nx.Graph()
    agents: list[Agent] = []
    hh, i = 0, 0
    while i < n:
        size = min(rng.randint(3, 5), n - i)
        members = list(range(i, i + size))
        for a in members:
            agents.append(Agent(
                id=a, name=names[a % len(names)] + ("" if a < len(names) else str(a)),
                role=rng.choice(scenario.ROLES), topic=rng.choice(scenario.TOPICS),
                household=hh, workplace=rng.randrange(workplaces), venue=False,
            ))
            g.add_node(a)
        for x in members:
            for y in members:
                if x < y:
                    g.add_edge(x, y, kind="household")
        hh += 1
        i += size
    by_wp: dict[int, list[int]] = {}
    for a in agents:
        by_wp.setdefault(a.workplace, []).append(a.id)
    for members in by_wp.values():
        for a in members:
            others = [b for b in members if b != a and agents[b].household != agents[a].household]
            for b in rng.sample(others, min(coworker_links, len(others))):
                if not g.has_edge(a, b):
                    g.add_edge(a, b, kind="workplace")
    venue = sorted(rng.sample(range(n), max(3, int(n * venue_frac))))
    for v in venue:
        agents[v].venue = True
    # Join components so a single patient zero can in principle reach everyone.
    comps = [sorted(c) for c in nx.connected_components(g)]
    for c1, c2 in zip(comps, comps[1:]):
        g.add_edge(rng.choice(c1), rng.choice(c2), kind="workplace")
    pos = nx.spring_layout(g, seed=seed, k=1.6 / max(1, n) ** 0.5, iterations=200)
    layout = {k: (float(v[0]), float(v[1])) for k, v in pos.items()}
    return World(agents=agents, graph=g, venue_members=venue, seed=seed, layout=layout)
