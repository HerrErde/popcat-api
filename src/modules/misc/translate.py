import random

import requests

from config import config


# TODO find free translation services
def text(input_text, to):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
        "Accept": "application/graphql+json, application/json",
        "Content-Type": "application/json",
    }

    urls_lingva = [
        "https://lingva.ml",
        "https://translate.plausibility.cloud",
        "https://lingva.lunar.icu",
        "https://lingva.thedaviddelta.com",
    ]
    urls_mozhi = [
        "https://mozhi.aryak.me",
        "https://translate.projectsegfau.lt",
        "https://nyc1.mz.ggtyler.dev",
        "https://translate.nerdvpn.de",
        "https://mozhi.pussthecat.org",
        "https://translate.privacyredirect.com",
        "https://mozhi.canine.tools",
        "https://mozhi.gitro.xyz",
    ]

    if config.translate_engine in ["lingva", "mozhi"] and config.translate_url:
        trans_engine = config.translate_engine
        trans_url = config.translate_url
    else:
        trans_engine = random.choice(["lingva", "mozhi"])
        trans_url = random.choice(
            urls_mozhi if trans_engine == "mozhi" else urls_lingva
        )

    if trans_engine == "mozhi":
        url = f"{trans_url}/api/translate"
        try:
            params = {"engine": "all", "from": "auto", "to": to, "text": input_text}
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()

            data = response.json()
            if isinstance(data, list) and data:
                translated_text = random.choice(data).get("translated-text", "")
                return translated_text
            else:
                print("Unexpected response format:", data)
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching translation: {e}")
            return None

    else:  # lingva
        url = f"{trans_url}/api/v1/auto/{to}/{input_text}"
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()
            return data.get("translation", "")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching translation from Lingva: {e}")
            return None
