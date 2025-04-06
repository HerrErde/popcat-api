import random

import requests

subreddit_list = ["carporn"]

filter = "top"  # filter options are(new, hot/best, top, rising)
age = "all"
limit = 75

# options are(hour, day, week, month, year, all)
params = {"age": age, "limit": limit}


def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"
    }
    try:
        while True:
            subreddit = random.choice(subreddit_list)
            # url = f"https://www.reddit.com/r/{subreddit}/{filter}.json"
            url = f"https://www.reddit.com/r/{subreddit}.json"

            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            if (
                data
                and "data" in data
                and "children" in data["data"]
                and len(data["data"]["children"]) > 0
            ):

                random_post = random.choice(
                    [
                        post["data"]
                        for post in data["data"]["children"]
                        if not post["data"].get("stickied", False)
                    ]
                )

                title = random_post.get("title")
                url_post = random_post.get("url")

                if title and url_post:
                    return {"title": title, "image": url_post}
                else:
                    return None
            else:
                print("No posts found in the response.")

    except requests.exceptions.HTTPError:
        print("Failed to retrieve data from Reddit.")
        return None
    except Exception as e:
        print(f"Error occurred during retrieval: {str(e)}")
    return None
