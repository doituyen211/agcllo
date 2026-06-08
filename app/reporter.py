from typing import Dict, Any


def build_final_report(
    task: str,
    plan: Dict[str, Any],
    build: Dict[str, Any],
    review: Dict[str, Any],
    qa: Dict[str, Any],
) -> str:
    return f"""# Final Report

## Task

{task}

## Planner Summary

{plan.get("summary", "")}

### Files to Inspect

{format_list(plan.get("files_to_inspect", []))}

### Plan Steps

{format_list(plan.get("steps", []))}

### Risks

{format_list(plan.get("risks", []))}

## Builder Summary

{build.get("summary", "")}

### Files Changed / Proposed

{format_list(build.get("files_changed", []))}

### Implementation Notes

{format_list(build.get("implementation_notes", []))}

### Tests to Run

{format_list(build.get("tests_to_run", []))}

## Reviewer Result

Approved: `{review.get("approved", False)}`

### Issues

{format_issues(review.get("issues", []))}

### Recommendation

{review.get("recommendation", "")}

## QA Result

Status: `{qa.get("status", "")}`

### Test Checklist

{format_list(qa.get("test_checklist", []))}

### Edge Cases

{format_list(qa.get("edge_cases", []))}

## Final Status

{final_status(review, qa)}
"""


def format_list(items):
    if not items:
        return "- None"
    return "\n".join(f"- {item}" for item in items)


def format_issues(issues):
    if not issues:
        return "- None"
    return "\n".join(
        f"- [{issue.get('severity', 'unknown')}] {issue.get('comment', '')}"
        for issue in issues
    )


def final_status(review, qa):
    if review.get("approved") is True and qa.get("status") == "ready":
        return "Ready for human review and implementation."
    return "Not ready. Human review required before implementation."