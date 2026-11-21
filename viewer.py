"""Arcade display for a WWII-era U.S. Army vs German Heer scenario."""
import arcade
from agent import Team, RANK_ORDERS, RANK_LABELS

SCREEN_W, SCREEN_H = 1240, 800
PANEL_W = 340
BG = (13, 18, 30)
BLUE = (75, 145, 205)
RED = (145, 105, 82)
PALE = (225, 232, 245)
GOLD = (255, 205, 90)
MUTED = (115, 130, 151)
HIT = (255, 194, 105)
MISS = (190, 205, 220)


class BattleWindow(arcade.Window):
    def __init__(self, simulation):
        super().__init__(SCREEN_W, SCREEN_H, "WWII Western Front — U.S. Army vs German Heer")
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
        if agent.state == "dead":
            arcade.draw_circle_filled(x, y, radius, (76, 82, 94))
            arcade.draw_line(x - radius, y - radius, x + radius, y + radius, PALE, 1.2)
            arcade.draw_line(x - radius, y + radius, x + radius, y - radius, PALE, 1.2)
        elif agent.state == "wounded":
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

        # Simple terrain colours keep the map readable without a complex tile system.
        terrain_colours = {
            "trench": (83, 91, 78), "wall": (126, 119, 101),
            "building": (105, 91, 79), "forest": (48, 83, 58),
            "road": (75, 76, 75), "crater": (48, 52, 57),
        }
        for feature in world.terrain:
            fx, fy = pos(feature.x, feature.y)
            fw, fh = feature.width * scale, feature.height * scale
            colour = terrain_colours.get(feature.kind, MUTED)
            if feature.kind == "crater":
                arcade.draw_ellipse_filled(fx + fw/2, fy + fh/2, fw, fh, colour)
            else:
                arcade.draw_lbwh_rectangle_filled(fx, fy, fw, fh, colour)
            arcade.draw_lbwh_rectangle_outline(fx, fy, fw, fh, (145, 145, 132), 1)

        def pos(x, y):
            return ox + x * scale, oy + y * scale

        gap_left = pos(world.blue_front_x + 1.5, 0)[0]
        gap_right = pos(world.red_front_x - 1.5, 0)[0]
        arcade.draw_lbwh_rectangle_filled(gap_left, oy, gap_right - gap_left, map_h, (31, 39, 52))
        for team, colour, title in (
            (Team.BLUE, BLUE, "U.S. ARMY"),
            (Team.RED, RED, "GERMAN HEER"),
        ):
            line_x, _ = pos(world.front_line_x(team), 0)
            arcade.draw_line(line_x, oy + 10, line_x, oy + map_h - 10, colour, 3)
            arcade.draw_text(title, line_x - 42, oy + map_h - 28, colour, 9, bold=True)

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
        arcade.draw_text("WESTERN FRONT · 1944", panel_x, SCREEN_H - 42, PALE, 17, bold=True)
        arcade.draw_text("U.S. Army vs German Heer", panel_x, SCREEN_H - 68, MUTED, 11)
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
        for team, colour, label in (
            (Team.BLUE, BLUE, "U.S. ARMY"),
            (Team.RED, RED, "GERMAN HEER"),
        ):
            arcade.draw_text(label, panel_x, y, colour, 13, bold=True)
            y -= 19
            for state in ("active", "wounded", "dead"):
                arcade.draw_text(
                    f"{state.title():<9} {summary[f'{team.value}_{state}']:>4}",
                    panel_x + 8, y, PALE, 10
                )
                y -= 15
            y -= 6

        arcade.draw_text("HISTORICAL RANKS · U.S. / HEER", panel_x, y, PALE, 9, bold=True)
        y -= 17
        us_order, de_order = RANK_ORDERS[Team.BLUE], RANK_ORDERS[Team.RED]
        rows = max(len(us_order), len(de_order))
        for index in range(rows):
            pieces = []
            if index < len(us_order):
                rank = us_order[index]
                label, abbr = RANK_LABELS[rank]
                count = sum(a.team == Team.BLUE and a.rank == rank for a in self.sim.agents)
                if count:
                    pieces.append(f"US {abbr} {count}")
            if index < len(de_order):
                rank = de_order[index]
                label, abbr = RANK_LABELS[rank]
                count = sum(a.team == Team.RED and a.rank == rank for a in self.sim.agents)
                if count:
                    pieces.append(f"DE {abbr} {count}")
            if pieces:
                arcade.draw_text("   ".join(pieces), panel_x + 3, y, MUTED, 8)
                y -= 12
            if y < 76:
                break

        arcade.draw_text("Space pause | ↑↓ speed | R restart | Esc quit",
                         panel_x, 52, PALE, 9)
        ammo = sum(a.ammo for a in self.sim.agents if a.team == Team.BLUE), sum(
            a.ammo for a in self.sim.agents if a.team == Team.RED
        )
        arcade.draw_text(f"Ammo remaining  U.S. {ammo[0]}  |  Heer {ammo[1]}",
                         panel_x, 70, PALE, 9)
        arcade.draw_text("Gold = wounded · Grey × = dead · Rings = hit/fire",
                         panel_x, 32, MUTED, 8)


def run_viewer(simulation):
    BattleWindow(simulation)
    arcade.run()
