from datetime import datetime

import requests


def search(query):
    npm_search = f"https://registry.npmjs.com/-/v1/search?text={query}&size=1"

    npm_api = f"https://api.npmjs.org/downloads/point/last-year/{query}"

    response = requests.get(npm_search)
    response_api = requests.get(npm_api)

    try:
        response.raise_for_status()
        data = response_api.json()
        downloads_this_year = data.get("downloads", "None")
    except requests.exceptions.HTTPError:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

    try:
        response.raise_for_status()
        response_json = response.json()

        objects = response_json.get("objects", [])

        if objects:
            # Get the first result
            result = objects[0]["package"]

            # Extract necessary details
            name = result.get("name", None)
            version = result.get("version", None)
            description = result.get("description", None)
            keywords = result.get("keywords", [])
            publisher = result.get("publisher", {})
            publisher_username = publisher.get("username", None)
            publisher_email = publisher.get("email", None)
            date = result.get("date", None)
            repository = result.get("links", {}).get("repository", "None")

            keywords_str = ", ".join(keywords) if keywords else None

            # Convert the ISO 8601 date string to a datetime object
            date_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")

            # Convert the datetime object to a human-readable string
            human_readable_date = date_obj.strftime("%a %b %d %Y")

        else:
            return None
    except requests.exceptions.HTTPError:
        print(f"Failed to retrieve data: {response.status_code}")

    return {
        "name": name,
        "version": version,
        "description": description,
        "keywords": keywords_str,
        "author": publisher_username,
        "author_email": publisher_email,
        "last_published": human_readable_date,
        "maintainers": publisher_username,
        "repository": repository,
        "downloads_this_year": f"{downloads_this_year:,}",
    }
