import random

import requests

subreddit_list = [
    "rarepuppers",
    "wholesomememes",
    "comedyheaven",
    "dankmemes",
    "memes",
    "funny",
    "rarepuppers",
    "me_irl",
    "Animemes",
    "MemesDaily",
]


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
                author = random_post.get("author_fullname")
                upvotes = random_post.get("ups")
                nsfw = random_post.get("over_18")
                spoiler = random_post.get("spoiler")
                id_ = random_post.get("id")
                random_post.get("url_overridden_by_dest")
                url = random_post.get("url_overridden_by_dest")
                imageHigh = (
                    random_post.get("preview", {})
                    .get("images", [{}])[0]
                    .get("resolutions", [{}])[-1]
                    .get("url", None)
                )

                if title:
                    return {
                        "title": title,
                        "author": author,
                        "link": f"https://redd.it/{id_}",
                        "subreddit": subreddit,
                        "content": {
                            "image": url,
                            "imageHigh": imageHigh,
                        },
                        "misc": {
                            "upvotes": upvotes,
                            "nsfw": nsfw,
                            "spoiler": spoiler,
                        },
                    }
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
