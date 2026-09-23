import argparse
import logging
import os
import requests

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("NexusCore")

# Pulls the webhook URL securely from Railway's environment variables
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


def send_discord_alert(asset_id):
  if not WEBHOOK_URL:
    logger.warning("DISCORD_WEBHOOK_URL environment variable is not set.")
    return

  payload = {
      "embeds": [{
          "title": "Asset Extraction Complete",
          "description": "Network capture pipeline finished successfully.",
          "color": 0x6366F1,
          "fields": [
              {"name": "Asset ID", "value": str(asset_id), "inline": True},
              {"name": "Status", "value": "Copied & Dispatched", "inline": True},
          ],
          "footer": {"text": "NexusStudio Automation Core"},
      }]
  }

  try:
    response = requests.post(WEBHOOK_URL, json=payload, timeout=5)
    if response.status_code == 204:
      logger.info("Discord webhook alert dispatched.")
    else:
      logger.warning(f"Webhook responded with status code: {response.status_code}")
  except Exception as e:
    logger.error(f"Failed to send webhook: {e}")


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--id", required=True, help="Target Asset ID")
  args = parser.parse_args()

  logger.info(f"Processing asset target: {args.id}")
  # Insert your asset processing / request logic here if needed

  # Trigger Discord notification after completion
  send_discord_alert(args.id)
