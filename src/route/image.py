from io import BytesIO
from urllib.parse import unquote

import requests
from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import JSONResponse, Response, StreamingResponse
from pydantic import BaseModel

from modules.images import *

img_router = APIRouter()


class ImageResponse(BaseModel):
    image: bytes


@img_router.get(
    "/welcomecard",
    name="Customizable Discord Welcome Cards",
    response_model=ImageResponse,
)
async def welcomecard_endpoint(
    request: Request,
    background: str = None,
    text1: str = None,
    text2: str = None,
    text3: str = None,
    avatar: str = None,
    color: str = "ffffff",
):

    if not background:
        raise HTTPException(
            status_code=400,
            content={
                "error": "One of your images (background/avatar) have an unsupported image format!!!!"
            },
        )
    elif not avatar:
        raise HTTPException(status_code=400, detail="Please provide an avatar image!")
    elif not text1:
        raise HTTPException(status_code=400, detail="Text 1 was not provided.")
    elif not text2:
        raise HTTPException(status_code=400, detail="Text 2 was not provided.")
    elif not text3:
        raise HTTPException(status_code=400, detail="Text 3 was not provided.")

    try:
        image_bytes = await welcomecard.create(
            background, text1, text2, text3, avatar, color
        )

        if image_bytes:
            return StreamingResponse(BytesIO(image_bytes), media_type="image/png")
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate welcome card. Please try again.",
            )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating welcome card: {str(e)}"
        )


@img_router.get("/jail", name="Jail overlay on image", response_model=ImageResponse)
async def jail_endpoint(
    request: Request,
    image: str = None,
):

    if not image:
        raise HTTPException(status_code=400, detail="Please provide an image query.")

    try:
        image_bytes = jail.create(
            image,
        )

        if image_bytes:
            return StreamingResponse(BytesIO(image_bytes), media_type="image/png")
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate jail image. Please try again.",
            )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating jail image: {str(e)}"
        )


@img_router.get(
    "/nokia", name="Add your image on a Nokia screen", response_model=ImageResponse
)
async def nokia_endpoint(
    request: Request,
    image: str = None,
):

    if not image:
        raise HTTPException(status_code=400, detail="Please provide an image query.")

    try:
        image_bytes = nokia.create(
            image,
        )

        if image_bytes:
            return StreamingResponse(BytesIO(image_bytes), media_type="image/png")
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate nokia image. Please try again.",
            )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating nokia image: {str(e)}"
        )


@img_router.get("/sadcat", name="Make a Sad Cat Meme", response_model=ImageResponse)
async def sadcat_endpoint(
    request: Request,
    text: str = None,
):

    if not text:
        raise HTTPException(status_code=400, detail="Please provide text!")

    try:
        image_bytes = sadcat.create(
            text,
        )

        return StreamingResponse(BytesIO(image_bytes), media_type="image/png")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating sadcat image: {str(e)}"
        )


@img_router.get(
    "/unforgivable", name="Some sins are unforgivable", response_model=ImageResponse
)
async def unforgivable_endpoint(
    request: Request,
    text: str = None,
):

    if not text:
        raise HTTPException(status_code=400, detail="Please provide text!")

    try:
        image_bytes = unforgivable.create(
            text,
        )

        return StreamingResponse(BytesIO(image_bytes), media_type="image/png")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating unforgivable image: {str(e)}"
        )


@img_router.get(
    "/oogway", name="Create an 'Oogway Quote' meme", response_model=ImageResponse
)
async def oogway_endpoint(
    request: Request,
    text: str = None,
):

    if not text:
        raise HTTPException(status_code=400, detail="Please provide text!")

    try:
        image_bytes = oogway.create(
            text,
        )

        return StreamingResponse(BytesIO(image_bytes), media_type="image/png")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating oogway image: {str(e)}"
        )


@img_router.get(
    "/communism", name="Create a communist overlay", response_model=ImageResponse
)
async def communism_endpoint(
    request: Request,
    image: str = None,
):

    if not image:
        raise HTTPException(status_code=400, detail="Please provide an image query.")

    try:
        image_bytes = communism.create(
            image,
        )

        return StreamingResponse(BytesIO(image_bytes), media_type="image/png")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating communism image: {str(e)}"
        )


