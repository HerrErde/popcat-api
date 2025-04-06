import random
import time

import requests

from config import config

# Cache for tokens close to reset
cooldown_tokens = {}  # Format: {"token": reset_time_ms}
valid_tokens = {}  # Format: {"token": remaining_requests}
data_cache = {}  # Format: {"username": user_data}
data_timestamp = {}  # Format: {"username": last_fetch_time_ms}


def get_gh_token():
    url = "https://api.github.com/rate_limit"
    global cooldown_tokens, valid_tokens

    try:
        raw_tokens = config.gh_token
        if isinstance(raw_tokens, str):
            token_list = [t.strip() for t in raw_tokens.split(",") if t.strip()]
        else:
            token_list = raw_tokens

        random.shuffle(token_list)
        valid_tokens.clear()

        for token in token_list:
            if token in cooldown_tokens:
                if time.time() * 1000 < cooldown_tokens[token]:
                    continue
                else:
                    del cooldown_tokens[token]

            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

            core = data.get("resources", {}).get("core", {})
            remaining = core.get("remaining", 0)
            reset = core.get("reset", 0)

            reset_time_ms = reset * 1000

            if remaining < 5:
                cooldown_tokens[token] = reset_time_ms
                continue

            valid_tokens[token] = remaining
            return token

        return None

    except Exception as e:
        print(f"Error getting GitHub Token: {e}")
        return None


def data(username):
    current_time_ms = time.time() * 1000
    five_minutes_ms = 5 * 60 * 1000

    if username in data_cache and username in data_timestamp:
        if current_time_ms - data_timestamp[username] < five_minutes_ms:
            return data_cache[username]

    url = f"https://api.github.com/users/{username}"
    try:
        token = get_gh_token()
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        user_data = {
            "url": data.get("html_url", "Not Available"),
            "avatar": data.get("avatar_url", "Not Available"),
            "account_type": data.get("type", "Not Available"),
            "name": data.get("login", "Not Available"),
            "company": data.get("company", "None"),
            "blog": data.get("blog", "None"),
            "location": data.get("location", "Not Set"),
            "email": data.get("email", "None"),
            "bio": data.get("bio", "No Bio"),
            "twitter": data.get("twitter_username", "Not Set"),
            "public_repos": data.get("public_repos", 0),
            "public_gists": data.get("public_gists", 0),
            "followers": data.get("followers", 0),
            "following": data.get("following", 0),
            "created_at": data.get("created_at", "Not Available"),
            "updated_at": data.get("updated_at", "Not Available"),
        }

        data_cache[username] = user_data
        data_timestamp[username] = current_time_ms
        return user_data

    except requests.exceptions.HTTPError:
        print("User not found")
        return None
    except Exception as e:
        print(f"An error occurred while fetching GitHub User Data: {e}")
        return None
