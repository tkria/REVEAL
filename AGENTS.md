# Agent instructions

> **REVEAL was developed by and is owned by Rachael Brett.**

## Project purpose

> REVEAL interprets gene lists with an LLM pipeline that combines local gene databases, PubMed literature mining and AI synthesis, for rare disease genomics.

Owner: Isabelle Bond. Stage: release-ready. Describe intended users and non-goals here.

## Scientific constraints

- Do not invent assumptions, labels, thresholds, metrics, dataset splits, or expected results.
- Ask for clarification or mark unresolved scientific decisions explicitly.
- Do not silently change filters, exclusions, splits, prompts, models, reference versions, evaluation procedures, or interpretation rules.
- Preserve links between results, code versions, configuration, and data provenance.
- Treat passing tests as necessary evidence, not proof that the scientific design is correct.

## Development workflow

Before implementing a change: state the intended behaviour, identify the scientific assumptions and invariants involved, define acceptance criteria and at least one failure case, and make the smallest reasonable change.

After implementing a change: inspect the complete diff, run the relevant tests or checks, inspect representative outputs, update documentation and provenance when behaviour changes, and commit a meaningful working checkpoint.

## Privacy and security

- Never commit credentials, tokens, private keys, identifying information, or restricted raw data.
- Use `.env.example` for variable names and placeholders only.
- Do not send restricted data to unapproved models, services, tools, or providers.
- Request human approval before expensive, destructive, modifying, or consequential operations.

## Commands

- Install: `pip install -r requirements.txt`
- Build the database: `python scripts/setup_database.py`
- Check the database: `python scripts/verify_database.py`
- Framework check: `python scripts/framework_check.py`
- Test: `python -m pytest tests/test_smoke.py`
- Run main example: `streamlit run streamlit_app.py`, or `python run_stateful_pipeline.py "<question that names genes>"`

## Definition of done

A scoped task is complete only when the requested behaviour is implemented, the relevant tests or validation checks pass, representative outputs have been inspected, documentation and provenance are updated where needed, no secrets or restricted data were introduced, and the complete AI-generated diff has been reviewed by a researcher.
