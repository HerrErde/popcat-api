import re

import requests
from bs4 import BeautifulSoup


def get_result(search_term):
    api_url = f"https://genius.com/api/search/multi?q={search_term}"

    response = requests.get(api_url)
    response.raise_for_status()

    json_response = response.json()

    # Check if sections exist and are not empty
    sections = json_response.get("response", {}).get("sections", [])
    if not sections:
        return None

    # Extract data from the first search result in the appropriate section
    for section in sections:
        if section.get("type") == "song":
            hits = section.get("hits", [])
            if hits:
                first_result = hits[0].get("result", {})

                title = first_result.get("title")
                image = first_result.get("song_art_image_thumbnail_url")
                artist = first_result.get("artist_names")
                lyrics_url = first_result.get("url")

                # Fetch lyrics from the specific song URL
                lyrics_text = lyrics(lyrics_url)

                # Format the extracted data into a dictionary
                formatted_data = {
                    "title": title,
                    "image": image,
                    "artist": artist,
                    "lyrics": lyrics_text,
                }

                return formatted_data

    return None


def lyrics(lyrics_url):
    response = requests.get(lyrics_url)

    try:
        response.raise_for_status()
        # Parse the page content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all divs with class starting with 'Lyrics__Container'
        lyrics_div = soup.find_all("div", attrs={"data-lyrics-container": "true"})

        # Check if any divs were found
        if lyrics_div:
            # Concatenate the text from all found divs
            lyrics_text = "\n".join(
                [div.get_text(separator="\n") for div in lyrics_divs]
            )
            lyrics_text = clean(lyrics_text)
            return lyrics_text
        else:
            print("Lyrics div not found")
    except requests.exceptions.HTTPError:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None


def clean(text):
    # Remve newlines inside parentheses
    text = re.sub(r"\(\n", "(", text)
    text = re.sub(r"\n\)", ")", text)
    # text = re.sub(r"\)\n", ") ", text) # Remove newlines after closing parentheses
    # Remove newlines before opening parentheses
    text = re.sub(r"\n\(", " (", text)
    # Remove sections specifically from [Intro] to the next tag, including newlines
    text = re.sub(r"\[Intro\][^\[]*\n?\[.*?\]", "", text)
    # Remove any remaining tags, including newlines
    text = re.sub(r"\[.*?\]\n?", "", text)
    # Replace newlines with spaces
    # text = re.sub(r"\n", " ", text)
    # Remove any text within parentheses, including any preceding spaces
    text = re.sub(r"\s*\(.*?\)", "", text)

    # Remove unwanted characters or additional cleaning steps
    return text.strip()


def search(search_term):
    # Get and format data from the first search result
    try:
        result_data = get_result(search_term)

        if result_data:
            return result_data
        else:
            print("No search results found.")

    except Exception as e:
        print(f"Error occurred during search: {str(e)}")
