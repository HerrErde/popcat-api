import html
import json
import urllib.parse

import aiohttp
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
    "Accept": "application/graphql+json, application/json",
    "Content-Type": "application/json",
}


async def movie_scores(query):
    try:
        # Rotten Tomatoes
        tomatoes_score = await rottentomatoes(query)

        # Metacritic
        metacritic_score = await metacritic(query)
        return tomatoes_score, metacritic_score
    except Exception as e:
        return f"API request error: {e}"


async def metacritic(query):
    url = f"https://backend.metacritic.com/finder/metacritic/search/{query}/web"

    params = {
        "offset": 0,
        "limit": 30,
        "componentName": "search",
        "componentDisplayName": "Search",
        "componentType": "SearchResults",
        "mcoTypeId": "1,2,3,13",
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                data = await response.json()

                # Check if the response contains the expected data
                if "data" in data and "items" in data["data"]:
                    items = data["data"]["items"]

                    # Iterate through the items to find the one with matching slug
                    for item in items:
                        if "title" in item and item["title"].lower() == query.lower():
                            # Check if the item contains the critic score summary and score
                            if (
                                "criticScoreSummary" in item
                                and "score" in item["criticScoreSummary"]
                            ):
                                score = item["criticScoreSummary"]["score"]
                                return score
                            else:
                                print("Score not available for the matched item.")
                                return None

                    print("No items found with the matching slug.")
                    return None
                else:
                    print("Invalid response format or data not available.")
                    return None

    except aiohttp.ClientError as e:
        return f"API request error: {e}"
    except ValueError:
        return "Error parsing the response JSON."


async def rottentomatoes1(query):
    query = query.replace(" ", "_")
    url = f"https://www.rottentomatoes.com/m/{query}"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                content = await response.text()
                soup = BeautifulSoup(content, "html.parser")
                script_tag = soup.find("script", {"data-json": "reviewsData"})

                if script_tag:
                    json_data = json.loads(script_tag.text)
                    score_percent = json_data.get("criticsScore", {}).get(
                        "scorePercent"
                    )
                    if score_percent:
                        score = "".join(filter(str.isdigit, score_percent))
                        return score
                    else:
                        print("Score not found in the data.")
                        return None
                else:
                    print("Score not found in the data.")
                    return None
        except Exception as e:
            return f"An error occurred: {e}"


async def rottentomatoes(query):
    url = "https://79frdp12pn-dsn.algolia.net/1/indexes/*/queries"
    headers = {
        "x-algolia-agent": "Algolia for JavaScript (4.24.0); Browser (lite)",
        "x-algolia-api-key": "175588f6e5f8319b27702e4cc4013561",
        "x-algolia-application-id": "79FRDP12PN",
    }
    data = {
        "requests": [
            {
                "indexName": "content_rt",
                "params": f"query={query}",
            }
        ]
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                response.raise_for_status()
                results = await response.json()

                results = results.get("results", [])[0].get("hits", [])

                for item in results:
                    title = item.get("title", "").lower().strip()

                    if title == query.lower().strip():
                        critics_score = item.get("rottenTomatoes", {}).get(
                            "criticsScore"
                        )
                        if critics_score is not None:
                            return critics_score
                        else:
                            return "Critics score not available for this title."

                return "No matching title found."
    except aiohttp.ClientError as e:
        return f"API request error: {e}"
    except ValueError:
        return "Error parsing the response JSON."


async def search(query):
    encoded_query = urllib.parse.quote(query)

    url = f"https://v3.sg.media-imdb.com/suggestion/x/{encoded_query}.json"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()

                data = await response.json()

                # Get the first item in the "d" list
                first_result = data["d"][0]
                result_id = first_result["id"]  # Extract the "id" field
                return result_id

    except aiohttp.ClientError as e:
        print(f"Request failed: {e}")
        return None
    except ValueError:
        print("Failed to parse JSON response")
        return None


async def imdbplot(query):
    base_url = "https://caching.graphql.imdb.com/"
    params = {
        "operationName": "TMD_Storyline",
        "variables": f'{{"locale":"en-US","titleId":"{query}"}}',
        "extensions": '{"persistedQuery":{"sha256Hash":"78f137c28457417c10cf92a79976e54a65f8707bfc4fd1ad035da881ee5eaac6","version":1}}',
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(base_url, headers=headers, params=params) as response:
            response.raise_for_status()
            data = await response.json()

            try:
                plot_text = data["data"]["title"]["summaries"]["edges"][0]["node"][
                    "plotText"
                ]["plaidHtml"]
                decoded_plot_text = html.unescape(plot_text)
                return decoded_plot_text
            except (KeyError, IndexError) as e:
                print("Error extracting plot text:", e)
                return "Plot text not available."


# TODO merge boxoffice and awards?
async def awards(query):
    url = f"https://www.imdb.com/title/{query}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                content = await response.text()
                soup = BeautifulSoup(content, "html.parser")

                # Find the span that contains wins and nominations
                a_element = soup.select_one(
                    'a[aria-label="See more awards and nominations"]'
                )
                span_element = soup.select_one(
                    "span.ipc-metadata-list-item__list-content-item"
                )

                if a_element:
                    # Extract the text
                    text = a_element.get_text(strip=True)
                    oscars = "".join(filter(str.isdigit, text))

                if span_element:
                    # Extract the text
                    text = span_element.get_text(strip=True)
                    wins, nominations = text.split(" & ")

                    # Clean up the text
                    wins = wins.split()[0]  # Get the number of wins
                    # Get the number of nominations
                    nominations = nominations.split()[0]

                    # Print the results
                    return oscars, wins, nominations
                else:
                    print("Could not find the span containing wins and nominations.")
                    return None, None, None

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None, None, None


async def imdbboxoffice(query):
    url = f"https://www.imdb.com/title/{query}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                content = await response.text()
                soup = BeautifulSoup(content, "html.parser")

                span_element = soup.select_one(
                    "li[data-testid='title-boxoffice-grossdomestic'] span.ipc-metadata-list-item__list-content-item"
                )

                if span_element:
                    text = span_element.text.strip()
                    boxoffice = f"${int(''.join(filter(str.isdigit, text))):,}"
                    return boxoffice
                else:
                    print("Span element not found.")

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


async def imdb_web(imdbid):
    url = f"https://www.imdb.com/title/{imdbid}/externalsites"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                content = await response.text()
                soup = BeautifulSoup(content, "html.parser")

                # Find <li> that contains an <a> with exact text "Official site"
                for li in soup.find_all("li"):
                    a_tag = li.find("a", string="Official site")
                    if a_tag and a_tag.has_attr("href"):
                        return a_tag["href"]

                print("Official site link not found.")
                return None

    except aiohttp.ClientError as e:
        print(f"Request failed: {e}")
        return None


async def imdb(query_id):
    # Define the URL and the query
    url = "https://graph.imdbapi.dev/v1"
    query_template = (
        """
    {
    title(id: "%s") {
        type
        primary_title
        runtime_minutes
        start_year
        end_year
        certificates {
        rating
        }
        rating {
        aggregate_rating
        votes_count
        }
        genres
        posters {
        url
        }
        certificates {
        rating
        }
        spoken_languages {
        name
        }
        origin_countries {
        name
        }
        directors: credits(first: 5, categories: ["director"]) {
        name {
        display_name
        }
        }
        writers: credits(first: 5, categories: ["writer"]) {
        name {
        display_name
        }
        }
        casts: credits(first: 5, categories: ["actor", "actress"]) {
        name {
        display_name
        }
        }
    }
}
    """
        % query_id
    )

    # Create the payload
    payload = {"query": query_template}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                response.raise_for_status()
                data = await response.json()
                return data
    except aiohttp.ClientError as e:
        print(f"Request failed: {e}")
        return None
    except ValueError as e:
        print(f"Failed to parse JSON response: {e}")
        return None


# TODO switch some info to tmdb
# FIXME still missing some stuff
async def main(query):
    tomatoes_score, metacritic_score = await movie_scores(query)
    imdbid = await search(query)
    imdbdata = await imdb(imdbid)
    plotsummary = await imdbplot(imdbid)
    boxoffice = await imdbboxoffice(imdbid)
    website = await imdb_web(imdbid)
    oscars, wins, nominations = await awards(imdbid)
    if oscars and wins and nominations:
        awards_text = f"Nominated for {oscars} Oscars. {wins} wins & {nominations} nominations total"

    # Extracting specific keys from the data
    type_ = imdbdata["data"]["title"]["type"]
    title = imdbdata["data"]["title"]["primary_title"]
    start_year = imdbdata["data"]["title"]["start_year"]
    end_year = imdbdata["data"]["title"]["end_year"] or ""
    runtime = imdbdata["data"]["title"]["runtime_minutes"]
    rating = imdbdata["data"]["title"]["rating"]["aggregate_rating"]
    votes = imdbdata["data"]["title"]["rating"]["votes_count"]
    poster = imdbdata["data"]["title"]["posters"][0]["url"]
    rated = imdbdata["data"]["title"]["certificates"][0]["rating"]
    directors_names = [
        name["name"]["display_name"]
        for name in imdbdata["data"]["title"]["directors"][:3]
    ]
    directors = ", ".join(directors_names)

    writer_names = [
        name["name"]["display_name"]
        for name in imdbdata["data"]["title"]["writers"][:3]
    ]
    writer = ", ".join(writer_names)

    actors_names = [
        name["name"]["display_name"] for name in imdbdata["data"]["title"]["casts"][:3]
    ]
    actors = ", ".join(actors_names)

    countries_names = [
        name["name"] for name in imdbdata["data"]["title"]["origin_countries"][:3]
    ]
    countries = ", ".join(countries_names)

    languages_names = [
        name["name"] for name in imdbdata["data"]["title"]["spoken_languages"][:10]
    ]
    languages = ", ".join(languages_names)

    genres = ", ".join(imdbdata["data"]["title"]["genres"])

    if type_ == "movie":
        output_data = {
            "ratings": [
                {"source": "Internet Movie Database", "value": f"{rating}/10"},
                {
                    "source": "Rotten Tomatoes",
                    "value": f"{tomatoes_score}%",
                },
                {"source": "Metacritic", "value": f"{metacritic_score}/100"},
            ],
            "title": title,
            "year": start_year,
            "rated": rated,
            # "released": releasedate,  # 2008-05-02T05:00:00.000Z
            "runtime": f"{runtime} min",
            "genres": genres,
            "directors": directors,
            "writer": writer,
            "actors": actors,
            "plot": plotsummary,
            "languages": languages,
            "country": countries,
            "awards": awards_text,
            "poster": poster.replace(".jpg", "SX300.jpg"),
            "metascore": metacritic_score,
            "rating": rating,
            "votes": f"{votes:,}",
            "imdbid": imdbid,
            "type": type_,
            "boxoffice": f"${boxoffice}",
            "production": "N/A",
            "website": website,
            "name": title,
            "series": False if type_ == "movie" else True,
            "imdburl": f"https://www.imdb.com/title/{imdbid}",
        }
    else:
        output_data = {
            "ratings": [
                {"source": "Internet Movie Database", "value": f"{rating}/10"},
            ],
            "title": title,
            "_yearData": f"{start_year}-{end_year}",
            "rated": rated,
            # "released": releasedate,  # 2008-05-02T05:00:00.000Z
            "runtime": f"{runtime} min",
            "genres": genres,
            "directors": directors,
            "writer": writer,
            "actors": actors,
            "plot": plotsummary,
            "languages": languages,
            "country": countries,
            "awards": awards_text,
            "poster": poster.replace(".jpg", "SX300.jpg"),
            "rating": rating,
            "votes": f"{votes:,}",
            "imdbid": imdbid,
            "type": "series",
            "website": website,
            "name": title,
            "series": False if type_ == "movie" else True,
            "imdburl": f"https://www.imdb.com/title/{imdbid}",
            "_episodes": [],
            "start_year": start_year,
            "totalseasons": 3,
        }

    return output_data
