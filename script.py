import requests
import os
import praw
import time

# GitHub Repo Info
GITHUB_API_URL = "https://api.github.com/repos/fredrikburmester/streamyfin/releases/latest"

# Reddit API Zugangsdaten
reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
    user_agent="YOUR_USER_AGENT"
)

dry_run = os.getenv("DRY_RUN", "false").lower() == "true"

# Subreddit, in dem der Bot posten soll
SUBREDDIT = "streamyfin"

# Funktion, um das neueste Release von GitHub zu holen
def get_latest_release():
    response = requests.get(GITHUB_API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        print("Fehler beim Abrufen der Daten von GitHub.")
        return None

# Funktion, um auf Reddit zu posten
def post_to_reddit(title, body):
    subreddit = reddit.subreddit(SUBREDDIT)
    subreddit.submit(title, selftext=body)
    print(f"Erfolgreich auf Reddit gepostet: {title}")

# Hauptfunktion
def main():
    latest_release_id = None

    while True:
        release = get_latest_release()

        if release:
            release_id = release["id"]
            if release_id != latest_release_id:  # Prüfen, ob es ein neues Release gibt
                title = f"Neues Release: {release['name']} ({release['tag_name']})"
                body = release['body'] or 'Keine Beschreibung verfügbar.'

                # Auf Reddit posten
                post_to_reddit(title, body)
                
                # Release-ID aktualisieren
                latest_release_id = release_id

        # Wartezeit bis zur nächsten Überprüfung (z.B. 1 Stunde)
        time.sleep(3600)

if __name__ == "__main__":
    main()