@img_router.get(
    "/wanted",
    name="Create a fake wanted poster with your image",
    response_model=ImageResponse,
)
async def wanted_endpoint(
    request: Request,
    image: str = None,
):

    if not image:
        raise HTTPException(status_code=400, detail="Please provide an image query.")

    try:
        image_bytes = wanted.create(
            image,
        )

        return StreamingResponse(BytesIO(image_bytes), media_type="image/png")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating wanted image: {str(e)}"
        )


@img_router.get(
    "/biden", name="Make Biden Tweet Anything", response_model=ImageResponse
)
async def biden_endpoint(
    request: Request,
    text: str = None,
):

    if not text:
        raise HTTPException(status_code=400, detail="Please provide text!")

    try:
        image_bytes = biden.create(
            text,
        )

        return StreamingResponse(BytesIO(image_bytes), media_type="image/png")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating biden image: {str(e)}"
        )


@img_router.get("/pikachu", name="Surprised pikachu!", response_model=ImageResponse)
async def pikachu_endpoint(
    request: Request,
    text: str = None,
):

    if not text:
        raise HTTPException(status_code=400, detail="Please provide text!")

    try:
        image_bytes = pikachu.create(
            text,
        )

        return StreamingResponse(BytesIO(image_bytes), media_type="image/png")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating pikachu image: {str(e)}"
        )


@img_router.get(
    "/colorify",
    name="Overlay a variety of colors on your picture",
    response_model=ImageResponse,
)
async def colorify_endpoint(
    request: Request,
    image: str = None,
    color: str = None,
):
    if not image:
        raise HTTPException(status_code=400, detail="An image was not provided!")

    if not color:
        raise HTTPException(status_code=400, detail="A color was not provided.")

    try:
        image_bytes, success = colorify.create(image, color)

        if not success:
            return JSONResponse(
                status_code=400,
                detail="Invalid image format! Must be either png or gif.",
            )

        return StreamingResponse(BytesIO(image_bytes), media_type="image/png")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating colorify image: {str(e)}"
        )


@img_router.get(
    "/drip",
    name="Pretend you're a rich person by wearing a fake expensive jacket",
    response_model=ImageResponse,
)
async def drip_endpoint(
    request: Request,
    image: str = None,
):

    if not image:
        raise HTTPException(status_code=400, detail="Please provide an image query.")

    try:
        image_bytes = drip.create(
            image,
        )

        return StreamingResponse(BytesIO(image_bytes), media_type="image/png")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating drip image: {str(e)}"
        )


@img_router.get("/clown", name="This person is a clown", response_model=ImageResponse)
async def clown_endpoint(
    request: Request,
    image: str = None,
):

    if not image:
        raise HTTPException(status_code=400, detail="Please provide an image query.")

    try:
        image_bytes = clown.create(
            image,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating clown image: {str(e)}"
        )

    return StreamingResponse(BytesIO(image_bytes), media_type="image/png")


@img_router.get("/ad", name="Make yourself an ad", response_model=ImageResponse)
async def ad_endpoint(
    request: Request,
    image: str = None,
):

    if not image:
        raise HTTPException(status_code=400, detail="Please provide an image query.")

    try:
        image_bytes = ad.create(
            image,
        )

        return StreamingResponse(BytesIO(image_bytes), media_type="image/png")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating ad image: {str(e)}"
        )


@img_router.get("/blur", name="Blur an image", response_model=ImageResponse)
async def blur_endpoint(
    request: Request,
    image: str = None,
):

    if not image:
        raise HTTPException(status_code=400, detail="Please provide an image query.")

    try:
        image_bytes = blur.create(
            image,
        )

        return StreamingResponse(BytesIO(image_bytes), media_type="image/png")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating blur image: {str(e)}"
        )


