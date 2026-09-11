from pyngrok import ngrok, conf
import time

conf.get_default().auth_token = "3Ix94VlIJJ0ayWfqlqQkGSwriKL_5VHKuHhtmT8ezPShnLU88"

public_url = ngrok.connect(8000)
print(f"\nYOUR PUBLIC URL: {public_url}\n")
print("Keep this window open. Press CTRL+C to stop.")

while True:
    time.sleep(1)