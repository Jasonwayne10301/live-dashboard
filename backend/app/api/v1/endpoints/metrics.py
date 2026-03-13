from fastapi import APIRouter, Query
from typing import Optional
from app.core.ws_manager import manager
from app.core.simulator import MetricSimulator

router = APIRouter(prefix="/metrics", tags=["Metrics"])

# In-memory store for last N snapshots per server
# In production: replace with PostgreSQL + TimescaleDB or InfluxDB
_history: dict[str, list] = {}
MAX_HISTORY = 100


def record_snapshot(snapshot: dict):
    """Called by simulator to store history."""
    sid = snapshot["server_id"]
    _history.setdefault(sid, []).append(snapshot)
    if len(_history[sid]) > MAX_HISTORY:
        _history[sid].pop(0)


@router.get("/servers")
async def list_servers():
    """List all monitored servers."""
    return {
        "servers": MetricSimulator.SERVERS,
        "total": len(MetricSimulator.SERVERS),
        "connected_clients": manager.client_count("metrics"),
    }


@router.get("/history/{server_id}")
async def get_history(
    server_id: str,
    limit: int = Query(default=50, ge=1, le=100),
    metric: Optional[str] = Query(default=None, description="Filter: cpu | memory | disk | request_rate | response_time"),
):
    """
    Get recent metric history for a server.
    Returns last `limit` snapshots.
    """
    if server_id not in MetricSimulator.SERVERS:
        return {"error": f"Unknown server: {server_id}"}

    history = _history.get(server_id, [])[-limit:]

    if metric:
        return {
            "server_id": server_id,
            "metric": metric,
            "data": [
                {"timestamp": s["timestamp"], "value": s.get(metric)}
                for s in history if metric in s
            ],
        }

    return {"server_id": server_id, "data": history}


@router.get("/summary")
async def get_summary():
    """Get latest snapshot for all servers (dashboard overview)."""
    summary = []
    for server_id in MetricSimulator.SERVERS:
        snapshots = _history.get(server_id, [])
        if snapshots:
            summary.append(snapshots[-1])
    return {"servers": summary, "total": len(summary)}


@router.get("/stats/connections")
async def get_connection_stats():
    return {
        "metrics_room": manager.client_count("metrics"),
        "alerts_room": manager.client_count("alerts"),
        "total": manager.total_clients(),
    }