@img_router.get(
    "/invert", name="Invert the colors of an image", response_model=ImageResponse
)
async def invert_endpoint(
    request: Request,
    image: str = None,
):

    if not image:
        raise HTTPException(status_code=400, detail="Please provide an image query.")

    try:
        image_bytes = invert.create(
            image,
        )

        return StreamingResponse(BytesIO(image_bytes), media_type="image/png")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating invert image: {str(e)}"
        )


@img_router.get(
    "/greyscale", name="Make an image more grey", response_model=ImageResponse
)
async def greyscale_endpoint(
    request: Request,
    image: str = None,
):

    if not image:
        raise HTTPException(status_code=400, detail="Please provide an image query.")

    try:
        image_bytes = greyscale.create(
            image,
        )

        return StreamingResponse(BytesIO(image_bytes), media_type="image/png")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating grayscale image: {str(e)}"
        )


@img_router.get(
    "/pooh",
    name="Create a meme of a pooh as normal and with a tuxedo",
    response_model=ImageResponse,
)
async def pooh_endpoint(
    request: Request,
    text1: str = None,
    text2: str = None,
):

    if not text1 and text2:
        raise HTTPException(status_code=400, detail="Please provide text1 and text2!")

    try:
        image_bytes = pooh.create(text1, text2)

        return StreamingResponse(BytesIO(image_bytes), media_type="image/png")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating pooh image: {str(e)}"
        )


@img_router.get(
    "/drake", name="Endpoint for making a drake meme", response_model=ImageResponse
)
async def drake_endpoint(
    request: Request,
    text1: str = None,
    text2: str = None,
):

    if not text1 and text2:
        raise HTTPException(status_code=400, detail="Please provide text1 and text2!")

    try:
        image_bytes = drake.create(text1, text2)

        return StreamingResponse(BytesIO(image_bytes), media_type="image/png")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating drake image: {str(e)}"
        )


@img_router.get(
    "/hue-rotate", name="Rotate the hue of an image", response_model=ImageResponse
)
async def huerotate_endpoint(request: Request, img: str, deg: str):

    if not img:
        raise HTTPException(status_code=400, detail="Please provide an image query.")
    elif not deg:
        raise HTTPException(status_code=400, detail="No degree provided")

    try:
        image_bytes = huerotate.create(img, deg)

        return StreamingResponse(BytesIO(image_bytes), media_type="image/png")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating huerotate image: {str(e)}"
        )


@img_router.get(
    "/pet",
    name="Generates a pet-pet gif of any image provided",
    response_model=ImageResponse,
)
def pet_endpoint(request: Request, image: str = Query(...)):
    try:
        url = unquote(image)
        resp = requests.get(url)
        resp.raise_for_status()
        gif_bytes = pet.create(resp.content)  # now works if create() supports raw bytes
        if not gif_bytes:
            return Response(content="Failed to generate pet image", status_code=500)
        return Response(content=gif_bytes, media_type="image/gif")
    except Exception as e:
        return Response(content=f"Error: {e}", status_code=500)


@img_router.get(
    "/ship",
    name="Make a lovely combination of 2 people's avatars",
    response_model=ImageResponse,
)
async def ship_endpoint(request: Request, user1: str, user2: str):

    if not user1:
        raise HTTPException(status_code=400, detail="User1's avatar was not provided!")
    elif not user2:
        raise HTTPException(status_code=400, detail="User2's avatar was not provided!")

    try:
        image_bytes = ship.create(user1, user2)

        return StreamingResponse(BytesIO(image_bytes), media_type="image/png")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating ship image: {str(e)}"
        )


@img_router.get(
    "/whowouldwin", name="Make a WhoWouldWin meme", response_model=ImageResponse
)
async def whowouldwin_endpoint(request: Request, image1: str, image2: str):

    if not image1 or image2:
        raise HTTPException(status_code=400, detail="Please provide image1 and image2!")

    try:
        image_bytes = await whowouldwin.create(image1, image2)

        return StreamingResponse(BytesIO(image_bytes), media_type="image/png")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating whowouldwin image: {str(e)}"
        )


@img_router.get(
    "/caution", name="A caution banner that looks real", response_model=ImageResponse
)
async def caution_endpoint(request: Request, text: str):

    if not text:
        raise HTTPException(status_code=400, detail="Please provide text!")

    try:
        image_bytes = caution.create(text)

        return StreamingResponse(BytesIO(image_bytes), media_type="image/png")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating caution image: {str(e)}"
        )


