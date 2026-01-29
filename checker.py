#!/usr/bin/env python3
"""
Avacta News Alert Checker

Monitors the Avacta RSS feed for new articles and sends Telegram notifications.
"""

import argparse
import os
import sys
import feedparser
import requests

RSS_FEED_URL = "https://avacta.com/feed/"
LAST_SEEN_FILE = "last_seen.txt"


def get_last_seen_url() -> str:
    """Read the last seen article URL from file."""
    if os.path.exists(LAST_SEEN_FILE):
        with open(LAST_SEEN_FILE, "r") as f:
            return f.read().strip()
    return ""


def save_last_seen_url(url: str) -> None:
    """Save the last seen article URL to file."""
    with open(LAST_SEEN_FILE, "w") as f:
        f.write(url)


def send_telegram_message(bot_token: str, chat_id: str, message: str) -> bool:
    """Send a message via Telegram Bot API."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }

    response = requests.post(url, json=payload, timeout=30)

    if response.status_code == 200:
        print("Telegram message sent successfully")
        return True
    else:
        print(f"Failed to send Telegram message: {response.status_code}")
        print(response.text)
        return False


def send_test_message(bot_token: str, chat_id: str) -> None:
    """Send a test message to verify Telegram configuration."""
    message = "🔔 <b>Avacta Alert Test</b>\n\nTelegram integration is working correctly!"
    if send_telegram_message(bot_token, chat_id, message):
        print("Test successful - Telegram is configured correctly")
        sys.exit(0)
    else:
        print("Test failed - check your TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID")
        sys.exit(1)


def check_for_new_articles() -> None:
    """Check RSS feed for new articles and send notifications."""
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        print("Error: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set")
        sys.exit(1)

    print(f"Fetching RSS feed: {RSS_FEED_URL}")
    feed = feedparser.parse(RSS_FEED_URL)

    if feed.bozo:
        print(f"Warning: Feed parsing issue: {feed.bozo_exception}")

    if not feed.entries:
        print("No entries found in feed")
        return

    latest_entry = feed.entries[0]
    latest_url = latest_entry.link
    latest_title = latest_entry.title

    print(f"Latest article: {latest_title}")
    print(f"URL: {latest_url}")

    last_seen_url = get_last_seen_url()

    if not last_seen_url:
        print("First run - saving current article as baseline")
        save_last_seen_url(latest_url)
        return

    if latest_url == last_seen_url:
        print("No new articles")
        return

    # Find all new articles (in case multiple were published)
    new_articles = []
    for entry in feed.entries:
        if entry.link == last_seen_url:
            break
        new_articles.append(entry)

    print(f"Found {len(new_articles)} new article(s)")

    # Send notifications for new articles (oldest first)
    for entry in reversed(new_articles):
        message = (
            f"<b>New Avacta News</b>\n\n"
            f"<b>{entry.title}</b>\n\n"
            f"{entry.link}"
        )
        send_telegram_message(bot_token, chat_id, message)

    # Update last seen
    save_last_seen_url(latest_url)
    print("Updated last seen article")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="Send test message")
    args = parser.parse_args()

    if args.test:
        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        if not bot_token or not chat_id:
            print("Error: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set")
            sys.exit(1)
        send_test_message(bot_token, chat_id)
    else:
        check_for_new_articles()
