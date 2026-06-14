from __future__ import annotations

from datetime import datetime, time, timezone
from statistics import mean, pstdev
from uuid import uuid4

from .models import Alert, EtlJob, Feed, FeedStatus, RevenueMetric, Severity


def _parse_hhmm(value: str) -> time:
    hour, minute = value.split(":")
    return time(hour=int(hour), minute=int(minute), tzinfo=timezone.utc)


def classify_feed(feed: Feed, now: datetime) -> FeedStatus:
    expected = _parse_hhmm(feed.expected_arrival_utc)
    expected_dt = datetime.combine(now.date(), expected)
    if feed.last_arrival_at and feed.last_arrival_at.date() == now.date() and feed.last_arrival_at <= expected_dt:
        return FeedStatus.healthy
    if now <= expected_dt:
        return FeedStatus.healthy
    if feed.last_arrival_at and feed.last_arrival_at.date() == now.date():
        return FeedStatus.warning
    return FeedStatus.failed


def estimate_feed_impact(feed: Feed, now: datetime) -> float:
    expected = _parse_hhmm(feed.expected_arrival_utc)
    expected_dt = datetime.combine(now.date(), expected)
    if now <= expected_dt or feed.average_daily_revenue_usd == 0:
        return 0
    hours_late = max((now - expected_dt).total_seconds() / 3600, 1)
    return round(min(feed.average_daily_revenue_usd, feed.average_daily_revenue_usd * hours_late / 24), 2)


def detect_feed_alerts(feeds: list[Feed], now: datetime) -> list[Alert]:
    alerts: list[Alert] = []
    for feed in feeds:
        status = classify_feed(feed, now)
        if status == FeedStatus.healthy:
            continue
        impact = estimate_feed_impact(feed, now)
        alert_type = "late_file" if status == FeedStatus.warning else "missing_file"
        title = f"{feed.name} is {'late' if status == FeedStatus.warning else 'missing'}"
        alerts.append(Alert(
            id=str(uuid4()),
            type=alert_type,
            severity=feed.criticality,
            title=title,
            description=(
                f"Expected {feed.expected_file_pattern} from {feed.source_system} by "
                f"{feed.expected_arrival_utc} UTC for {feed.destination_system}."
            ),
            owner=feed.owner,
            created_at=now,
            estimated_revenue_at_risk_usd=impact,
            confidence="high" if impact else "medium",
            recommended_next_steps=[
                "Confirm whether the source system generated the file.",
                "Check transfer logs and credentials for the source location.",
                "Notify the revenue assurance owner before downstream billing runs.",
            ],
            related_feed_id=feed.id,
            related_metric_id=feed.associated_metric_id,
        ))
    return alerts


def detect_job_alerts(jobs: list[EtlJob], now: datetime) -> list[Alert]:
    alerts: list[Alert] = []
    for job in jobs:
        if job.status == "failed":
            alerts.append(Alert(
                id=str(uuid4()),
                type="etl_failure",
                severity=Severity.high,
                title=f"ETL job failed: {job.name}",
                description="A monitored ETL job reported failed status and may block downstream revenue reporting.",
                owner=job.owner,
                created_at=now,
                estimated_revenue_at_risk_usd=0,
                confidence="medium",
                recommended_next_steps=["Open scheduler logs.", "Check upstream feed completeness.", "Rerun only after validating source data."],
                related_job_id=job.id,
            ))
        if job.actual_runtime_minutes and job.actual_runtime_minutes > job.expected_runtime_minutes * 1.5:
            alerts.append(Alert(
                id=str(uuid4()),
                type="runtime_anomaly",
                severity=Severity.medium,
                title=f"ETL runtime anomaly: {job.name}",
                description=f"Runtime is {job.actual_runtime_minutes} minutes versus expected {job.expected_runtime_minutes} minutes.",
                owner=job.owner,
                created_at=now,
                estimated_revenue_at_risk_usd=0,
                confidence="medium",
                recommended_next_steps=["Check warehouse load and queue depth.", "Review recent upstream volume changes."],
                related_job_id=job.id,
            ))
    return alerts


def detect_revenue_alerts(metrics: list[RevenueMetric], now: datetime) -> list[Alert]:
    alerts: list[Alert] = []
    for metric in metrics:
        if len(metric.historical_values_usd) < 3:
            continue
        baseline = mean(metric.historical_values_usd)
        deviation = baseline - metric.actual_value_usd
        std_dev = pstdev(metric.historical_values_usd) or baseline * 0.05
        percent_drop = deviation / baseline if baseline else 0
        if deviation > max(std_dev * 2, baseline * 0.15):
            alerts.append(Alert(
                id=str(uuid4()),
                type="revenue_variance",
                severity=Severity.critical if percent_drop >= 0.25 else Severity.high,
                title=f"Abnormal revenue variance: {metric.name}",
                description=(
                    f"{metric.segment} revenue is {percent_drop:.0%} below historical baseline "
                    f"(${baseline:,.0f} expected vs ${metric.actual_value_usd:,.0f} actual)."
                ),
                owner=metric.owner,
                created_at=now,
                estimated_revenue_at_risk_usd=round(deviation, 2),
                confidence="high",
                recommended_next_steps=[
                    "Compare contributing product and channel totals.",
                    "Check today's file arrivals linked to this metric.",
                    "Validate whether the variance is a real business event or data delay.",
                ],
                related_metric_id=metric.id,
            ))
    return alerts