@img_router.get(
    "/alert", name="Make a fake iPhone alert picture", response_model=ImageResponse
)
async def alert_endpoint(request: Request, text: str):

    if not text:
        raise HTTPException(status_code=400, detail="Please provide text!")

    try:
        image_bytes = alert.create(text)

        return StreamingResponse(BytesIO(image_bytes), media_type="image/png")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating alert image: {str(e)}"
        )


@img_router.get(
    "/jokeoverhead",
    name="That guy doesn't get jokes at all lol",
    response_model=ImageResponse,
)
async def jokeoverhead_endpoint(request: Request, image: str):

    if not img:
        raise HTTPException(status_code=400, detail="Please provide an image query.")

    try:
        image_bytes = jokeoverhead.create(image)

        return StreamingResponse(BytesIO(image_bytes), media_type="image/png")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating jokeoverhead image: {str(e)}"
        )


@img_router.get(
    "/gun", name="Get a perfect Gun overlay on your image", response_model=ImageResponse
)
async def gun_endpoint(request: Request, image: str, text: str = None):

    if not image:
        raise HTTPException(status_code=400, detail="Please provide an image query.")

    try:
        image_bytes = gun.create(image, text)

        return StreamingResponse(BytesIO(image_bytes), media_type="image/png")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating gun image: {str(e)}"
        )


@img_router.get(
    "/quote",
    name="Quote a text with any picture as background!",
    response_model=ImageResponse,
)
@img_router.get("/user-quote", include_in_schema=False, response_model=ImageResponse)
async def userquote_endpoint(request: Request, text: str, image: str, name: str):

    if not text > 125:
        raise HTTPException(
            status_code=400,
            detail="Please provide text under 125 characters!",
        )

    elif not name:
        raise HTTPException(status_code=400, detail="Please provide an author's name!")
    elif not image:
        raise HTTPException(status_code=400, detail="Please provide a valid image!")

    try:
        image_bytes = userquote.create(text, image, name)

        return StreamingResponse(BytesIO(image_bytes), media_type="image/png")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating userquote image: {str(e)}"
        )


@img_router.get(
    "/mnm", name="Make your picture into a shape of m&ms", response_model=ImageResponse
)
async def mnm_endpoint(request: Request, image: str):

    if not img:
        raise HTTPException(
            status_code=400,
            detail="You must provide an image as a parameter!",
        )

    try:
        image_bytes = mnm.create(image)

        return StreamingResponse(BytesIO(image_bytes), media_type="image/png")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating MNM image: {str(e)}"
        )


@img_router.get(
    "/facts", name="This man is speaking facts", response_model=ImageResponse
)
async def facts_endpoint(request: Request, text: str):

    if not text:
        raise HTTPException(status_code=400, detail="Please provide text!")

    try:
        image_bytes = facts.create(text)

        return StreamingResponse(BytesIO(image_bytes), media_type="image/png")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating facts image: {str(e)}"
        )


@img_router.get("/opinion", name="Make an opinion meme", response_model=ImageResponse)
async def opinion_endpoint(
    request: Request,
    image: str,
    text: str,
):

    if not text:
        raise HTTPException(
            status_code=400, detail="Please provide a valid image and text!"
        )
    elif not image:
        raise HTTPException(status_code=400, detail="Invalid image!")

    try:
        image_bytes = opinion.create(image, text)

        return StreamingResponse(BytesIO(image_bytes), media_type="image/png")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating jail image: {str(e)}"
        )


@img_router.get(
    "/uncover",
    name="Ooo! This person was hiding behind the wall all the time?!",
    response_model=ImageResponse,
)
async def uncover_endpoint(
    request: Request,
    image: str,
):

    if not image:
        raise HTTPException(status_code=400, detail="Please provide a valid image!")

    try:
        image_bytes = uncover.create(image)

        return StreamingResponse(BytesIO(image_bytes), media_type="image/png")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating uncover image: {str(e)}"
        )
