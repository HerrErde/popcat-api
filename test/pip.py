import json
import os
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

CACHE_FILE = "pypi_index_cache.json"
CACHE_EXPIRY_DAYS = 1


def fetch_pypi_index():
    index_url = "https://pypi.org/simple/"
    # pip_stats = f"https://pypistats.org/api/packages/{query}/overall"
    response = requests.get(index_url)

    try:
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        package_links = [a.text for a in soup.find_all("a")]
        return package_links
    except requests.exceptions.HTTPError:

        print(f"Failed to retrieve index: {response.status_code}")
        return []


def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            cache_data = json.load(f)
            cache_date = datetime.strptime(cache_data["date"], "%Y-%m-%d")
            if datetime.now() - cache_date < timedelta(days=CACHE_EXPIRY_DAYS):
                return cache_data["packages"]
    return None


def save_cache(packages):
    cache_data = {"date": datetime.now().strftime("%Y-%m-%d"), "packages": packages}
    with open(CACHE_FILE, "w") as f:
        json.dump(cache_data, f)


def package_exists(package_name):
    packages = load_cache()
    if packages is None:
        packages = fetch_pypi_index()
        save_cache(packages)
    return package_name in packages


def search(query):
    if not package_exists(query):
        return f"Package '{query}' not found in the PyPI index."

    # Define the URL with the query parameter
    pypi_url = f"https://pypi.org/pypi/{query}/json"

    # Send a GET request to the PyPI registry
    response = requests.get(pypi_url)

    try:
        response.raise_for_status()
        # Parse the response JSON
        response = response.json()

        # Extract the "releases" dictionary from the response
        releases = response.get("releases", {})

        if releases:
            name = response.get("info", {}).get("name", None)
            response.get("info", {}).get("description", None)
            version = response.get("info", {}).get("version", None)
            summary = response.get("info", {}).get("summary", None)
            keywords = response.get("info", {}).get("keywords", [])
            author = response.get("info", {}).get("author", None)
            author_email = response.get("info", {}).get("maintainer_email", "N/A")
            repository = (
                response.get("info", {})
                .get("project_urls", {})
                .get("Repository", "None")
            )

            keywords_str = ", ".join(keywords) if keywords else None
        else:
            return None
    except requests.exceptions.HTTPError:
        print(f"Failed to retrieve data: {response.status_code}")
        return None

    return {
        "name": name,
        "version": version,
        "summary": summary,
        "keywords": keywords_str,
        "author": author,
        "author_email": author_email,
        "repository": repository,
        "downloads_this_year": "34,352",  # Placeholder, as downloads data is not directly fetched in this script
    }


# Example usage:
result = search("numpy")
print(json.dumps(result, indent=2))
