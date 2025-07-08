from datetime import datetime
from io import BytesIO
from typing import Dict, List

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, HttpUrl, RootModel, ValidationError

from config import config
from helper import host_address
from modules.misc import *

misc_router = APIRouter()


class ImageResponse(BaseModel):
    image: bytes


class HexColorRespone(BaseModel):
    hex: str
    name: str
    # rgb: Tuple[int, int, int]
    rgb: str
    color_image: str
    brightened: str


@misc_router.get(
    "/color/{hex_color}", name="Get info on a hex color", response_model=HexColorRespone
)
async def color_endpoint(
    request: Request,
    hex_color: str = None,
):
    if not hex_color:
        raise HTTPException(status_code=400, detail="Please provide a value!")

    try:
        domain = host_address(request)
        response = color.color_info(hex_color, domain)

        return response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating color info: {str(e)}"
        )


@misc_router.get("/color/image/{hex_color}", response_model=ImageResponse)
async def color_image_endpoint(
    request: Request,
    hex_color: str = None,
):
    if not hex_color:
        raise HTTPException(status_code=400, detail="Not valid!")

    try:
        image_bytes = color.create(hex_color)
        return StreamingResponse(BytesIO(image_bytes), media_type="image/png")

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating color image: {str(e)}"
        )


@misc_router.get(
    "/randomcolor", name="OpinGet a random hex color with an image and nameion"
)
async def randomcolor_endpoint(request: Request):
    try:
        domain = host_address(request)
        response = color.randomcolor(domain)

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error random color: {str(e)}")


@misc_router.get("/screenshot", name="Screenshot a website")
async def screenshot_endpoint(request: Request, url: HttpUrl):
    if not config.screenshot:
        raise HTTPException(
            status_code=403, detail="Screenshot functionality is disabled"
        )

    try:
        image_bytes = await screenshot.take(str(url))

        if not image_bytes:
            raise HTTPException(status_code=400, detail="No image available")

        if image_bytes:
            return StreamingResponse(BytesIO(image_bytes), media_type="image/png")

    except ValidationError:
        raise HTTPException(status_code=400, detail="Please provide a valid URL.")

    except Exception as e:
        print(f"Error taking screenshot: {e}")
        raise HTTPException(status_code=500, detail="Error getting screenshot")


class EightBallResponse(BaseModel):
    answer: str


@misc_router.get(
    "/8ball", name="Ask the 8ball some questions", response_model=EightBallResponse
)
async def eightball_endpoint(request: Request, url: str = None):
    try:
        answer = eightball.answer()

        return {"answer": answer}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating 8ball answer: {str(e)}"
        )


class PeriodicTableResponse(BaseModel):
    name: str
    symbol: str
    atomic_number: int
    atomic_mass: float
    period: int
    phase: str
    discovered_by: str
    image: str
    summary: str


@misc_router.get(
    "/periodic-table",
    name="Get info on a chemical element",
    response_model=PeriodicTableResponse,
)
async def periodic_endpoint(request: Request, element: str = None):
    if not element:
        return JSONResponse(status_code=400, detail="Please provide an element query.")

    try:
        domain = host_address(request)
        response = periodic.get_element(element, domain)

        return response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating periodic element: {str(e)}"
        )


@misc_router.get("/periodic-table/image/{element}", response_model=ImageResponse)
async def periodic_image_endpoint(request: Request, element: str):
    if not element:
        return JSONResponse(status_code=400, detail="Please provide an element query.")

    try:
        image_bytes = periodic.create(element=element)
        return StreamingResponse(BytesIO(image_bytes), media_type="image/png")

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating periodic element image: {str(e)}"
        )


@misc_router.get(
    "/periodic-table/random",
    name="Get a random element from the periodic table",
    response_model=PeriodicTableResponse,
)
async def periodic_rand_endpoint(request: Request):
    try:
        domain = host_address(request)
        name, symbol, number, atomic_mass, period, phase, discovered_by, summary = (
            periodic.get_random_element()
        )

        return {
            "name": name,
            "symbol": symbol,
            "atomic_number": number,
            "atomic_mass": atomic_mass,
            "period": period,
            "phase": phase,
            "discovered_by": discovered_by,
            "image": f"{domain}/periodic-table/image/{number}",
            "summary": summary,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating random periodic element: {str(e)}",
        )


