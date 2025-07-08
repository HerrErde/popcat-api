from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from helper import deco
from modules.text import *

text_router = APIRouter()


class TextResponse(BaseModel):
    text: str


@text_router.get(
    "/mock", name="Manipulate text in a sarcastic tone", response_model=TextResponse
)
async def mock_endpoint(
    request: Request,
    text: str = None,
):
    if not text:
        raise HTTPException(status_code=400, detail="No text provided.")

    try:
        response = mock.mock(
            text=text,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating mock text: {str(e)}"
        )

    return {"text": response}


class WyrResponse(BaseModel):
    ops1: str
    ops2: str


@text_router.get(
    "/wyr", name="Get Would You Rather Questions", response_model=WyrResponse
)
async def wyr_endpoint(
    request: Request,
):
    try:
        ops1, ops2 = wyr.text()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating wyr text: {str(e)}"
        )

    return {"ops1": ops1, "ops2": ops2}


@text_router.get(
    "/reverse", name="Reverse the text you provide", response_model=TextResponse
)
async def reverse_endpoint(request: Request, text: str = None):
    if not text:
        raise HTTPException(status_code=400, detail="No text provided.")

    try:
        reversed_text = reverse.text(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reversing text: {str(e)}")

    return {"text": reversed_text}


class EncodeResponse(BaseModel):
    binary: str


@text_router.get(
    "/encode", name="Encode text into binary numbers", response_model=EncodeResponse
)
async def encode_endpoint(
    request: Request,
    text: str = None,
):
    if not text:
        raise HTTPException(status_code=400, detail="No text provided.")

    try:
        response = binary.encode(text)

        return {"binary": response}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating binary text: {str(e)}"
        )


@text_router.get(
    "/decode", name="Decode binary numbers into text", response_model=TextResponse
)
async def decode_endpoint(
    request: Request,
    binary: str = None,
):
    if not text:
        raise HTTPException(status_code=400, detail="No binary numbers provided!")

    try:
        response = binary.decode(binary)

        return {"text": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating text: {str(e)}")


@text_router.get(
    "/texttomorse",
    name="Converts provided text to morse code",
    response_model=TextResponse,
)
async def texttomorse_endpoint(
    request: Request,
    text: str = None,
):
    if not text:
        raise HTTPException(status_code=400, detail="No text provided.")

    try:
        text = convert.morse_code(text)

        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating text: {str(e)}")


@text_router.get(
    "/doublestruck",
    name="Convert your text into the doublestruck font",
    response_model=TextResponse,
)
async def doublestruck_endpoint(
    request: Request,
    text: str = None,
):
    if not text:
        raise HTTPException(status_code=400, detail="No text provided.")

    try:
        text = convert.doublestruck_text(text)
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating text: {str(e)}")


@text_router.get(
    "/lulcat",
    name="Translate your text into funny Lul Cat Language",
    response_model=TextResponse,
)
async def lulcat_endpoint(
    request: Request,
    text: str = None,
):

    if not text:
        raise HTTPException(status_code=400, detail="No text provided.")

    try:
        text = convert.translate(text)
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating text: {str(e)}")


@text_router.get(
    "/pickuplines", name="Get some pickup lines", response_model=TextResponse
)
async def pickuplines_endpoint(
    request: Request,
):
    try:
        response = pickuplines.text()
        return {"text": response}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating pickupline text: {str(e)}"
        )


class FactResponse(BaseModel):
    fact: str


# fix rotation
@text_router.get("/fact", name="Random Facts", response_model=FactResponse)
async def facts_endpoint(
    request: Request,
):
    try:
        response = fact.text()
        return {"fact": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating fact: {str(e)}")


class JokeResponse(BaseModel):
    joke: str


@text_router.get("/joke", name="Get random jokes", response_model=JokeResponse)
async def jokes_endpoint(
    request: Request,
):
    try:
        response = joke.text()
        return {"joke": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating joke: {str(e)}")


class ShowerThoughtResponse(BaseModel):
    showerthought: str


@text_router.get(
    "/showerthoughts",
    name="Get random Shower Thoughts",
    response_model=ShowerThoughtResponse,
)
async def showerthoughts_endpoint(
    request: Request,
):
    try:
        response = showerthoughts.main()
        return {"showerthought": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error showerthought: {str(e)}")


class ChatBotResponse(BaseModel):
    response: str


@text_router.get(
    "/chatbot",
    name="A free custom chatbot API",
    response_model=ChatBotResponse,
)
@deco.EndpointOOF
async def chatbot_endpoint(
    request: Request, msg: str = None, owner: str = None, botname: str = None
):
    if not msg:
        raise HTTPException(status_code=400, detail="Please provide a message!")

    try:
        response = chatbot.chat(msg, owner, botname)
        return {"response": response}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating ai text: {str(e)}"
        )
