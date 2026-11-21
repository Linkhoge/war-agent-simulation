import unittest
from agent import Agent, AgentState, Rank, Team
from simulation import Simulation, SimulationConfig


class AgentTests(unittest.TestCase):
    def test_rank_visual_hierarchy(self):
        recruit = Agent(0, Team.BLUE, Rank.RECRUIT, 1, 1)
        regular = Agent(1, Team.BLUE, Rank.REGULAR, 1, 1)
        veteran = Agent(2, Team.BLUE, Rank.VETERAN, 1, 1)
        self.assertLess(recruit.visual_scale, regular.visual_scale)
        self.assertLess(regular.visual_scale, veteran.visual_scale)
        self.assertLess(recruit.resilience, veteran.resilience)

    def test_death_is_persistent(self):
        agent = Agent(0, Team.BLUE, Rank.RECRUIT, 1, 1)
        agent.apply_abstract_hit(10)
        self.assertEqual(agent.state, AgentState.DEAD)
        agent.apply_abstract_hit(1)
        self.assertEqual(agent.state, AgentState.DEAD)


class SimulationTests(unittest.TestCase):
    def test_seed_reproducibility(self):
        config = SimulationConfig(blue_count=12, red_count=12, steps=100, seed=17)
        first = Simulation(config)
        second = Simulation(config)
        first.run()
        second.run()
        self.assertEqual(first.summary(), second.summary())
        self.assertEqual(first.history, second.history)

    def test_population_is_conserved(self):
        sim = Simulation(SimulationConfig(blue_count=8, red_count=9, steps=40, seed=3))
        sim.run()
        final = sim.summary()
        self.assertEqual(final["blue_active"] + final["blue_wounded"] + final["blue_dead"], 8)
        self.assertEqual(final["red_active"] + final["red_wounded"] + final["red_dead"], 9)

    def test_dead_agents_remain_in_population(self):
        sim = Simulation(SimulationConfig(blue_count=5, red_count=5, steps=10, seed=4))
        sim.agents[0].apply_abstract_hit(10)
        self.assertEqual(sim.agents[0].state, AgentState.DEAD)
        self.assertIn(sim.agents[0], sim.agents)

    def test_recruits_are_ahead_of_regulars_and_veterans(self):
        sim = Simulation(SimulationConfig(blue_count=60, red_count=60, seed=12))
        for team in (Team.BLUE, Team.RED):
            recruits = [a for a in sim.agents if a.team == team and a.rank == Rank.RECRUIT]
            regulars = [a for a in sim.agents if a.team == team and a.rank == Rank.REGULAR]
            veterans = [a for a in sim.agents if a.team == team and a.rank == Rank.VETERAN]
            self.assertTrue(recruits and regulars and veterans)
            if team == Team.BLUE:
                self.assertGreater(min(a.x for a in regulars), min(a.x for a in recruits))
                self.assertGreater(min(a.x for a in veterans), min(a.x for a in regulars))
            else:
                self.assertGreater(min(a.x for a in regulars), max(a.x for a in recruits))
                self.assertGreater(min(a.x for a in veterans), max(a.x for a in regulars))

    def test_formation_positions_stay_fixed(self):
        sim = Simulation(SimulationConfig(blue_count=12, red_count=12, steps=20, seed=9))
        before = [(a.x, a.y) for a in sim.agents]
        sim.run()
        self.assertEqual(before, [(a.x, a.y) for a in sim.agents])


if __name__ == "__main__":
    unittest.main()
