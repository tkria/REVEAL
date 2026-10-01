"""
Smoke tests for REVEAL.

These tests need no database, no API keys and no network access, so CI can run them.
They do not check the scientific output. Use scripts/verify_database.py for the database
and an expert review for the interpretations.
"""
import os
import py_compile
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Some agents create an OpenAI client at import time, which fails without a key.
# These tests make no API calls, so a placeholder is enough.
os.environ.setdefault("OPENAI_API_KEY", "smoke-test-placeholder")


def test_cli_module_imports():
    import run_stateful_pipeline

    assert run_stateful_pipeline.PIPELINE_NODE_IDS


def test_pipeline_graph_builds():
    # Build the graph in a fresh interpreter, as a real run does. Under pytest,
    # pydantic_graph can be imported before the Python 3.13 compatibility patch in
    # src/graph/gene_graph.py, and the graph then fails to resolve its node types.
    script = (
        "import run_stateful_pipeline as cli\n"
        "from src.graph.gene_graph import get_reveal_graph\n"
        "nodes = set(get_reveal_graph().node_defs)\n"
        "assert nodes == cli.PIPELINE_NODE_IDS, nodes ^ cli.PIPELINE_NODE_IDS\n"
        "print(len(nodes))\n"
    )
    result = subprocess.run(
        [sys.executable, "-W", "ignore", "-c", script],
        cwd=ROOT, capture_output=True, text=True, timeout=120,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip().splitlines()[-1] == "21"


def test_streamlit_app_compiles():
    for path in [ROOT / "streamlit_app.py", *sorted((ROOT / "app").rglob("*.py"))]:
        py_compile.compile(str(path), doraise=True)
