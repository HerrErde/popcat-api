from datetime import datetime

import aiohttp

from config import config

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
    "Accept": "application/graphql+json, application/json",
    "Content-Type": "application/json",
}


def format_released_date(released):
    try:
        return datetime.strptime(released, "%d %b %Y").strftime(
            "%Y-%m-%dT00:00:00.000Z"
        )
    except ValueError:
        return None


async def main(query):
    url = "https://omdbapi.com"
    params = {"apikey": config.omdb_apikey, "t": query, "plot": "full"}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                response.raise_for_status()
                data = await response.json()

                # Extract data
                year = data.get("Year", "0")
                type_ = data.get("Type", "").lower()
                rating = data.get("imdbRating")
                released = format_released_date(data.get("Released", ""))
                ratings = data.get("Ratings", [])
                title = data.get("Title")
                rated = data.get("Rated")
                runtime = data.get("Runtime")
                genres = data.get("Genre")
                director = data.get("Director")
                writer = data.get("Writer")
                actors = data.get("Actors")
                plot = data.get("Plot")
                language = data.get("Language")
                country = data.get("Country")
                awards = data.get("Awards")
                poster = data.get("Poster")
                metascore = data.get("Metascore")
                votes = data.get("imdbVotes")
                imdbid = data.get("imdbID")
                boxoffice = data.get("BoxOffice")
                production = data.get("Production")
                website = data.get("Website")
                totalSeasons = data.get("totalSeasons")

                # Return structured data for movies
                if type_ == "movie":
                    output_data = {
                        "ratings": [
                            {
                                "source": "Internet Movie Database",
                                "value": f"{rating}/10",
                            },
                            {
                                "source": "Rotten Tomatoes",
                                "value": ratings[1].get("Value"),
                            },
                            {
                                "source": "Metacritic",
                                "value": f"{metascore}/100",
                            },
                        ],
                        "title": title,
                        "year": int(year) if year.isdigit() else None,
                        "_yearData": year,
                        "rated": rated,
                        "released": released,
                        "runtime": runtime,
                        "genres": genres,
                        "director": director,
                        "writer": writer,
                        "actors": actors,
                        "plot": plot,
                        "languages": language,
                        "country": country,
                        "awards": awards,
                        "poster": poster,
                        "metascore": metascore,
                        "rating": (
                            float(rating)
                            if rating and rating.replace(".", "").isdigit()
                            else None
                        ),
                        "votes": votes,
                        "imdbid": imdbid,
                        "type": type_,
                        "boxoffice": boxoffice,
                        "production": production,
                        "website": website,
                        "name": title,
                        "series": False,
                        "imdburl": f"https://www.imdb.com/title/{imdbid}",
                    }
                # Return structured data for series
                else:
                    start_year = year.split("–")[0]
                    output_data = {
                        "ratings": [
                            {
                                "source": "Internet Movie Database",
                                "value": f"{rating}/10",
                            }
                        ],
                        "title": title,
                        "year": int(year) if year.isdigit() else 0,
                        "_yearData": year,
                        "rated": rated,
                        "released": released,
                        "runtime": runtime,
                        "genres": genres,
                        "director": director,
                        "writer": writer,
                        "actors": actors,
                        "plot": plot,
                        "languages": language,
                        "country": country,
                        "awards": awards,
                        "poster": poster,
                        "metascore": metascore,
                        "rating": (
                            float(rating)
                            if rating and rating.replace(".", "").isdigit()
                            else None
                        ),
                        "votes": votes,
                        "imdbid": imdbid,
                        "type": type_,
                        "name": title,
                        "series": True,
                        "imdburl": f"https://www.imdb.com/title/{imdbid}",
                        "_episodes": [],
                        "start_year": int(start_year) if start_year.isdigit() else None,
                        "totalseasons": (
                            int(totalSeasons)
                            if totalSeasons and totalSeasons.isdigit()
                            else None
                        ),
                    }

                return output_data

    except aiohttp.ClientError as e:
        print(f"Request failed: {e}")
        return None
    except ValueError:
        print("Failed to parse JSON response")
        return None
