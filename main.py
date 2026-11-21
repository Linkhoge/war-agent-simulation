"""Command-line entry point for War Agent Simulation."""
import argparse
from simulation import Simulation, SimulationConfig


def parse_args():
    parser = argparse.ArgumentParser(description="Fictional agent-based battlefield toy model")
    parser.add_argument("--blue", type=int, default=30)
    parser.add_argument("--red", type=int, default=30)
    parser.add_argument("--steps", type=int, default=1200)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--headless", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    config = SimulationConfig(
        blue_count=args.blue, red_count=args.red,
        steps=args.steps, seed=args.seed
    )
    sim = Simulation(config)
    if args.headless:
        print("Final simulation summary:")
        print(sim.run())
        return
    try:
        from viewer import run_viewer
        run_viewer(sim)
    except ImportError as exc:
        raise SystemExit(
            "The graphical viewer requires Arcade. Install requirements.txt "
            "or run with --headless."
        ) from exc


if __name__ == "__main__":
    main()
