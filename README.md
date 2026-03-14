# raspberry-pi
This repo hosts practical projects for a Raspberry Pi home setup.

## Projects

### 1. File Upload Server
A simple and secure web server for uploading and saving files locally on your Raspberry Pi.

**Features:**
- Web-based upload interface
- RESTful API for file operations
- Secure filename handling
- File type validation
- Automatic timestamping

**Location:** [`file_server/`](file_server/)

**Quick Start:**
```bash
cd file_server
pip3 install -r requirements.txt
python3 server.py
```

See the [file_server/README.md](file_server/README.md) for detailed documentation.

### 2. Homelab Stack (Pi-hole + Website + optional Minecraft)
A Docker-Compose based setup to run:
- **Pi-hole** for network-wide ad blocking
- **Caddy** for hosting your website with HTTPS
- Existing **file_server** behind reverse proxy
- Optional **Minecraft server** profile

**Location:** [`homelab/`](homelab/)

**Quick Start:**
```bash
cd homelab
cp .env.example .env
docker compose up -d --build
```

See [homelab/README.md](homelab/README.md) for full setup details.

Includes a step-by-step section to prepare everything on an SD card before first boot.