class NpmResponse(BaseModel):
    name: str
    version: str
    description: str
    keywords: str
    author: str
    author_email: str
    last_published: str
    maintainers: str
    repository: str
    downloads_this_year: str


@misc_router.get("/npm", name="Get info on an NPM package", response_model=NpmResponse)
async def npm_endpoint(request: Request, q: str):
    if not q:
        return JSONResponse(status_code=400, detail="No query was provided!")

    try:
        response = npm.search(query=q)

        return response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting npm package: {str(e)}"
        )


class ItunesResponse(BaseModel):
    url: str
    name: str
    artist: str
    album: str
    release_date: str
    price: str
    length: str
    maintainers: str
    genre: str
    thumbnail: str


@misc_router.get(
    "/itunes", name="Search on iTunes for any song", response_model=ItunesResponse
)
async def itunes_endpoint(request: Request, q: str):
    if not q:
        return JSONResponse(status_code=400, detail="No query was provided!")

    try:
        response = itunes.search(query=q)

        return response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting itunes track: {str(e)}"
        )


class LyricsResponse(BaseModel):
    title: str
    image: str
    artist: str
    lyrics: str


@misc_router.get(
    "/lyrics", name="Get lyrics and info on a song", response_model=LyricsResponse
)
async def lyrics_endpoint(request: Request, song: str):
    if not song:
        raise HTTPException(
            status_code=400,
            detail="Song not found!",
        )

    try:
        response = lyrics.search(search_term=song)
        if not response:
            raise HTTPException(status_code=404, detail="Lyrics not found")

        return response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting song lyrics: {str(e)}"
        )


class MemeContent(BaseModel):
    image: str
    imageHigh: str


class MemeMisc(BaseModel):
    upvotes: int
    nsfw: bool
    spoiler: bool


class MemeResponse(BaseModel):
    title: str
    author: str
    link: str
    subreddit: str
    content: MemeContent
    misc: MemeMisc


@misc_router.get(
    "/meme",
    name="Spam this endpoint and get tons of memes",
    response_model=MemeResponse,
)
async def meme_endpoint(request: Request):
    try:
        response = meme.main()

        return response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting meme info: {str(e)}"
        )


class GithubResponse(BaseModel):
    url: str
    avatar: str
    account_type: str
    name: str
    company: str | None
    blog: str
    location: str | None
    email: str | None
    bio: str | None
    twitter: str | None
    public_repos: int
    public_gists: int
    followers: int
    following: int
    created_at: str
    updated_at: str


@misc_router.get(
    "/github/{username}",
    name="Get info on a GitHub user",
    response_model=GithubResponse,
)
async def github_endpoint(request: Request, username: str):
    if not username:
        raise HTTPException(
            status_code=400,
            detail="Please provide 'username' path in request URL",
        )

    try:
        response = github.data(username=username)

        return response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting github user info: {str(e)}"
        )


class TranslateResponse(BaseModel):
    translated: str


@misc_router.get(
    "/translate",
    name="Translate given text to a specified language",
    response_model=TranslateResponse,
)
async def translate_endpoint(request: Request, text: str, to: str):

    if not text and to:
        raise HTTPException(
            status_code=400,
            content={
                "error": "Please provide the text and langauge you want to translate to"
            },
        )
    elif not text:
        raise HTTPException(
            status_code=400,
            detail="Please provide the text translate",
        )
    elif not to:
        raise HTTPException(
            status_code=400,
            detail="Please provide a language to translate to",
        )

    try:
        response = translate.text(text, to)

        return {"translated": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error translating text: {str(e)}")


class SteamResponse(BaseModel):
    type: str
    name: str
    thumbnail: str
    controller_support: str
    description: str
    website: str
    banner: str
    developers: List[str]
    publishers: List[str]
    price: str


@misc_router.get(
    "/steam",
    name="Get info on an application on Steam",
    response_model=SteamResponse,
)
async def steam_endpoint(request: Request, q: str):

    if not q:
        raise HTTPException(status_code=400, detail="Provide a steam game")

    try:
        response = steam.steam_data(q)

        return response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting game data: {str(e)}"
        )


class ImdbResponse(BaseModel):
    ratings: List[Dict[str, str]]
    title: str
    year: int
    rated: str
    # released: str
    runtime: str
    genres: str
    directors: str
    writer: str
    actors: str
    plot: str
    languages: str
    country: str
    awards: str
    poster: str
    metascore: int
    rating: float
    votes: str
    imdbid: str
    type: str
    boxoffice: str
    production: str
    website: str
    name: str
    series: bool
    imdburl: str


