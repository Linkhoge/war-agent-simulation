"""Arcade viewer for army formations and animated battle events."""
import arcade
from agent import AgentState, Team, RANK_ORDER, RANK_LABELS

SCREEN_W, SCREEN_H = 1240, 800
PANEL_W = 340
BG = (13, 18, 30)
BLUE = (65, 155, 255)
RED = (245, 85, 95)
PALE = (225, 232, 245)
GOLD = (255, 205, 90)
MUTED = (115, 130, 151)
HIT = (255, 194, 105)
MISS = (150, 205, 255)


class BattleWindow(arcade.Window):
    def __init__(self, simulation):
        super().__init__(SCREEN_W, SCREEN_H, "War Agent Simulation — army ranks")
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

    def _draw_agent(self, agent, pos):
        x, y = pos(agent.x, agent.y)
        colour = BLUE if agent.team == Team.BLUE else RED
        radius = 3.2 + agent.visual_scale * 3.2
        if agent.state.value == "dead":
            arcade.draw_circle_filled(x, y, radius, (76, 82, 94))
            arcade.draw_line(x - radius, y - radius, x + radius, y + radius, PALE, 1.2)
            arcade.draw_line(x - radius, y + radius, x + radius, y - radius, PALE, 1.2)
        elif agent.state.value == "wounded":
            arcade.draw_circle_filled(x, y, radius, GOLD)
            arcade.draw_circle_outline(x, y, radius + 2, colour, 1.5)
        else:
            arcade.draw_circle_filled(x, y, radius, colour)
            arcade.draw_circle_outline(x, y, radius + 1, PALE, 1)
        if agent.fire_flash_until >= self.sim.tick and agent.is_operational:
            arcade.draw_circle_outline(x, y, radius + 5, GOLD, 2)
        if agent.hit_flash_until >= self.sim.tick:
            arcade.draw_circle_outline(x, y, radius + 7, (255, 245, 220), 2)

    def on_draw(self):
        self.clear(BG)
        world = self.sim.world
        scale = min((SCREEN_W - PANEL_W - 50) / world.width, (SCREEN_H - 50) / world.height)
        ox, oy = 20, 20
        map_w, map_h = world.width * scale, world.height * scale
        arcade.draw_lbwh_rectangle_filled(ox, oy, map_w, map_h, (25, 34, 48))
        arcade.draw_lbwh_rectangle_outline(ox, oy, map_w, map_h, (75, 91, 115), 2)

        def pos(x, y):
            return ox + x * scale, oy + y * scale

        gap_left = pos(world.blue_front_x + 1.5, 0)[0]
        gap_right = pos(world.red_front_x - 1.5, 0)[0]
        arcade.draw_lbwh_rectangle_filled(gap_left, oy, gap_right - gap_left, map_h, (31, 39, 52))
        for team, colour in ((Team.BLUE, BLUE), (Team.RED, RED)):
            line_x, _ = pos(world.front_line_x(team), 0)
            arcade.draw_line(line_x, oy + 10, line_x, oy + map_h - 10, colour, 3)
            label_x = line_x - 34 if team == Team.BLUE else line_x + 8
            arcade.draw_text("FRONT", label_x, oy + map_h - 28, colour, 9, bold=True)

        arcade.draw_text("CASUALTIES", pos(world.margin, 0)[0], oy + 8, MUTED, 8)
        arcade.draw_text("CASUALTIES", pos(world.width - world.margin, 0)[0] - 62, oy + 8, MUTED, 8)

        for tracer in self.sim.tracers:
            age = max(0, self.sim.tick - tracer.created_at)
            progress = min(1.0, age / 4.0)
            x1, y1 = pos(*tracer.start)
            x2, y2 = pos(*tracer.end)
            bx = x1 + (x2 - x1) * progress
            by = y1 + (y2 - y1) * progress
            colour = HIT if tracer.hit else MISS
            arcade.draw_line(x1, y1, bx, by, colour, 2)
            arcade.draw_circle_filled(bx, by, 2.5, colour)

        for agent in self.sim.agents:
            self._draw_agent(agent, pos)

        panel_x = SCREEN_W - PANEL_W + 18
        arcade.draw_text("WAR AGENT SIM", panel_x, SCREEN_H - 42, PALE, 19, bold=True)
        arcade.draw_text("Ranked opposing formations", panel_x, SCREEN_H - 68, MUTED, 11)
        arcade.draw_text(
            f"Step {self.sim.tick:,} / {self.sim.config.steps:,}",
            panel_x, SCREEN_H - 106, PALE, 13
        )
        arcade.draw_text(
            f"Speed {self.speed}x   {'PAUSED' if self.paused else 'RUNNING'}",
            panel_x, SCREEN_H - 130, GOLD, 11
        )

        summary = self.sim.summary()
        y = SCREEN_H - 174
        for team, colour in ((Team.BLUE, BLUE), (Team.RED, RED)):
            arcade.draw_text(team.value.upper(), panel_x, y, colour, 14, bold=True)
            y -= 21
            for state in ("active", "wounded", "dead"):
                arcade.draw_text(
                    f"{state.title():<9} {summary[f'{team.value}_{state}']:>4}",
                    panel_x + 8, y, PALE, 11
                )
                y -= 17
            y -= 8

        arcade.draw_text("RANK LADDER · BLUE / RED", panel_x, y, PALE, 10, bold=True)
        y -= 19
        for rank in RANK_ORDER:
            blue_count = sum(a.rank == rank and a.team == Team.BLUE for a in self.sim.agents)
            red_count = sum(a.rank == rank and a.team == Team.RED for a in self.sim.agents)
            if blue_count or red_count:
                label, abbreviation = RANK_LABELS[rank]
                arcade.draw_text(
                    f"{abbreviation:<4} {label:<22} {blue_count:>2}/{red_count:<2}",
                    panel_x + 4, y, MUTED, 8
                )
                y -= 13
                if y < 76:
                    break

        arcade.draw_text("Space pause | ↑↓ speed | R restart | Esc quit",
                         panel_x, 52, PALE, 9)
        arcade.draw_text("Gold = wounded · Grey × = dead · Rings = hit/fire",
                         panel_x, 32, MUTED, 8)

    def on_close(self):
        super().on_close()


def run_viewer(simulation):
    BattleWindow(simulation)
    arcade.run()
