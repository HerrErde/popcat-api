import requests

from config import config


def chat(msg, owner, botname):
    uid = "web"
    url = f"http://api.brainshop.ai/get?bid={config.brainshop_id}&key={config.brainshop_apikey}&uid={uid}&msg={msg}"

    if owner:
        url += f"&owner={owner}"
    if botname:
        url += f"&botname={botname}"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        response_message = data.get("cnt")

        return response_message

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None