@misc_router.get(
    "/imdb",
    name="Get information on movies",
    # response_model=ImdbResponse,
)
async def imdb_endpoint(request: Request, q: str):

    if not q:
        raise HTTPException(status_code=400, detail="Provide a movie name")

    try:
        response = await imdb.main(q)

        return response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting movie data: {str(e)}"
        )


class Location(BaseModel):
    name: str
    lat: str
    long: str
    timezone: str
    alert: str
    degreetype: str
    imagerelativeurl: str


class Current(BaseModel):
    temperature: str
    skycode: str
    skytext: str
    date: str
    observationtime: str
    observationpoint: str
    feelslike: str
    humidity: str
    winddisplay: str
    day: str
    shortday: str
    windspeed: str
    imageUrl: str


class ForecastItem(BaseModel):
    low: str
    high: str
    skycodeday: str
    skytextday: str
    date: str
    day: str
    shortday: str
    precip: str


class WeatherModelItem(BaseModel):
    location: Location
    current: Current
    forecast: List[ForecastItem]


class WeatherResponse(RootModel[List[WeatherModelItem]]):
    pass


@misc_router.get(
    "/weather",
    name="Get weather info and forecast",
    response_model=WeatherResponse,
)
async def weather_endpoint(request: Request, q: str):

    if not q:
        raise HTTPException(status_code=400, detail="Provide a city ")

    try:
        response = weather.get(q)

        return response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting weather data: {str(e)}"
        )


class CarResponse(BaseModel):
    title: str
    image: str


@misc_router.get(
    "/car",
    name="Get car pictures",
    response_model=CarResponse,
)
async def car_endpoint(request: Request):
    try:
        response = car.main()

        return response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting car image: {str(e)}"
        )


class SubRedditResponse(BaseModel):
    title: str
    subscribers: int
    active_users: int
    created: datetime
    description: str
    isover18: bool
    url: str


@misc_router.get(
    "/subreddit/{subreddit}",
    name="Get tons of info on a subreddit",
    response_model=SubRedditResponse,
)
async def reddit_endpoint(subreddit: str, request: Request):
    try:
        response = await reddit.get(subreddit)

        return response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting reddi data: {str(e)}"
        )


@misc_router.get("/shorten", name="Shorten Url")
async def shorten_endpoint(request: Request, url: HttpUrl, extension: str):
    if not config.shortener:
        raise HTTPException(
            status_code=403, detail="Shortener functionality is disabled"
        )

    if not url:
        raise HTTPException(
            status_code=400,
            detail="Please provide a URL to shorten!",
        )
    elif not extension:
        raise HTTPException(
            status_code=400,
            detail=f"Please provide an extension for the shortened URL! Which is: https://{shorturl}/your-chosen-extension",
        )

    try:
        success, shortcode = await shorten.short(str(url), extension)

        if success and shortcode:
            return {"shortened": shortcode}

        raise HTTPException(status_code=400, detail="Short URL already exists")

    except HTTPException as e:
        raise e

    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@misc_router.get(
    "/countries/{country}",
    name="Countries Url",
)
async def countries_endpoint(
    request: Request,
    country: str,
):

    try:
        data = await countries.get(country)
        if data:
            return data

        raise HTTPException(status_code=500, detail="Country not found.")

    except Exception as e:
        print(f"Error getting country info: {str(e)}")
        raise HTTPException(status_code=500, detail="Error getting country info")


class CodeBinPayload(BaseModel):
    title: str
    description: str
    code: str


@misc_router.post("/createbin", name="Create a Code Bin")
async def codebin_endpoint(request: Request, payload: CodeBinPayload):
    if not config.codebin:
        raise HTTPException(status_code=403, detail="Codebin functionality is disabled")

    if not payload.title:
        raise HTTPException(
            status_code=400, detail="The property 'title' was left in the options!"
        )
    if not payload.description:
        raise HTTPException(
            status_code=400,
            detail="The property 'description' was left in the options!",
        )
    if not payload.code:
        raise HTTPException(
            status_code=400, detail="The property 'code' was left in the options!"
        )

    try:
        success, slug = await codebin.create(
            payload.title, payload.description, payload.code
        )
        if success and slug:
            return {"slug": slug}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
