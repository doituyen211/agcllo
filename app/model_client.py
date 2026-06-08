import json
from typing import Dict, Any


def call_model(agent_name: str, system_prompt: str, user_input: str) -> Dict[str, Any]:
    """
    MVP mock model.
    Replace this function later with a real LLM provider call.
    """

    if agent_name == "planner":
        return {
            "summary": "Fix the login success redirect target.",
            "files_to_inspect": [
                "src/auth/login.py",
                "tests/test_login.py"
            ],
            "steps": [
                "Inspect the login success handler.",
                "Find the current redirect target.",
                "Change redirect target to dashboard.",
                "Add or update a regression test."
            ],
            "risks": [
                "Auth flow may have next_url or return_to behavior.",
                "Changing redirect logic may affect existing tests."
            ]
        }

    if agent_name == "builder":
        return {
            "summary": "Proposed implementation for login redirect fix.",
            "files_changed": [
                "src/auth/login.py",
                "tests/test_login.py"
            ],
            "implementation_notes": [
                "Update login success redirect target from '/' to '/dashboard'.",
                "Preserve existing next_url behavior if present.",
                "Add test coverage for successful login redirect."
            ],
            "tests_to_run": [
                "pytest tests/test_login.py"
            ]
        }

    if agent_name == "reviewer":
        return {
            "approved": False,
            "issues": [
                {
                    "severity": "medium",
                    "comment": "Builder must explicitly preserve next_url behavior before changing redirect."
                }
            ],
            "recommendation": "Revise implementation plan to preserve next_url/return_to if the app supports it."
        }

    if agent_name == "qa":
        return {
            "test_checklist": [
                "Login with valid credentials redirects to dashboard.",
                "Invalid login still shows validation error.",
                "Existing session behavior remains unchanged.",
                "next_url behavior is preserved if supported."
            ],
            "edge_cases": [
                "User already authenticated.",
                "Missing or malformed next_url.",
                "Inactive user account."
            ],
            "status": "not_ready"
        }

    raise ValueError(f"Unknown agent: {agent_name}")


def to_pretty_json(data: Dict[str, Any]) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False)