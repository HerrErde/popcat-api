import requests


async def get(subreddit: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"
    }

    try:
        url = f"https://www.reddit.com/r/{subreddit}/about.json"
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json().get("data", {})

        display_name = data.get("display_name")
        title = data.get("title")
        icon = data.get("community_icon") or data.get("icon_img")
        banner = data.get("banner_background_image")
        active_user_count = data.get("active_user_count") or data.get("accounts_active")
        subscribers = data.get("subscribers")
        description = data.get("public_description")
        allow_images = data.get("allow_images")
        allow_videos = data.get("allow_videos")
        over18 = data.get("over18")

        subreddit_url = f"https://reddit.com/r/{display_name}"

        return {
            "name": display_name,
            "title": title,
            "active_users": f"{active_user_count:,}" if active_user_count else "N/A",
            "members": f"{subscribers:,}" if subscribers else "N/A",
            "description": description,
            "icon": icon.split("?")[0],
            "banner": banner.split("?")[0],
            "allow_videos": allow_videos,
            "allow_images": allow_images,
            "over_18": over18,
            "url": subreddit_url,
        }

    except requests.exceptions.HTTPError:
        print("Failed to retrieve data from Reddit.")
        return None
    except Exception as e:
        print(f"Error occurred during retrieval: {str(e)}")
        return None
