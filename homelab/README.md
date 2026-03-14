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
