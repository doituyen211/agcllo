from pathlib import Path
from typing import Dict, Any

from app.model_client import call_model
from app.reporter import build_final_report
from app.store import RunStore


AGENTS_DIR = Path("agents")


def load_agent_prompt(agent_name: str) -> str:
    path = AGENTS_DIR / f"{agent_name}.md"
    if not path.exists():
        raise FileNotFoundError(f"Missing agent prompt: {path}")
    return path.read_text(encoding="utf-8")


def run_agent(agent_name: str, user_input: str, store: RunStore) -> Dict[str, Any]:
    system_prompt = load_agent_prompt(agent_name)

    store.append_trace({
        "event": "agent_started",
        "agent": agent_name
    })

    result = call_model(
        agent_name=agent_name,
        system_prompt=system_prompt,
        user_input=user_input,
    )

    store.append_trace({
        "event": "agent_finished",
        "agent": agent_name,
        "result_keys": list(result.keys())
    })

    return result


def run_workflow(task_path: Path) -> Path:
    if not task_path.exists():
        raise FileNotFoundError(f"Task not found: {task_path}")

    task = task_path.read_text(encoding="utf-8")

    store = RunStore()
    run_dir = store.start()

    store.write_text("task.md", task)

    plan = run_agent(
        "planner",
        user_input=task,
        store=store,
    )
    store.write_json("01_plan.json", plan)

    build_input = f"""
TASK:
{task}

PLANNER_OUTPUT:
{plan}
"""
    build = run_agent(
        "builder",
        user_input=build_input,
        store=store,
    )
    store.write_json("02_build.json", build)

    review_input = f"""
TASK:
{task}

PLAN:
{plan}

BUILD_OUTPUT:
{build}
"""
    review = run_agent(
        "reviewer",
        user_input=review_input,
        store=store,
    )
    store.write_json("03_review.json", review)

    qa_input = f"""
TASK:
{task}

PLAN:
{plan}

BUILD_OUTPUT:
{build}

REVIEW:
{review}
"""
    qa = run_agent(
        "qa",
        user_input=qa_input,
        store=store,
    )
    store.write_json("04_qa.json", qa)

    final_report = build_final_report(
        task=task,
        plan=plan,
        build=build,
        review=review,
        qa=qa,
    )
    store.write_text("final_report.md", final_report)

    return run_dir