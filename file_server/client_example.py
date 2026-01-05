#!/usr/bin/env python3
"""
Example client for uploading files to the Raspberry Pi file server
"""

import requests
import sys
import os

def upload_file(server_url, file_path):
    """
    Upload a file to the server
    
    Args:
        server_url: URL of the file server (e.g., http://192.168.1.100:5000)
        file_path: Path to the file to upload
    """
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist")
        return False
    
    print(f"Uploading {file_path} to {server_url}...")
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{server_url}/upload", files=files, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! File uploaded as: {data['filename']}")
            print(f"   Size: {data['size']} bytes")
            print(f"   Timestamp: {data['timestamp']}")
            return True
        else:
            error = response.json().get('error', 'Unknown error')
            print(f"❌ Upload failed: {error}")
            return False
    
    except requests.exceptions.ConnectionError:
        print(f"❌ Error: Could not connect to {server_url}")
        print("   Make sure the server is running and the URL is correct")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def list_files(server_url):
    """
    List all files on the server
    
    Args:
        server_url: URL of the file server
    """
    print(f"Fetching file list from {server_url}...")
    
    try:
        response = requests.get(f"{server_url}/files", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            files = data.get('files', [])
            
            if not files:
                print("No files found on the server")
            else:
                print(f"\n📁 Found {len(files)} file(s):\n")
                for file in files:
                    print(f"  • {file['name']}")
                    print(f"    Size: {file['size']} bytes")
                    print(f"    Modified: {file['modified']}")
                    print()
            return True
        else:
            print("❌ Failed to list files")
            return False
    
    except requests.exceptions.ConnectionError:
        print(f"❌ Error: Could not connect to {server_url}")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def check_health(server_url):
    """
    Check if the server is healthy
    
    Args:
        server_url: URL of the file server
    """
    try:
        response = requests.get(f"{server_url}/health", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Server is {data['status']}")
            print(f"   Upload folder: {data['upload_folder']}")
            return True
        else:
            print("❌ Server is not healthy")
            return False
    
    except requests.exceptions.ConnectionError:
        print(f"❌ Error: Could not connect to {server_url}")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Upload file:  python3 client_example.py upload <server_url> <file_path>")
        print("  List files:   python3 client_example.py list <server_url>")
        print("  Health check: python3 client_example.py health <server_url>")
        print("\nExample:")
        print("  python3 client_example.py upload http://192.168.1.100:5000 document.pdf")
        print("  python3 client_example.py list http://192.168.1.100:5000")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "upload":
        if len(sys.argv) != 4:
            print("Error: Upload requires server URL and file path")
            print("Usage: python3 client_example.py upload <server_url> <file_path>")
            sys.exit(1)
        
        server_url = sys.argv[2]
        file_path = sys.argv[3]
        upload_file(server_url, file_path)
    
    elif command == "list":
        if len(sys.argv) != 3:
            print("Error: List requires server URL")
            print("Usage: python3 client_example.py list <server_url>")
            sys.exit(1)
        
        server_url = sys.argv[2]
        list_files(server_url)
    
    elif command == "health":
        if len(sys.argv) != 3:
            print("Error: Health check requires server URL")
            print("Usage: python3 client_example.py health <server_url>")
            sys.exit(1)
        
        server_url = sys.argv[2]
        check_health(server_url)
    
    else:
        print(f"Error: Unknown command '{command}'")
        print("Valid commands: upload, list, health")
        sys.exit(1)

if __name__ == '__main__':
    main()
