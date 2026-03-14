# Raspberry Pi File Upload Server

A simple and secure file upload server for Raspberry Pi that allows you to save files locally via a web interface or API.

## Features

- 🌐 Web-based file upload interface
- 🔒 Secure filename handling
- 📁 Automatic upload directory creation
- 📊 File listing API endpoint
- ✅ File type validation
- 📏 File size limits
- ⏰ Timestamped filenames to prevent conflicts
- 💚 Health check endpoint

## Requirements

- Python 3.7 or higher
- Raspberry Pi (or any Linux system)

## Installation

1. Clone this repository or navigate to the `file_server` directory:

```bash
cd file_server
```

2. Install the required dependencies:

```bash
pip3 install -r requirements.txt
```

## Usage

### Starting the Server

Run the server with:

```bash
python3 server.py
```

The server will start on `http://0.0.0.0:5000` and will be accessible from any device on your network.

You'll see output like:
```
Starting file upload server...
Upload folder: /home/pi/file_server/uploads
Max file size: 16.0MB
Allowed extensions: txt, pdf, png, jpg, jpeg, gif, doc, docx, zip
 * Running on http://0.0.0.0:5000
```

### Accessing the Web Interface

1. Find your Raspberry Pi's IP address:
```bash
hostname -I
```

2. Open a web browser and navigate to:
```
http://<raspberry-pi-ip>:5000
```

3. Use the web form to select and upload files

## VS Code Debugging (F5)

If you develop locally in VS Code, this repository includes a debug configuration in
`.vscode/launch.json`.

1. Open the repository folder in VS Code.
2. Select your Python interpreter (`file_server/.venv/bin/python` if you use a venv).
3. Go to **Run and Debug** and start **Python: File Server** (or press `F5`).

The server starts in the integrated terminal with working directory `file_server/`.

Quick checks in a second terminal:

```bash
curl http://127.0.0.1:5000/health
curl http://127.0.0.1:5000/files
```


### Running with Docker

```bash
docker build -t raspberry-file-server .
docker run --rm -p 5000:5000 -v "$(pwd)/uploads:/app/uploads" raspberry-file-server
```

### API Endpoints

#### Upload a File (POST)
```bash
curl -X POST -F "file=@/path/to/your/file.txt" http://<raspberry-pi-ip>:5000/upload
```

### Upload from your laptop to your Raspberry Pi ("private cloud" in home network)

1. **Find your Raspberry Pi IP address** on the Pi:

```bash
hostname -I
```

2. **Start the server on the Pi** (host `0.0.0.0` is already configured):

```bash
cd file_server
python3 server.py
```

3. **From your laptop**, upload a file via curl:

```bash
curl -X POST -F "file=@/path/to/local/file.pdf" http://<RASPBERRY_PI_IP>:5000/upload
```

4. List uploaded files from your laptop:

```bash
curl http://<RASPBERRY_PI_IP>:5000/files
```

5. Optional: use the included Python client script from your laptop:

```bash
python3 client_example.py upload http://<RASPBERRY_PI_IP>:5000 /path/to/local/file.pdf
python3 client_example.py list http://<RASPBERRY_PI_IP>:5000
python3 client_example.py health http://<RASPBERRY_PI_IP>:5000
```

If your laptop cannot connect:
- Ensure both devices are in the same network.
- Ensure port `5000` is not blocked by firewall (`sudo ufw allow 5000` on the Pi).
- Test reachability first: `ping <RASPBERRY_PI_IP>`.

Response:
```json
{
  "success": true,
  "message": "File uploaded successfully",
  "filename": "file_20260105_143022.txt",
  "size": 1024,
  "timestamp": "20260105_143022"
}
```

#### List Uploaded Files (GET)
```bash
curl http://<raspberry-pi-ip>:5000/files
```

Response:
```json
{
  "files": [
    {
      "name": "file_20260105_143022.txt",
      "size": 1024,
      "modified": "2026-01-05 14:30:22"
    }
  ]
}
```

#### Health Check (GET)
```bash
curl http://<raspberry-pi-ip>:5000/health
```

Response:
```json
{
  "status": "healthy",
  "upload_folder": "/home/pi/file_server/uploads",
  "timestamp": "2026-01-05T14:30:22.123456"
}
```

## Configuration

You can modify the following settings in `server.py`:

- `UPLOAD_FOLDER`: Directory where files are saved (default: `uploads`)
- `MAX_FILE_SIZE`: Maximum file size in bytes (default: 16MB)
- `ALLOWED_EXTENSIONS`: Set of allowed file extensions
- `host`: Server host (default: `0.0.0.0` for network access)
- `port`: Server port (default: `5000`)

## Security Considerations

- The server validates file extensions against a whitelist
- Filenames are sanitized using `secure_filename()` to prevent path traversal
- File size is limited to prevent disk space exhaustion
- Timestamps are added to filenames to prevent conflicts
- Consider running the server behind a reverse proxy (nginx) with SSL for production use
- Add authentication if exposing the server to the internet

## Running as a Service (Optional)

To run the server automatically on boot, create a systemd service:

1. Create a service file:
```bash
sudo nano /etc/systemd/system/file-upload-server.service
```

2. Add the following content:
```ini
[Unit]
Description=Raspberry Pi File Upload Server
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/file_server
ExecStart=/usr/bin/python3 /home/pi/file_server/server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

3. Enable and start the service:
```bash
sudo systemctl enable file-upload-server
sudo systemctl start file-upload-server
```

4. Check the status:
```bash
sudo systemctl status file-upload-server
```

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, change the port in `server.py`:
```python
app.run(host='0.0.0.0', port=8080, debug=False)
```

### Permission Denied
Ensure the user running the server has write permissions to the upload directory:
```bash
chmod 755 uploads
```

### Cannot Access from Network
Check your firewall settings:
```bash
sudo ufw allow 5000
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
