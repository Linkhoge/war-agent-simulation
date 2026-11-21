"""Arcade viewer for opposing formations, rank depth, tracers and casualties."""
import arcade
from agent import AgentState, Rank, Team

SCREEN_W, SCREEN_H = 1120, 760
PANEL_W = 300
BG = (13, 18, 30)
BLUE = (65, 155, 255)
RED = (245, 85, 95)
PALE = (225, 232, 245)
GOLD = (255, 205, 90)
MUTED = (115, 130, 151)


class BattleWindow(arcade.Window):
    def __init__(self, simulation):
        super().__init__(SCREEN_W, SCREEN_H, "War Agent Simulation — formations")
        self.sim = simulation
        self.paused = False
        self.speed = 1
        self.accumulator = 0.0
        self.set_update_rate(1 / 60)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.SPACE:
            self.paused = not self.paused
        elif symbol == arcade.key.UP:
            self.speed = min(8, self.speed + 1)
        elif symbol == arcade.key.DOWN:
            self.speed = max(1, self.speed - 1)
        elif symbol == arcade.key.R:
            from simulation import Simulation
            self.sim = Simulation(self.sim.config)
        elif symbol == arcade.key.ESCAPE:
            self.close()

    def on_update(self, delta_time):
        if self.paused:
            return
        self.accumulator += delta_time * 30 * self.speed
        while self.accumulator >= 1:
            self.accumulator -= 1
            if not self.sim.step():
                break

    def on_draw(self):
        self.clear(BG)
        world = self.sim.world
        scale = min((SCREEN_W - PANEL_W - 40) / world.width, (SCREEN_H - 40) / world.height)
        ox, oy = 20, 20
        map_w, map_h = world.width * scale, world.height * scale
        arcade.draw_lbwh_rectangle_filled(ox, oy, map_w, map_h, (25, 34, 48))
        arcade.draw_lbwh_rectangle_outline(ox, oy, map_w, map_h, (75, 91, 115), 2)

        def pos(x, y):
            return ox + x * scale, oy + y * scale

        # The central no-man's-land sits between the two coloured front lines.
        gap_left = pos(world.blue_front_x + 2, 0)[0]
        gap_right = pos(world.red_front_x - 2, 0)[0]
        arcade.draw_lbwh_rectangle_filled(gap_left, oy, gap_right - gap_left, map_h, (31, 39, 52))
        for team, colour in ((Team.BLUE, BLUE), (Team.RED, RED)):
            line_x, _ = pos(world.front_line_x(team), 0)
            arcade.draw_line(line_x, oy + 10, line_x, oy + map_h - 10, colour, 3)
            label_x = line_x - 34 if team == Team.BLUE else line_x + 8
            arcade.draw_text("FRONT LINE", label_x, oy + map_h - 28, colour, 9)

        # Tracers are short-lived abstract encounter indicators, not physical trajectories.
        for tracer in self.sim.tracers:
            x1, y1 = pos(*tracer.start)
            x2, y2 = pos(*tracer.end)
            age = self.sim.tick - tracer.created_at
            alpha = max(35, 230 - age * 38)
            arcade.draw_line(x1, y1, x2, y2, (255, 220, 125, alpha), 2)

        for agent in self.sim.agents:
            x, y = pos(agent.x, agent.y)
            colour = BLUE if agent.team == Team.BLUE else RED
            radius = {Rank.RECRUIT: 3.4, Rank.REGULAR: 5.0, Rank.VETERAN: 7.0}[agent.rank]
            if agent.state == AgentState.DEAD:
                arcade.draw_circle_filled(x, y, radius, (85, 91, 102))
                arcade.draw_line(x - radius, y - radius, x + radius, y + radius, PALE, 1)
                arcade.draw_line(x - radius, y + radius, x + radius, y - radius, PALE, 1)
            elif agent.state == AgentState.WOUNDED:
                arcade.draw_circle_filled(x, y, radius, GOLD)
                arcade.draw_circle_outline(x, y, radius + 2, colour, 1)
            else:
                arcade.draw_circle_filled(x, y, radius, colour)
                arcade.draw_circle_outline(x, y, radius + 1, PALE, 1)

        panel_x = SCREEN_W - PANEL_W + 18
        arcade.draw_text("WAR AGENT SIM", panel_x, SCREEN_H - 42, PALE, 18, bold=True)
        arcade.draw_text("Two opposing rank formations", panel_x, SCREEN_H - 68, MUTED, 11)
        arcade.draw_text(f"Step: {self.sim.tick} / {self.sim.config.steps}", panel_x, SCREEN_H - 108, PALE, 13)
        arcade.draw_text(f"Speed: {self.speed}x   {'PAUSED' if self.paused else ''}", panel_x, SCREEN_H - 132, GOLD, 11)
        summary = self.sim.summary()
        y = SCREEN_H - 190
        for team, colour in ((Team.BLUE, BLUE), (Team.RED, RED)):
            arcade.draw_text(team.value.upper(), panel_x, y, colour, 15, bold=True)
            y -= 25
            for state in ("active", "wounded", "dead"):
                arcade.draw_text(f"{state.title()}: {summary[f'{team.value}_{state}']}", panel_x + 8, y, PALE, 12)
                y -= 20
            y -= 15
        arcade.draw_text("FRONT → BACK", panel_x, 150, PALE, 10, bold=True)
        arcade.draw_text("Recruit  •  Regular  •  Veteran", panel_x, 128, MUTED, 10)
        arcade.draw_text("Space pause | ↑↓ speed | R restart | Esc quit", panel_x, 78, MUTED, 9)
        arcade.draw_text("Gold = wounded   Grey × = dead", panel_x, 52, MUTED, 9)
        arcade.draw_text("Tracers = abstract encounter events", panel_x, 30, MUTED, 9)


def run_viewer(simulation):
    BattleWindow(simulation)
    arcade.run()
