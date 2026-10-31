import os
import time
from pyngrok import ngrok, conf

token = os.environ.get("NGROK_AUTHTOKEN")
if not token:
    raise SystemExit("Set the NGROK_AUTHTOKEN environment variable first.")

conf.get_default().auth_token = token

public_url = ngrok.connect(8000)
print(f"\nYOUR PUBLIC URL: {public_url}\n")
print("Keep this window open. Press CTRL+C to stop.")

while True:
    time.sleep(1)
