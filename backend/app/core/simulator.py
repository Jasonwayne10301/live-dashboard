import asyncio
import random
import math
from datetime import datetime, timezone
from typing import Optional
import psutil
import paramiko
from app.core.config import settings
from app.core.ws_manager import manager
from app.schemas.metric import MetricSnapshot, AlertEvent, AlertSeverity
from app.core.prometheus_metrics import cpu_gauge, memory_gauge, disk_gauge, network_in_gauge, network_out_gauge, request_rate_gauge, response_time_gauge, active_connections_gauge


class MetricSimulator:
    """
    Simulates realistic system metrics for multiple servers.
    Broadcasts snapshots via WebSocket every METRIC_EMIT_INTERVAL seconds.
    Uses sine waves + noise to create natural-looking fluctuations.
    """

    SERVERS = ["server-01", "server-02", "server-03"]

    def __init__(self):
        self._task: Optional[asyncio.Task] = None
        self._tick = 0
        # Per-server state for smooth transitions
        self._cpu_base = {s: random.uniform(20, 50) for s in self.SERVERS}
        self._mem_base = {s: random.uniform(40, 65) for s in self.SERVERS}

    async def start(self):
        self._task = asyncio.create_task(self._run())

    async def stop(self):
        if self._task:
            self._task.cancel()

    async def _run(self):
        while True:
            await asyncio.sleep(settings.METRIC_EMIT_INTERVAL)
            self._tick += 1
            for server in self.SERVERS:
                snapshot = self._generate(server)
                await manager.broadcast(snapshot.model_dump(), room="metrics")

                # Update Prometheus metrics
                cpu_gauge.labels(server=server).set(snapshot.cpu)
                memory_gauge.labels(server=server).set(snapshot.memory)
                disk_gauge.labels(server=server).set(snapshot.disk)
                network_in_gauge.labels(server=server).set(snapshot.network_in)
                network_out_gauge.labels(server=server).set(snapshot.network_out)
                request_rate_gauge.labels(server=server).set(snapshot.request_rate)
                response_time_gauge.labels(server=server).set(snapshot.response_time)
                active_connections_gauge.labels(server=server).set(snapshot.active_connections)

                # Check alert thresholds
                alerts = self._check_alerts(snapshot)
                for alert in alerts:
                    await manager.broadcast(alert.model_dump(), room="alerts")

    def _generate(self, server: str) -> MetricSnapshot:
        if settings.USE_REAL_METRICS:  # Thêm setting này vào config.py
            return self._generate_real(server)
        else:
            return self._generate_simulated(server)

    def _generate_real(self, server: str) -> MetricSnapshot:
        server_config = settings.REMOTE_SERVERS.get(server, {})
        host = server_config.get('host', 'localhost')
        
        if host == 'localhost':
            # Local metrics
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            net = psutil.net_io_counters()
            net_in = net.bytes_recv / 1024 / 1024 * 8  # Mbps
            net_out = net.bytes_sent / 1024 / 1024 * 8  # Mbps
        else:
            # Remote metrics via SSH
            cpu, mem, disk, net_in, net_out = self._get_remote_metrics(host, server_config)
        
        # Simulated request_rate and response_time (or get from app)
        req_rate = random.uniform(100, 300)
        response_time = random.uniform(50, 150)
        
        return MetricSnapshot(
            server_id=server,
            timestamp=datetime.now(timezone.utc).isoformat(),
            cpu=round(cpu, 1),
            memory=round(mem, 1),
            disk=round(disk, 1),
            network_in=round(net_in, 1),
            network_out=round(net_out, 1),
            request_rate=round(req_rate, 0),
            response_time=round(response_time, 0),
            active_connections=random.randint(50, 500),
        )

    def _get_remote_metrics(self, host: str, config: dict) -> tuple:
        """Get metrics from remote server via SSH."""
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host, username=config.get('user'), password=config.get('password'), key_filename=config.get('key'))
            
            # Run psutil commands remotely (assuming Python with psutil installed on remote)
            commands = {
                'cpu': "python3 -c 'import psutil; print(psutil.cpu_percent(interval=1))'",
                'mem': "python3 -c 'import psutil; print(psutil.virtual_memory().percent)'",
                'disk': "python3 -c 'import psutil; print(psutil.disk_usage(\"/\").percent)'",
                'net': "python3 -c 'import psutil; n=psutil.net_io_counters(); print(n.bytes_recv/1024/1024*8, n.bytes_sent/1024/1024*8)'"
            }
            
            cpu = float(self._run_ssh_command(client, commands['cpu']))
            mem = float(self._run_ssh_command(client, commands['mem']))
            disk = float(self._run_ssh_command(client, commands['disk']))
            net_data = self._run_ssh_command(client, commands['net']).split()
            net_in, net_out = float(net_data[0]), float(net_data[1])
            
            client.close()
            return cpu, mem, disk, net_in, net_out
        except Exception as e:
            print(f"Error getting remote metrics for {host}: {e}")
            # Fallback to simulated
            return random.uniform(10, 90), random.uniform(20, 80), random.uniform(30, 95), random.uniform(10, 100), random.uniform(5, 50)

    def _run_ssh_command(self, client: paramiko.SSHClient, command: str) -> str:
        stdin, stdout, stderr = client.exec_command(command)
        return stdout.read().decode().strip()
    def _generate_simulated(self, server: str) -> MetricSnapshot:
        t = self._tick
        # CPU: base + sine wave + random noise
        cpu = (
            self._cpu_base[server]
            + 15 * math.sin(t * 0.3)
            + 10 * math.sin(t * 0.07)
            + random.gauss(0, 3)
        )
        # Occasional spike
        if random.random() < 0.05:
            cpu += random.uniform(20, 40)
        cpu = max(1.0, min(99.9, cpu))

        # Memory: slower drift
        mem = (
            self._mem_base[server]
            + 8 * math.sin(t * 0.05)
            + random.gauss(0, 1.5)
        )
        mem = max(10.0, min(95.0, mem))

        # Disk: slowly increases (simulate writes) with trend
        disk_trend = (t * 0.005) % 20  # Tăng chậm theo thời gian
        disk = 45.0 + disk_trend + random.gauss(0, 0.5)
        disk = max(10.0, min(98.0, disk))

        # Network (Mbps)
        net_in = abs(50 + 40 * math.sin(t * 0.2) + random.gauss(0, 5))
        net_out = abs(30 + 25 * math.sin(t * 0.15 + 1) + random.gauss(0, 4))
        # Thêm failure: 1% chance network drop
        if random.random() < 0.01:
            net_in = 0
            net_out = 0

        # Request rate (req/s)
        req_rate = abs(200 + 150 * math.sin(t * 0.1) + random.gauss(0, 20))

        # Response time (ms)
        response_time = abs(80 + 60 * math.sin(t * 0.12) + random.gauss(0, 10))
        if cpu > 85:
            response_time *= 1.5  # Spike response time when CPU is high

        return MetricSnapshot(
            server_id=server,
            timestamp=datetime.now(timezone.utc).isoformat(),
            cpu=round(cpu, 1),
            memory=round(mem, 1),
            disk=round(disk, 1),
            network_in=round(net_in, 1),
            network_out=round(net_out, 1),
            request_rate=round(req_rate, 0),
            response_time=round(response_time, 0),
            active_connections=random.randint(50, 500),
        )

    def _check_alerts(self, snap: MetricSnapshot) -> list[AlertEvent]:
        alerts = []
        if snap.cpu > settings.ALERT_THRESHOLD_CPU:
            alerts.append(AlertEvent(
                server_id=snap.server_id,
                timestamp=snap.timestamp,
                metric="cpu",
                value=snap.cpu,
                threshold=settings.ALERT_THRESHOLD_CPU,
                severity=AlertSeverity.CRITICAL if snap.cpu > 95 else AlertSeverity.WARNING,
                message=f"{snap.server_id}: CPU at {snap.cpu}%",
            ))
        if snap.memory > settings.ALERT_THRESHOLD_MEMORY:
            alerts.append(AlertEvent(
                server_id=snap.server_id,
                timestamp=snap.timestamp,
                metric="memory",
                value=snap.memory,
                threshold=settings.ALERT_THRESHOLD_MEMORY,
                severity=AlertSeverity.WARNING,
                message=f"{snap.server_id}: Memory at {snap.memory}%",
            ))
        return alerts
