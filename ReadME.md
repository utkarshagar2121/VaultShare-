# DevOps nginx reverse proxy task

This demonstrates a simple multi-service environment using Docker Compose.  
It includes two backend services (Go and Python Flask) and an Nginx reverse proxy that routes requests to the appropriate service.

---

## 📁 Project Structure

```
./
├── service_1/ # Go service
│ ├── Dockerfile
│ └── main.go
├── service_2/ # Python Flask service
│ ├── Dockerfile
│ └── app.py
├── nginx/ # Nginx reverse proxy
│ ├── Dockerfile
│ └── nginx.conf
├── docker-compose.yml
└── README.md
```

---

## 📦 Requirements

- Docker
- Docker Compose

---

## 🚀 Setup and Running

Clone the repository

```bash
git clone https://github.com/whonehuljain/nginx-reverse-proxy-docker.git
```

To build and start all services, run:

```bash
docker compose up --build
```

This command will:

- Build Docker images for each service
- Start all containers in the correct order
- Expose the Nginx proxy on port **8000**

---

## 🔗 Access the Services

- **Nginx Proxy**: [http://localhost:8000](http://localhost:8000)
- **Service 1 (Go)**: [http://localhost:8000/service1/ping](http://localhost:8000/service1/ping)
- **Service 2 (Python Flask)**: [http://localhost:8000/service2/ping](http://localhost:8000/service2/ping)

---

## ✅ Testing

You can test the setup using the included test script:

```bash
./test.sh
```

This script checks:

- Container health status
- Nginx proxy routing

---

## ⚙️ How It Works

- **Service 1**: Go server listening on port `8001`
- **Service 2**: Python Flask server listening on port `8002`
- **Nginx**: Reverse proxy listening on port `8000`, routing:
  - `/service1/` → Service 1
  - `/service2/` → Service 2

---

## Bonus Tasks

- Healthchecks: Each container has a health check configured to ensure the service is running and responsive.
- Test Script: Added a test.sh script file that automatically tests the system.
- Clear Logging: Added a custom log format for Nginx to provide clear and structured logs.

---

## 🛑 Stopping the System

To stop all services and clean up:

```bash
docker compose down
```
