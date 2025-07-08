import html
import json
import re

import requests
from bs4 import BeautifulSoup


def get_result(search_term):
    api_url = f"https://genius.com/api/search/multi?q={search_term}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
    }
    response = requests.get(api_url, headers=headers)

    json_response = response.json()
    sections = json_response.get("response", {}).get("sections", [])
    if not sections:
        return None

    for section in sections:
        if section.get("type") == "song":
            hits = section.get("hits", [])
            if hits:
                first_result = hits[0].get("result", {})

                title = first_result.get("title")
                id = first_result.get("id")
                image = first_result.get("song_art_image_thumbnail_url")
                artist = first_result.get("artist_names")
                lyrics_url = first_result.get("url")

                lyrics_text = lyrics(id)

                return {
                    "title": title,
                    "image": image,
                    "artist": artist,
                    "lyrics": lyrics_text.strip().replace("\n", "\n"),
                }

    return None


def js_unescape(js_str):
    js_str = js_str.replace(r"\'", "'").replace(r"\"", '"').replace(r"\/", "/")
    return bytes(js_str, "utf-8").decode("unicode_escape")


def extract_lyrics(content):
    match = re.search(r"JSON\.parse\('(.+?)'\)", content, re.DOTALL)
    if not match:
        raise ValueError("Lyrics JSON not found")

    escaped_js = match.group(1)
    unescaped = js_unescape(escaped_js)
    html_content = json.loads(unescaped)

    end_pos = html_content.find("</p>")
    if end_pos != -1:
        html_content = html_content[: end_pos + 4]

    # Remove 'Powered by Genius'
    html_content = re.sub(r"Powered by Genius\s*", "", html_content)

    # Unescape HTML entities
    html_content = html.unescape(html_content)

    # Remove all HTML tags
    text = re.sub(r"<[^>]+>", "", html_content)

    return text.strip()


def lyrics(song_id):
    url = f"https://genius.com/songs/{song_id}/embed.js"
    response = requests.get(url)
    try:
        file_content = response.text
        response.raise_for_status()

        match = re.search(r"JSON\.parse\('(.+)'\)", response.text)
        if not match:
            raise ValueError("Lyrics JSON not found")

        lyrics = extract_lyrics(file_content)

        return lyrics
    except requests.exceptions.HTTPError:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None


def search(search_term):
    try:
        return get_result(search_term) or print("No search results found.")
    except Exception as e:
        print(f"Error occurred during search: {str(e)}")
