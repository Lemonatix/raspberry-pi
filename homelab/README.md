# Raspberry Pi Homelab Stack

Diese Konfiguration bereitet deinen Raspberry Pi für drei typische Aufgaben vor:

1. **Netzwerkweiter Adblock** mit Pi-hole.
2. **Eigene Website hosten** mit Caddy (HTTPS automatisch).
3. **Optional Minecraft-Server** per Docker Profile.

## Voraussetzungen

- Raspberry Pi OS 64-bit
- Docker + Docker Compose Plugin installiert
- Statische IP für den Pi im Router (wichtig für Pi-hole)
- Portfreigaben nur falls externer Zugriff benötigt wird

## Auf SD-Karte vorbereiten (empfohlen)

Ja — du kannst die Grundlage komplett auf einer SD-Karte vorbereiten und sie danach in den Raspberry Pi stecken.

### Schritt 1: Raspberry Pi OS auf die SD-Karte schreiben

Nutze **Raspberry Pi Imager** und setze dabei direkt:

- Hostname (z. B. `rpi-homelab`)
- SSH aktivieren
- Benutzer + Passwort
- WLAN (falls kein LAN genutzt wird)
- Zeitzone + Keyboard Layout

### Schritt 2: Erststart am Raspberry Pi

Nach dem Booten per SSH verbinden und Grundsystem aktualisieren:

```bash
sudo apt update && sudo apt upgrade -y
```

Docker + Compose Plugin installieren:

```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker
docker --version
docker compose version
```

### Schritt 3: Repository auf den Pi bringen

Option A (üblich): auf dem Pi klonen

```bash
git clone <DEIN_REPO_URL>
cd raspberry-pi/homelab
```

Option B: lokal vorbereiten und Ordner auf die SD-Karte / den Pi kopieren (z. B. via SCP/USB).

### Schritt 4: Stack starten

```bash
cp .env.example .env
mkdir -p volumes/pihole/etc-pihole volumes/pihole/etc-dnsmasq.d \
         volumes/caddy/data volumes/caddy/config \
         volumes/file_server/uploads volumes/minecraft/data site
docker compose up -d --build
```

## Schnellstart

```bash
cd homelab
cp .env.example .env
mkdir -p volumes/pihole/etc-pihole volumes/pihole/etc-dnsmasq.d \
         volumes/caddy/data volumes/caddy/config \
         volumes/file_server/uploads volumes/minecraft/data site
```

Passe danach in `.env` mindestens diese Werte an:
- `PIHOLE_WEBPASSWORD`
- `LETSENCRYPT_EMAIL`
- `WEBSITE_DOMAIN`
- `FILE_SERVER_DOMAIN`

Starte Basisdienste (Adblock + Website + File Server):

```bash
docker compose up -d --build
```

Wenn du zusätzlich Minecraft starten willst:

```bash
docker compose --profile minecraft up -d
```

## In VSCode vortesten

Ja, das geht sehr gut. Zwei sinnvolle Wege:

1. **Lokal in VSCode** (wenn dein Rechner Docker hat):

```bash
cd homelab
cp .env.example .env
docker compose config
docker compose up -d --build
docker compose ps
```

2. **VSCode Remote-SSH direkt auf den Raspberry Pi** (empfohlen für realistische Tests):

- In VSCode die Erweiterung **Remote - SSH** nutzen.
- Auf den Pi verbinden und den Ordner `raspberry-pi/homelab` öffnen.
- Die gleichen `docker compose` Befehle im integrierten Terminal ausführen.

### Was du in VSCode prüfen solltest

- `docker compose config` läuft ohne Fehler.
- `docker compose ps` zeigt `pihole`, `caddy`, `file_server` als `running`.
- Logs prüfen:

```bash
docker compose logs -f pihole
docker compose logs -f caddy
docker compose logs -f file_server
```

### Wichtiger Hinweis für lokale Tests am PC

Pi-hole braucht Port `53`. Falls dieser Port auf deinem Rechner schon belegt ist (häufig), teste zunächst nur Website/File-Server oder passe Ports temporär an.

## Zugriff

- Pi-hole Admin: `http://<RASPBERRY_PI_IP>:8080/admin`
- Website: `https://<WEBSITE_DOMAIN>`
- File Server: `https://<FILE_SERVER_DOMAIN>`
- Minecraft: `<RASPBERRY_PI_IP>:25565`

## DNS im Heimnetz auf Pi-hole umstellen

Für netzwerkweites Blocking im Router als **primären DNS-Server die IP deines Raspberry Pi** eintragen.

Tipp:
- Wenn dein Router keine DNS-Änderung pro DHCP erlaubt, setze DNS in den Client-Geräten oder arbeite mit einem eigenen DHCP (Pi-hole kann das auch übernehmen).

## Sicherheitshinweise

- Nutze starke Passwörter in `.env`.
- Öffne Ports ins Internet nur bei Bedarf.
- Für externen Zugriff am besten über VPN (z. B. WireGuard/Tailscale) statt direkter Freigaben.
- Halte Images aktuell:

```bash
docker compose pull
docker compose up -d
```

## Nützliche Befehle

```bash
docker compose ps
docker compose logs -f pihole
docker compose logs -f caddy
docker compose logs -f file_server
docker compose logs -f minecraft
```
