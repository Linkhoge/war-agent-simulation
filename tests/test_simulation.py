import unittest
from agent import Agent, AgentState, USRank, GermanRank, Team, RANK_ORDERS
from simulation import Simulation, SimulationConfig


class AgentTests(unittest.TestCase):
    def test_historical_rank_ladders_are_distinct(self):
        self.assertEqual(RANK_ORDERS[Team.BLUE][0], USRank.PRIVATE)
        self.assertEqual(RANK_ORDERS[Team.BLUE][-1], USRank.GENERAL)
        self.assertEqual(RANK_ORDERS[Team.RED][0], GermanRank.SCHUTZE)
        self.assertEqual(RANK_ORDERS[Team.RED][-1], GermanRank.GENERALFELDMARSCHALL)
        self.assertNotEqual(USRank.CAPTAIN.value, GermanRank.HAUPTMANN.value)

    def test_rank_changes_marker_size_and_game_resilience(self):
        junior = Agent(0, Team.BLUE, USRank.PRIVATE, 1, 1)
        senior = Agent(1, Team.BLUE, USRank.GENERAL, 1, 1)
        self.assertLess(junior.visual_scale, senior.visual_scale)
        self.assertLess(junior.resilience, senior.resilience)

    def test_german_rank_profiles_are_ordered(self):
        junior = Agent(0, Team.RED, GermanRank.SCHUTZE, 1, 1)
        senior = Agent(1, Team.RED, GermanRank.GENERALFELDMARSCHALL, 1, 1)
        self.assertLess(junior.visual_scale, senior.visual_scale)
        self.assertLess(junior.resilience, senior.resilience)

    def test_death_is_persistent(self):
        agent = Agent(0, Team.BLUE, USRank.PRIVATE, 1, 1)
        agent.apply_abstract_hit(10)
        self.assertEqual(agent.state, AgentState.DEAD)
        agent.apply_abstract_hit(1)
        self.assertEqual(agent.state, AgentState.DEAD)


class SimulationTests(unittest.TestCase):
    def test_seed_reproducibility(self):
        config = SimulationConfig(blue_count=24, red_count=24, steps=100, seed=17)
        first, second = Simulation(config), Simulation(config)
        first.run()
        second.run()
        self.assertEqual(first.summary(), second.summary())
        self.assertEqual(first.history, second.history)

    def test_population_is_conserved(self):
        sim = Simulation(SimulationConfig(blue_count=18, red_count=19, steps=80, seed=3))
        sim.run()
        final = sim.summary()
        self.assertEqual(final["blue_active"] + final["blue_wounded"] + final["blue_dead"], 18)
        self.assertEqual(final["red_active"] + final["red_wounded"] + final["red_dead"], 19)

    def test_dead_agents_remain_in_population(self):
        sim = Simulation(SimulationConfig(blue_count=5, red_count=5, steps=10, seed=4))
        sim.agents[0].apply_abstract_hit(10)
        self.assertEqual(sim.agents[0].state, AgentState.DEAD)
        self.assertIn(sim.agents[0], sim.agents)

    def test_each_team_gets_its_own_rank_ladder(self):
        sim = Simulation(SimulationConfig(blue_count=100, red_count=100, seed=12))
        for agent in sim.agents:
            if agent.team == Team.BLUE:
                self.assertIsInstance(agent.rank, USRank)
            else:
                self.assertIsInstance(agent.rank, GermanRank)

    def test_casualty_moves_out_of_formation(self):
        sim = Simulation(SimulationConfig(blue_count=20, red_count=20, seed=5))
        agent = next(a for a in sim.agents if a.team == Team.BLUE)
        original = (agent.x, agent.y)
        agent.apply_abstract_hit(10)
        sim._send_to_casualty_area(agent)
        for _ in range(sim.config.casualty_animation_ticks):
            sim.tick += 1
            sim._advance_casualties()
        self.assertNotEqual((agent.x, agent.y), original)
        self.assertEqual((agent.x, agent.y), agent.casualty_target)

    def test_shots_create_visible_tracer_events(self):
        sim = Simulation(SimulationConfig(blue_count=60, red_count=60, steps=5, seed=21,
                                          encounter_probability=1.0))
        sim._abstract_encounters()
        self.assertTrue(sim.tracers)
        self.assertTrue(all(t.source_id != t.target_id for t in sim.tracers))

    def test_formation_positions_stay_fixed_for_survivors(self):
        sim = Simulation(SimulationConfig(blue_count=20, red_count=20, steps=20, seed=9,
                                          encounter_probability=0.0))
        before = {a.agent_id: (a.x, a.y) for a in sim.agents}
        sim.run()
        for agent in sim.agents:
            self.assertEqual((agent.x, agent.y), before[agent.agent_id])


if __name__ == "__main__":
    unittest.main()
