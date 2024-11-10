import requests
from Observer import Observer

class TeamsNotifier(Observer):
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    def update(self, message: str):
        """Send a Teams notification."""
        self.send_teams_message(message)
    
    def send_teams_message(self, message: str):
        headers = {"Content-Type": "application/json"}
        payload = {
            "text": message
        }
        response = requests.post(self.webhook_url, json=payload, headers=headers)
        if response.status_code == 200:
            logger.info(f"Teams notification sent: {message}")
        else:
            logger.error(f"Failed to send Teams notification: {response.status_code}")
