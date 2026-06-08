import argparse
from pathlib import Path

from app.orchestrator import run_workflow


def cmd_init(_args):
    Path("agents").mkdir(exist_ok=True)
    Path("tasks").mkdir(exist_ok=True)
    Path("app").mkdir(exist_ok=True)
    Path(".runs").mkdir(exist_ok=True)

    print("Initialized agent harness structure.")


def cmd_run(args):
    task_path = Path(args.task)
    run_dir = run_workflow(task_path)

    print("Workflow completed.")
    print(f"Run directory: {run_dir}")
    print(f"Final report: {run_dir / 'final_report.md'}")


def main():
    parser = argparse.ArgumentParser(
        prog="agentctl",
        description="Local coding agent harness CLI"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser(
        "init",
        help="Initialize harness folders"
    )
    init_parser.set_defaults(func=cmd_init)

    run_parser = subparsers.add_parser(
        "run",
        help="Run an agent workflow from a task file"
    )
    run_parser.add_argument(
        "task",
        help="Path to task markdown file"
    )
    run_parser.set_defaults(func=cmd_run)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()