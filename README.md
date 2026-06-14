# DataGuard AI

DataGuard AI is an enterprise SaaS MVP for telecom data and revenue-assurance teams. It monitors critical data feeds and ETL jobs, detects missing files and abnormal revenue variance, generates operational alerts, and estimates business impact before failures become revenue leakage.

## What this MVP includes

- Feed registry for critical telecom files and pipelines.
- Missing-file and late-file detection.
- ETL job health and runtime anomaly detection.
- Revenue variance anomaly detection using historical baselines.
- Business-impact estimation for revenue at risk.
- Alert dashboard with severity, owners, and recommended next steps.
- REST API plus a runnable static web UI.
- Seed telecom scenarios inspired by missing files, batch lag, replication failures, and revenue variance.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .[dev]  # optional, for editable imports
PYTHONPATH=src python -m dataguard_ai.api
```

Open `http://127.0.0.1:8000` in your browser.

## Run tests

```bash
pytest
```

## API examples

```bash
curl http://127.0.0.1:8000/api/dashboard
curl http://127.0.0.1:8000/api/feeds
curl http://127.0.0.1:8000/api/alerts
```

## Product scope

See [`docs/product-plan.md`](docs/product-plan.md) for the ICP, MVP scope, architecture, validation plan, pricing, first-customer motion, and one-year roadmap.
