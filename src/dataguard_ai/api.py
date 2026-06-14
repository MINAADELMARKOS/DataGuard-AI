from __future__ import annotations

import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from .models import Alert, Dashboard
from .monitoring import classify_feed, detect_feed_alerts, detect_job_alerts, detect_revenue_alerts
from .seed import NOW, seed_feeds, seed_jobs, seed_metrics

FEEDS = seed_feeds()
JOBS = seed_jobs()
METRICS = seed_metrics()
WEB_ROOT = Path(__file__).resolve().parents[2] / "web"


def current_alerts() -> list[Alert]:
    return [*detect_feed_alerts(FEEDS, NOW), *detect_job_alerts(JOBS, NOW), *detect_revenue_alerts(METRICS, NOW)]


def dashboard_payload() -> Dashboard:
    statuses = [classify_feed(feed, NOW) for feed in FEEDS]
    alerts = current_alerts()
    return Dashboard(
        total_feeds=len(FEEDS),
        healthy_feeds=sum(status == "healthy" for status in statuses),
        warning_feeds=sum(status == "warning" for status in statuses),
        failed_feeds=sum(status == "failed" for status in statuses),
        open_alerts=len(alerts),
        critical_alerts=sum(alert.severity == "critical" for alert in alerts),
        estimated_revenue_at_risk_usd=round(sum(alert.estimated_revenue_at_risk_usd for alert in alerts), 2),
        feeds=[{"id": feed.id, "name": feed.name, "status": classify_feed(feed, NOW).value, "owner": feed.owner} for feed in FEEDS],
        alerts=alerts,
    )


def serialize(value: Any) -> Any:
    if hasattr(value, "to_dict"):
        return value.to_dict()
    if isinstance(value, list):
        return [serialize(item) for item in value]
    return value


class DataGuardHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, directory=str(WEB_ROOT), **kwargs)

    def do_GET(self) -> None:
        routes = {
            "/api/health": {"status": "ok", "service": "dataguard-ai"},
            "/api/feeds": FEEDS,
            "/api/jobs": JOBS,
            "/api/metrics": METRICS,
            "/api/alerts": current_alerts(),
            "/api/dashboard": dashboard_payload(),
        }
        if self.path in routes:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(serialize(routes[self.path])).encode("utf-8"))
            return
        super().do_GET()


def run(host: str = "127.0.0.1", port: int = 8000) -> None:
    server = ThreadingHTTPServer((host, port), DataGuardHandler)
    print(f"DataGuard AI running at http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
