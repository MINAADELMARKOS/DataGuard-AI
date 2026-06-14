from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from typing import Literal, Any


class Severity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class FeedStatus(str, Enum):
    healthy = "healthy"
    warning = "warning"
    failed = "failed"


@dataclass
class Serializable:
    def to_dict(self) -> dict[str, Any]:
        def convert(value: Any) -> Any:
            if isinstance(value, datetime):
                return value.isoformat()
            if isinstance(value, Enum):
                return value.value
            if isinstance(value, list):
                return [convert(item) for item in value]
            if isinstance(value, dict):
                return {key: convert(item) for key, item in value.items()}
            return value
        return convert(asdict(self))


@dataclass
class Feed(Serializable):
    id: str
    name: str
    source_system: str
    destination_system: str
    owner: str
    expected_arrival_utc: str
    last_arrival_at: datetime | None
    expected_file_pattern: str
    criticality: Severity
    last_file_size_mb: float | None = None
    associated_metric_id: str | None = None
    average_daily_revenue_usd: float = 0


@dataclass
class EtlJob(Serializable):
    id: str
    name: str
    owner: str
    status: Literal["success", "failed", "running", "late"]
    started_at: datetime | None
    ended_at: datetime | None
    expected_runtime_minutes: int
    actual_runtime_minutes: int | None = None
    upstream_feed_ids: list[str] = field(default_factory=list)


@dataclass
class RevenueMetric(Serializable):
    id: str
    name: str
    business_date: str
    actual_value_usd: float
    historical_values_usd: list[float]
    owner: str
    segment: str


@dataclass
class Alert(Serializable):
    id: str
    type: Literal["missing_file", "late_file", "etl_failure", "runtime_anomaly", "revenue_variance"]
    severity: Severity
    title: str
    description: str
    owner: str
    created_at: datetime
    estimated_revenue_at_risk_usd: float
    confidence: Literal["low", "medium", "high"]
    recommended_next_steps: list[str]
    related_feed_id: str | None = None
    related_job_id: str | None = None
    related_metric_id: str | None = None


@dataclass
class Dashboard(Serializable):
    total_feeds: int
    healthy_feeds: int
    warning_feeds: int
    failed_feeds: int
    open_alerts: int
    critical_alerts: int
    estimated_revenue_at_risk_usd: float
    feeds: list[dict]
    alerts: list[Alert]
