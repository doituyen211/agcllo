# Task: Fix login redirect

## Objective

After successful login, user should be redirected to dashboard.

## Context

The login flow currently redirects to home page.

## Acceptance Criteria

- User goes to dashboard after login.
- Existing login behavior remains unchanged.
- Add or update test if possible.

## Constraints

- Do not change database schema.
- Do not add dependencies.
- Do not refactor unrelated auth modules.

## Test Command

pytest tests/test_login.py
