import requests

api_url = "https://meme-api.com/gimme"


def get_image():
    try:
        response = requests.get(api_url)
        data = response.json()

        meme_url = data["url"]

        response = requests.get(meme_url)
        image_data = response.content

        return image_data

    except Exception as e:
        print(f"An error occurred: {e}")
