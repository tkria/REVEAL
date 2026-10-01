# REVEAL: Retrieval and Evidence-based Validated Interpretation Analysis for gene Lists

> **REVEAL was developed by and is owned by Rachael Brett.**

A stateful, LLM-powered pipeline for comprehensive gene function interpretation and analysis. Combines local database queries, PubMed literature mining, and AI-driven synthesis to produce detailed gene interpretation reports.

## Objective

REVEAL interprets gene lists with an LLM pipeline that combines local gene databases, PubMed literature mining and AI synthesis, for rare disease genomics. You give a question in plain English that names a list of genes. REVEAL returns a report for each gene and a synthesis across the genes.

## Project Status

- **Stage:** release-ready (in preparation). Version 0.1.0. REVEAL is runnable. The first release tag and the independent reproduction are not complete yet.
- **Repository:** [tkria/REVEAL](https://github.com/tkria/REVEAL) is the main repository for development. It is a one-time copy of [brettrj03/REVEAL](https://github.com/brettrj03/REVEAL), the original repository. The two repositories are not synchronised.
- **Tests and CI:** `tests/test_smoke.py` contains smoke tests. The `ci` workflow runs them on Python 3.11, 3.12 and 3.13. The `framework-check` workflow runs the TI framework check.
- **Licence:** MIT. Refer to [LICENSE](LICENSE).

## Features

- **Natural Language Queries** — Analyse genes using plain English ("What is the functional role of MED12, EOMES, PEG3, ZIM2, PCDHA6, PCDHGA3, F8A2, MIMT1, ADPRHL1, RGPD1, and F8A3 in neurodevelopmental disorders?")
- **Comprehensive Data Integration** — Gene info, GO terms, expression data, protein interactions
- **Adaptive Literature Mining** — Tiered PubMed queries with BM25 pre-ranking and LLM-powered relevance ranking
- **LLM-Powered Interpretation** — Generate biological insights and cross-gene synthesis
- **State Persistence** — Resume interrupted runs and reuse expensive computations
- **Resume & Checkpointing** — Pick up from any node if a run is interrupted
- **Web Interface** — Streamlit app for interactive exploration of results
- **Optional Observability** — Phoenix tracing integration for debugging LLM calls

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/tkria/REVEAL.git
cd REVEAL

# 2. Create virtual environment (Python 3.11+ required)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure API keys
cp .env.example .env
# Edit .env with your API keys (see below)

# 5. Build the database (downloads ~500MB, creates ~1.3GB database)
python scripts/setup_database.py

# 6. Verify setup
python scripts/verify_database.py

# 7. Launch the web interface
streamlit run streamlit_app.py
# Or run via command line
python run_stateful_pipeline.py "What is the functional role of MED12, EOMES, PEG3, ZIM2, PCDHA6, PCDHGA3, F8A2, MIMT1, ADPRHL1, RGPD1, and F8A3 in neurodevelopmental disorders?"
```

---

## Prerequisites

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Python | 3.11 | 3.11 or 3.12 |
| RAM | 8 GB | 16 GB |
| Disk Space | 10 GB | 20 GB |
| OS | macOS 11+, Ubuntu 20.04+, Windows 10+ (WSL2 recommended) |

### Required API Keys

| Key | Required | Purpose | Get it at |
|-----|----------|---------|-----------|
| `OPENAI_API_KEY` | Yes | Gene interpretation, literature ranking | [platform.openai.com](https://platform.openai.com/api-keys) |
| `NCBI_EMAIL` | Yes | PubMed API identification | Any valid email |
| `NCBI_API_KEY` | No | Higher PubMed rate limits (10 req/s vs 3) | [ncbi.nlm.nih.gov](https://www.ncbi.nlm.nih.gov/account/) |

---

## Setup

### Step 1: Clone and Set Up Environment

```bash
git clone https://github.com/tkria/REVEAL.git
cd REVEAL

python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Verify core imports work:
```bash
python -c "import pydantic_graph; import openai; import streamlit; print('All imports OK')"
```

### Step 3: Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your API keys:
```bash
OPENAI_API_KEY=sk-your-actual-key-here
NCBI_EMAIL=your.email@example.com
# NCBI_API_KEY=your-ncbi-key-here  # Optional — delete this line if you don't have one
```

> **Important:** If you don't have an NCBI API key, remove or comment out the `NCBI_API_KEY` line entirely. Leaving it blank causes 400 errors.

### Step 4: Build the Database

```bash
python scripts/setup_database.py
```

This downloads and processes:
- GENCODE v49 gene annotations (~45 MB)
- Gene Ontology terms and associations (~53 MB)
- GTEx v8 tissue expression data (~13 MB)
- STRING v12 protein interactions (~450 MB)
- NCBI gene descriptions (~8 MB)

Takes approximately 10–15 minutes. Final database size: ~1.3 GB at `src/database/gene_database.sqlite`.

### Step 5: Verify Installation

```bash
python scripts/verify_database.py
```

This checks database integrity, table counts, and API configuration.

---

## Usage

### Web Interface

```bash
streamlit run streamlit_app.py
```

Open http://localhost:8501 in your browser. Load a saved state file from the sidebar to explore previous results interactively.

### Command Line

```bash
# Full analysis with LLM interpretation (default)
python run_stateful_pipeline.py "What is the functional role of MED12, EOMES, PEG3, ZIM2, PCDHA6, PCDHGA3, F8A2, MIMT1, ADPRHL1, RGPD1, and F8A3 in neurodevelopmental disorders?"

# Fast mode — database facts only, no LLM calls, free
python run_stateful_pipeline.py "What is the functional role of GATA4, PTGFR, BNC1, PRAG1, IQGAP1, TXNDC5, ENAM, ZNF619, TMEM71, ZNF717, and NETO1-DT in congenital heart disease and cardiomyocyte function?" --factual-only

# Resume an interrupted run
python run_stateful_pipeline.py "What is the functional role of SETBP1, COL2A1, IGFBP5, VIM, DNAJC6, KYAT3, ESRP2, JARID2, NXPH4, CDK19, and DLL4 in neurodevelopmental disorders and neural progenitor cell differentiation?" --resume

# Resume from a specific node
python run_stateful_pipeline.py "What is the functional role of MED12, EOMES, PEG3, ZIM2, PCDHA6, PCDHGA3, F8A2, MIMT1, ADPRHL1, RGPD1, and F8A3 in neurodevelopmental disorders?" --resume-from InterpretAllGenes

# Check the status of a previous run
python run_stateful_pipeline.py --status results/stateful_pipeline/run_20260429_123456_query_abc123

# Run without saving state to disk
python run_stateful_pipeline.py "What is the functional role of GATA4, PTGFR, BNC1, PRAG1, IQGAP1, TXNDC5, ENAM, ZNF619, TMEM71, ZNF717, and NETO1-DT in congenital heart disease and cardiomyocyte function?" --no-persist
```

### Analysis Modes

| Mode | Speed | LLM Calls | Cost | Use Case |
|------|-------|-----------|------|----------|
| Default (interpreted) | ~20s/gene | Yes | ~$0.01–0.03/gene | Full analysis with biological insights |
| `--factual-only` | ~2s/gene | No | Free | Quick data retrieval, debugging |

---

## Data

REVEAL uses public reference data only. `scripts/setup_database.py` downloads these sources and loads them into `src/database/gene_database.sqlite`:

| Source | Release | Content |
|--------|---------|---------|
| GENCODE | v49 | Gene annotations |
| NCBI Gene | current at download | Gene descriptions |
| Gene Ontology (GO) | current at download | Ontology terms and human gene associations |
| GTEx | v8 | Median gene expression (TPM) in 54 tissues |
| STRING | v12.0 | Human protein interactions and aliases |

At run time, REVEAL also queries PubMed through the NCBI E-utilities API. Git does not track the downloaded files or the database.

For the download URLs, the retrieval dates, the file hashes and the terms of use, refer to [data/README.md](data/README.md).

## Expected Output

Each run writes one directory: `results/stateful_pipeline/run_<YYYYMMDD_HHMMSS>_query_<id>/`. The directory contains these files:

| File | Content |
|------|---------|
| `state.json` | The full pipeline state after each node: gene data, ranked papers, interpretations, validation results and the final report |
| `completion_summary.txt` | The number of genes and interpretations, the time for each node and the token usage for each node |
| `pipeline.log` | The run log |

A full run executes 21 nodes. To see the report, open `state.json` in the Streamlit app (`streamlit run streamlit_app.py`). With `--no-persist`, REVEAL writes no state to disk.

## Validation

- **Database check:** `python scripts/verify_database.py` checks the database integrity, the table counts and the API configuration.
- **Output validation in the pipeline:** five validation nodes check the LLM output (gene summaries, GO interpretation, network interpretation, literature findings and cross-gene synthesis). The code is in `src/validation/`, and the settings are in `src/validation_config/`. Each node can send an output back for refinement. The results are in `state.validation_results`.
- **Smoke tests:** `python -m pytest tests/test_smoke.py`. The tests check that the CLI imports, that the pipeline graph builds with its 21 nodes, and that the Streamlit app compiles. They need no database, no API keys and no network. CI runs them.
- **Framework check:** `python scripts/framework_check.py`.

The smoke tests do not check the scientific output. The pipeline validation is an LLM check of LLM output. It does not replace an expert review of the results.

## Project Structure

```
gene-annotation/
├── run_stateful_pipeline.py     # CLI entry point
├── streamlit_app.py             # Web interface
├── requirements.txt             # Python dependencies
├── pyproject.toml               # Package configuration
├── .env.example                 # Environment variable template
├── src/
│   ├── agents/                  # LLM agents (8 agents)
│   ├── nodes/                   # Pipeline nodes (21 nodes)
│   ├── graph/                   # Graph definition & state
│   ├── models/                  # Pydantic data models
│   ├── reports/                 # Report generation
│   ├── utils/                   # Utilities (BM25, persistence, tracing)
│   ├── integrations/            # External API clients (PubMed, etc.)
│   ├── database/                # SQLite database layer
│   ├── validation/              # Output validation logic
│   └── validation_config/       # Validation configuration
├── scripts/
│   ├── setup_database.py        # Database setup (run once)
│   └── verify_database.py       # Database verification
├── docs/                        # Extended documentation
└── tests/                       # Test suite
```

---

## Configuration

Key settings in `src/config.py`:

```python
# LLM Models
GENE_EXTRACTION_MODEL = "gpt-4.1-mini"
INTERPRETATION_MODEL = "gpt-4.1-mini"

# Database
DEFAULT_DB_PATH = "src/database/gene_database.sqlite"

# Retry Settings
MAX_INTERPRETATION_RETRIES = 2
MAX_EXTRACTION_RETRIES = 2
```

---

## Pipeline Overview

The pipeline executes 21 nodes organised into 5 phases:

| Phase | Nodes | Purpose | Key Outputs |
|-------|-------|---------|-------------|
| 1. Extraction | 2 | Parse query, fetch gene data | Gene profiles, database data |
| 2. Analysis | 3 | Cross-gene network & GO analysis | Shared partners, enriched terms |
| 3. Literature | 4 | PubMed search, BM25 pre-ranking, LLM ranking | Top papers per gene |
| 4. Interpretation & Validation | 11 | LLM insights + validation + refinement | Summaries, synthesis |
| 5. Report | 1 | Final report assembly | Comprehensive report |

State is persisted after each node — if a run is interrupted, use `--resume` to continue from the last checkpoint.


## Reproduction

To reproduce a run, follow these steps:

1. Clone the repository at the release tag, and complete the steps in [Setup](#setup).
2. Build the database with `python scripts/setup_database.py`.
3. Compare the SHA-256 hashes of the files in `src/database/data/` with the hashes in [data/README.md](data/README.md). Use `shasum -a 256 src/database/data/*`. The GO and NCBI Gene URLs give the current release, so a new download can have different hashes.
4. Run `python scripts/verify_database.py`.
5. Run `python -m pytest tests/test_smoke.py`.
6. Run the pipeline with the same question and the same models (`src/config.py`).

A run is not fully deterministic, for two reasons:

- The LLM output can change between runs, and between model versions.
- The PubMed results change when new papers are published.

For a comparison, keep the `state.json` file of each run. It records the papers that REVEAL used and the output of each node.

## Current Limitations

- The automated tests are smoke tests only. No test checks the scientific output.
- REVEAL uses OpenAI models only (`gpt-4.1-mini` by default). The LLM interpretations can be wrong, and an expert must review them.
- The pipeline validation is an LLM check of LLM output.
- The GO and NCBI Gene downloads use "current" URLs. The release label `2025-01` in `scripts/setup_database.py` does not identify the downloaded version. The retrieval date in [data/README.md](data/README.md) is the reliable reference.
- GTEx v8 is an older GTEx release.
- A full run calls paid APIs, at approximately $0.01–0.03 for each gene.
- The Project Structure section lists `docs/`, but this directory does not exist yet.

## Feedback Requested

The project owner must confirm this list.

- Is the gene interpretation correct and useful for rare disease genomics? Feedback from clinical and research geneticists is especially useful.
- Which reference data releases must REVEAL use, and must they be pinned?
- What is a good benchmark gene set to evaluate REVEAL?
- Which other LLM providers must REVEAL support?

## Troubleshooting

### "ModuleNotFoundError: No module named 'X'"

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "Database not found"

```bash
python scripts/setup_database.py
ls -lh src/database/gene_database.sqlite
```

### "Invalid API key" errors

Check your `.env` file — make sure there are no quotes around the key value:
```bash
# Correct:
OPENAI_API_KEY=sk-abc123...

# Incorrect:
OPENAI_API_KEY="sk-abc123..."
```

### "Port 8501 already in use"

```bash
streamlit run streamlit_app.py --server.port 8502
# or: lsof -i :8501 → kill -9 <PID>
```

### Database setup fails with 403 Forbidden

Some data sources (especially Gene Ontology) occasionally block automated downloads. Try again — temporary server issues are common. The setup script includes User-Agent headers and fallback URLs.

### PubMed returns 400 Bad Request

Your `NCBI_EMAIL` is likely still the placeholder, or `NCBI_API_KEY` is set but empty. Set a real email, and if you don't have an NCBI API key, **remove the line entirely** rather than leaving it blank.
