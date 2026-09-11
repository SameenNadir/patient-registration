import urllib.request
import zipfile
import os
import time

os.makedirs(r"C:\ngrok", exist_ok=True)

url = "https://bin.ngrok.com/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip"
zip_path = r"C:\ngrok\ngrok.zip"

print("Downloading ngrok...")
urllib.request.urlretrieve(url, zip_path)

size = os.path.getsize(zip_path)
print(f"Downloaded file size: {size} bytes")

print("Waiting a moment before extracting...")
time.sleep(3)

print("Extracting...")
with zipfile.ZipFile(zip_path, "r") as z:
    z.extractall(r"C:\ngrok")

print("Done! ngrok.exe is now in C:\\ngrok")