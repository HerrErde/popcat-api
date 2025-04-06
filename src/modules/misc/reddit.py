from datetime import datetime, timezone  # Import datetime and timezone

import asyncpraw

from config import config


async def get(subreddit_name):
    reddit = None

    try:
        reddit = asyncpraw.Reddit(
            client_id=config.reddit_id,
            client_secret=config.reddit_secret,
            user_agent="popcat-api:v1.0 (by /u/herrerde)",
        )

        subreddit = await reddit.subreddit(subreddit_name)

        await subreddit.load()

        title = subreddit.title
        subscribers = subreddit.subscribers
        active_users = subreddit.accounts_active
        created = datetime.fromtimestamp(subreddit.created_utc, timezone.utc)
        description = subreddit.public_description
        over18 = subreddit.over18
        subreddit_url = f"https://www.reddit.com/r/{subreddit.display_name}/"

        return {
            "title": title,
            "subscribers": subscribers,
            "active_users": active_users,
            "created": created,
            "description": description,
            "isover18": over18,
            "url": subreddit_url,
        }

    except asyncpraw.exceptions.PRAWException as e:
        print(f"Error fetching Reddit data: {e}")
    finally:
        if reddit:
            await reddit.close()
