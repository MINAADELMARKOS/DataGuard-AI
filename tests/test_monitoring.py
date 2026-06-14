from datetime import datetime, timezone

from dataguard_ai.monitoring import classify_feed, detect_feed_alerts, detect_revenue_alerts
from dataguard_ai.models import Feed, RevenueMetric, Severity


def test_missing_critical_feed_creates_revenue_impact_alert():
    now = datetime(2026, 6, 14, 8, 0, tzinfo=timezone.utc)
    feed = Feed(
        id="f1",
        name="Prepaid recharge",
        source_system="Gateway",
        destination_system="Warehouse",
        owner="Revenue Assurance",
        expected_arrival_utc="02:00",
        last_arrival_at=None,
        expected_file_pattern="PREPAID_YYYYMMDD.csv",
        criticality=Severity.critical,
        average_daily_revenue_usd=2_400_000,
    )

    alerts = detect_feed_alerts([feed], now)

    assert classify_feed(feed, now) == "failed"
    assert alerts[0].type == "missing_file"
    assert alerts[0].estimated_revenue_at_risk_usd == 600_000


def test_revenue_variance_detects_large_drop():
    metric = RevenueMetric(
        id="m1",
        name="Daily prepaid revenue",
        business_date="2026-06-14",
        actual_value_usd=700_000,
        historical_values_usd=[1_000_000, 1_040_000, 990_000, 1_020_000],
        owner="Revenue Assurance",
        segment="Prepaid",
    )

    alerts = detect_revenue_alerts([metric], datetime(2026, 6, 14, tzinfo=timezone.utc))

    assert len(alerts) == 1
    assert alerts[0].severity == "critical"
    assert alerts[0].estimated_revenue_at_risk_usd > 300_000
