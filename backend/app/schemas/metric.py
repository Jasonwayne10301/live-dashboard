from pydantic import BaseModel
from typing import Optional
from enum import Enum


class MetricSnapshot(BaseModel):
    """One reading of all metrics for a single server."""
    type: str = "metric"
    server_id: str
    timestamp: str
    cpu: float          # percent 0-100
    memory: float       # percent 0-100
    disk: float         # percent 0-100
    network_in: float   # Mbps
    network_out: float  # Mbps
    request_rate: float # requests/sec
    response_time: float  # milliseconds
    active_connections: int


class AlertSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class AlertEvent(BaseModel):
    """Triggered when a metric exceeds its threshold."""
    type: str = "alert"
    server_id: str
    timestamp: str
    metric: str
    value: float
    threshold: float
    severity: AlertSeverity
    message: str


class MetricHistoryResponse(BaseModel):
    server_id: str
    metric: str
    data: list[dict]  # [{timestamp, value}, ...]
