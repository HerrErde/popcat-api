import json

import requests


def search(query):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0",
            "Accept": "application/json",
            "Referer": "https://steamdb.info/",
            "x-algolia-application-id": "94HE6YATEI",
            "x-algolia-api-key": "MTFlMWQ0NGE4ODI5YmNiZGQ3ZGFmYWE1NmMyMmU3N2I1YTQ4MmI1Zjg3OGU4YWU4ZTU0ODdkMzhiYmUxNGIwOXZhbGlkVW50aWw9MTczOTI4NDYzMCZ1c2VyVG9rZW49MGM1ZjcwOTYwNTU2YWViMWYwYWMzN2Y5NmIwOWQ1NTI=",
            "Content-Type": "text/plain;charset=UTF-8",
            "Origin": "https://steamdb.info",
        }

        params = {
            "x-algolia-agent": "SteamDB Autocompletion",
        }

        data = json.dumps(
            {
                "hitsPerPage": 10,
                "attributesToSnippet": None,
                "attributesToHighlight": "name",
                "attributesToRetrieve": "objectID,lastUpdated,small_capsule",
                "query": query,
            }
        )
        print(data)

        response = requests.post(
            "https://94he6yatei-dsn.algolia.net/1/indexes/steamdb/query",
            params=params,
            headers=headers,
            data=data,
        )

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: {response.status_code}")
            return None

    except Exception as e:
        print(f"Error getting steam data: {str(e)}")
        return None


def steam_data(query):
    search_result = search(query)

    if not search_result:
        print("No search results.")
        return None

    try:
        app_ids = search_result["hits"]
        if not app_ids:
            print("No games found for the given query.")
            return None

        app_id = app_ids[0]["objectID"]
        print(app_id)

        # Get the details of the game using the obtained app ID
        data = requests.get(
            f"https://store.steampowered.com/api/appdetails?appids={app_id}"
        )
        game_data = data.json().get(str(app_id), {}).get("data", {})
        if not game_data:
            print("No game data found.")
            return None

        game_type = game_data.get("type", "N/A")
        game_name = game_data.get("name", "N/A")
        thumbnail = game_data.get("capsule_image", "N/A")
        controller_support = game_data.get("controller_support", "N/A")
        short_description = game_data.get("short_description", "N/A")
        website = game_data.get("website", "N/A")
        banner = game_data.get("header_image", "N/A")
        price = game_data.get("price_overview", {}).get("final_formatted", "N/A")
        developers = game_data.get("developers", [])
        publishers = game_data.get("publishers", [])

        return {
            "type": game_type,
            "name": game_name,
            "thumbnail": thumbnail,
            "controller_support": controller_support,
            "description": short_description,
            "website": website,
            "banner": banner,
            "developers": developers,
            "publishers": publishers,
            "price": price,
        }

    except Exception as e:
        print(f"Error processing game data: {str(e)}")
        return None


"""

from config import config
from steam_web_api import Steam

steam = Steam(config.steam_web_key)


def steam_data(query):
    try:
        search_result = steam.apps.search_games(query)

        if not search_result.get("apps"):
            print("No games found for the given query.")
            return None

        else:
            # Get the app ID of the first result
            app_ids = search_result["apps"][0]["id"]

            # If multiple app IDs are returned, use the first one
            if isinstance(app_ids, list):
                app_id = app_ids[0]

        # Get the details of the game using the obtained app ID
        data = steam.apps.get_app_details(app_id)
        game_data = data.get(str(app_id), {}).get("data", {})

        game_type = game_data["type"]
        game_name = game_data["name"]
        is_free = game_data["is_free"]
        required_age = game_data["required_age"]
        short_description = game_data["short_description"]
        supported_languages = game_data["supported_languages"]
        header_image = game_data["header_image"]

        return {
            "type": game_type,
            "name": game_name,
            "is_free": is_free,
            "required_age": required_age,
            "short_description": short_description,
            "supported_languages": supported_languages,
            "header_image": header_image,
        }

    except Exception as e:
        print(f"Error getting steam data: {str(e)}")
"""
