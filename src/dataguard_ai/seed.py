from __future__ import annotations

from datetime import datetime, timedelta, timezone

from .models import EtlJob, Feed, RevenueMetric, Severity

NOW = datetime(2026, 6, 14, 8, 30, tzinfo=timezone.utc)


def seed_feeds() -> list[Feed]:
    return [
        Feed(
            id="feed-prepaid-recharge",
            name="Daily prepaid recharge file",
            source_system="Payment gateway",
            destination_system="Billing warehouse",
            owner="Revenue Assurance",
            expected_arrival_utc="02:00",
            last_arrival_at=NOW - timedelta(days=1, hours=6),
            last_file_size_mb=944.2,
            expected_file_pattern="PREPAID_RECHARGE_YYYYMMDD.csv",
            criticality=Severity.critical,
            associated_metric_id="metric-prepaid-revenue",
            average_daily_revenue_usd=5_100_000,
        ),
        Feed(
            id="feed-roaming-usage",
            name="Roaming usage mediation file",
            source_system="Roaming mediation",
            destination_system="Usage rating platform",
            owner="Billing Operations",
            expected_arrival_utc="06:00",
            last_arrival_at=NOW.replace(hour=6, minute=42),
            last_file_size_mb=122.8,
            expected_file_pattern="ROAMING_USAGE_YYYYMMDD.dat",
            criticality=Severity.high,
            average_daily_revenue_usd=620_000,
        ),
        Feed(
            id="feed-postpaid-billing",
            name="Postpaid billing extract",
            source_system="CRM billing",
            destination_system="Enterprise data warehouse",
            owner="Data Engineering",
            expected_arrival_utc="07:30",
            last_arrival_at=NOW.replace(hour=7, minute=12),
            last_file_size_mb=1800.4,
            expected_file_pattern="POSTPAID_BILLING_YYYYMMDD.parquet",
            criticality=Severity.high,
            associated_metric_id="metric-postpaid-revenue",
            average_daily_revenue_usd=8_400_000,
        ),
    ]


def seed_jobs() -> list[EtlJob]:
    return [
        EtlJob(
            id="job-prepaid-load",
            name="Load prepaid recharge to billing mart",
            owner="Data Engineering",
            status="failed",
            started_at=NOW.replace(hour=2, minute=15),
            ended_at=NOW.replace(hour=2, minute=23),
            expected_runtime_minutes=35,
            actual_runtime_minutes=8,
            upstream_feed_ids=["feed-prepaid-recharge"],
        ),
        EtlJob(
            id="job-revenue-aggregate",
            name="Aggregate daily revenue metrics",
            owner="BI Platform",
            status="success",
            started_at=NOW.replace(hour=7, minute=35),
            ended_at=NOW.replace(hour=8, minute=25),
            expected_runtime_minutes=25,
            actual_runtime_minutes=50,
            upstream_feed_ids=["feed-postpaid-billing", "feed-prepaid-recharge"],
        ),
    ]


def seed_metrics() -> list[RevenueMetric]:
    return [
        RevenueMetric(
            id="metric-prepaid-revenue",
            name="Daily prepaid recharge revenue",
            business_date="2026-06-14",
            actual_value_usd=3_350_000,
            historical_values_usd=[5_120_000, 5_050_000, 5_210_000, 4_980_000, 5_180_000, 5_090_000, 5_160_000],
            owner="Revenue Assurance",
            segment="Prepaid",
        ),
        RevenueMetric(
            id="metric-postpaid-revenue",
            name="Daily postpaid billing revenue",
            business_date="2026-06-14",
            actual_value_usd=8_220_000,
            historical_values_usd=[8_310_000, 8_420_000, 8_390_000, 8_360_000, 8_510_000, 8_280_000, 8_440_000],
            owner="Billing Operations",
            segment="Postpaid",
        ),
    ]
