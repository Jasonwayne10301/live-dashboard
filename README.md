# Live System Dashboard

A comprehensive real-time system metrics dashboard built with **FastAPI WebSocket** and **Vue.js**. Monitors CPU, memory, disk, network, and response time across multiple servers with live alerts, Prometheus integration, and remote monitoring capabilities.

![CI](https://github.com/Jasonwayne10301/live-dashboard/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12-blue)
![Vue](https://img.shields.io/badge/vue-3.5-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)

---

## ✨ Features

- **Real-time Metrics Streaming**: WebSocket-powered updates every 2 seconds
- **Multi-Server Monitoring**: Support for local and remote servers via SSH or HTTP (query /metrics endpoint)
- **Interactive Charts**: Live CPU, Memory, Disk, Response Time charts using Chart.js
- **Intelligent Alert System**: Auto-triggered alerts for CPU > 85%, Memory > 80%, Disk > 90%
- **Modern UI**: Dark-themed interface built with Vue 3, Pinia, and Vue Router
- **Auto-Reconnect**: Robust WebSocket reconnection on network issues
- **RESTful API**: Comprehensive endpoints for metrics, history, and stats
- **Prometheus Integration**: Expose metrics for monitoring and alerting
- **Docker Ready**: One-command deployment with Docker Compose
- **Scalable Architecture**: Modular backend with async support

---

## 🛠 Tech Stack

| Layer       | Technology                  | Description |
|-------------|-----------------------------|-------------|
| **Backend** | FastAPI + Uvicorn          | High-performance async web framework |
| **Real-time**| WebSocket (FastAPI)        | Native WebSocket support for live data |
| **Frontend**| Vue 3 + Vite               | Modern reactive UI framework |
| **State Mgmt**| Pinia                      | Intuitive state management for Vue |
| **Charts**  | Chart.js + vue-chartjs     | Interactive data visualization |
| **Database**| PostgreSQL                 | Persistent storage for metrics history |
| **Cache**   | Redis                      | High-speed caching and session storage |
| **Monitoring**| Prometheus Client         | Metrics exposition for monitoring |
| **Remote Access**| Paramiko                | SSH client for remote server monitoring |
| **Container**| Docker + Docker Compose   | Containerization and orchestration |
| **CI/CD**   | GitHub Actions             | Automated testing and deployment |

---

## 🚀 Quick Start

### Prerequisites
- **Docker & Docker Compose** (recommended)
- **Python 3.12+** (for local development)
- **Node.js 20+** (for frontend development)
- **Git** (for version control)

### Installation

#### Option 1: Docker (Recommended)
```bash
# Clone the repository
git clone https://github.com/Jasonwayne10301/live-dashboard.git
cd live-dashboard

# Start all services
docker compose up -d

# View logs
docker compose logs -f
```

#### Option 2: Local Development
```bash
# Clone and setup backend
git clone https://github.com/Jasonwayne10301/live-dashboard.git
cd live-dashboard/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start backend
uvicorn app.main:app --reload

# Frontend (new terminal)
cd ../frontend
npm install
npm run dev
```

### Access Points
- **Dashboard UI**: http://localhost:5173
- **API Documentation**: http://localhost:8000/docs
- **Prometheus Metrics**: http://localhost:8000/metrics
- **WebSocket Metrics**: `ws://localhost:8000/ws/metrics`
- **WebSocket Alerts**: `ws://localhost:8000/ws/alerts`

### Running on Personal Laptop
After cloning from GitHub, simply run:
```bash
docker compose up --build -d
```
Then access the dashboard at http://localhost:5173. All dependencies are containerized - no local Python/Node.js setup required!

---

## ⚙️ Configuration

### Environment Variables
Create a `.env` file in the `backend/` directory:

```env
# Database
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=live_dashboard

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Application
SECRET_KEY=your_jwt_secret_key_here
USE_REAL_METRICS=true
METRIC_EMIT_INTERVAL=2.0

# Remote Servers (for multi-server monitoring)
# Add SSH credentials for remote servers
```

### Remote Server Configuration
Edit `backend/app/core/config.py`:

```python
REMOTE_SERVERS = {
    'server-01': {'host': 'localhost', 'user': '', 'password': ''},
    'server-02': {'host': '192.168.1.10', 'port': 8001, 'protocol': 'http'},  # HTTP remote monitoring
    'server-03': {'host': 'remote-server.com', 'user': 'monitor', 'key': '/path/to/ssh/key'},  # SSH remote
}
```

**Protocols Supported**:
- **HTTP**: Query `/metrics` endpoint from remote dashboard instances (recommended for testing)
- **SSH**: Direct SSH connection with psutil commands (requires Python/psutil on remote server)

**Security Note**: Never commit passwords or private keys to Git. Use environment variables or secure key management.

---

## 📡 API Reference

### REST Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/docs` | Interactive API documentation |
| GET | `/metrics` | Prometheus metrics exposition |
| GET | `/api/v1/metrics/servers` | List all monitored servers |
| GET | `/api/v1/metrics/summary` | Latest metrics snapshot for all servers |
| GET | `/api/v1/metrics/history/{server_id}` | Historical metrics (last 30 snapshots) |
| GET | `/api/v1/metrics/stats/connections` | WebSocket connection statistics |

### WebSocket Endpoints

| Endpoint | Description | Message Format |
|----------|-------------|----------------|
| `/ws/metrics` | Real-time metrics stream | `{"type": "metric", "server_id": "...", "cpu": 45.2, ...}` |
| `/ws/alerts` | Real-time alert notifications | `{"type": "alert", "server_id": "...", "metric": "cpu", "value": 90.5, ...}` |

### Sample API Usage

```bash
# Get server list
curl http://localhost:8000/api/v1/metrics/servers

# Get latest metrics
curl http://localhost:8000/api/v1/metrics/summary

# WebSocket connection (using wscat)
wscat -c ws://localhost:8000/ws/metrics
```

---

## 🏗 Project Architecture

```
live-dashboard/
├── backend/
│   ├── app/
│   │   ├── api/v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── metrics.py      # REST API endpoints
│   │   │   │   └── websocket.py    # WebSocket handlers
│   │   │   └── router.py           # API routing
│   │   ├── core/
│   │   │   ├── config.py           # Settings & configuration
│   │   │   ├── simulator.py        # Metrics generation & remote monitoring
│   │   │   ├── ws_manager.py       # WebSocket connection management
│   │   │   └── prometheus_metrics.py # Prometheus gauges
│   │   ├── schemas/
│   │   │   └── metric.py           # Pydantic models
│   │   └── main.py                 # FastAPI application
│   ├── requirements.txt            # Python dependencies
│   ├── Dockerfile                  # Backend containerization
│   └── pytest.ini                  # Testing configuration
├── frontend/
│   ├── src/
│   │   ├── components/             # Vue components
│   │   ├── composables/            # Reusable logic
│   │   ├── stores/                 # Pinia state management
│   │   ├── views/                  # Page components
│   │   └── router/                 # Vue Router configuration
│   ├── package.json                # Node dependencies
│   ├── vite.config.js              # Vite configuration
│   └── index.html                  # HTML template
├── docker-compose.yml              # Multi-service orchestration
├── README.md                       # This file
└── .gitignore                      # Git ignore rules
```

### Key Components

- **Simulator**: Generates metrics using psutil (local) or SSH (remote)
- **WS Manager**: Handles WebSocket connections and broadcasting
- **Metric Store**: Vue state management with real-time updates
- **Prometheus Integration**: Exposes metrics for external monitoring

---

## 🔧 Development

### Running Tests
```bash
cd backend
pytest tests/
```

### Code Quality
```bash
# Backend linting
pip install black isort flake8
black .
isort .
flake8 .

# Frontend linting
cd frontend
npm run lint
```

### Building for Production
```bash
# Backend
cd backend
docker build -t dashboard-api .

# Frontend
cd frontend
npm run build
```

---

## 🚀 Deployment

### Docker Deployment
```bash
# Build and deploy
docker compose up -d --build

# Scale backend instances
docker compose up -d --scale backend=3
```

### Production Considerations
- **Environment Variables**: Use secure secrets management
- **Database**: Configure PostgreSQL with backups
- **Redis**: Set up persistence and clustering
- **Monitoring**: Integrate with Prometheus/Grafana
- **Security**: Enable HTTPS, configure CORS properly
- **Scaling**: Use load balancer for multiple backend instances

### Prometheus Setup
Add to your `prometheus.yml`:
```yaml
scrape_configs:
  - job_name: 'live-dashboard'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
```

---

## 🚀 Production Readiness

This dashboard is designed for production use with:
- **Async/Await**: All I/O operations are non-blocking for high concurrency
- **Error Handling**: Graceful fallbacks for network/remote server failures
- **Security**: CORS, input validation, and secure configuration practices
- **Monitoring**: Built-in Prometheus metrics and health checks
- **Scalability**: WebSocket broadcasting supports multiple clients
- **Remote Monitoring**: HTTP-based remote queries (easier than SSH for testing)

### Next Steps for Production
- Add JWT authentication for API/WebSocket endpoints
- Implement persistent metrics storage in PostgreSQL
- Set up Kubernetes deployment with Helm charts
- Configure TLS/HTTPS with Let's Encrypt
- Add rate limiting and DDoS protection

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use Vue Composition API style
- Write tests for new features
- Update documentation for API changes
- Ensure Docker compatibility

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [Vue.js](https://vuejs.org/) for the reactive frontend framework
- [Chart.js](https://www.chartjs.org/) for data visualization
- [Prometheus](https://prometheus.io/) for metrics monitoring

---

## 📞 Support

If you have questions or need help:
- Open an issue on GitHub
- Check the API documentation at `/docs`
- Review the code comments for implementation details

Happy monitoring! 📊
