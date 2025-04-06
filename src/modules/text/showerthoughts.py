import random

import requests


def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"
    }
    subreddit = "showerthoughts"
    url = f"https://www.reddit.com/r/{subreddit}.json"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        random_post = random.choice(
            [
                post["data"]
                for post in data["data"]["children"]
                if not post["data"].get("stickied", False)
            ]
        )

        title = random_post.get("title")
        return title

    except requests.exceptions.HTTPError:
        print("Failed to retrieve shower thought from Reddit.")
        return None
    except Exception as e:
        print(f"Error occurred during retrieval: {str(e)}")
        return None
