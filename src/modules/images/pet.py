import os
from collections import defaultdict
from io import BytesIO
from itertools import chain
from random import randrange
from typing import List, Tuple, Union

import requests
from PIL import Image

FRAMES, RES, DELAY = 10, (128, 128), 20


def make(src, dest):
    base = Image.open(src).convert("RGBA").resize(RES)
    images = []
    for i in range(FRAMES):
        s = i if i < FRAMES / 2 else FRAMES - i
        w, h = 0.8 + s * 0.02, 0.8 - s * 0.05
        ox, oy = (1 - w) * 0.5 + 0.1, (1 - h) - 0.08
        canvas = Image.new("RGBA", RES, (0, 0, 0, 0))
        resized = base.resize((round(w * RES[0]), round(h * RES[1])))
        canvas.paste(resized, (round(ox * RES[0]), round(oy * RES[1])))
        pet = Image.open(f"assets/img/pet/pet{i}.gif").convert("RGBA").resize(RES)
        canvas.paste(pet, mask=pet)
        images.append(canvas)
    save_transparent_gif(images, DELAY, dest)


def create(img_bytes):
    try:
        if isinstance(img_bytes, bytes):
            img_bytes = BytesIO(img_bytes)

        out = BytesIO()
        make(img_bytes, out)
        return out.getvalue()
    except Exception as e:
        print("Error creating image:", e)
        return None


class TransparentAnimatedGifConverter:
    def __init__(self, img_rgba: Image, alpha_threshold=0):
        self.img = img_rgba
        self.threshold = alpha_threshold
        self.replacements = {"idx_from": [], "idx_to": []}

    def process(self) -> Image:
        img_p = self.img.convert("P")
        data = bytearray(img_p.tobytes())
        transparent = {
            i
            for i, a in enumerate(self.img.getchannel("A").getdata())
            if a <= self.threshold
        }
        palette = img_p.getpalette()
        used = {i for j, i in enumerate(data) if j not in transparent}
        parsed = {i: tuple(palette[i * 3 : i * 3 + 3]) for i in used}

        if 0 in used:
            free = set(range(256)) - used
            new_idx = (
                free.pop()
                if free
                else min(
                    range(1, 256),
                    key=lambda i: sum(
                        abs(parsed[0][j] - parsed[i][j]) for j in range(3)
                    ),
                )
            )
            parsed[new_idx] = parsed.pop(0)
            self.replacements["idx_from"].append(0)
            self.replacements["idx_to"].append(new_idx)
            used.add(new_idx)

        parsed[0] = next(
            c
            for c in (
                (randrange(256), randrange(256), randrange(256)) for _ in range(1000)
            )
            if c not in parsed.values()
        )

        if self.replacements["idx_from"]:
            data = data.translate(
                bytearray.maketrans(
                    bytes(self.replacements["idx_from"]),
                    bytes(self.replacements["idx_to"]),
                )
            )

        for i in transparent:
            data[i] = 0

        img_p.frombytes(bytes(data))
        flat = chain.from_iterable(parsed.get(i, (0, 0, 0)) for i in range(256))
        img_p.putpalette(list(flat))
        img_p.info["transparency"] = img_p.info["background"] = 0
        return img_p


def _create_animated_gif(
    images: List[Image], durations: Union[int, List[int]]
) -> Tuple[Image, dict]:
    frames = [
        TransparentAnimatedGifConverter(img.convert("RGBA")).process() for img in images
    ]
    return frames[0], {
        "format": "GIF",
        "save_all": True,
        "append_images": frames[1:],
        "duration": durations,
        "disposal": 2,
        "loop": 0,
    }


def save_transparent_gif(
    images: List[Image], durations: Union[int, List[int]], save_file
):
    img, opts = _create_animated_gif(images, durations)
    img.save(save_file, **opts)
